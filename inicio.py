##librerias importadas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 # #02273b codigo color logo
## configuracion de ancho de pagina
st.set_page_config(layout="wide")
##logo de la presentacion
st.image("img/logo.png")
#titulo
st.title("Analisis financiero")
#subtitulos
st.subheader("Preanalisis del Mercado")
#titulo del grafico
st.markdown("<h1 style='font-size: 24px;'>Sector con mayor crecimiento en los ultimos 3 años</h1>", unsafe_allow_html=True)
#grafico de sectores con mas crecimientos los ultimos 3 años
st.image("img/grafico1.png")
#descripcion del grafico
st.text("en el grafico se observa que el rubro con mayor crecimiento estos \nultimos 4 años fue el rubro de IT con un 49%")
#datrame crecimiento de empresas IT
st.markdown('<br><h3 align="center"><u>Empresas IT con mayor crecimiento en los ultimos 3 años</u></h3><br>', unsafe_allow_html=True)
df=pd.read_csv("datos/it.csv")
df=df.sort_values(by="Close",ascending=False)
#separar columnas
col1,col2=st.columns([1,2])
with st.container():
    with col1:
        #dataframe empresas IT
        st.dataframe(df)
    with col2:
        #imagen con las empresas seleccionadas
        st.image("img/top5.jpg",use_column_width="always")