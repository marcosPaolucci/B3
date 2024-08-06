import os
from openai import OpenAI
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# Configurar a chave da API da OpenAI
client = OpenAI(api_key="sk-proj-2z8UhJtQ1fxwidNX852lT3BlbkFJbPwFk6JFnORpaJsuQgmn")

# Tamanho máximo do segmento
tamanho_maximo_segmento = 8192

# Conectar ao Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
if not es.indices.exists(index="meu_indice"):
    es.indices.create(index="meu_indice", ignore=400)

# Função para gerar embeddings
def gerar_embeddings(texto, id_arquivo):
    # Segmentar o texto em partes menores
    segmentos = segmentar_texto(texto, tamanho_maximo_segmento)

    # Gerar embeddings para cada segmento
    embeddings = []
    posicao_segmento = 0
    for segmento in segmentos:
        embedding = gerar_embedding_segmento(segmento, posicao_segmento)
        embeddings.append({
            "_index": "meu_indice",
            "_source": {
                "id_arquivo": id_arquivo,
                "posicao_segmento": posicao_segmento,
                "embedding": embedding,
                "texto": segmento  # Armazenar o segmento de texto original
            }
        })
        posicao_segmento += 1

    return embeddings

# Função para gerar embedding de um segmento de texto
def gerar_embedding_segmento(segmento, posicao_segmento):
    # Truncar o segmento para 8192 tokens (se necessário)
    if len(segmento) > tamanho_maximo_segmento:
        segmento = segmento[:tamanho_maximo_segmento]

    # Gerar embedding
    resposta = client.embeddings.create(input=segmento,
                                        model="text-embedding-ada-002")  # Escolha o modelo apropriado
    return resposta.data[0].embedding

# Função para segmentar o texto em partes menores
def segmentar_texto(texto, tamanho_maximo_segmento):
    segmentos = []
    posicao_inicial = 0
    while posicao_inicial < len(texto):
        segmento_final = min(posicao_inicial + tamanho_maximo_segmento, len(texto))
        segmento = texto[posicao_inicial:segmento_final]
        segmentos.append(segmento)
        posicao_inicial = segmento_final

    return segmentos

# Obter o diretório atual
diretorio_atual = os.getcwd()

# Construir o caminho para a pasta "textos"
caminho_pasta = os.path.join(diretorio_atual, 'textos')

# Verificar se a pasta existe
if not os.path.exists(caminho_pasta):
    raise FileNotFoundError(f"A pasta 'textos' não foi encontrada no diretório atual: {diretorio_atual}")

# Preparar a lista de documentos para indexação
documentos = []

# Iterar sobre os arquivos na pasta "textos"
for nome_arquivo in os.listdir(caminho_pasta):
    caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
    if os.path.isfile(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            embeddings = gerar_embeddings(conteudo, nome_arquivo)
            documentos.extend(embeddings)

# Indexar embeddings no Elasticsearch
bulk(es, documentos)
