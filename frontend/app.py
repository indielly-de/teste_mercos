import json
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import requests
import seaborn as sns
import streamlit as st


API_URL = "http://api:8000/api/v1"

column_mapper = {
    "amount": "valor",
    "id_transaction": "id_lancamento",
    "payment_method_id": "id_metodo_pagamento",
    "result_center_id": "id_centro_resultado",
    "cost_center_id": "id_centro_custo",
    "due_date": "dt_vencimento",
    "segment": "ds_segmento",
    "prorated_value": "valor_rateado",
    "reference_date": "dt_referencia",
    "acquisition_channel": "ds_canal_aquisicao",
    "metric_description": "ds_metrica",
    "competence_date": "dt_competencia",
    "periodicity": "ds_periodicidade",
    "payment_date": "dt_pagamento"
}


@st.cache_data
def get_allocations():
    try:
        response = requests.get(f"{API_URL}/allocations")
        if response.status_code == 200:
            return pd.DataFrame(json.loads(response.json()))
    except requests.exceptions.ConnectionError:
        st.error("Erro ao conectar com a API. Verifique se o backend está rodando.")
    return pd.DataFrame()



st.title("📊 Painel de Rateio Financeiro")


df = get_allocations()
df.rename(columns=column_mapper, inplace=True)

if df.empty:
    st.warning("Nenhum dado encontrado.")
    st.stop()

# -------------------- FILTROS INTERATIVOS --------------------

st.sidebar.header("Filtros")

# Filtro por etapa
steps = ["Todas", "Primeira Etapa", "Segunda Etapa", "Nao alocados"]
selected_step = st.sidebar.selectbox("Selecione uma etapa", steps)

segments = df["ds_segmento"].unique()
selected_segment = st.sidebar.selectbox("Selecione um segmento", ["Todos"] + [entry for entry in segments if entry])

# Filtro por canal de aquisição (se existir no DataFrame)
if "ds_canal_aquisicao" in df.columns:
    channels = df["ds_canal_aquisicao"].dropna().unique()
    selected_channel = st.sidebar.selectbox(
        "Selecione um Canal", ["Todos"] + list(channels)
    )
else:
    selected_channel = "Todos"

# Filtro por período (competência)
df["dt_competencia"] = pd.to_datetime(df["dt_competencia"])
data_min = df["dt_competencia"].min()
data_max = df["dt_competencia"].max()
selected_date = st.sidebar.date_input(
    "Selecione o Período", [data_min, data_max], format="DD/MM/YYYY"
)

df_filtered = df

# Aplicar os filtros ao DataFrame
if selected_segment != "Todos":
    df_filtered = df_filtered[df_filtered["ds_segmento"] == selected_segment]

if selected_step == "Primeira Etapa":
    df_filtered = df_filtered[df_filtered["id_centro_resultado"].isin([100, 204])]
    df_filtered = df_filtered[df_filtered["ds_metrica"] == "metrica_2"]

if selected_step == "Segunda Etapa":
    df_filtered = df_filtered[df_filtered["id_centro_resultado"].isin([268, 288])]
    df_filtered = df_filtered[~df_filtered["valor_rateado"].isnull()]

if selected_step == "Nao alocados":
    df_filtered = df_filtered[df_filtered["valor_rateado"].isnull()]

if selected_channel != "Todos":
    df_filtered = df_filtered[df_filtered["ds_canal_aquisicao"] == selected_channel]

df_filtered = df_filtered[
    (df_filtered["dt_competencia"] >= pd.to_datetime(selected_date[0]))
    & (df_filtered["dt_competencia"] <= pd.to_datetime(selected_date[1]))
]

# -------------------- TABELA INTERATIVA --------------------

st.subheader("📜 Lançamentos Filtrados")
st.dataframe(df_filtered)

# -------------------- GRÁFICOS --------------------

st.subheader("📊 Gráfico de Distribuição dos Rateios")

# Gráfico de Barras - Rateio por Centro de Custo
fig_bar = px.bar(
    df_filtered,
    x="id_centro_custo",
    y="valor_rateado",
    color="ds_canal_aquisicao",
    title="Rateio por Centro de Custo",
    labels={"id_centro_custo": "Centro de Custo", "valor_rateado": "Valor Rateado"},
    barmode="group",
)
st.plotly_chart(fig_bar)

# Gráfico de Pizza - Distribuição de Rateios
fig_pie = px.pie(
    df_filtered,
    values="valor_rateado",
    names="ds_canal_aquisicao",
    labels={"valor_rateado": "Valor Rateado", "ds_canal_aquisicao": "Canal de aquisição"},
    title="Distribuição dos Rateios por Canal",
)
st.plotly_chart(fig_pie)

# Gráfico de Linha - Evolução do Rateio ao longo do tempo
fig_line = px.line(
    df_filtered,
    x="dt_competencia",
    y="valor_rateado",
    color="ds_canal_aquisicao",
    labels={"dt_competencia": "Data da competencia",  "valor_rateado": "Valor Rateado"},
    title="Evolução dos Rateios ao Longo do Tempo",
)
st.plotly_chart(fig_line)

# -------------------- GRÁFICO DE HEATMAP (Seaborn) --------------------

st.subheader("🔥 Heatmap de Correlação")

# Criar heatmap
plt.figure(figsize=(8, 5))
correlation = df_filtered[["id_centro_custo", "valor_rateado"]].corr()
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
st.pyplot(plt)
