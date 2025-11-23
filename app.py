import io
import unicodedata

import joblib
import numpy as np
import pandas as pd
import requests
import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando Streamlit) ---
st.set_page_config(
    page_title="Predição de Risco de Obesidade",
    page_icon="🩺",
    layout="centered"
)


# --- DEFINIÇÃO DE FUNÇÕES ---

def ordenar_opcoes(lista):
    """
    Ordena uma lista de strings ignorando acentos e maiúsculas para exibição correta.
    Exemplo: Faz 'Às vezes' vir antes de 'Raramente'.
    """
    def normalizar(texto):
        if isinstance(texto, str):
            return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').lower()
        return str(texto)
    
    return sorted(lista, key=normalizar)


@st.cache_resource
def load_model():
    """
    Carrega o modelo treinado (.joblib).
    Tenta carregar localmente primeiro, depois via URL do GitHub.
    """
    # 1. Tentativa Local
    try:
        return joblib.load('modelo_risco_obesidade_random_forest.joblib')
    except FileNotFoundError:
        pass

    # 2. Tentativa Remota (GitHub Raw)
    # ATENÇÃO: Substitua pelo link 'Raw' do seu repositório
    url_modelo = "https://raw.githubusercontent.com/SEU_USUARIO/NOME_REPO/main/modelo_risco_obesidade_random_forest.joblib"
    
    try:
        response = requests.get(url_modelo)
        if response.status_code == 200:
            return joblib.load(io.BytesIO(response.content))
    except Exception:
        pass
    
    return None


def get_user_input_features():
    """
    Cria a barra lateral, coleta os dados do usuário e retorna um DataFrame.
    """
    st.sidebar.header("Dados do Paciente")

    # --- 1. Dados Pessoais ---
    st.sidebar.subheader("1. Dados Pessoais")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        idade = st.number_input("Idade", min_value=10, max_value=100, value=25)
        altura = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70)
    
    with col2:
        genero_label = st.selectbox("Gênero", ordenar_opcoes(["Masculino", "Feminino"]))
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0)

    # Cálculo de IMC e Gênero
    imc = int(np.ceil(peso / (altura ** 2)))
    genero = 1 if genero_label == "Feminino" else 0
    
    st.sidebar.info(f"IMC Calculado: {imc}")
    st.sidebar.markdown("---")

    # --- 2. Histórico e Hábitos Binários ---
    st.sidebar.subheader("2. Histórico e Monitoramento")
    
    historico = st.sidebar.radio("Histórico familiar de sobrepeso?", ["Sim", "Não"], horizontal=True)
    fuma = st.sidebar.radio("Você fuma?", ["Sim", "Não"], horizontal=True)
    caloricos = st.sidebar.radio("Consome alimentos calóricos frequentemente?", ["Sim", "Não"], horizontal=True)
    monitora = st.sidebar.radio("Monitora calorias ingeridas?", ["Sim", "Não"], horizontal=True)

    # Mapeamento Binário
    b_historico_familiar = 1 if historico == "Sim" else 0
    b_fuma = 1 if fuma == "Sim" else 0
    b_come_alimentos_caloricos = 1 if caloricos == "Sim" else 0
    b_monitora_calorias = 1 if monitora == "Sim" else 0

    st.sidebar.markdown("---")

    # --- 3. Hábitos Alimentares ---
    st.sidebar.subheader("3. Hábitos Alimentares")

    # Mapeamentos
    mapa_refeicoes = {
        '1': 'Uma_refeicao_principal_por_dia',
        '2': 'Duas_refeicoes_principais_por_dia',
        '3': 'Tres_refeicoes_principais_por_dia',
        '4+': 'Quatro_ou_mais_refeicoes_principais_por_dia'
    }
    mapa_vegetais = {'Raramente': 'Raramente', 'Às vezes': 'As_vezes', 'Sempre': 'Sempre'}
    mapa_agua = {'< 1 Litro': 'Baixo_consumo', '1-2 Litros': 'Consumo_adequado', '> 2 Litros': 'Alto_consumo'}
    mapa_fora_hora = {'Não': 'no', 'Às vezes': 'Sometimes', 'Frequentemente': 'Frequently', 'Sempre': 'Always'}
    mapa_alcool = {'Não': 'no', 'Às vezes': 'Sometimes', 'Frequentemente': 'Frequently', 'Sempre': 'Always'}

    # Inputs com Selectbox e Ordenação
    refeicao_key = st.sidebar.selectbox(
        "Quantas refeições principais por dia?", 
        options=sorted(['1', '2', '3', '4+'])
    )
    
    veg_key = st.sidebar.selectbox(
        "Consumo de vegetais nas refeições?", 
        options=ordenar_opcoes(['Raramente', 'Às vezes', 'Sempre'])
    )
    
    agua_key = st.sidebar.selectbox(
        "Consumo diário de água?", 
        options=ordenar_opcoes(['< 1 Litro', '1-2 Litros', '> 2 Litros'])
    )
    
    fora_key = st.sidebar.selectbox(
        "Come entre as refeições?", 
        options=ordenar_opcoes(list(mapa_fora_hora.keys()))
    )
    
    alcool_key = st.sidebar.selectbox(
        "Consome álcool?", 
        options=ordenar_opcoes(list(mapa_alcool.keys()))
    )

    # Atribuição dos valores mapeados
    qtd_refeicao = mapa_refeicoes[refeicao_key]
    qtd_vegetais = mapa_vegetais[veg_key]
    qtd_agua = mapa_agua[agua_key]
    freq_come_fora_refeicao = mapa_fora_hora[fora_key]
    freq_alcool = mapa_alcool[alcool_key]

    st.sidebar.markdown("---")

    # --- 4. Estilo de Vida ---
    st.sidebar.subheader("4. Estilo de Vida")

    mapa_atv = {
        'Sedentário': 'Sedentario', 
        'Baixa': 'Baixa_frequencia', 
        'Moderada': 'Moderada_frequencia', 
        'Alta': 'Alta_frequencia'
    }
    mapa_net = {
        'Baixo (0-2h)': 'Uso_baixo', 
        'Moderado (3-5h)': 'Uso_moderado', 
        'Intenso (>5h)': 'Uso_intenso'
    }
    mapa_transporte = {
        'Transporte Público': 'Public_Transportation', 
        'Caminhada': 'Walking', 
        'Carro': 'Automobile', 
        'Bicicleta': 'Bike', 
        'Moto': 'Motorbike'
    }

    atv_key = st.sidebar.selectbox(
        "Frequência de atividade física?", 
        options=ordenar_opcoes(list(mapa_atv.keys()))
    )
    
    net_key = st.sidebar.selectbox(
        "Tempo em dispositivos eletrônicos?", 
        options=ordenar_opcoes(list(mapa_net.keys()))
    )
    
    transporte_key = st.sidebar.selectbox(
        "Meio de transporte principal?", 
        options=ordenar_opcoes(list(mapa_transporte.keys()))
    )

    qtd_atv_fisicas = mapa_atv[atv_key]
    qtd_tmp_na_internet = mapa_net[net_key]
    meio_de_transporte = mapa_transporte[transporte_key]

    # Dicionário de dados para o DataFrame
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


# --- EXECUÇÃO DO APP ---

def main():
    # Carregamento do Modelo
    model = load_model()

    # Layout Principal
    st.title("🩺 Análise de Risco de Obesidade")
    st.write("Este aplicativo utiliza Machine Learning para prever se um paciente possui alto risco de obesidade.")
    st.markdown("---")

    # Captura dos dados da Sidebar
    input_df = get_user_input_features()

    # Exibição do resumo dos dados (opcional, para conferência do usuário)
    with st.expander("Ver dados selecionados"):
        st.dataframe(input_df)

    # Botão de Predição
    st.markdown("###")
    if st.button("Realizar Predição", type="primary"):
        if model is not None:
            try:
                prediction = model.predict(input_df)
                probability = model.predict_proba(input_df)

                st.markdown("---")
                st.subheader("Resultado da Análise")

                if prediction[0] == 1:
                    st.error("⚠️ **Risco de Obesidade Identificado**")
                    st.write(f"Probabilidade estimada: **{probability[0][1] * 100:.2f}%**")
                    st.warning("Recomenda-se procurar orientação médica e nutricional.")
                else:
                    st.success("✅ **Sem Risco Imediato de Obesidade**")
                    st.write(f"Probabilidade de risco: **{probability[0][1] * 100:.2f}%**")
                    st.info("Continue mantendo hábitos saudáveis!")
            except Exception as e:
                st.error(f"Ocorreu um erro ao realizar a predição: {e}")
        else:
            st.error("Modelo não carregado. Verifique o arquivo .joblib no repositório.")

# Ponto de entrada do script
if __name__ == "__main__":
    main()