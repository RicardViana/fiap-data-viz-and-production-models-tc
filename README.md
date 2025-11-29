# Modelo de ML para Previsão de Obesidade

[![CCDS](https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter)](https://cookiecutter-data-science.drivendata.org/) ![Python](https://img.shields.io/badge/Python-3.10-blue) ![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

## 📋 Sobre o Projeto
Este projeto tem como objetivo desenvolver um modelo de **Machine Learning** capaz de prever se uma pessoa pode ter obesidade. O objetivo é auxiliar na identificação precoce de fatores de risco e apoiar a tomada de decisão em saúde preventiva.

O projeto segue as melhores práticas de Engenharia de Machine Learning, utilizando uma estrutura modular para processamento de dados, treinamento e inferência.

### 🎯 Objetivos
* Realizar análise exploratória para entender correlações entre hábitos e obesidade.
* Criar um pipeline de pré-processamento de dados robusto.
* Treinar e validar modelos preditivos (e.g., Random Forest, XGBoost, Logistic Regression).

### 👨‍💻 Equipe
* [Elton José Araujo Silva](https://www.linkedin.com/in/elton-araujo-silva/)  
* [Leonardo Fajoli Formigon](https://www.linkedin.com/in/leonardo-formigon-63052320b/)  
* [Lucas Augusto Fernandes de Lira](https://www.linkedin.com/in/lucas--lira-/)  
* [Mariana Domingues Brandão](https://www.linkedin.com/in/maridbrandao)  
* [Ricardo Vieira Viana](https://www.linkedin.com/in/ricardvviana)  

### 🚀 Aplicação no Streamlit
Aplicação desenvolvida no Streamlit e disponibilizada através do link
[Análise de Risco de Obesidade](https://fiap-fase4-tc.streamlit.app/)

## 🗂 Estrutura do Projeto
A organização de diretórios segue o padrão **Cookiecutter Data Science** com algumas adaptações:

```text
├── .streamlit/
    └── config.toml
├── data/
│   └── external
│   └── interim
│   └── processed/
        └──  base_limpa.csv
│   └── raw  
        └──  Obesity.csv       
├── docs/
    └──  getting-started.md
    └──  index.md  
    └──  modelagem.md              
├── models/
    └── modelo_risco_obesidade_random_forest.joblib  
├── notebooks/
    └── tech_challenge_codigo.ipynb        
├── references 
    └── POSTECH - Tech Challenge - Fase 4 - Data Analytics_.pdf
    └── dicionario_obesity_fiap.pdf       
├── reports       
├── LICENSE  
├── README.md  
├── app.py     
├── environment.yaml  
├── mkdocs.yml
├── requirements.txt            
```