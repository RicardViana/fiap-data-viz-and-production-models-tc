# Importar biblioteca completa - padrão
import io
import unicodedata

# Importar biblioteca completa - terceiro
import joblib
import numpy as np
import pandas as pd
import requests
import streamlit as st

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Predição de Risco de Obesidade",
    page_icon="🩺",
    layout="centered"
)

# DEFINIÇÃO DE FUNÇÕES
def ordenar_opcoes(lista):
    """
    Ordena uma lista de strings ignorando acentos e maiúsculas.
    """
    def normalizar(texto):
        if isinstance(texto, str):
            return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').lower()
        return str(texto)
    
    return sorted(lista, key=normalizar)

@st.cache_resource
def load_model():
    """
    Carrega o modelo treinado (.joblib) localmente ou via GitHub.
    """
    # Tentativa Local
    try:
        return joblib.load('modelo_risco_obesidade_random_forest.joblib')
    except FileNotFoundError:
        pass

    # Tentativa Remota (GitHub)
    url_modelo = "https://github.com/RicardViana/fiap-data-viz-and-production-models-tc/raw/refs/heads/main/models/modelo_risco_obesidade_random_forest.joblib"
    
    try:
        response = requests.get(url_modelo)
        if response.status_code == 200:
            return joblib.load(io.BytesIO(response.content))
    except Exception:
        pass
    
    return None

def configurar_sidebar():
    """
    Configura o conteúdo da barra lateral (Sobre, Equipe, Links).
    """
    with st.sidebar:
        st.header("📌 Sobre o Projeto")
        
        st.info(
            """
            Este aplicativo e modelo foi desenvolvido como parte da entrega do **Tech Challenge** da **Fase 4** sobre **Data Viz and Production Models**.
            
            🎓 **Curso:** Pós-Graduação em Data Analytics  
            🏫 **Instituição:** FIAP + Alura
            """
        )
        
        st.markdown("---")
        
        st.subheader("👨‍💻 Equipe de Desenvolvimento")
        
        membros = [
            {"nome": "Elton José Araujo Silva", "link": "https://www.linkedin.com/in/elton-araujo-silva/"},
            {"nome": "Leonardo Fajoli Formigon", "link": "https://www.linkedin.com/in/leonardo-formigon-63052320b/"}, 
            {"nome": "Lucas Augusto Fernandes de Lira", "link": "https://www.linkedin.com/in/lucas--lira-/"},
            {"nome": "Mariana Domingues Brandão", "link": "https://www.linkedin.com/in/maridbrandao"},
            {"nome": "Ricardo Vieira Viana", "link": "https://www.linkedin.com/in/ricardvviana"}

        ]
        
        for membro in membros:
            st.markdown(f"• [{membro['nome']}]({membro['link']})")
            
        st.markdown("---")
        
        st.subheader("📂 Código Fonte")
        st.markdown("Acesse o repositório completo do projeto:")
        st.link_button("🔗 Ver no GitHub", "https://github.com/RicardViana/fiap-data-viz-and-production-models-tc")

def get_user_input_features():
    """
    Coleta os dados do usuário no corpo principal da página e retorna um DataFrame.
    """
    
    # DADOS PESSOAIS
    st.header("1. Dados Pessoais")
    st.markdown("Inicie informando as características físicas básicas.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        idade = st.number_input("Idade", min_value=10, max_value=100, value=25)
        altura = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70)
    
    with col2:
        genero_label = st.selectbox("Gênero", ordenar_opcoes(["Masculino", "Feminino"]))
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0)

    # Cálculo de IMC e Gênero
    imc = int(np.ceil(peso / (altura ** 2)))
    genero = 1 if genero_label == "Feminino" else 0
    
    st.info(f"ℹ️ **IMC Calculado:** {imc} kg/m²")
    st.markdown("---")

    # HISTÓRICO E HÁBITOS
    st.header("2. Histórico e Monitoramento")
    
    col_h1, col_h2 = st.columns(2)
    
    with col_h1:
        historico = st.radio("Possui histórico familiar de sobrepeso?", ["Sim", "Não"], horizontal=True)
        fuma = st.radio("Você fuma?", ["Sim", "Não"], horizontal=True)
    
    with col_h2:
        caloricos = st.radio("Consome alimentos calóricos frequentemente?", ["Sim", "Não"], horizontal=True)
        monitora = st.radio("Costuma monitorar as calorias ingeridas?", ["Sim", "Não"], horizontal=True)

    b_historico_familiar = 1 if historico == "Sim" else 0
    b_fuma = 1 if fuma == "Sim" else 0
    b_come_alimentos_caloricos = 1 if caloricos == "Sim" else 0
    b_monitora_calorias = 1 if monitora == "Sim" else 0

    st.markdown("---")

    # HÁBITOS ALIMENTARES
    st.header("3. Hábitos Alimentares")

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

    col_alim1, col_alim2 = st.columns(2)

    with col_alim1:
        refeicao_key = st.selectbox(
            "Quantas refeições principais faz por dia?", 
            options=sorted(['1', '2', '3', '4+'])
        )
        veg_key = st.selectbox(
            "Frequência de consumo de vegetais?", 
            options=ordenar_opcoes(['Raramente', 'Às vezes', 'Sempre'])
        )
        agua_key = st.selectbox(
            "Consumo diário de água?", 
            options=ordenar_opcoes(['< 1 Litro', '1-2 Litros', '> 2 Litros'])
        )

    with col_alim2:
        fora_key = st.selectbox(
            "Costuma comer entre as refeições?", 
            options=ordenar_opcoes(list(mapa_fora_hora.keys()))
        )
        alcool_key = st.selectbox(
            "Consome bebidas alcoólicas?", 
            options=ordenar_opcoes(list(mapa_alcool.keys()))
        )

    qtd_refeicao = mapa_refeicoes[refeicao_key]
    qtd_vegetais = mapa_vegetais[veg_key]
    qtd_agua = mapa_agua[agua_key]
    freq_come_fora_refeicao = mapa_fora_hora[fora_key]
    freq_alcool = mapa_alcool[alcool_key]

    st.markdown("---")

    # ESTILO DE VIDA
    st.header("4. Estilo de Vida")

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

    col_estilo1, col_estilo2 = st.columns(2)

    with col_estilo1:
        atv_key = st.selectbox(
            "Frequência de atividade física?", 
            options=ordenar_opcoes(list(mapa_atv.keys()))
        )
        net_key = st.selectbox(
            "Tempo diário em dispositivos eletrônicos?", 
            options=ordenar_opcoes(list(mapa_net.keys()))
        )

    with col_estilo2:
        transporte_key = st.selectbox(
            "Meio de transporte principal?", 
            options=ordenar_opcoes(list(mapa_transporte.keys()))
        )

    qtd_atv_fisicas = mapa_atv[atv_key]
    qtd_tmp_na_internet = mapa_net[net_key]
    meio_de_transporte = mapa_transporte[transporte_key]

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

# FUNÇÃO PRINCIPAL

def main():
    # Configura a Barra Lateral
    configurar_sidebar()

    # Carrega o Modelo
    model = load_model()

    # Corpo Principal
    st.title("🩺 Análise de Risco de Obesidade")
    st.markdown("""
    Preencha o formulário abaixo com os dados do paciente.
    O sistema utilizará Machine Learning  para calcular a probabilidade de risco de obesidade.
    """)
    st.markdown("---")

    # Formulário
    input_df = get_user_input_features()

    # Botão e Predição
    st.markdown("###")
    
    if st.button("🔍 Realizar Predição", type="primary", use_container_width=True):
        if model is not None:
            try:
                prediction = model.predict(input_df)
                probability = model.predict_proba(input_df)

                st.markdown("---")
                st.header("Resultado da Análise")

                if prediction[0] == 1:
                    st.error("⚠️ **ALTO RISCO DE OBESIDADE IDENTIFICADO**")
                    st.metric(label="Probabilidade de Risco", value=f"{probability[0][1] * 100:.1f}%")
                    st.warning("👉 **Recomendação:** Sugere-se encaminhamento para orientação médica e nutricional especializada.")
                else:
                    st.success("✅ **BAIXO RISCO IMEDIATO**")
                    st.metric(label="Probabilidade de Risco", value=f"{probability[0][1] * 100:.1f}%")
                    st.info("👉 **Recomendação:** Continue mantendo hábitos saudáveis e acompanhamento regular.")
            
            except Exception as e:
                st.error(f"Ocorreu um erro técnico ao realizar a predição: {e}")
        else:
            st.error("⚠️ O modelo de Inteligência Artificial não foi carregado corretamente. Verifique os arquivos.")

if __name__ == "__main__":
    main()