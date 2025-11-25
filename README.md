# Modelo de ML para Previsão de Obesidade

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>
<img src="https://img.shields.io/badge/Python-3.8%2B-blue" />
<img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow" />

## 📋 Sobre o Projeto

Este projeto tem como objetivo desenvolver um modelo de **Machine Learning** capaz de classificar ou prever níveis de obesidade com base em dados demográficos, hábitos alimentares e condição física. O objetivo é auxiliar na identificação precoce de fatores de risco e apoiar a tomada de decisão em saúde preventiva.

O projeto segue as melhores práticas de Engenharia de Machine Learning, utilizando uma estrutura modular para processamento de dados, treinamento e inferência.

### 🎯 Objetivos
* Realizar análise exploratória para entender correlações entre hábitos e obesidade.
* Criar um pipeline de pré-processamento de dados robusto.
* Treinar e validar modelos preditivos (e.g., Random Forest, XGBoost, Logistic Regression).
* Disponibilizar scripts para inferência em novos dados.

---

## 🗂 Estrutura do Projeto

A organização de diretórios segue o padrão **Cookiecutter Data Science**:

```text
├── LICENSE            <- Licença do projeto (ex: MIT, Apache)
├── Makefile           <- Comandos de automação (ex: `make data`, `make train`)
├── README.md          <- Documentação principal do projeto
├── data
│   ├── external       <- Dados de fontes terceiras
│   ├── interim        <- Dados intermediários/transformados
│   ├── processed      <- Dados finais prontos para modelagem
│   └── raw            <- Dados originais (imutáveis)
│
├── docs               <- Documentação gerada (mkdocs)
├── models             <- Modelos serializados (.pkl, .joblib) e artefatos
├── notebooks          <- Jupyter notebooks para exploração e prototipagem
├── pyproject.toml     <- Configuração do projeto e ferramentas (black, flake8)
├── references         <- Dicionários de dados e manuais
├── reports            <- Análises geradas (HTML, PDF)
│   └── figures        <- Gráficos e visualizações salvas
├── requirements.txt   <- Dependências do projeto
├── setup.cfg          <- Configurações de linter
└── modelo_ml_para_prever_obesidade   <- Código fonte principal (Pacote Python)
    ├── __init__.py
    ├── config.py               <- Variáveis globais e configurações
    ├── dataset.py              <- Scripts para baixar/gerar dados
    ├── features.py             <- Engenharia de features
    ├── modeling                
    │   ├── predict.py          <- Script de inferência/predição
    │   └── train.py            <- Script de treinamento do modelo
    └── plots.py                <- Scripts de visualização
```

## Aplicação no Streamlit

https://fiap-fase4-tc.streamlit.app/
