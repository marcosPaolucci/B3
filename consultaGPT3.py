from openai import OpenAI
from elasticsearch import Elasticsearch
import logging

# Configurar a chave da API da OpenAI
client = OpenAI(api_key="sk-proj-2z8UhJtQ1fxwidNX852lT3BlbkFJbPwFk6JFnORpaJsuQgmn")

# Conectar ao Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Função para gerar embedding da consulta
def gerar_embedding_consulta(consultasimplificada):
    try:
        resposta = client.embeddings.create(input=consulta, model="text-embedding-ada-002")
        return resposta.data[0].embedding
    except Exception as e:
        logging.error(f"Erro ao gerar embedding da consulta: {e}")
        return None

# Função para buscar documentos baseados em embeddings no Elasticsearch
def buscar_documentos_no_elasticsearch(embedding_consulta, es, indice="meu_indice"):
    try:
        query = {
            "size": 5,  # Número de resultados
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": "cosineSimilarity(params.embedding, 'embedding')",
                        "params": {
                            "embedding": embedding_consulta
                        }
                    }
                }
            },
            "_source": ["texto", "id_arquivo"]  # Garantir que os campos de texto e id_arquivo sejam retornados
        }

        response = es.search(index=indice, body=query)
        return response['hits']['hits']
    except Exception as e:
        logging.error(f"Erro ao buscar documentos no Elasticsearch: {e}")
        return []

# Função para extrair os textos e informações dos documentos retornados
def extrair_informacoes(resultados):
    informacoes = []
    for resultado in resultados:
        if "texto" in resultado["_source"] and "id_arquivo" in resultado["_source"]:
            informacoes.append({
                "texto": resultado["_source"]["texto"],
                "id_arquivo": resultado["_source"]["id_arquivo"],
                "pontuacao_similaridade": resultado["_score"]
            })
        else:
            logging.warning(f"Resultado sem campo 'texto' ou 'id_arquivo': {resultado}")
    return informacoes

# Função para dividir o texto em segmentos de aproximadamente 250 tokens, respeitando os pontos finais
def dividir_texto_em_segmentos(texto, max_tokens=250):
    import re
    sentencas = re.split(r'(?<=[.!?]) +', texto)
    segmentos = []
    segmento_atual = []
    tokens_no_segmento = 0

    for sentenca in sentencas:
        tokens_na_sentenca = len(sentenca.split())
        if tokens_no_segmento + tokens_na_sentenca > max_tokens:
            if segmento_atual:
                segmentos.append(" ".join(segmento_atual))
                segmento_atual = []
                tokens_no_segmento = 0
        segmento_atual.append(sentenca)
        tokens_no_segmento += tokens_na_sentenca

    if segmento_atual:
        segmentos.append(" ".join(segmento_atual))

    return segmentos

# Função para gerar embedding para cada segmento
def gerar_embeddings_segmentos(segmentos):
    embeddings = []
    for segmento in segmentos:
        try:
            resposta = client.embeddings.create(input=segmento, model="text-embedding-ada-002")
            embeddings.append(resposta.data[0].embedding)
        except Exception as e:
            logging.error(f"Erro ao gerar embedding para segmento: {e}")
    return embeddings

# Função para calcular similaridade entre embeddings
def calcular_similaridade(embedding1, embedding2):
    from numpy import dot
    from numpy.linalg import norm
    return dot(embedding1, embedding2) / (norm(embedding1) * norm(embedding2))

# Função para limitar os textos a 350 tokens cada
def limitar_texto(texto, max_tokens=350):
    tokens = texto.split()
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return " ".join(tokens)

# Função para combinar trechos em um contexto
def combinar_trechos(informacoes):
    contexto_combinado = []
    for info in informacoes:
        trecho_identificado = f"Fundo: {info['id_arquivo']}\nTrecho: {info['trecho']}\n"
        contexto_combinado.append(trecho_identificado)
    return "\n".join(contexto_combinado)

# Função para responder a consulta usando contexto combinado
def responder_consulta(consulta, es, indice="meu_indice"):
    embedding_consulta = gerar_embedding_consulta(consulta)
    if not embedding_consulta:
        return "Erro ao gerar embedding da consulta."

    resultados = buscar_documentos_no_elasticsearch(embedding_consulta, es, indice)
    if not resultados:
        logging.warning("Nenhum resultado encontrado no Elasticsearch.")
        return "Nenhum resultado encontrado."

    informacoes = extrair_informacoes(resultados)
    if not informacoes:
        logging.warning("Nenhuma informação extraída dos resultados.")
        return "Nenhuma informação extraída dos resultados."

    trechos_relevantes = []
    for info in informacoes:
        segmentos = dividir_texto_em_segmentos(info["texto"])
        embeddings_segmentos = gerar_embeddings_segmentos(segmentos)
        similaridades = [calcular_similaridade(embedding_consulta, embedding) for embedding in embeddings_segmentos]

        for segmento, similaridade in zip(segmentos, similaridades):
            trechos_relevantes.append({
                "id_arquivo": info["id_arquivo"],
                "trecho": limitar_texto(segmento),
                "similaridade": similaridade
            })

    # Ordenar os trechos por similaridade decrescente
    trechos_relevantes = sorted(trechos_relevantes, key=lambda x: x["similaridade"], reverse=True)

    # Selecionar os 5 trechos mais relevantes
    trechos_selecionados = trechos_relevantes[:5]

    # Combinar trechos em um contexto
    contexto = combinar_trechos(trechos_selecionados)

    prompt = f"Consulta: {consulta}\n\nContexto relevante:\n{contexto}\n\nResposta:"
    print(prompt)
    resposta = client.completions.create(prompt=prompt, model="gpt-3.5-turbo-instruct", max_tokens=150)

    return resposta.choices[0].text.strip()

def transformar_consulta(consulta):
    system = {"role": "system", "content": "Você é um assistente que transforma consultas de linguagem natural em strings otimizadas para buscas no Elasticsearch. Converta a consulta em uma string de busca eficiente."}
    exemplos = [{"Consulta": "Estou procurando o melhor fundo de investimento em ouro disponível no mercado.", "Resposta": "fundos investimento ouro"},
{"Consulta": "Quais fundos imobiliários oferecem os melhores dividendos atualmente?", "Resposta": "fundos imobiliários melhores dividendos"},
{"Consulta": "Preciso de informações sobre os riscos de investir no fundo de ações ABV11.", "Resposta": "riscos fundo ABV11"},
{"Consulta": "Gostaria de saber como foi o desempenho do fundo VGHF11 nos últimos anos.", "Resposta": "desempenho fundo VGHF11"},
{"Consulta": "Quais são os melhores fundos de investimento em tecnologia disponíveis?", "Resposta": "fundos investimento tecnologia"},
{"Consulta": "Onde estão localizados os imóveis que fazem parte do fundo BRCR11?", "Resposta": "localização imóveis fundo BRCR11"},
{"Consulta": "Estou procurando informações sobre fundos de investimento sustentáveis. Pode me ajudar?", "Resposta": "fundos investimento sustentáveis"},
{"Consulta": "Quais são as principais características do fundo de investimento KNRI11?", "Resposta": "características fundo KNRI11"},
{"Consulta": "Estou interessado nos informes financeiros mais recentes do fundo GGRC11.", "Resposta": "informes financeiros fundo GGRC11"},
{"Consulta": "Qual é o fundo de investimento mais seguro em termos de risco?", "Resposta": "fundo investimento menor risco"}]

    prompt = f"system: {system}\n\nExemplos:\n{exemplos}\n\nConsulta a ser transformada: {consulta}\n\nResposta:"
    print(prompt)
    resposta = client.completions.create(prompt=prompt, model="gpt-3.5-turbo-instruct", max_tokens=50)
    return resposta.choices[0].text.strip()


# Exemplo de uso
#consulta = "Quais os requisitos para isenção do Imposto de Renda Retido na Fonte e na Declaração de Ajuste Anual das Pessoas Físicas com relação aos  rendimentos  distribuídos  pelo  Fundo RBRD11?"
#consulta = "Qual o patrimônio líquido do fundo IT NOW S&P® KENSHO® MOONSHOTS FUNDO DE INDICE?"
#consulta = "O VGIA11 está levando em conta as inundações do Rio Grande do Sul?"
consulta = "Qual a data do IPO do fundo RBRD11?"

consultasimplificada = transformar_consulta(consulta)
print(f"consultasimplificada é {consultasimplificada}")

resposta = responder_consulta(consulta, es)
print("Resultado da consulta:")
print(resposta)
