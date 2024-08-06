from openai import OpenAI
from elasticsearch import Elasticsearch
import logging

# Configurar a chave da API da OpenAI
client = OpenAI(api_key="sk-proj-2z8UhJtQ1fxwidNX852lT3BlbkFJbPwFk6JFnORpaJsuQgmn")

# Conectar ao Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Função para gerar embedding da consulta
def gerar_embedding_consulta(consulta):
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

# Função para responder a consulta e imprimir as informações detalhadas
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
                "trecho": segmento,
                "similaridade": similaridade
            })

    # Ordenar os trechos por similaridade decrescente
    trechos_relevantes = sorted(trechos_relevantes, key=lambda x: x["similaridade"], reverse=True)

    for trecho in trechos_relevantes[:5]:  # Mostrar os 5 trechos mais relevantes
        print(f"ID do Arquivo: {trecho['id_arquivo']}")
        print(f"Pontuação de similaridade: {trecho['similaridade']}")
        print(f"Trecho: {trecho['trecho']}")
        print("------------------")

    return "Consulta processada com sucesso."

# Exemplo de uso
consulta = "Quais os requisitos para isenção do Imposto de Renda Retido na Fonte e na Declaração de Ajuste Anual das Pessoas Físicas com relação aos  rendimentos  distribuídos  pelo  Fundo RBRD11?"  
resposta = responder_consulta(consulta, es)

print("Resultado da consulta:")
print(resposta)
