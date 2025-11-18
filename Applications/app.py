import spacy
import streamlit as st
from collections import Counter
import pandas as pd
import altair as alt
import os

st.set_page_config(
    page_title="Dashboard de Tendências",
    layout="centered",          
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_model():
    model_path = "model_news2"  
    if not os.path.exists(model_path):
        st.error(f"Modelo '{model_path}' não encontrado.")
        return None
    return spacy.load(model_path)

nlp = load_model()

st.title("Dashboard de Tendências")
st.write("Visualize dinamicamente as entidades mais mencionadas.")

texts = [
    "Fernando Haddad apresenta nova proposta para o arcabouço fiscal em Brasília.",
    "O Banco Central decidiu manter a taxa Selic inalterada na última reunião do Copom.",
    "Gabriel Galípolo defende cautela na redução dos juros durante evento em São Paulo.",
    "A Reforma Tributária é considerada prioridade para a equipe econômica.",
    "Mercado financeiro reage positivamente às falas de Gabriel Galípolo sobre a inflação.",
    "Banco Central divulga relatório de inflação com projeções otimistas para o próximo ano.",
    "Fernando Haddad se reúne com líderes do Senado para destravar a Reforma Tributária.",
    "Indústria pressiona o Banco Central por cortes mais agressivos na taxa Selic.",
    "A votação da Reforma Tributária deve ocorrer ainda este mês, segundo Fernando Haddad.",
    "Petrobras anuncia descoberta de novo campo de petróleo na Margem Equatorial.",
    "Ações da Petrobras sobem após divulgação de lucro recorde no trimestre.",
    "Tarcísio de Freitas busca investimentos estrangeiros para o estado de São Paulo.",
    "BNDES libera crédito bilionário para obras de infraestrutura no Nordeste.",
    "Presidente da Petrobras discute transição energética com o governo federal.",
    "BNDES e Petrobras firmam parceria para investir em energia eólica offshore.",
    "Tarcísio de Freitas inaugura trecho de rodovia no interior de São Paulo.",
    "Flamengo vence clássico no Maracanã e assume a liderança do campeonato.",
    "Governo de São Paulo, liderado por Tarcísio de Freitas, anuncia privatização da Sabesp.",
    "Torcida do Flamengo lota aeroporto para apoiar o time antes da final da Libertadores.",
    "Tarcísio de Freitas busca investimentos estrangeiros para o estado em viagem à Europa."
]

if nlp:
    people, orgs, themes = [], [], []

    for texto in texts:
        doc = nlp(texto)
        for ent in doc.ents:
            if ent.label_ == "PER":
                people.append(ent.text)
            elif ent.label_ == "ORG":
                orgs.append(ent.text)
            elif ent.label_ == "TEMA":
                themes.append(ent.text)

    data_dict = {
        "Pessoas": Counter(people),
        "Organizações": Counter(orgs),
        "Temas": Counter(themes)
    }

    category = st.selectbox("Selecione a categoria para visualizar:", ["Pessoas", "Organizações", "Temas"])

    df = pd.DataFrame(data_dict[category].items(), columns=[category, "Menções"])
    df = df.sort_values("Menções", ascending=False)

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(category, sort='-y'),
            y="Menções",
            tooltip=[category, "Menções"]
        )
        .properties(height=400, title=f"{category} Mais Mencionadas")
    )

    st.altair_chart(chart, width='stretch')
