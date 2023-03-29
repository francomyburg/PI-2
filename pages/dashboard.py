import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime


df5=pd.read_csv("datos/df5.csv")
df5.round(4)
df5["Date"]=df5["Date"].astype("datetime64")
df=pd.read_csv("datos/empresas.csv")
st.sidebar.image("img/logo.png", use_column_width=True)
### codigo para el grafico de ROI###########################
filtro2022=df5[df5["Date"]=="2022-03-18"][["Close","Security"]].set_index("Security")
filtro2023=df5[df5["Date"]=="2023-03-20"][["Close","Security"]].set_index("Security")
roi=((filtro2023-filtro2022)/filtro2022)*100
roi.reset_index(inplace=True)
################################################################################
#funcion grafico RSI
def rsigrapgh(empresa):
    """FX que duevuelve grafico rsi segun la empresa eligida"""
    firstsolar=df5[df5["Symbol"]==empresa]
    firstsolar2=firstsolar[firstsolar["Date"]>"2022-04-01"]
    mask=firstsolar2[firstsolar2["Date"]>"2022-04-04"]
    change=firstsolar2.Close.diff()
    change.dropna(inplace=True)
    change_up=change.copy()
    change_down=change.copy()
    change_up[change_up<0]=0
    change_down[change_down>0]=0
    #if change.equals(change_up+change_down) == True:
    #    pass
    #else:
    #    print("error")
        
    avg_up=change_up.rolling(14).mean()
    avg_down=change_down.rolling(14).mean().abs()
    rsi=(100 * avg_up/(avg_up+avg_down))
    plt.style.use('fivethirtyeight')

   
    
    plt.rcParams['figure.figsize'] = (14, 5)
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    # creando dos figuras
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)

    # Primer grafico:
    # precios de cierre en el primer grafico
    ax1.plot(firstsolar2["Date"],firstsolar2['Close'], linewidth=2)
    ax1.set_title('FSLR Close Price')

    # Segundo Grafico
    # Grafico Rsi
    ax2.set_title('Relative Strength Index')
    ax2.plot(mask["Date"],rsi, color='orange', linewidth=1)
    # Se añaden dos lineas horizontales de señales de compra y venta
    # Oversold
    ax2.axhline(30, linestyle='--', linewidth=1.5, color='green')
    # Overbought
    ax2.axhline(70, linestyle='--', linewidth=1.5, color='red')

    return fig#plt.show()
## Funcion que devuelve el ultimo valor de rsi#####
def rsi(symbol):
    firstsolar=df5[df5["Symbol"]==symbol]
    firstsolar2=firstsolar[firstsolar["Date"]>"2022-04-01"]
    mask=firstsolar2[firstsolar2["Date"]>"2022-04-04"]
    change=firstsolar2.Close.diff()
    change.dropna(inplace=True)
    change_up=change.copy()
    change_down=change.copy()
    change_up[change_up<0]=0
    change_down[change_down>0]=0
    avg_up=change_up.rolling(14).mean()
    avg_down=change_down.rolling(14).mean().abs()
    rsi=(100 * avg_up/(avg_up+avg_down))
    return round(rsi.iloc[-1],0)


empresas=['ANET', 'ENPH', 'FSLR', 'NVDA', 'ON']
empresa_elegida = st.sidebar.selectbox("Elige una empresa", empresas)

st.subheader('Información de '+df5[df5["Symbol"]==empresa_elegida].Security.iloc[0])
df_filtrado = df[df["symbol"] == empresa_elegida]
col1,col2,col3=st.columns(3)
col1.metric("Market Cap","$"+str(round(df_filtrado["marketCap"].iloc[0]/1000000,0))+"M")
col2.metric("EPS",value=df_filtrado["epsTrailingTwelveMonths"])
col3.metric("RSI",value=rsi(empresa_elegida))
##slider para elegir fecha 
fecha=st.sidebar.slider("Fecha de inicio",2000,2023)
fig = px.line(df5[df5["Date"]>(str(fecha)+"-01-01")], x="Date", y="Close", color="Symbol")
fig.update_layout(title="Valores del mercado", xaxis_title="Fecha", yaxis_title="Precio de cierre")
col4,col5=st.columns([2,1])
#grafico de precios atraves del tiempo
with st.container():
    with col4:
        st.plotly_chart(fig,use_container_width=True)
    with col5:
        fig2=px.bar(roi, x="Security", y="Close", title="ROI",color="Security")
        st.plotly_chart(fig2,use_container_width=True)
#grafico rsi
st.markdown('<h1 align="center">RSI</h1>', unsafe_allow_html=True)
with st.container():
    st.pyplot(rsigrapgh(empresa_elegida))