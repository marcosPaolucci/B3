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
Para o nosso modelo, utilizamos 2 tipos diferentes de métricas de avaliação:

### 1.Precision e Recall

### 2.BLEU Score, Cosine Similarity, ROUGE-L Score

**Por que Usar Duas Validações?** 

- **1. Avaliação de Similaridade do Chatbot**

A primeira validação (usando BLEU, Cosine Similarity e ROUGE-L) é adequada para medir a precisão semântica e similaridade entre respostas geradas pelo chatbot e respostas esperadas. Ela ajuda a avaliar se as respostas do chatbot estão coerentes e em linha com a expectativa, o que é fundamental para melhorar a qualidade do diálogo.

- **2. Avaliação de Recuperação de Informações no Elasticsearch**

A segunda validação com precisão e revocação mede a capacidade do Elasticsearch de recuperar documentos relevantes. Enquanto a primeira validação está focada em avaliar o conteúdo das respostas geradas pelo chatbot, a segunda se concentra em avaliar a precisão da busca realizada no Elasticsearch. A precisão ajuda a verificar se o Elasticsearch está trazendo documentos úteis sem resultados irrelevantes, enquanto a revocação garante que todos os documentos relevantes sejam incluídos na resposta.

Em Resumo

Ambas as validações têm propósitos diferentes mas complementares:

**Primeira validação** (similaridade de respostas): Avalia a qualidade e a precisão do conteúdo gerado pelo chatbot, garantindo que ele responda de forma adequada.

**Segunda validação** (precisão e revocação): Avalia a capacidade do Elasticsearch de realizar buscas eficientes e completas, garantindo que a base de dados de documentos retorne informações relevantes para cada consulta.

Essas duas avaliações juntas fornecem uma análise abrangente da eficácia tanto do modelo de resposta quanto da recuperação de dados, ajudando a garantir a qualidade das interações e a relevância das informações fornecidas pelo sistema.

#### 1. Avaliação das Métricas de Precision e Recall
Este código utiliza as métricas Precision e Recall para avaliar o desempenho do modelo de busca configurado no Elasticsearch. A seguir, descrevemos cada etapa do processo de avaliação:

- **Configuração das Consultas de Teste**:

Definimos um conjunto de consultas de teste, cada uma representando uma busca que esperamos que o modelo de busca do Elasticsearch atenda corretamente.
Cada consulta de teste inclui:
Um termo de busca (consulta), que representa o que um usuário pode buscar.
Uma lista de documentos relevantes (IDs dos documentos), que são os documentos esperados como resultado relevante para essa consulta específica.
Essas consultas e seus documentos relevantes são usados como padrão para avaliar a precisão e a completude das respostas do Elasticsearch.

- **Execução da Busca no Elasticsearch**:

Para cada consulta de teste, o código executa uma busca no índice do Elasticsearch, tentando encontrar documentos que correspondam ao termo de busca usando a função es.search.
A busca é feita no campo especificado (neste caso, "text"), e o Elasticsearch retorna uma lista de documentos correspondentes, incluindo seus IDs e suas pontuações de relevância.

- **Extração dos Documentos Retornados:**

A lista de documentos retornados pela busca é filtrada para obter apenas os IDs dos documentos encontrados.
Esses IDs representam os documentos que o Elasticsearch considera relevantes para a consulta, com base em sua indexação e configuração de busca.

- **Cálculo de Precision e Recall:**

True Positives (TP): Documentos que foram recuperados pela busca e que também estão na lista de documentos relevantes para a consulta.
False Positives (FP): Documentos que foram recuperados pela busca, mas que não estão na lista de documentos relevantes.
False Negatives (FN): Documentos que não foram recuperados pela busca, mas que estão na lista de documentos relevantes.

Com essas contagens, as métricas são calculadas da seguinte forma:

**Precision:** Mede a proporção de documentos relevantes entre os documentos recuperados. É calculada como Precision = TP / (TP + FP).
**Recall:** Mede a proporção de documentos relevantes recuperados em relação ao total de documentos relevantes existentes. É calculada como Recall = TP / (TP + FN).

- **Média de Precision e Recall:**

Para obter uma avaliação geral do desempenho, o código calcula a média das métricas de Precision e Recall de todas as consultas de teste.
A média de Precision e Recall oferece uma visão do desempenho geral do modelo de busca no índice, considerando todas as consultas.

Essas métricas fornecem insights sobre a qualidade dos resultados da busca:

Alta **Precision** indica que a maioria dos documentos recuperados é relevante.
Alta **Recall** indica que a maioria dos documentos relevantes é recuperada pelo modelo de busca.

Essas informações ajudam a entender a eficácia do modelo de busca configurado no Elasticsearch e podem orientar ajustes para melhorar seu desempenho em cenários reais.


#### 2. Métricas de Avaliação: BLEU Score, Cosine Similarity, ROUGE-L Score:

- **Contexto da Avaliação**

Imagine que você tem um chatbot e quer medir o quanto ele é preciso nas respostas que fornece. Para isso, você tem uma resposta correta em mente (o que o chatbot deveria responder) e várias respostas geradas pelo modelo. O objetivo aqui é comparar essas respostas geradas com a resposta correta e ver o quanto elas se aproximam, usando três diferentes tipos de métricas de avaliação.

- **Métricas de Avaliação**

Para essa tarefa de comparação, usamos três métricas que são amplamente utilizadas em tarefas de processamento de linguagem natural. Essas métricas são como “régua” para medir a qualidade das respostas em relação ao que esperamos.

**BLEU Score**: O BLEU é uma métrica que examina a quantidade de palavras e sequências de palavras (chamadas de n-gramas) que aparecem na resposta gerada e também na resposta correta. Imagine que estamos verificando se a resposta gerada “fala” as mesmas coisas que a resposta esperada, inclusive na mesma ordem e usando expressões parecidas. Essa métrica vai de 0 a 1, onde um valor mais alto significa que as respostas têm muito em comum. BLEU é amplamente usado em áreas como tradução automática e ajuda a ver o quanto a resposta do chatbot está próxima do que seria a resposta ideal.

**Cosine Similarity**: Essa métrica funciona com base na matemática vetorial. Ela transforma as respostas em vetores (ou seja, uma representação numérica) e depois calcula o ângulo entre esses vetores para ver o quanto eles são semelhantes. Quando o ângulo é pequeno, significa que as respostas têm uma “direção” muito parecida (ou seja, contêm palavras e frases que ocorrem em contextos semelhantes). O resultado dessa métrica vai de -1 a 1, sendo que valores mais próximos de 1 indicam que as respostas compartilham muito em termos de palavras e significado.

**ROUGE-L Score**: O ROUGE-L é uma métrica que mede a quantidade de palavras em comum entre a resposta gerada e a resposta correta, considerando especialmente a ordem dessas palavras. Em outras palavras, ele avalia se a sequência de palavras na resposta gerada é semelhante à sequência na resposta correta. Isso é útil para ver se a resposta gerada cobre os principais pontos ou conteúdos que você quer que o chatbot transmita.

- **Como as Métricas São Calculadas e Usadas**

Na prática, cada uma dessas métricas é calculada para cada resposta que o chatbot gera, comparando-a com a resposta correta que você tem como referência. Por exemplo, para cada resposta gerada, é verificado o quanto ela se parece com a resposta correta em termos de palavras exatas (BLEU), palavras e contexto (Cosine Similarity), e sequência de palavras importantes (ROUGE-L).

- **Interpretação das Métricas**

Depois de calcular todas as métricas para cada resposta gerada, tiramos uma média desses valores para cada métrica. Essa média nos dá uma visão geral de quão bem as respostas do chatbot se alinham com a resposta correta em relação aos três aspectos que mencionamos. Se as médias forem altas, indica que o chatbot está sendo bastante preciso e está fornecendo respostas que se aproximam do que é esperado. Se as médias forem baixas, isso pode indicar que o chatbot precisa de ajustes para dar respostas mais coerentes e relevantes.

- **Conclusão**
Em resumo, usamos essas três métricas para obter uma avaliação quantitativa da qualidade das respostas do chatbot. Essa análise permite observar o desempenho do chatbot de forma objetiva e identificar áreas onde ele pode melhorar, tornando-o mais preciso e útil em suas interações.

## Evidências de Testes

Métricas de Avaliação: Precision e Recall:


![image](https://github.com/user-attachments/assets/65e709c4-1c95-4bdc-8a9a-ecef63a7f6fe)

Métricas de Avaliação: BLEU Score, Cosine Similarity, ROUGE-L Score:

![image](https://github.com/user-attachments/assets/1c50c54c-2692-498c-878e-9101d48a7412)


## Discussão dos Resultados 

Os testes de desempenho do modelo de busca no Elasticsearch foram realizados com sucesso, e os resultados obtidos foram muito satisfatórios. 

As métricas de Precision e Recall alcançaram valores quase perfeitos, indicando que o modelo está recuperando com precisão os documentos relevantes para as consultas de teste. Essa alta precisão e recall mostram que o modelo consegue tanto retornar uma grande quantidade de documentos relevantes quanto evitar a inclusão de documentos irrelevantes nos resultados.

Adicionalmente, avaliamos o modelo com outras métricas: BLEU Score, Cosine Similarity e ROUGE-L Score. Essas métricas são comumente utilizadas para avaliar a similaridade textual, e visam medir quão compatível é a resposta gerada pelo sistema em relação ao conteúdo original dos documentos. No entanto, os valores dessas métricas não foram tão altos, o que já era esperado, pois o objetivo do nosso modelo não é apenas reproduzir o conteúdo exato dos documentos, mas sim “traduzir” a informação de forma simplificada para o usuário.

Nosso foco está em fornecer respostas que transmitam o conteúdo principal de maneira mais acessível e compreensível, em vez de uma correspondência literal ao texto do documento original. Por isso, um desempenho mais baixo nessas métricas de similaridade textual não reflete uma falha do modelo, mas sim uma adaptação intencional para melhorar a experiência do usuário.

Em resumo, os resultados foram excelentes, com alto desempenho nas métricas de precisão e recall e uma abordagem de simplificação das respostas que atende ao objetivo de facilitar o entendimento das informações para o usuário.

## Soluções Futuras 

Para aprimorar ainda mais o desempenho e a versatilidade do modelo de busca, uma das soluções futuras planejadas é explorar **outras abordagens de busca disponíveis no Elasticsearch**. Embora o modelo atual tenha se mostrado eficaz em termos de precisão e recall, testar diferentes tipos de busca pode ajudar a garantir que o modelo seja robusto em uma variedade ainda maior de cenários e tipos de consulta, atendendo às demandas de usuários que buscam informações de formas distintas.

**1. Implementação de Vários Tipos de Busca:**
- O Elasticsearch oferece uma gama de tipos de busca, como match, match_phrase, multi_match, bool e fuzzy, cada uma com características próprias. Cada uma dessas abordagens pode trazer vantagens específicas em contextos variados.

- Por exemplo:
  - match_phrase: seria útil para capturar expressões exatas, como nomes próprios ou termos específicos do setor.

  - multi_match: permite buscar em múltiplos campos, o que seria útil para consultas mais amplas que podem se aplicar a várias seções de um documento (como título, resumo, e corpo do texto).

  - fuzzy: ajuda a lidar com erros de digitação ou pequenas variações nos termos de busca, tornando o sistema mais amigável para usuários que possam cometer erros de digitação ou buscar de forma imprecisa.

**2. Ajuste de Parâmetros e Peso dos Campos:**

- Outra melhoria potencial seria ajustar os pesos dos diferentes campos usados nas consultas. Por exemplo, o título de um documento pode ser mais relevante do que o corpo em algumas buscas. Com o Elasticsearch, podemos atribuir pesos maiores aos campos mais importantes para certos tipos de consultas, o que ajuda a melhorar a relevância dos resultados.

- Esse ajuste seria particularmente útil para consultas em que certas partes do documento (como título ou resumo) fornecem uma visão mais precisa do conteúdo, ajudando o usuário a obter resultados mais focados e relevantes.

**3. Busca Semântica e Similaridade de Contexto:**

- Outra abordagem futura envolve a utilização de técnicas de busca semântica, que poderiam ser incorporadas ao Elasticsearch por meio de integrações com modelos de aprendizado profundo, como embeddings de texto. Isso permitiria que o sistema interpretasse a intenção por trás das consultas do usuário, mesmo quando a busca não coincide exatamente com os termos usados nos documentos.

- Com isso, o Elasticsearch poderia retornar resultados que sejam semanticamente relevantes, melhorando a experiência do usuário ao capturar o contexto e o significado subjacente da consulta, e não apenas as palavras exatas.

**4. Avaliação e Adaptação Contínuas:**

- Testar o modelo em uma variedade de cenários de busca permitirá uma avaliação contínua da sua eficácia e adaptabilidade. Implementar uma estratégia de testes automatizados com consultas representativas ajudaria a identificar, de forma rápida e consistente, áreas onde o modelo precisa de ajustes.

- Além disso, realizar uma análise mais aprofundada das consultas mais frequentes dos usuários reais poderia ajudar a ajustar e priorizar as configurações de busca, garantindo que o modelo evolua conforme as necessidades dos usuários mudam.

**5. Integração com Modelos de Relevância Ponderada:**

- Uma abordagem avançada que pode ser considerada é a criação de um sistema de relevância ponderada, em que diferentes modelos de busca e abordagens são testados e combinados para maximizar a precisão e recall em um espectro mais amplo de consultas.

- Esse sistema poderia selecionar automaticamente a abordagem de busca mais adequada com base nas características da consulta do usuário, proporcionando uma experiência de busca adaptativa e mais precisa.

### Conclusão

Essas soluções futuras visam tornar o modelo de busca mais flexível, robusto e orientado ao usuário, atendendo a diferentes tipos de consultas com alta precisão e relevância. Explorar e implementar essas abordagens permitirá ao modelo responder eficazmente a uma gama maior de cenários e melhorar continuamente a experiência dos usuários na recuperação de informações.

