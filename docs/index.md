# 🩺 Predição de Risco de Obesidade

Bem-vindo à documentação oficial do projeto **Tech Challenge - Fase 4**. Este projeto foi desenvolvido como parte da Pós-Graduação em **Data Analytics** da **FIAP + Alura**.

## 🎯 Objetivo do Projeto

O objetivo principal é desenvolver um modelo de **Machine Learning** capaz de estimar o **risco de obesidade** de um indivíduo com base em seus hábitos alimentares, estilo de vida e histórico familiar.

Além da modelagem, o projeto engloba a construção de um pipeline de dados robusto e o deploy de uma aplicação interativa para uso de profissionais da saúde.

## 🧠 A Solução

Nossa abordagem consistiu em:

1.  **Análise Exploratória:** Estudo aprofundado de uma base de dados com registros de hábitos de vida e condições físicas.
2.  **Engenharia de Atributos:** Criação de uma variável alvo personalizada (`Risco de Obesidade`) baseada em regras de negócio clínicas (IMC + Comorbidades/Hábitos).
3.  **Machine Learning:** Treinamento e comparação de modelos (Regressão Logística e Random Forest), utilizando técnicas como **SMOTE** para balanceamento de dados.
4.  **Aplicação Web:** Desenvolvimento de uma interface amigável com **Streamlit** para realizar predições em tempo real.

## 🏆 Resultados Chave

* **Modelo Escolhido:** Random Forest Classifier.
* **Performance:** O modelo atingiu uma acurácia superior a **99%** e um **Recall de 100%** nos dados de teste, garantindo que casos de risco não passem despercebidos.
* **Fatores Críticos:** O IMC, histórico familiar e frequência de refeições foram identificados como os fatores mais determinantes.

## 👨‍💻 Equipe de Desenvolvimento

Este projeto foi realizado pelo **Grupo 63**:

* **Elton José Araujo Silva**
* **Leonardo Fajoli Formigon**
* **Lucas Augusto Fernandes de Lira**
* **Mariana Domingues Brandão**
* **Ricardo Vieira Viana**

---

Para começar a usar ou contribuir com o projeto, visite a página [Getting Started](getting-started.md).