# 🤖 Documentação da Modelagem e Algoritmos

Esta seção detalha o processo de construção, treinamento e validação dos modelos de Machine Learning utilizados para prever o risco de obesidade.

## 1. Definição do Problema e Variável Alvo

O objetivo do modelo não é apenas classificar o tipo de obesidade, mas sim identificar o **Risco de Obesidade** (Binário).

A variável alvo (`target`) foi construída através de uma regra de negócio baseada em condições clínicas e comportamentais. Um paciente é considerado com **Risco (1)** se atender a critérios de sobrepeso E possuir hábitos de risco (sedentarismo, baixo consumo de água, histórico familiar, etc).

* **0:** Sem risco imediato.
* **1:** Alto risco de obesidade.

## 2. Pré-processamento dos Dados

Antes da modelagem, os dados passaram por um rigoroso processo de tratamento:

1.  **Limpeza e Tradução:** Conversão de variáveis categóricas do inglês para o português e padronização de escalas (ex: `Sometimes` -> `As_vezes`).
2.  **Engenharia de Atributos:**
    * Cálculo do **IMC** (Índice de Massa Corporal) baseado em Peso e Altura.
    * Criação da variável alvo binária baseada em regras condicionais.
3.  **Tratamento de Tipos:** Conversão de floats e inteiros para garantir consistência.

## 3. Pipeline de Transformação

Para garantir a reprodutibilidade e evitar *data leakage*, utilizamos um **Pipeline do Scikit-Learn** com as seguintes etapas:

* **Variáveis Numéricas (`idade`, `imc`):** Normalização com `MinMaxScaler` para colocar os dados na mesma escala.
* **Variáveis Categóricas:** Transformação com `OneHotEncoder` para converter categorias em vetores binários.
* **Balanceamento de Classes:** Aplicação do **SMOTE** (Synthetic Minority Over-sampling Technique) para corrigir o desbalanceamento entre as classes de risco e não-risco.

## 4. Comparação de Modelos

Foram testados dois algoritmos de classificação para identificar qual performava melhor no cenário proposto.

### Modelo 1: Regressão Logística
Utilizado como *baseline* devido à sua interpretabilidade.
* **Acurácia:** 94.8%
* **AUC-ROC:** 0.99

### Modelo 2: Random Forest (Escolhido) 🏆
Utilizado pela sua robustez em lidar com dados não lineares e complexos.
* **Acurácia:** 99.2%
* **AUC-ROC:** 1.00

**Tabela Comparativa de Métricas (Dados de Teste):**

| Métrica | Regressão Logística | Random Forest |
| :--- | :--- | :--- |
| **Acurácia** | 0.948 | **0.992** |
| **Precisão** | 0.976 | **0.989** |
| **Recall** | 0.952 | **1.000** |
| **F1-Score** | 0.964 | **0.995** |

> O modelo **Random Forest** foi selecionado para produção devido à sua performance superior, especialmente no **Recall (1.0)**, garantindo que o modelo raramente deixe de identificar um paciente em risco.

## 5. Importância das Variáveis

A análise de *feature importance* do Random Forest revelou quais fatores mais influenciam no diagnóstico de risco:

1.  **IMC (Índice de Massa Corporal):** O fator predominante (peso ~53%).
2.  **Histórico Familiar:** Forte componente genético/ambiental.
3.  **Idade:** Fator demográfico relevante.
4.  **Hábitos Alimentares:** Comer entre refeições ("beliscar") apareceu com destaque.

## 6. Implementação em Produção

O modelo final foi serializado utilizando a biblioteca `joblib` e está integrado ao aplicativo Streamlit.

* **Arquivo do modelo:** `models/modelo_risco_obesidade_random_forest.joblib`
* **Input:** O modelo recebe um DataFrame com 15 variáveis processadas pelo formulário do usuário.
* **Output:** Classe (0 ou 1) e Probabilidade (%).