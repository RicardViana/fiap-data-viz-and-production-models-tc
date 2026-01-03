# 🧠 Modelo de Machine Learning para Previsão de Obesidade

[![CCDS](https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter)](https://cookiecutter-data-science.drivendata.org/) ![Python](https://img.shields.io/badge/Python-3.10-blue) ![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

## 📋 Sobre o Projeto

Este repositório reúne todo o desenvolvimento do **Tech Challenge – Fase 4 (Data Analytics)** da pós-graduação FIAP. O desafio consiste em criar um **modelo preditivo de obesidade** utilizando Machine Learning, além de uma aplicação em Streamlit e um painel analítico com insights relevantes para suporte à equipe médica.

A solução foi construída seguindo boas práticas de **Engenharia de Machine Learning**, utilizando estrutura modular, versionamento de dados e documentação organizada.

---

## 🎯 Objetivos do Projeto

* Realizar **análise exploratória** completa da base *Obesity.csv*.
* Construir **pipeline de pré-processamento**, incluindo engenharia de atributos.
* Treinar diferentes modelos (Random Forest, XGBoost, Regressão Logística etc.) e selecionar aquele com melhor desempenho (acurácia mínima 75%).
* Implementar uma **aplicação preditiva no Streamlit** para utilização pelos profissionais da saúde.
* Criar um **dashboard analítico** com os principais insights obtidos.
* Publicar a solução completa com documentação e reprodutibilidade.

---

## 🏥 Contexto do Problema

A obesidade é uma condição multifatorial relacionada a hábitos alimentares, estilo de vida, genética e fatores ambientais. Prever antecipadamente o risco de obesidade auxilia profissionais da saúde em ações preventivas e diagnósticos mais rápidos.

O modelo desenvolvido utiliza variáveis como alimentação, atividade física, consumo de água, alcoolismo, tabagismo e tempo de uso de dispositivos eletrônicos para prever o nível de obesidade de um indivíduo.

---

## 🚀 Aplicação no Streamlit

A aplicação preditiva pode ser acessada no link:
👉 **[Análise de Risco de Obesidade](https://fiap-fase4-tc.streamlit.app/)**

Nela, o usuário pode inserir suas informações e obter uma previsão imediata do nível de risco conforme o modelo treinado.

---

## 📘 Documentação no MkDocs
E para auxiliar foi desenvolvido a documentação via MkDocs e disponibilizado no link
**[Projeto Tech Challenge](https://ricardviana.github.io/fiap-data-viz-and-production-models-tc/)**

---

## 🗂 Estrutura do Projeto

A organização segue o padrão **Cookiecutter Data Science**, com pequenas adaptações:

```
├── .streamlit/
│   └── config.toml
├── data/
│   ├── raw/
│   │   └── Obesity.csv
│   ├── processed/
│   │   └── base_limpa.csv
│   ├── interim/
│   └── external/
├── docs/
│   ├── getting-started.md
│   ├── index.md
│   └── modelagem.md
├── models/
│   └── modelo_risco_obesidade_random_forest.joblib
├── notebooks/
│   └── tech_challenge_codigo.ipynb
├── references/
│   ├── dicionario_obesity_fiap.pdf
│   └── POSTECH - Tech Challenge - Fase 4 - Data Analytics_.pdf
├── reports/
├── environment.yaml
├── requirements.txt
├── mkdocs.yml
├── app.py
├── LICENSE
└── README.md
```

---

## 📊 Dados

O dicionário de dados utilizado está disponível na pasta `references/`. As variáveis incluem:

* hábitos alimentares
* atividade física
* consumo de água e álcool
* tabagismo
* uso de dispositivos eletrônicos
* dados antropométricos (peso, altura, idade)

A variável-alvo é **Obesity**, com níveis variando de *Insufficient Weight* até *Obesity Type III*.

---

## 🧪 Metodologia

### **1. Pré-processamento**

* Tratamento e limpeza de dados
* Codificação de variáveis categóricas
* Normalização/Padronização
* Feature Engineering

### **2. Modelagem**

Modelos testados:

* Random Forest (modelo final escolhido)
* Logistic Regression

Métricas avaliadas:

* Acurácia
* F1-Score
* Matriz de confusão

### **3. Deploy**

* Aplicação Streamlit
* Modelo versionado em `.joblib`
* Ambiente reproduzível (conda + requirements)

---

## 📈 Dashboard Analítico

O painel apresenta insights como:

* IMC Médio
* Média de idade
* Risco de obesidade 
* Nível de obesidade 

E pode ser consultando através do [Dashboard](https://app.powerbi.com/view?r=eyJrIjoiYjU2ZThiZjktMWVmMS00ZGI0LThmMTItMGE2ZjcyNWNhZmY2IiwidCI6ImM0MjlmMGY3LTY4YzEtNGVlZC05NzRlLTRhMDZlYzUzOTc5MiJ9)

---

## 👨‍💻 Equipe

* [Elton José Araujo Silva](https://www.linkedin.com/in/elton-araujo-silva/)
* [Leonardo Fajoli Formigon](https://www.linkedin.com/in/leonardo-formigon-63052320b/)
* [Lucas Augusto Fernandes de Lira](https://www.linkedin.com/in/lucas--lira-/)
* [Mariana Domingues Brandão](https://www.linkedin.com/in/maridbrandao)
* [Ricardo Vieira Viana](https://www.linkedin.com/in/ricardvviana)

---

## 📜 Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.

---

**Obrigado por visitar o projeto!** 🚀
