import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Predição de Risco de Obesidade", layout="centered")

# --- CARREGAMENTO DO MODELO DO GITHUB ---
@st.cache_resource
def carregar_modelo_github():
    # URL RAW do seu modelo no GitHub (SUBSTITUA PELO SEU LINK REAL)
    # Exemplo: https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main/modelo.joblib
    url_modelo = "https://github.com/RicardViana/fiap-data-viz-and-production-models-tc/raw/refs/heads/main/models/modelo_risco_obesidade_random_forest.joblib" 
    
    try:
        if "COLE_AQUI" in url_modelo:
            st.warning("⚠️ Você precisa substituir a variável 'url_modelo' no código pelo link Raw do seu GitHub.")
            return None
            
        response = requests.get(url_modelo)
        response.raise_for_status()
        
        modelo_arquivo = io.BytesIO(response.content)
        modelo = joblib.load(modelo_arquivo)
        return modelo
    except Exception as e:
        st.error(f"Erro ao baixar/carregar o modelo do GitHub: {e}")
        return None

modelo = carregar_modelo_github()

def main():
    st.title("Monitor de Saúde & Predição")
    st.write("Preencha os dados abaixo para analisar o perfil de risco.")

    # ==============================================================================
    # SEÇÃO 1: MAPEAMENTOS
    # ==============================================================================
    
    mapa_genero = {"Feminino": np.int64(0), "Masculino": np.int64(1)}
    
    mapa_refeicoes = {
        "Uma refeição principal por dia": "Uma_refeicao_principal_por_dia",
        "Duas refeições principais por dia": "Duas_refeicoes_principais_por_dia",
        "Três refeições principais por dia": "Tres_refeicoes_principais_por_dia",
        "Quatro ou mais refeições principais": "Quatro_ou_mais_refeicoes_principais_por_dia"
    }

    mapa_vegetais = {"Sempre": "Sempre", "Às vezes": "As_vezes", "Raramente": "Raramente"}

    mapa_agua = {
        "Menos de 1 litro (Baixo)": "Baixo_consumo",
        "Entre 1 e 2 litros (Adequado)": "Consumo_adequado",
        "Mais de 2 litros (Alto)": "Alto_consumo"
    }

    mapa_atv_fisica = {
        "Sedentário": "Sedentario",
        "Baixa frequência": "Baixa_frequencia",
        "Moderada frequência": "Moderada_frequencia",
        "Alta frequência": "Alta_frequencia"
    }

    mapa_internet = {"Pouco uso": "Uso_baixo", "Uso moderado": "Uso_moderado", "Uso intenso": "Uso_intenso"}

    mapa_frequencia_geral = {
        "Sempre": "Always", "Frequentemente": "Frequently", "Às vezes": "Sometimes", "Nunca": "no"
    }

    mapa_transporte = {
        "Automóvel": "Automobile", "Bicicleta": "Bike", "Motocicleta": "Motorbike", 
        "Transporte Público": "Public_Transportation", "Caminhando / A pé": "Walking"
    }

    mapa_sim_nao = {"Não": np.int64(0), "Sim": np.int64(1)}

    # ==============================================================================
    # SEÇÃO 2: FORMULÁRIO
    # ==============================================================================

    st.subheader("Dados Pessoais")

    label_genero = st.radio("Gênero:", list(mapa_genero.keys()), horizontal=True)
    val_genero = mapa_genero[label_genero]

    col_dados_fisicos = st.columns(3)
    idade = col_dados_fisicos[0].number_input("Idade", min_value=10, max_value=100, value=25)
    altura = col_dados_fisicos[1].number_input("Altura (m)", min_value=1.00, max_value=2.50, value=1.70, step=0.01)
    peso = col_dados_fisicos[2].number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)

    label_refeicao = st.selectbox("Refeições diárias:", list(mapa_refeicoes.keys()))
    val_refeicao = mapa_refeicoes[label_refeicao]

    label_vegetais = st.selectbox("Consumo de vegetais:", list(mapa_vegetais.keys()))
    val_vegetais = mapa_vegetais[label_vegetais]

    label_agua = st.selectbox("Consumo de água:", list(mapa_agua.keys()))
    val_agua = mapa_agua[label_agua]

    label_atv = st.selectbox("Atividade física:", list(mapa_atv_fisica.keys()))
    val_atv = mapa_atv_fisica[label_atv]

    label_internet = st.selectbox("Tempo de tela (Internet):", list(mapa_internet.keys()))
    val_internet = mapa_internet[label_internet]

    st.markdown("---")
    st.subheader("Hábitos")
    
    label_fuma = st.radio("Fuma?", list(mapa_sim_nao.keys()), horizontal=True)
    val_fuma = mapa_sim_nao[label_fuma]

    label_caloricos = st.radio("Come alimentos muito calóricos?", list(mapa_sim_nao.keys()), horizontal=True)
    val_caloricos = mapa_sim_nao[label_caloricos]

    label_monitora = st.radio("Monitora calorias?", list(mapa_sim_nao.keys()), horizontal=True)
    val_monitora = mapa_sim_nao[label_monitora]

    label_historico = st.radio("Histórico familiar de obesidade?", list(mapa_sim_nao.keys()), horizontal=True)
    val_historico = mapa_sim_nao[label_historico]
    
    st.markdown("---")
    st.subheader("Estilo de Vida")

    label_come_fora = st.selectbox("Comer fora de hora/refeição:", list(mapa_frequencia_geral.keys()))
    val_come_fora = mapa_frequencia_geral[label_come_fora]

    label_alcool = st.selectbox("Consumo de álcool:", list(mapa_frequencia_geral.keys()))
    val_alcool = mapa_frequencia_geral[label_alcool]

    label_transporte = st.selectbox("Principal transporte:", list(mapa_transporte.keys()))
    val_transporte = mapa_transporte[label_transporte]

    # ==============================================================================
    # SEÇÃO 3: PROCESSAMENTO E PREDIÇÃO
    # ==============================================================================
    
    st.markdown("---")
    
    if st.button("Calcular Risco"):
        if modelo is None:
            st.error("Erro: Modelo não carregado. Verifique o link do GitHub no código.")
        else:
            # 1. CÁLCULO DO IMC (Feature Engineering)
            # O modelo exige 'imc', então calculamos aqui
            imc_calculado = peso / (altura ** 2)

            # 2. MONTAGEM DOS DADOS (Usando os nomes exatos do erro)
            dados_entrada = {
                "genero": [val_genero],
                "idade": [idade],
                "imc": [imc_calculado],  # Aqui entra o IMC calculado
                "b_historico_familiar": [val_historico],
                "b_come_alimentos_caloricos": [val_caloricos],
                "qtd_vegetais": [val_vegetais],
                "qtd_refeicao": [val_refeicao],
                "freq_come_fora_refeicao": [val_come_fora],
                "b_fuma": [val_fuma],
                "qtd_agua": [val_agua],
                "b_monitora_calorias": [val_monitora],
                "qtd_atv_fisicas": [val_atv],
                "qtd_tmp_na_internet": [val_internet],
                "freq_alcool": [val_alcool],
                "meio_de_transporte": [val_transporte]
            }

            df_input = pd.DataFrame(dados_entrada)

            # 3. ORDENAÇÃO DAS COLUNAS
            # Garante que a ordem é igual à lista que apareceu no erro
            colunas_ordenadas = [
                'genero', 'idade', 'imc', 
                'b_historico_familiar', 'b_come_alimentos_caloricos', 
                'qtd_vegetais', 'qtd_refeicao', 'freq_come_fora_refeicao', 
                'b_fuma', 'qtd_agua', 'b_monitora_calorias', 
                'qtd_atv_fisicas', 'qtd_tmp_na_internet', 
                'freq_alcool', 'meio_de_transporte'
            ]
            
            try:
                # Reordena
                df_input = df_input[colunas_ordenadas]
                
                # Predição
                predicao = modelo.predict(df_input)
                
                # Mapeamento do Resultado
                # ATENÇÃO: Verifique se essa ordem (0 a 6) bate com o seu LabelEncoder do notebook
                mapa_resultado = {
                    0: "Peso Insuficiente",
                    1: "Peso Normal",
                    2: "Sobrepeso Nível I",
                    3: "Sobrepeso Nível II",
                    4: "Obesidade Tipo I",
                    5: "Obesidade Tipo II",
                    6: "Obesidade Tipo III"
                }
                
                resultado_texto = mapa_resultado.get(predicao[0], f"Classe {predicao[0]}")
                
                st.success(f"Resultado da Análise: **{resultado_texto}**")
                st.info(f"IMC Calculado: {imc_calculado:.2f}")

            except Exception as e:
                st.error(f"Erro na predição: {e}")
                st.write("Dados enviados:")
                st.dataframe(df_input)

if __name__ == "__main__":
    main()