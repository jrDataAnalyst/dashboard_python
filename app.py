import streamlit as st
#import pandas as pd
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go

countries = ['brazil', 'united states', 'portugal']
intervals = ['Daily', 'Weekly', 'Monthly']

# Pegando datas
start_date = datetime.today() - timedelta(days=365)
end_date = datetime.today()

@st.cache
def consultar_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(stock=stock, country=country, from_date=from_date, to_date=to_date, interval=interval)
    return df

def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)

# Criando CandleStick

def plotClandleStick(df, acao='ticket'):

    tracel = {
        'x' : df.index,
        'open' : df.Open,
        'close' : df.Close,
        'high' : df.High,
        'low' : df.Low,
        'type' : 'candlestick',
        'name' : acao,
        'showlegend' : False

    }

    data = [tracel]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig

# Criando barra lateral

barra_lateral = st.sidebar.empty()
country_select = st.sidebar.selectbox("Selecione o país: ", countries)
acoes = ip.get_stocks_list(country=country_select)
stock_select = st.sidebar.selectbox("Selecione a ação: ", acoes)

# Area de datas barra lateral

from_date = st.sidebar.date_input("Inicio: ", start_date)
to_date = st.sidebar.date_input("Fim: ", end_date)

select_intervals = st.sidebar.selectbox("Selecionar intervalo: ", intervals) # Intervalo

carregar_dados = st.sidebar.checkbox("Carregar dados")


# Elementos centrais da pagina

st.title("Monitor de ações em tempo real")
st.header("Acões")
st.subheader("Visualização gráfica")

grafico_candle = st.empty()
grafico_line = st.empty()

if from_date > to_date:
    st.error("Data de inicio maior que data final")
else:
    df = consultar_acao(stock_select, country_select, format_date(from_date), format_date(to_date), select_intervals)
    try:
        fig = plotClandleStick(df)
        grafico_candle = st.plotly_chart(fig)
        grafico_line = st.line_chart(df.Close)

        if carregar_dados:
            st.subheader("Dados")
            dados = st.dataframe(df)

    except Exception as e:
        st.error(e)


