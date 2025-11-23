import streamlit as st
import pandas as pd
import joblib
import numpy as np
import requests
import io

# Configuração da Página
st.set_page_config(
    page_title="Predição de Risco de Obesidade",
    page_icon="🩺",
    layout="centered"
)

# --- FUNÇÃO PARA CARREGAR O MODELO ---
@st.cache_resource
def load_model():
    # 1. Tenta carregar localmente
    try:
        return joblib.load('modelo_risco_obesidade_random_forest.joblib')
    except FileNotFoundError:
        pass

    # 2. Se não encontrar, tenta baixar do GitHub (ajuste o link se necessário)
    url_modelo = "https://github.com/RicardViana/fiap-data-viz-and-production-models-tc/raw/refs/heads/main/models/modelo_risco_obesidade_random_forest.joblib"
    
    try:
        response = requests.get(url_modelo)
        if response.status_code == 200:
            return joblib.load(io.BytesIO(response.content))
    except Exception:
        pass
    
    st.error("Erro: O modelo não foi encontrado localmente nem via URL.")
    return None

model = load_model()

# --- CABEÇALHO ---
st.title("🩺 Análise de Risco de Obesidade")
st.write("Este aplicativo utiliza Machine Learning para prever se um paciente possui alto risco de obesidade.")
st.markdown("---")

# --- FORMULÁRIO DE ENTRADA ---
st.sidebar.header("Dados do Paciente")

def user_input_features():
    # --- 1. Dados Pessoais ---
    st.subheader("1. Dados Pessoais")
    col1, col2 = st.columns(2)
    
    with col1:
        idade = st.number_input("Idade", min_value=10, max_value=100, value=25)
        altura = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70)
    
    with col2:
        # Gênero com ordem alfabética (Feminino, Masculino)
        genero_label = st.selectbox("Gênero", sorted(["Masculino", "Feminino"]))
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0)

    imc = int(np.ceil(peso / (altura ** 2)))
    st.info(f"IMC Calculado: {imc}")

    genero = 1 if genero_label == "Feminino" else 0

    st.markdown("---")

    # --- 2. Histórico e Hábitos Binários ---
    st.subheader("2. Histórico e Monitoramento")
    
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        historico = st.radio("Histórico familiar de sobrepeso?", ["Sim", "Não"], horizontal=True)
        fuma = st.radio("Você fuma?", ["Sim", "Não"], horizontal=True)
    
    with col_h2:
        caloricos = st.radio("Consome alimentos calóricos frequentemente?", ["Sim", "Não"], horizontal=True)
        monitora = st.radio("Monitora calorias ingeridas?", ["Sim", "Não"], horizontal=True)

    b_historico_familiar = 1 if historico == "Sim" else 0
    b_fuma = 1 if fuma == "Sim" else 0
    b_come_alimentos_caloricos = 1 if caloricos == "Sim" else 0
    b_monitora_calorias = 1 if monitora == "Sim" else 0

    st.markdown("---")

    # --- 3. Hábitos Alimentares ---
    st.subheader("3. Hábitos Alimentares")

    # Qtd Refeições
    mapa_refeicoes = {
        '1': 'Uma_refeicao_principal_por_dia',
        '2': 'Duas_refeicoes_principais_por_dia',
        '3': 'Tres_refeicoes_principais_por_dia',
        '4+': 'Quatro_ou_mais_refeicoes_principais_por_dia'
    }
    # Ordenação Alfabética aplicada
    refeicao_key = st.selectbox("Quantas refeições principais por dia?", options=sorted(['1', '2', '3', '4+']))
    qtd_refeicao = mapa_refeicoes[refeicao_key]

    # Qtd Vegetais
    mapa_vegetais = {'Raramente': 'Raramente', 'Às vezes': 'As_vezes', 'Sempre': 'Sempre'}
    # Ordenação Alfabética aplicada (Às vezes, Raramente, Sempre)
    veg_key = st.selectbox("Consumo de vegetais nas refeições?", options=sorted(['Raramente', 'Às vezes', 'Sempre']))
    qtd_vegetais = mapa_vegetais[veg_key]

    # Qtd Água
    mapa_agua = {'< 1 Litro': 'Baixo_consumo', '1-2 Litros': 'Consumo_adequado', '> 2 Litros': 'Alto_consumo'}
    # Ordenação Alfabética aplicada
    agua_key = st.selectbox("Consumo diário de água?", options=sorted(['< 1 Litro', '1-2 Litros', '> 2 Litros']))
    qtd_agua = mapa_agua[agua_key]

    col_alim1, col_alim2 = st.columns(2)
    with col_alim1:
        mapa_fora_hora = {'Não': 'no', 'Às vezes': 'Sometimes', 'Frequentemente': 'Frequently', 'Sempre': 'Always'}
        # Ordenação Alfabética aplicada
        fora_key = st.selectbox("Come entre as refeições?", options=sorted(list(mapa_fora_hora.keys())))
        freq_come_fora_refeicao = mapa_fora_hora[fora_key]

    with col_alim2:
        mapa_alcool = {'Não': 'no', 'Às vezes': 'Sometimes', 'Frequentemente': 'Frequently', 'Sempre': 'Always'}
        # Ordenação Alfabética aplicada
        alcool_key = st.selectbox("Consome álcool?", options=sorted(list(mapa_alcool.keys())))
        freq_alcool = mapa_alcool[alcool_key]

    st.markdown("---")

    # --- 4. Estilo de Vida ---
    st.subheader("4. Estilo de Vida")

    # Atividade Física
    mapa_atv = {'Sedentário': 'Sedentario', 'Baixa': 'Baixa_frequencia', 'Moderada': 'Moderada_frequencia', 'Alta': 'Alta_frequencia'}
    # Ordenação Alfabética aplicada (Alta, Baixa, Moderada, Sedentário)
    atv_key = st.selectbox("Frequência de atividade física?", options=sorted(list(mapa_atv.keys())))
    qtd_atv_fisicas = mapa_atv[atv_key]

    # Tempo na Internet
    mapa_net = {'Baixo (0-2h)': 'Uso_baixo', 'Moderado (3-5h)': 'Uso_moderado', 'Intenso (>5h)': 'Uso_intenso'}
    # Ordenação Alfabética aplicada
    net_key = st.selectbox("Tempo em dispositivos eletrônicos?", options=sorted(list(mapa_net.keys())))
    qtd_tmp_na_internet = mapa_net[net_key]

    # Transporte
    mapa_transporte = {
        'Transporte Público': 'Public_Transportation', 
        'Caminhada': 'Walking', 
        'Carro': 'Automobile', 
        'Bicicleta': 'Bike', 
        'Moto': 'Motorbike'
    }
    # Ordenação Alfabética aplicada
    transporte_key = st.selectbox("Meio de transporte principal?", options=sorted(list(mapa_transporte.keys())))
    meio_de_transporte = mapa_transporte[transporte_key]

    # Montagem do DataFrame (ordem idêntica ao notebook)
    data = {
        'idade': idade,
        'genero': genero,
        'qtd_refeicao': qtd_refeicao,
        'qtd_vegetais': qtd_vegetais,
        'qtd_agua': qtd_agua,
        'qtd_atv_fisicas': qtd_atv_fisicas,
        'qtd_tmp_na_internet': qtd_tmp_na_internet,
        'b_fuma': b_fuma,
        'b_come_alimentos_caloricos': b_come_alimentos_caloricos,
        'b_monitora_calorias': b_monitora_calorias,
        'b_historico_familiar': b_historico_familiar,
        'freq_come_fora_refeicao': freq_come_fora_refeicao,
        'freq_alcool': freq_alcool,
        'meio_de_transporte': meio_de_transporte,
        'imc': imc
    }
    
    return pd.DataFrame(data, index=[0])

# Captura os dados
input_df = user_input_features()

# --- BOTÃO DE PREDIÇÃO ---
st.markdown("###")
if st.button("Realizar Predição", type="primary"):
    if model is not None:
        prediction = model.predict(input_df)
        probability = model.predict_proba(input_df)

        st.markdown("---")
        st.subheader("Resultado da Análise")

        if prediction[0] == 1:
            st.error(f"⚠️ **Risco de Obesidade Identificado**")
            st.write(f"Probabilidade estimada: **{probability[0][1] * 100:.2f}%**")
            st.warning("Recomenda-se procurar orientação médica e nutricional.")
        else:
            st.success(f"✅ **Sem Risco Imediato de Obesidade**")
            st.write(f"Probabilidade de risco: **{probability[0][1] * 100:.2f}%**")
            st.info("Continue mantendo hábitos saudáveis!")
    else:
        st.warning("Modelo não carregado. Verifique o arquivo .joblib no repositório.")