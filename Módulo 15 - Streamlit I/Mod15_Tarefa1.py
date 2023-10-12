import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time


st.set_page_config(
        page_title = 'EBAC - Mod 15 - Streamlit I', 
        page_icon = 'https://img.icons8.com/external-flaticons-lineal-color-flat-icons/600w/000000/external-data-science-media-agency-flaticons-lineal-color-flat-icons-2.png',
        layout='wide')

st.title('Módulo 15: Streamlit I')
st.header('Tarefa 1')
st.info('Crie uma aplicação com streamlit reproduzindo pelo menos 20 códigos.', icon="ℹ️")

st.markdown('----')

st.subheader('Uber pickups in NYC')

if st.button('Carregar dados!'):
    st.caption('Aguarde um instante.')
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(100):
        latest_iteration.text(f'Carregando... {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)
    st.caption('Feito.')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

st.markdown('----')

st.subheader('Raw data')

if st.checkbox('Show raw data'):
    colunas = st.multiselect(
    'Selecione a(s) coluna(s) que deseja visualizar:)',
    ['date/time', 'lat', 'lon', 'base'])
    if colunas == []:
        st.warning('Você precisa selecionar a coluna para visualizar os dados.', icon="⚠️")
    else:
        st.write(data[colunas])
        st.success('Dados carregados!', icon="✅")
    st.write(data[colunas].shape)

st.markdown('----')

st.subheader('Data filtred by hour')

min_time = data['date/time'].dt.time.min()
max_time = data['date/time'].dt.time.max()

hora_inicial = st.time_input('Hora inicial', value=min_time, step=60)
hora_final = st.time_input('Hora final', value=max_time, step=60)

teste = data[(data['date/time'].dt.time >= hora_inicial) & (data['date/time'].dt.time <= hora_final)]
st.write(teste.shape)
st.write(teste)

st.markdown('----')

st.subheader('Number of pickups by hour')

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

option = st.selectbox(
    'Selecione o gráfico que deseja visualizar:',
    ('line chart', 'area chart', 'bar chart'))

st.write('You selected:', option)

if option == 'line chart':
    st.line_chart(hist_values)
elif option == 'area chart':
    st.area_chart(hist_values)
elif option == 'bar chart':
    st.bar_chart(hist_values)

st.markdown('----')

hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)

st.markdown('----')

col1, col2, col3 = st.sidebar.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

st.sidebar.markdown('----')

