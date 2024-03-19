import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(layout='wide')

@st.cache_data
def gerar_df():
    df = pd.read_excel(
        io= 'database_anp.xlsx',
        engine= 'openpyxl',
        sheet_name= 'ESTADOS - DESDE JANEIRO DE 2013',
        usecols= 'A:Q',
        nrows= 21405
    )
    return df
df = gerar_df()
colunasUteis = ['MÊS', 'PRODUTO', 'REGIÃO', 'ESTADO', 'PREÇO MÉDIO REVENDA']
df = df[colunasUteis]

with st.sidebar:
    st.subheader('Explorador de Preços de Combustíveis no Brasil')
    logo_teste = Image.open('grafico.png')
    st.image(logo_teste,use_column_width=True)
    st.subheader('SELEÇÃO DE FILTROS')
    fProduto = st.selectbox(
        'Selecione o combustivél:',
        options=df['PRODUTO'].unique()
    )
    fEstado = st.selectbox(
        'Selecione o estado:',
        options = df['ESTADO'].unique()
    )

    dadosUsuario = df.loc[(
        df['PRODUTO'] == fProduto) &
        (df['ESTADO'] == fEstado)
    ]

updateDatas = dadosUsuario['MÊS'].dt.strftime('%Y/%b')
dadosUsuario['MÊS'] = updateDatas[0:]

st.header('PREÇOS DOS COMBUSTÍVEIS NO BRASIL: 2013 À 2023')
st.markdown('**Combustível selecionado:** ' + fProduto)
st.markdown('**Estado:** ' + fEstado)

grafCombEstado = alt.Chart(dadosUsuario).mark_line(
    point=alt.OverlayMarkDef(color='red',size=20)
).encode(
    x = 'MÊS:T',
    y = 'PREÇO MÉDIO REVENDA',
    strokeWidth = alt.value(3)
).properties(
    height= 450,
    width= 1050
)

st.altair_chart(grafCombEstado)
