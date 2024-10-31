# Introdução

Este projeto foi desenvolvido para facilitar a consulta e análise de informações sobre fundos de investimentos da B3, a bolsa de valores brasileira. Devido ao grande volume de documentos e dados disponíveis sobre o mercado financeiro, os investidores e analistas encontram dificuldades em localizar rapidamente as informações mais relevantes para suas tomadas de decisão.

O objetivo deste projeto é criar uma solução que permita a consulta inteligente sobre fundos de investimentos, utilizando técnicas de Web Scraping, análise semântica e modelos de linguagem pré-treinados. A solução busca transformar consultas textuais em respostas precisas, extraídas de grandes volumes de documentos financeiros, facilitando o processo de análise para o usuário.

# Desenvolvimento

A arquitetura do projeto foi desenhada para processar eficientemente os documentos sobre fundos de investimentos da B3, utilizando um pipeline que combina técnicas de machine learning e busca semântica. Abaixo está o diagrama da arquitetura utilizado para este projeto:


## Componentes da Arquitetura:

1. Interação entre usuário e robô: O usuário insere consultas relacionadas a fundos de investimentos da B3, buscando informações específicas, como regras, rentabilidade ou estratégias dos fundos.

2. Consulta na base de dados: A consulta é enviada à base de dados, que contém documentos financeiros e relatórios sobre os fundos de investimentos.

3. Transformação da consulta em Embedding: A consulta é transformada em um embedding (representação vetorial), o que permite a análise semântica e a busca por similaridade com documentos financeiros.

4. Web Scraping: O sistema utiliza técnicas de scraping para coletar automaticamente novos relatórios e documentos financeiros de fontes confiáveis, incluindo relatórios de fundos, regulamentos, históricos de rentabilidade e documentos regulatórios da B3.

5. Criação dos Embeddings dos arquivos: Os documentos capturados (relatórios de fundos, prospectos, regulamentos, etc.) são convertidos em embeddings para permitir a busca por similaridade. Cada documento financeiro é representado em um formato que facilita a comparação com as consultas dos usuários.

6. Elastic Search: O sistema utiliza o Elastic Search para realizar uma busca eficiente, indexando os documentos financeiros e comparando-os com o embedding gerado pela consulta do usuário.

7. Busca por Similaridade: O Elastic Search identifica os documentos financeiros com maior similaridade em relação à consulta do usuário. Estes documentos podem incluir relatórios detalhados, dados de rentabilidade ou regras de investimento dos fundos.

8. Análise pelo modelo pré-treinado: Os documentos mais relevantes são analisados por um modelo de linguagem pré-treinado, que refina os resultados e identifica trechos específicos que respondem à consulta.

9. Geração do Texto: A partir dos trechos relevantes dos documentos financeiros, o sistema gera uma resposta clara e objetiva para a consulta do usuário.

10. Retorno para o Usuário: O texto gerado é devolvido ao usuário na interface da aplicação, apresentando a resposta com base em informações extraídas dos documentos financeiros mais relevantes.

![image](https://github.com/user-attachments/assets/d4823e70-e777-44f8-aa87-0d2eb5e01811)

## Tecnologias Utilizadas:
Web Scraping: Para coletar automaticamente relatórios e documentos financeiros atualizados da B3. Atualmente feito via código Python com chromedriver.

Elastic Search: Para indexação e busca por similaridade entre os documentos financeiros da B3 e a consulta do usuário.

Embeddings: Para transformar tanto as consultas quanto os documentos em representações vetoriais, permitindo a comparação semântica. Estamos usando embeddings do modelo text-embedding-3-large da OpenAI.

Modelos de linguagem pré-treinado (como GPT): Para interpretar e refinar as consultas e documentos, gerando respostas significativas e concisas. Utilizando o modelo gpt-4o-mini e ajustando com Prompt engineering.

# Resultados

A aplicação é capaz de processar documentos relacionados aos fundos de investimentos da B3 e gerar respostas precisas com base nas consultas dos usuários. Abaixo está um exemplo de execução da aplicação, ilustrando os resultados esperados:

Consulta via código Python:
![image](https://github.com/user-attachments/assets/43ae708e-308b-4db2-bc9c-d04236382b81)

Resposta do Modelo:
![image](https://github.com/user-attachments/assets/1c05f979-cba8-4b7e-8eee-2c09c956bc7f)


# Testes de Desempenho

## Definição da Ferramente de Teste


## Evidências de Testes
Métricas de Avaliação: BLEU Score, Cosine Similarity, ROUGE-L Score:
![image](https://github.com/user-attachments/assets/65e709c4-1c95-4bdc-8a9a-ecef63a7f6fe)

Métricas de Avaliação: Precision e Recall:
![image](https://github.com/user-attachments/assets/1c50c54c-2692-498c-878e-9101d48a7412)


## Discussão dos Resultados 



