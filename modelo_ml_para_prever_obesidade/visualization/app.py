# Importar biblioteca completa
import streamlit as st
import joblib 
import numpy as np
import pandas as pd

# Importar algo especifico de uma biblioteca

# Criar Funções (def) 
def main():
    st.title("Formulário de Saúde (Brasil)")
    st.write("Preencha os dados abaixo para análise")

    # SEÇÃO 1: MAPEAMENTOS (O "DE-PARA")
    # Gênero
    # Nota: Verifica no teu modelo se 0 é Feminino ou Masculino.
    mapa_genero = {
        "Feminino": np.int64(0),
        "Masculino": np.int64(1)
    }

    # Quantidade de Refeições
    # Tiramos os underlines (_) para ficar bonito na tela
    mapa_refeicoes = {
        "Uma refeição principal por dia": "Uma_refeicao_principal_por_dia",
        "Duas refeições principais por dia": "Duas_refeicoes_principais_por_dia",
        "Três refeições principais por dia": "Tres_refeicoes_principais_por_dia",
        "Quatro ou mais refeições principais": "Quatro_ou_mais_refeicoes_principais_por_dia"
    }

    # Quantidade de Vegetais
    mapa_vegetais = {
        "Sempre": "Sempre",
        "Às vezes": "As_vezes",
        "Raramente": "Raramente"
    }

    # Quantidade de Água
    mapa_agua = {
        "Menos de 1 litro (Baixo)": "Baixo_consumo",
        "Entre 1 e 2 litros (Adequado)": "Consumo_adequado",
        "Mais de 2 litros (Alto)": "Alto_consumo"
    }

    # Atividades Físicas
    mapa_atv_fisica = {
        "Sedentário": "Sedentario",
        "Baixa frequência": "Baixa_frequencia",
        "Moderada frequência": "Moderada_frequencia",
        "Alta frequência": "Alta_frequencia"
    }

    # Tempo na Internet
    mapa_internet = {
        "Pouco uso": "Uso_baixo",
        "Uso moderado": "Uso_moderado",
        "Uso intenso": "Uso_intenso"
    }

    # Frequências Gerais (Para Comer Fora e Álcool)
    # O modelo pede em Inglês: 'Always', 'Frequently', 'Sometimes', 'no'
    mapa_frequencia_geral = {
        "Sempre": "Always",
        "Frequentemente": "Frequently",
        "Às vezes": "Sometimes",
        "Nunca": "no"
    }

    # Meio de Transporte
    # O modelo pede em Inglês
    mapa_transporte = {
        "Automóvel": "Automobile",
        "Bicicleta": "Bike",
        "Motocicleta": "Motorbike",
        "Transporte Público": "Public_Transportation",
        "Caminhando / A pé": "Walking"
    }

    # Sim/Não (Binários)
    mapa_sim_nao = {
        "Não": np.int64(0), 
        "Sim": np.int64(1)
    }

    # SEÇÃO 2: CRIAÇÃO DOS WIDGETS NA TELA
    
    # --- Bloco 1: Dados Pessoais ---
    st.subheader("Dados Pessoais")

    # 1. Gênero
    label_genero = st.radio("Gênero:", list(mapa_genero.keys()), horizontal=True)
    val_genero = mapa_genero[label_genero]

    # 2. Refeições
    label_refeicao = st.selectbox("Refeições diárias:", list(mapa_refeicoes.keys()))
    val_refeicao = mapa_refeicoes[label_refeicao]

    # 3. Vegetais
    label_vegetais = st.selectbox("Consumo de vegetais:", list(mapa_vegetais.keys()))
    val_vegetais = mapa_vegetais[label_vegetais]

    # 4. Água
    label_agua = st.selectbox("Consumo de água:", list(mapa_agua.keys()))
    val_agua = mapa_agua[label_agua]

    # 5. Atividades Físicas
    label_atv = st.selectbox("Atividade física:", list(mapa_atv_fisica.keys()))
    val_atv = mapa_atv_fisica[label_atv]

    # 6. Internet
    label_internet = st.selectbox("Tempo de tela (Internet):", list(mapa_internet.keys()))
    val_internet = mapa_internet[label_internet]

    st.markdown("---") # Uma linha para separar visualmente
    st.subheader("Hábitos")
    
    # 7. Fuma
    label_fuma = st.radio("Fuma?", list(mapa_sim_nao.keys()), horizontal=True)
    val_fuma = mapa_sim_nao[label_fuma]

    # 8. Alimentos Calóricos
    label_caloricos = st.radio("Come alimentos muito calóricos?", list(mapa_sim_nao.keys()), horizontal=True)
    val_caloricos = mapa_sim_nao[label_caloricos]

    # 9. Monitora Calorias
    label_monitora = st.radio("Monitora calorias?", list(mapa_sim_nao.keys()), horizontal=True)
    val_monitora = mapa_sim_nao[label_monitora]

    # 10. Histórico Familiar
    label_historico = st.radio("Histórico familiar de obesidade?", list(mapa_sim_nao.keys()), horizontal=True)
    val_historico = mapa_sim_nao[label_historico]
    
    st.markdown("---")
    st.subheader("Estilo de Vida")

    # 11. Comer Fora
    label_come_fora = st.selectbox("Comer fora de hora/refeição:", list(mapa_frequencia_geral.keys()))
    val_come_fora = mapa_frequencia_geral[label_come_fora]

    # 12. Álcool
    label_alcool = st.selectbox("Consumo de álcool:", list(mapa_frequencia_geral.keys()))
    val_alcool = mapa_frequencia_geral[label_alcool]

    # 13. Transporte
    label_transporte = st.selectbox("Principal transporte:", list(mapa_transporte.keys()))
    val_transporte = mapa_transporte[label_transporte]

    # SEÇÃO 3: PROCESSAMENTO
    st.markdown("---")
    
    if st.button("Enviar Dados"):
        # Montamos o dicionário final usando as variáveis 'val_' que contêm os dados em INGLÊS/NUMÉRICO
        dados_finais = {
            "genero": val_genero,
            "qtd_refeicao": val_refeicao,
            "qtd_vegetais": val_vegetais,
            "qtd_agua": val_agua,
            "qtd_atv_fisicas": val_atv,
            "qtd_tmp_na_internet": val_internet,
            "b_fuma": val_fuma,
            "b_come_alimentos_caloricos": val_caloricos,
            "b_monitora_calorias": val_monitora,
            "b_historico_familiar": val_historico,
            "freq_come_fora_refeicao": val_come_fora,
            "freq_alcool": val_alcool,
            "meio_de_transporte": val_transporte
        }

        st.success("Dados convertidos e prontos para o modelo!")
        
        # Mostra visualmente a tradução para você conferir
        st.write("O que o modelo vai receber (JSON):")
        st.json(dados_finais)

        # DataFrame
        df = pd.DataFrame([dados_finais])
        st.write("Formato Tabela:")
        st.dataframe(df)

#Criar app no Streamlit
st.write('# Modelo para prever obesidade')

st.write('## Observação')
st.write('### ' \
    'Aplicação criada como entrega do Tech Challenge da fase 4 referente a Data Viz and Production Models  \
    Link do repositorio: https://github.com/RicardViana/fiap-data-viz-and-production-models-tc'
    )

if __name__ == "__main__":
    main()

