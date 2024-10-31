from elasticsearch import Elasticsearch

# Conectar ao Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Dados de teste: consultas e documentos relevantes
# Atualize esta lista com consultas que fazem sentido para o seu caso e os IDs dos documentos esperados.
test_queries = [
    {"query": "Gestor:  Milênio Capital Gestão de Inv . Ltda. ", "relevant_docs": ["gKDlTJIBRdn837Lw7ogx"]},
    {"query": "Administrador:  Singulare Corretora de Títulos e Valores Mobiliários S.A. ", "relevant_docs": ["gqDlTJIBRdn837Lw7ogy"]},
    {"query": "O Fundo foi registrado na Comissão de Valores Mobiliários – CVM em 28 de fevereiro  de 202 4 ", "relevant_docs": ["hKDlTJIBRdn837Lw7ogy"]},
    # Adicione mais consultas de teste conforme necessário
]

# Função para calcular Precision e Recall
def calculate_precision_recall(query, relevant_docs, index="meu_indice3"):
    # Realiza a busca
    response = es.search(index=index, query={"match_phrase": {"texto": query}})
    retrieved_docs = [hit["_id"] for hit in response["hits"]["hits"]]

    # Calcula True Positives, False Positives e False Negatives
    tp = len(set(retrieved_docs) & set(relevant_docs))  # Documentos relevantes recuperados
    fp = len(set(retrieved_docs) - set(relevant_docs))  # Documentos não relevantes recuperados
    fn = len(set(relevant_docs) - set(retrieved_docs))  # Documentos relevantes não recuperados

    # Precision e Recall
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    return precision, recall

# Executa os testes e calcula métricas
total_precision, total_recall = 0, 0
for test in test_queries:
    precision, recall = calculate_precision_recall(test["query"], test["relevant_docs"])
    total_precision += precision
    total_recall += recall
    print(f"Consulta: '{test['query']}' -> Precision: {precision:.2f}, Recall: {recall:.2f}")

# Calcula a média de Precision e Recall para todos os testes
average_precision = total_precision / len(test_queries) if len(test_queries) > 0 else 0
average_recall = total_recall / len(test_queries) if len(test_queries) > 0 else 0

print(f"\nMédia de Precision: {average_precision:.2f}")
print(f"Média de Recall: {average_recall:.2f}")
