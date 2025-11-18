## Aplicação dos estudos sobre Reconhecimento de Entidades Nomeadas

Esse projeto tem o objetivo de colocar em prática estudos sobre Reconhecimento de Entidades Nomeadas, além de aprender como usar a biblioteca spacy, fazer rotulações, criar exemplos que simulam cenários da vida real e também usar a LLM do Gemini para fazer as rotulações.

## Estrutura das pastas
```plaintext
/
├── 📁 Applications/                  # Contém a aplicação do ner
│   ├dashboard_trend_analysis.ipynb    # Aplicação do ner para analisar tendências de notícias   
│   ├search.ipynb                      # Aplicação do ner para fazer buscas
|   
├── 📁 Data/                           # Contém os dados utilizados na aplicação   
|    ├convert.ipynb                     # Converte os dados do Label-studio pr formato do spacy
│
├── 📁 LLM/
|    ├ner.ipynb                         # Uso de LLM pr rotulação de entidades nomeadas e avaliação
|
├── 📁 Train_teste/
|    ├train_test.ipynb                  # Treino e teste usando spacy     
└── pyproject.toml                      # Dependências do projeto.

## Download do Modelo

Como o GitHub não permite arquivos maiores que 100MB, disponibilizei os arquivos grandes no Google Drive:

🔗 **Download do modelo completo:**  

https://drive.google.com/drive/folders/1wovYthihMs5DESz26aq9ulSD-ACOajo7?usp=sharing

Após baixar, coloque o arquivo na pasta: Applications




## Avaliação do modelo treinado no spacy

**Score F1 Geral (Média de todas entidades): 70.62%**


========================================================
                  DESEMPENHO POR ENTIDADE                  
========================================================
Entidade     |   Precision |      Recall |    F1-Score
--------------------------------------------------------
PER          |     100.00% |     100.00% |     100.00%
LOC          |      96.67% |      85.29% |      90.62%
ORG          |      84.38% |      81.82% |      83.08%
CARGO        |      68.75% |      73.33% |      70.97%
VALOR        |      80.00% |      61.54% |      69.57%
TEMA         |      44.07% |      48.15% |      46.02%
========================================================

---------------------------------------------------------------------------
## Avaliação da LLM

Score F1 Geral (Média de todas entidades): 60.73%


========================================================
                  DESEMPENHO POR ENTIDADE                  
========================================================
Entidade     |   Precision |      Recall |    F1-Score
--------------------------------------------------------
PER          |     100.00% |     100.00% |     100.00%
LOC          |      77.00% |      93.90% |      84.62%
ORG          |      58.00% |      87.00% |      69.60%
CARGO        |      32.23% |      78.00% |      45.61%
VALOR        |      53.85% |      91.30% |      67.74%
TEMA         |      34.75% |      53.25% |      42.06%
========================================================



## Aplicação do NER usando o modelo do spacy para análise de tendências em notícias






## Aplicação do NER para buscas


