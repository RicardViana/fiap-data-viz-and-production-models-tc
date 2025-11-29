# 🤖 Documentação da Modelagem — Tech Challenge Fase 4

Este documento apresenta, de forma estruturada e clara, todo o processo de **modelagem, tratamento de dados e avaliação dos algoritmos** utilizados no desenvolvimento do sistema preditivo de risco de obesidade.

---

## 1. 🎯 Definição do Problema

O objetivo principal é prever **o risco de obesidade** de um paciente com base em hábitos, características físicas e comportamentais — permitindo que profissionais da saúde tomem decisões preventivas de forma mais assertiva.

A variável-alvo foi convertida em um problema **binário**, indicando:

* **0 — Sem Risco Imediato**
* **1 — Alto Risco de Obesidade**

A regra de negócio para definir o risco considerou:

* níveis de sobrepeso/obesidade da variável original `Obesity`,
* hábitos de risco (sedentarismo, ingestão de água reduzida, consumo frequente de alimentos calóricos, histórico familiar etc.).

---

## 2. 🧼 Pré-processamento dos Dados

O conjunto de dados passou por diversas etapas de preparação, garantindo consistência e qualidade para a etapa de modelagem.

### 🔹 **2.1 Limpeza e Padronização**

* Padronização de categorias em inglês.
* Correção de ruídos nas variáveis de escala (1–3 ou 1–4) conforme dicionário FIAP.
* Normalização de representações inconsistentes.

### 🔹 **2.2 Engenharia de Atributos**

Principais variáveis criadas:

* **IMC (peso / altura²):** indicador central para risco de obesidade.
* **Variável‑alvo binária** com base em critérios clínicos e comportamentais.

### 🔹 **2.3 Tratamento de Tipos**

* Conversão de numéricos para `float`/`int`.
* Conversão de categóricos para `string`.

---

## 3. 🧱 Pipeline de Transformação

Para garantir reprodutibilidade e evitar *data leakage*, foi utilizado um pipeline Scikit‑Learn.

### Componentes do Pipeline:

* **Numéricas (idade, IMC):** normalização com `MinMaxScaler`.
* **Categóricas:** codificação com `OneHotEncoder`.
* **Balanceamento:** técnica **SMOTE** devido ao desbalanceamento entre classes.

Esse pipeline foi salvo junto ao modelo final para ser utilizado tanto no treinamento quanto no ambiente de produção (Streamlit).

---

## 4. 🤖 Modelos Testados

Diversos modelos foram avaliados para identificar aquele com melhor desempenho e menor risco de subdiagnosticar pacientes.

### **Modelo 1 — Regressão Logística (Baseline)**

* Simples e interpretável.
* Serviu como referência inicial.
* **Acurácia:** 94.8%
* **AUC‑ROC:** 0.99

### **Modelo 2 — Random Forest (Modelo Final)** 🏆

Escolhido por sua robustez, não linearidade e excelente desempenho.

* **Acurácia:** 99.2%
* **AUC‑ROC:** 1.00

### 📊 Comparação de Métricas (Dados de Teste)

| Métrica      | Regressão Logística | Random Forest |
| ------------ | ------------------- | ------------- |
| **Acurácia** | 0.948               | **0.992**     |
| **Precisão** | 0.976               | **0.989**     |
| **Recall**   | 0.952               | **1.000**     |
| **F1-Score** | 0.964               | **0.995**     |

📌 **Motivo da escolha:** o Random Forest apresentou **Recall = 1.0**, garantindo que praticamente nenhum paciente em risco seja classificado como seguro.

---

## 5. 📌 Importância das Variáveis

A análise de *feature importance* mostrou os fatores mais relevantes para o risco de obesidade:

1. **IMC — fator mais influente (>50%)**
2. **Histórico familiar de sobrepeso**
3. **Idade**
4. **Hábitos alimentares:** especialmente `CAEC` (comer entre refeições)
5. **Nível de atividade física (FAF)**

---

## 6. ⚙️ Deploy e Produção

O modelo final foi integrado ao aplicativo Streamlit.

### 🔹 Arquivos Importantes

* `models/modelo_risco_obesidade_random_forest.joblib` — modelo final treinado
* `app.py` — lógica do formulário e predição
* `data/processed/base_limpa.csv` — dados processados
* Pipeline salvo junto ao modelo

### 🔹 Entrada do Modelo

Um DataFrame com as variáveis já transformadas e codificadas.

### 🔹 Saída do Modelo

* **Classe (0 ou 1)**
* **Probabilidade de risco (%)**

Essa estrutura permite que o sistema seja facilmente adaptado para novos dados ou reentreinamento.

---

## 7. 📎 Referências

* Dicionário oficial FIAP (`dicionario_obesity_fiap.pdf`)
* Documento técnico do Tech Challenge Fase 4
* Notebook do projeto (`notebooks/tech_challenge_codigo.ipynb`)
