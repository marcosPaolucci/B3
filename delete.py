from elasticsearch import Elasticsearch

# Conecte-se ao servidor Elasticsearch
es = Elasticsearch('http://localhost:9200')

# Defina o nome do índice
indice_nome = 'meu_indice'

# Exclua o índice
es.indices.delete(index=indice_nome)