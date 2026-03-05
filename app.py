import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
from io import BytesIO
import base64

# Configuração da página
st.set_page_config(
    page_title="Sistema PLANAT 2026 - IPEM/RJ",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #003366;
        text-align: center;
        padding: 1rem;
        background-color: #f0f8ff;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #003366;
        padding: 0.5rem;
        border-bottom: 2px solid #003366;
        margin-bottom: 1rem;
    }
    .status-ok { color: green; font-weight: bold; }
    .status-atencao { color: orange; font-weight: bold; }
    .status-critico { color: red; font-weight: bold; }
    .stButton > button {
        background-color: #003366;
        color: white;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #004488;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<p class="main-header">📋 SISTEMA DE MONITORAMENTO DO PLANAT 2026</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem;">Instituto de Pesos e Medidas do Estado do Rio de Janeiro - IPEM/RJ</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1rem;">Auditoria Interna - AUDIT</p>', unsafe_allow_html=True)
st.markdown("---")

# Inicialização do estado da sessão
if 'checklists_data' not in st.session_state:
    st.session_state.checklists_data = {}
if 'itens_status' not in st.session_state:
    st.session_state.itens_status = {
        1: "OK", 2: "OK", 3: "OK", 4: "Atenção", 5: "OK", 6: "OK", 7: "OK",
        8: "Em andamento", 9: "OK", 10: "OK", 11: "Não iniciado", 12: "Não iniciado",
        13: "OK", 14: "OK", 15: "Atenção", 16: "OK", 17: "Crítico", 18: "Em andamento"
    }

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/RJ-01.png/200px-RJ-01.png", width=100)
    st.markdown("## 🗓️ Controle")
    
    meses_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    mes_atual = datetime.now().month
    mes_selecionado = st.selectbox("Mês", range(1, 13), 
                                   format_func=lambda x: meses_pt[x-1], 
                                   index=mes_atual-1)
    ano_selecionado = 2026
    
    st.markdown("---")
    
    # Menu de navegação
    opcao = st.radio(
        "Menu",
        ["🏠 Dashboard", "📝 Checklists", "📊 Visualizar", "📈 Relatórios", "📄 Exportar"]
    )
    
    st.markdown("---")
    st.markdown("👥 **Milana & José**")
    st.markdown("Auditoria Interna")

# Dados dos itens
itens_data = {
    "Item": list(range(1, 19)),
    "Descrição": [
        "Atos de Gestão",
        "Gestão do Planejamento Orçamentário",
        "Gestão Orçamentária",
        "Gestão Financeira",
        "Gestão Contábil-Patrimonial",
        "Gestão Previdenciária",
        "Gestão da Descentralização",
        "Bens Móveis e Almoxarifado",
        "Tomada de Contas",
        "Prestação de Contas de Adiantamento",
        "PLANAT 2027",
        "RANAT 2026",
        "Assessoramento ao Órgão",
        "Demandas TCE/CGE",
        "Elaboração de Normativos",
        "Demandas Extraordinárias",
        "SIAUDI",
        "Temas AGE (IN 55/2025)"
    ],
    "Status": [
        "✅ OK", "✅ OK", "✅ OK", "⚠️ Atenção", "✅ OK", "✅ OK", "✅ OK",
        "🔄 Em andamento", "✅ OK", "✅ OK", "⏳ Pendente", "⏳ Pendente",
        "✅ OK", "✅ OK", "⚠️ Atenção", "✅ OK", "❌ Crítico", "🔄 Em andamento"
    ],
    "Responsável": [
        "Milana", "José", "José", "José", "José", "José", "Milana",
        "José", "Milana", "Milana", "Equipe", "Equipe", "Equipe",
        "Equipe", "Milana", "Equipe", "José", "Milana"
    ]
}
df = pd.DataFrame(itens_data)

# Função para criar link de download CSV
def get_csv_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download CSV</a>'
    return href

# DASHBOARD
if opcao == "🏠 Dashboard":
    st.markdown('<p class="sub-header">🏠 DASHBOARD</p>', unsafe_allow_html=True)
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Itens", "18")
    with col2:
        ok_count = len([s for s in df["Status"] if "✅" in s])
        st.metric("Itens OK", ok_count, f"{ok_count*100/18:.0f}%")
    with col3:
        atencao = len([s for s in df["Status"] if "⚠️" in s or "🔄" in s])
        st.metric("Em Atenção", atencao)
    with col4:
        critico = len([s for s in df["Status"] if "❌" in s])
        st.metric("Críticos", critico)
    
    st.markdown("---")
    
    # Gráfico
    status_counts = df["Status"].str.extract(r"([✅⚠️❌🔄⏳])")[0].value_counts()
    fig = px.pie(values=status_counts.values, names=status_counts.index,
                 title="Distribuição por Status")
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela
    st.dataframe(df, use_container_width=True, hide_index=True)

# CHECKLISTS
elif opcao == "📝 Checklists":
    st.markdown(f'<p class="sub-header">📝 CHECKLISTS - {meses_pt[mes_selecionado-1]}/{ano_selecionado}</p>', unsafe_allow_html=True)
    
    # Seleção de item
    item = st.selectbox("Selecione o item", df["Item"].tolist(),
                        format_func=lambda x: f"{x} - {df[df['Item']==x]['Descrição'].iloc[0]}")
    
    st.markdown("---")
    
    # Checklist por item
    if item == 1:
        st.markdown("#### 📋 Atos de Gestão")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Novas determinações TCE/CGE?", ["Não", "Sim"])
            st.selectbox("Status monitoramento", ["OK", "Atenção", "Crítico", "Andamento"])
        with col2:
            st.selectbox("Concurso Público", ["Sem mov.", "Andamento", "Concluído"])
            st.text_area("Observações")
    
    elif item == 3:
        st.markdown("#### 💰 Gestão Orçamentária")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Receita x Previsão", ["OK", "Atenção", "Crítico"])
            st.selectbox("Despesa x Fixada", ["OK", "Atenção", "Crítico"])
        with col2:
            st.selectbox("Restos a Pagar", ["OK", "Atenção", "Crítico"])
            st.selectbox("Pagamentos", ["OK", "Atenção", "Crítico"])
    
    elif item == 17:
        st.markdown("#### 🔍 SIAUDI")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Recomendações AGE", ["Registradas", "Pendentes", "Parcial"])
            st.number_input("Pendentes", 0, 50, 5)
        with col2:
            st.selectbox("Evidências", ["Anexadas", "Pendentes", "Parcial"])
            st.number_input("Concluídas no mês", 0, 50, 2)
    
    else:
        for i in range(1, 6):
            st.selectbox(f"Campo {i}", ["OK", "Atenção", "Crítico", "N/A"])
    
    if st.button("💾 SALVAR", type="primary"):
        st.success("Checklist salvo com sucesso!")

# VISUALIZAR
elif opcao == "📊 Visualizar":
    st.markdown('<p class="sub-header">📊 CHECKLISTS SALVOS</p>', unsafe_allow_html=True)
    
    if st.session_state.checklists_data:
        st.write("Dados salvos na sessão atual:")
        st.json(st.session_state.checklists_data)
    else:
        st.info("Nenhum checklist salvo nesta sessão.")
    
    st.markdown("---")
    st.markdown("📥 **Exportar dados**")
    st.markdown(get_csv_download_link(df, "planat_dados.csv"), unsafe_allow_html=True)

# RELATÓRIOS
elif opcao == "📈 Relatórios":
    st.markdown('<p class="sub-header">📈 INDICADORES</p>', unsafe_allow_html=True)
    
    # Gráfico de evolução
    meses = [m[:3] for m in meses_pt]
    valores = [10, 12, 15, 14, 16, 18, 17, 19, 20, 22, 23, 25]
    
    fig = px.line(x=meses, y=valores, markers=True,
                  title="Evolução do Monitoramento",
                  labels={"x": "Mês", "y": "Itens Monitorados"})
    st.plotly_chart(fig, use_container_width=True)
    
    # Indicadores
    indicadores = pd.DataFrame({
        "Indicador": ["Conformidade Orçamentária", "Conciliações", "Licitações Analisadas",
                      "Prestações de Contas", "SIAUDI Atualizado"],
        "Meta": ["100%", "100%", "30%", "100%", "100%"],
        "Atual": ["95%", "90%", "25%", "100%", "60%"],
        "Status": ["🟡", "🟡", "🟡", "✅", "🔴"]
    })
    st.dataframe(indicadores, use_container_width=True, hide_index=True)

# EXPORTAR
elif opcao == "📄 Exportar":
    st.markdown('<p class="sub-header">📄 EXPORTAR RELATÓRIO</p>', unsafe_allow_html=True)
    
    st.markdown("### Opções de Exportação")
    
    col1, col2 = st.columns(2)
    with col1:
        mes_inicio = st.selectbox("Mês inicial", meses_pt, index=0)
    with col2:
        mes_fim = st.selectbox("Mês final", meses_pt, index=11)
    
    formato = st.radio("Formato", ["CSV", "Excel", "JSON"])
    
    if st.button("📥 GERAR RELATÓRIO", type="primary"):
        st.success("Relatório gerado!")
        
        if formato == "CSV":
            st.markdown(get_csv_download_link(df, f"relatorio_planat_{datetime.now().strftime('%Y%m%d')}.csv"),
                       unsafe_allow_html=True)
        elif formato == "JSON":
            json_str = json.dumps(df.to_dict(), indent=2)
            b64 = base64.b64encode(json_str.encode()).decode()
            st.markdown(f'<a href="data:file/json;base64,{b64}" download="relatorio.json">📥 Download JSON</a>',
                       unsafe_allow_html=True)
        else:
            st.info("Exportação Excel disponível em breve!")

# Rodapé
st.markdown("---")
st.markdown("**Auditoria Interna - IPEM/RJ**")
st.markdown("Milana Aghara Conde Soares Leite | José Francisco Chao Cabanas")
