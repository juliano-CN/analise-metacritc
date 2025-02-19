#%%
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

#python -m streamlit run dashboard.py

#configura layout da pagina
st.set_page_config(layout="wide",page_title="Dashboard")

df = pd.read_csv("MetacriticData.csv")
df = df[~df["Lançamento"].isna()]

df['Lançamento'] = pd.to_datetime(df['Lançamento'])

anos = df['Lançamento'].dropna().dt.year.unique()
anos = np.sort(anos)[::-1]#sortear de tras pra frente

#df["Lançamento"] = df["Lançamento"].apply(lambda x: str)

#ano = st.sidebar.selectbox("Ano", anos)
ano = st.multiselect("Ano", anos)
plataforma = st.multiselect("Plataforma", df["Plataforma"].unique())

if not ano:
    ano = anos

if not plataforma:
    plataforma = df["Plataforma"].unique()

dfFinal = df[(df["Lançamento"].dt.year.isin(ano)) & (df["Plataforma"].isin(plataforma))]
dfFinalTbd = df[(df["Lançamento"].dt.year.isin(ano)) & (df["Plataforma"].isin(plataforma)) & (df["Userscore"] != "tbd")]

metascore = dfFinal["Metascore"]
usercore = dfFinalTbd["Userscore"].astype(float)

col1,col2 = st.columns(2,border=True)
col3,col4 = st.columns(2,border=True)
col5,col6 = st.columns(2,border=True)

if len(dfFinal) > 0:
    #col1.text("Anos: " + str(np.sort(ano)))
    #col1.text("Plataformas: " + str(plataforma))
    col1.text("Média metascore: " + str(metascore.mean().round(1)))
    col1.text("Mediana metascore: " + str(metascore.median().round(1)))
    col1.text("Média userscore: " + str(usercore.mean().round(1)))
    col1.text("Mediana userscore: " + str(usercore.median().round(1)))
    col1.text("Correlação: " + str(dfFinalTbd[["Metascore","Userscore"]].corr().iloc[0,1].round(2)))
    col1.text("Quantidade de jogos: " + str(len(metascore)))
    #primeiro grafico
    fig_date = px.scatter(dfFinalTbd,x = "Metascore",y = "Userscore",title="Metascore x Userscore",
    hover_data={"Metascore": True, "Userscore": True, "nome": True})
    col2.plotly_chart(fig_date)
    #segundo grafico
    mouthFreq = dfFinal["Lançamento"].dt.month.value_counts().sort_index()
    mouthFreq = mouthFreq.reindex(np.arange(12)+1,fill_value=0)
    mouthFreq.index = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"]

    fig_date2 = px.bar(mouthFreq,y=mouthFreq.values,title = "Quantidades de lançamentos por mês",labels={"y": "", "index": ""})
    col3.plotly_chart(fig_date2)
    #terceiro grafico
    yearFreq = dfFinal["Lançamento"].dt.year.value_counts().sort_index()
    #yearFreq = yearFreq.reindex(ano,fill_value=0)

    if len(ano) > 1:
        fig_date3 = px.bar(yearFreq,y=yearFreq.values,title = "Quantidades de lançamentos por ano",labels={"y": "","Lançamento":""})
        col4.plotly_chart(fig_date3)
    else:
        col4.write("Para melhor visualização selecione pelo menos dois anos diferentes")
    #quarto e quinto grafico    
    fig_date4 = px.histogram(dfFinal, x="Metascore",nbins = 10,title="Distribuição metascore",labels={"count": ""})
    fig_date5 = px.histogram(dfFinal, x="Userscore",nbins = 10,title="Distribuição userscore",labels={"count": ""})
    col5.plotly_chart(fig_date4)
    col6.plotly_chart(fig_date5)
else:
    col1.text("Nenhum resultado encontrado")

st.write(dfFinal)#df[df["Lançamento"].dt.year.isin(ano)]
#%%
#df.info()
#df.columns

#%%
#print(1:12)
