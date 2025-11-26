
import streamlit as st
import spacy
import pandas as pd

st.set_page_config(
    page_title="News Entity Search",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONALIZADO (ESTILO) ---
st.markdown("""
<style>
    /* Estilo para os destaques no texto (Marcador) */
    .highlight-match {
        background-color: #ff4b4b;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    .highlight-other {
        background-color: #f0f2f6;
        color: #31333F;
        padding: 2px 6px;
        border-radius: 4px;
        border: 1px solid #d6d6d8;
    }
    /* Melhorar aparência dos cards de resultado */
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Título principal centralizado */
    h1 {
        text-align: center;
        color: #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# --- DADOS ---
TEXTS_TO_CATALOG = [
    "O Nubank anunciou um lucro recorde no último trimestre, superando as expectativas de Wall Street. O CEO David Vélez comemorou os resultados.",
    "A Magazine Luiza informou que vai fechar parcerias logísticas no Nordeste. A empresa busca competir com a Amazon na região.",
    "A B3, bolsa de valores brasileira, fechou em queda de 1,5% nesta terça-feira. O Ibovespa foi puxado pelas ações da Vale.",
    "A fábrica da BYD em Camaçari deve começar a operar em breve. O governo da Bahia prometeu incentivos fiscais para a montadora chinesa.",
    "O iFood enfrenta novos processos trabalhistas em São Paulo. Entregadores pedem vínculo empregatício com a plataforma.",
    "O Flamengo venceu o Fluminense no Maracanã por 2 a 0. O atacante Gabigol marcou os dois gols da partida.",
    "Neymar Jr. deve voltar aos campos em breve pelo Al-Hilal. O jogador fez exames em uma clínica de Belo Horizonte.",
    "O Palmeiras anunciou a contratação de um novo zagueiro argentino. A presidente Leila Pereira confirmou a negociação.",
    "O ministro Alexandre de Moraes, do STF, determinou novas diligências. A Polícia Federal cumpriu mandados em Brasília e Curitiba.",
    "O Senado Federal aprovou a nova lei de diretrizes orçamentárias. O presidente do Senado, Rodrigo Pacheco, elogiou a votação.",
    "O governador Tarcísio de Freitas inaugurou uma nova estação de trem. O evento ocorreu na zona leste de São Paulo.",
    "A colheita de soja no Mato Grosso atingiu 80% da área plantada. A Embrapa alertou para os riscos climáticos na região.",
    "O Ibama multou madeireiras ilegais no sul do Pará. A ministra Marina Silva reforçou a importância da fiscalização na Amazônia.",
    "A JBS anunciou a compra de uma nova planta de processamento nos Estados Unidos. A empresa brasileira expande sua atuação global.",
    "A cantora Anitta confirmou um show gratuito na praia de Copacabana. A prefeitura do Rio de Janeiro espera 1 milhão de pessoas.",
    "O Rock in Rio anunciou as atrações principais do palco mundo. A venda de ingressos começa na próxima semana pela Ticketmaster.",
    "A Fiocruz entregou um novo lote de vacinas contra a dengue ao Ministério da Saúde. A distribuição começa pelo Distrito Federal.",
    "Pesquisadores da USP descobriram uma nova molécula promissora. O estudo foi publicado em parceria com a Fapesp.",
    "Um forte temporal atingiu Porto Alegre ontem à noite. A Defesa Civil emitiu alertas para o interior do Rio Grande do Sul.",
    "A Embraer fechou um contrato bilionário para venda de jatos comerciais. A entrega será feita para uma companhia aérea da Europa.",
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
    "Tarcísio de Freitas busca investimentos estrangeiros para o estado em viagem à Europa.",
    "Governadores do Nordeste se reuniram em Recife para discutir investimentos em infraestrutura hídrica após novos alertas de seca severa emitidos pelo Inmet",
    "Pesquisadores brasileiros da USP desenvolveram um algoritmo de detecção de fraudes capaz de identificar padrões anômalos em transações bancárias em tempo real.",
    "A Anatel iniciou testes para expandir o 5G Standalone em regiões rurais, buscando reduzir desigualdades no acesso à internet.",
    "O Inpe registrou queda de 21% no desmatamento na Amazônia em comparação com o ano anterior, destacando avanços na fiscalização integrada",
    "Uma operação conjunta do Ibama e da Polícia Federal apreendeu 150 caminhões de madeira ilegal no Pará, desmontando um grande esquema de extração clandestina.",
    "O Ministério da Saúde anunciou uma nova campanha nacional de vacinação contra a gripe após aumento de casos em vários estados.",
    "Um relatório da Fiocruz mostrou crescimento nos casos de dengue em regiões urbanas densamente povoadas, reforçando a importância do combate ao Aedes aegypti.",
    "A Anvisa aprovou o uso de um novo medicamento para controle de diabetes tipo 2, trazendo alternativas para pacientes com resistência a tratamentos anteriores."
]

# --- FUNÇÕES ---
@st.cache_resource
def load_model(model_path="model_news2"):
    try:
        nlp = spacy.load(model_path)
        return nlp, "custom"
    except IOError:
        try:
            return spacy.load("pt_core_news_lg"), "standard"
        except:
            return None, "none"

@st.cache_data
def catalog_documents(_nlp, text_list):
    db = []
    docs = _nlp.pipe(text_list)
    for i, doc in enumerate(docs):
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        db.append({"id": f"Notícia #{i+1:02d}", "text": doc.text, "entities": entities})
    return db

def search_documents(db, query_dict, logic="AND"):
    results = []
    for entry in db:
        match = True if logic == "AND" else False
        for query_label, query_text in query_dict.items():
            found_entity_match = False 
            for entity in entry['entities']:
                if (entity['label'] == query_label and 
                    entity['text'].strip().lower() == query_text.strip().lower()):
                    found_entity_match = True
                    break 
            
            if logic == "AND":
                if not found_entity_match:
                    match = False; break 
            elif logic == "OR":
                if found_entity_match:
                    match = True; break 
        if match:
            results.append(entry)
    return results

# --- SIDEBAR (CONFIGURAÇÕES) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2535/2535556.png", width=80)
    st.title("Painel de Controle")
    
    nlp, model_type = load_model("model_news2")
    
    st.divider()
    
    st.subheader("⚙️ Lógica de Busca")
    logic_option = st.radio(
        "Como filtrar?",
        ["Todas obrigatórias (AND)", "Qualquer uma (OR)"],
        captions=["O documento deve ter TODAS as entidades.", "O documento deve ter PELO MENOS UMA."]
    )
    logic_mode = "AND" if "AND" in logic_option else "OR"

# --- ÁREA PRINCIPAL ---
st.title("Busca em Notícias")
st.write("")

if nlp:
    db = catalog_documents(nlp, TEXTS_TO_CATALOG)
    if 'filtros_ativos' not in st.session_state: st.session_state.filtros_ativos = {}

    # Container de Busca (Estilizado)
    with st.container(border=True):
        c1, c2, c3 = st.columns([1.5, 3, 1])
        with c1:
            label_input = st.selectbox(" Tipo (Label)", ["ORG", "PER", "LOC", "CARGO", "TEMA", "VALOR"])
        with c2:
            text_input = st.text_input(" Texto da Entidade", placeholder="Ex: Petrobras, Neymar...", key="input_text")
        with c3:
            st.write("")
            st.write("")
            if st.button("➕ Adicionar", type="primary", use_container_width=True):
                if text_input:
                    st.session_state.filtros_ativos[label_input] = text_input
                    st.rerun()

    # Filtros Ativos (Visualização de Tags)
    if st.session_state.filtros_ativos:
        st.write("---")
        c_left, c_right = st.columns([4, 1])
        with c_left:
            st.caption(f"Filtros aplicados ({logic_mode}):")
            # Gambiarra visual para mostrar tags bonitas
            html_tags = ""
            for k, v in st.session_state.filtros_ativos.items():
                html_tags += f"""
                <span style='background-color: #e0e2e6; padding: 4px 10px; border-radius: 15px; margin-right: 5px; font-size: 0.9em;'>
                    <b>{k}</b>: {v}
                </span>
                """
            st.markdown(html_tags, unsafe_allow_html=True)
            
        with c_right:
            if st.button(" Limpar Tudo"):
                st.session_state.filtros_ativos = {}
                st.rerun()

        # Resultados
        resultados = search_documents(db, st.session_state.filtros_ativos, logic=logic_mode)
        
        st.write("")
        st.subheader(f" Resultados: {len(resultados)}")
        
        if resultados:
            for res in resultados:
                # Criação do Expander com Ícone
                with st.expander(f" {res['id']} (Ver conteúdo)", expanded=True):
                    texto_html = res['text']
                    
                    # Highlight inteligente com HTML/CSS
                    for ent in res['entities']:
                        is_match = False
                        # Verifica se é match para destacar em vermelho
                        for f_label, f_text in st.session_state.filtros_ativos.items():
                             if (ent['label'] == f_label and ent['text'].strip().lower() == f_text.strip().lower()):
                                 is_match = True
                        
                        if is_match:
                            # Destaque de match (vermelho/branco)
                            texto_html = texto_html.replace(
                                ent['text'], 
                                f"<span class='highlight-match'>{ent['text']} <small style='font-size:0.6em'>({ent['label']})</small></span>"
                            )
                        else:
                            # Destaque neutro para outras entidades (cinza)
                            texto_html = texto_html.replace(
                                ent['text'], 
                                f"<span class='highlight-other'>{ent['text']}</span>"
                            )
                    
                    st.markdown(texto_html, unsafe_allow_html=True)
                    st.caption("Entidades detectadas:")
                    st.json([e['text'] for e in res['entities']], expanded=False)
        else:
            st.warning(f"Nenhum resultado encontrado para a combinação selecionada ({logic_mode}).")
    else:
        st.info(" Comece adicionando filtros na barra acima.")
