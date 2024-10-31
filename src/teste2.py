import nltk
import numpy as np
from nltk.translate.bleu_score import sentence_bleu
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rouge_score import rouge_scorer

# Certifique-se de que você já baixou os pacotes necessários do NLTK (somente na primeira vez)
nltk.download('punkt_tab')

# Função para calcular métricas entre uma resposta esperada e uma lista de respostas geradas
def evaluate_responses(expected_response, generated_responses):
    metrics = {
        "BLEU": [],
        "Cosine Similarity": [],
        "ROUGE-L": []
    }
    
    # Configurar o calculador de ROUGE
    rouge = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    
    # TF-IDF Vectorizer para Cosine Similarity
    vectorizer = TfidfVectorizer()
    # Treinar o vetor de TF-IDF com a resposta esperada e as geradas
    vectorizer.fit([expected_response] + generated_responses)
    expected_vector = vectorizer.transform([expected_response])
    
    # Calcular métricas para cada resposta gerada
    for response in generated_responses:
        # BLEU Score
        bleu_score = sentence_bleu([nltk.word_tokenize(expected_response)], nltk.word_tokenize(response))
        metrics["BLEU"].append(bleu_score)
        
        # Cosine Similarity
        response_vector = vectorizer.transform([response])
        cosine_sim = cosine_similarity(expected_vector, response_vector)[0][0]
        metrics["Cosine Similarity"].append(cosine_sim)
        
        # ROUGE-L Score
        rouge_score = rouge.score(expected_response, response)['rougeL'].fmeasure
        metrics["ROUGE-L"].append(rouge_score)
    
    # Retornar as médias das métricas para avaliação geral
    avg_metrics = {metric: np.mean(scores) for metric, scores in metrics.items()}
    
    return avg_metrics

# Exemplo de uso
expected_response = "a s Cotas Subordinadas Júnior devem representar, pelo menos, 30,0% do Patrimônio total do Fundo."
generated_responses = [
    """
    As cotas subordinadas júnior do Bravano Fundo de Investimento em Direitos Creditórios devem representar pelo menos 30% do patrimônio total do fundo. Este requisito está estabelecido no regulamento do fundo, que especifica que as cotas subordinadas (incluindo júnior) devem ter uma participação mínima equivalente a 50% do patrimônio líquido (PL) do fundo, com as cotas subordinadas júnior exigindo especificamente os 30% mencionados. 
    
    """,
    """
    As cotas subordinadas Júnior do Bravano Fundo de Investimento em Direitos Creditórios devem representar, pelo menos, 30% do patrimônio total do fundo. Essa exigência é estipulada no regulamento do fundo e se refere à estrutura de capital que inclui as cotas seniores, subordinadas mezanino e subordinadas júnior.
    """,
    """
    As cotas subordinadas Júnior do Bravano Fundo de Investimento em Direitos Creditórios devem representar, no mínimo, 30% do patrimônio total do fundo. Isso é estabelecido na estrutura de capital do fundo, onde as cotas subordinadas (incluindo as Júnior) precisam ter uma participação mínima equivalente a 50% do patrimônio líquido, sendo que as cotas Júnior especificamente devem manter essa proporção de 30% do patrimônio total.    
    """,
    """
    As cotas subordinadas Júnior do Bravano Fundo de Investimento em Direitos Creditórios devem representar, no mínimo, 30,0% do patrimônio total do fundo. Isso está em conformidade com as regras estabelecidas no regulamento do fundo.
    """
]

# Avaliar as respostas geradas
results = evaluate_responses(expected_response, generated_responses)

# Exibir resultados
print("Métricas de avaliação:")
print("Média BLEU Score:", results["BLEU"])
print("Média Cosine Similarity:", results["Cosine Similarity"])
print("Média ROUGE-L Score:", results["ROUGE-L"])