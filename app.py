import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import base64
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Sistema PLANAT 2026 - IPEM/RJ",
    page_icon="✅",
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
    .card {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #003366;
        margin-bottom: 1rem;
    }
    .progress-text {
        font-size: 1.2rem;
        font-weight: bold;
        color: #003366;
    }
    .status-concluido {
        color: green;
        font-weight: bold;
    }
    .status-pendente {
        color: orange;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        padding: 1rem;
        color: gray;
        font-size: 0.8rem;
    }
    .stButton > button {
        background-color: #003366;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<p class="main-header">✅ SISTEMA DE MONITORAMENTO DO PLANAT 2026</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem;">Instituto de Pesos e Medidas do Estado do Rio de Janeiro - IPEM/RJ</p>', unsafe_allow_html=True)
st.markdown("---")

# Inicialização do estado da sessão
if 'checklists' not in st.session_state:
    st.session_state.checklists = {}

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/RJ-01.png/200px-RJ-01.png", width=100)
    st.markdown("## 📅 Controle Mensal")
    
    meses_pt = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    mes_atual = datetime.now().month
    ano_atual = 2026
    
    mes_selecionado = st.selectbox(
        "Selecione o mês",
        range(1, 13),
        format_func=lambda x: f"{meses_pt[x-1]}/{ano_atual}",
        index=mes_atual-1
    )
    
    st.markdown("---")
    st.markdown("### 👥 Equipe")
    st.markdown("**Milana Aghara Conde Soares Leite**")
    st.markdown("**José Francisco Chao Cabanas**")
    
    st.markdown("---")
    if st.button("🔄 Nova Sessão", use_container_width=True):
        st.session_state.checklists = {}
        st.rerun()

# Dicionário com todos os itens do PLANAT
itens_planat = {
    1: {
        "descricao": "Atos de Gestão",
        "responsavel": "Milana",
        "tarefas": [
            "Verificar Cadastro de Responsáveis",
            "Monitorar recomendações TCE/CGE",
            "Acompanhar Concurso Público",
            "Avaliar Programa de Integridade",
            "Verificar documentação arquivada"
        ]
    },
    2: {
        "descricao": "Gestão do Planejamento Orçamentário",
        "responsavel": "José",
        "tarefas": [
            "Analisar PPA 2024-2027",
            "Verificar LOA 2026",
            "Acompanhar metas do planejamento"
        ]
    },
    3: {
        "descricao": "Gestão Orçamentária",
        "responsavel": "José",
        "tarefas": [
            "Conferir receita realizada x prevista",
            "Analisar despesa executada x fixada",
            "Verificar execução de DEA",
            "Analisar restos a pagar",
            "Acompanhar alterações orçamentárias"
        ]
    },
    4: {
        "descricao": "Gestão Financeira",
        "responsavel": "José",
        "tarefas": [
            "Verificar integração SIAFERIO",
            "Realizar conciliações bancárias",
            "Analisar saldos de caixa",
            "Verificar transferências financeiras"
        ]
    },
    5: {
        "descricao": "Gestão Contábil-Patrimonial",
        "responsavel": "José",
        "tarefas": [
            "Analisar restos a pagar",
            "Verificar dívida ativa",
            "Acompanhar registros de irregularidades",
            "Conferir bens móveis e imóveis"
        ]
    },
    6: {
        "descricao": "Gestão Previdenciária",
        "responsavel": "José",
        "tarefas": [
            "Verificar pagamento de GPS",
            "Conferir GFIP",
            "Analisar contribuição patronal"
        ]
    },
    7: {
        "descricao": "Gestão da Descentralização",
        "responsavel": "Milana",
        "tarefas": [
            "Analisar convênios vigentes",
            "Verificar prestações de contas",
            "Emitir relatórios de auditoria"
        ]
    },
    8: {
        "descricao": "Bens Móveis e Almoxarifado",
        "responsavel": "José",
        "tarefas": [
            "Atualizar inventário",
            "Verificar termos de responsabilidade",
            "Conferir estoque do almoxarifado",
            "Identificar bens inservíveis"
        ]
    },
    9: {
        "descricao": "Tomada de Contas",
        "responsavel": "Milana",
        "tarefas": [
            "Identificar processos instaurados",
            "Emitir relatórios de auditoria",
            "Encaminhar ao TCE/CGE"
        ]
    },
    10: {
        "descricao": "Prestação de Contas de Adiantamento",
        "responsavel": "Milana",
        "tarefas": [
            "Receber prestações de contas",
            "Analisar documentos fiscais",
            "Verificar devolução de saldos",
            "Emitir relatórios"
        ]
    },
    11: {
        "descricao": "PLANAT 2027",
        "responsavel": "Equipe",
        "tarefas": [
            "Iniciar elaboração",
            "Elaborar minuta",
            "Realizar revisão interna",
            "Obter aprovação",
            "Enviar à CGE"
        ]
    },
    12: {
        "descricao": "RANAT 2026",
        "responsavel": "Equipe",
        "tarefas": [
            "Consolidar relatórios mensais",
            "Elaborar minuta",
            "Revisar documento",
            "Obter aprovação",
            "Enviar à CGE"
        ]
    },
    13: {
        "descricao": "Assessoramento ao Órgão",
        "responsavel": "Equipe",
        "tarefas": [
            "Atender demandas da Presidência",
            "Orientar setores",
            "Emitir notas técnicas"
        ]
    },
    14: {
        "descricao": "Demandas TCE/CGE",
        "responsavel": "Equipe",
        "tarefas": [
            "Registrar demandas recebidas",
            "Responder dentro do prazo",
            "Arquivar documentação"
        ]
    },
    15: {
        "descricao": "Elaboração de Normativos",
        "responsavel": "Milana",
        "tarefas": [
            "Elaborar checklists",
            "Criar manuais",
            "Atualizar instruções normativas"
        ]
    },
    16: {
        "descricao": "Demandas Extraordinárias",
        "responsavel": "Equipe",
        "tarefas": [
            "Registrar demandas",
            "Emitir notas técnicas",
            "Acompanhar prazos"
        ]
    },
    17: {
        "descricao": "SIAUDI",
        "responsavel": "José",
        "tarefas": [
            "Registrar recomendações",
            "Anexar evidências",
            "Atualizar status",
            "Monitorar prazos"
        ]
    },
    18: {
        "descricao": "Temas AGE (IN 55/2025)",
        "responsavel": "Milana",
        "tarefas": [
            "Avaliar contas de obras",
            "Monitorar TAG de pessoal",
            "Acompanhar RJ Digital"
        ]
    }
}

# Função para criar chave do mês
def get_chave_mes(mes, ano):
    return f"{ano}-{mes:02d}"

chave_mes = get_chave_mes(mes_selecionado, ano_atual)

# Inicializar checklist do mês se não existir
if chave_mes not in st.session_state.checklists:
    st.session_state.checklists[chave_mes] = {}
    for item_num, item_data in itens_planat.items():
        st.session_state.checklists[chave_mes][item_num] = {
            "tarefas": {tarefa: False for tarefa in item_data["tarefas"]},
            "observacoes": "",
            "concluido": False
        }

# Função para calcular progresso
def calcular_progresso(mes):
    total_tarefas = 0
    tarefas_concluidas = 0
    
    for item_num in itens_planat.keys():
        if item_num in st.session_state.checklists[mes]:
            for concluida in st.session_state.checklists[mes][item_num]["tarefas"].values():
                total_tarefas += 1
                if concluida:
                    tarefas_concluidas += 1
    
    return total_tarefas, tarefas_concluidas

# Função para gerar relatório do mês
def gerar_relatorio_mes(mes):
    relatorio = []
    relatorio.append(f"RELATÓRIO DE MONITORAMENTO - {meses_pt[mes_selecionado-1]}/{ano_atual}")
    relatorio.append("=" * 60)
    relatorio.append(f"Data de emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    relatorio.append("")
    
    total_tarefas, tarefas_concluidas = calcular_progresso(mes)
    percentual = (tarefas_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0
    
    relatorio.append(f"PROGRESSO GERAL: {tarefas_concluidas}/{total_tarefas} tarefas ({percentual:.1f}%)")
    relatorio.append("")
    
    for item_num, item_data in itens_planat.items():
        if item_num in st.session_state.checklists[mes]:
            item_status = st.session_state.checklists[mes][item_num]
            tarefas_item = item_status["tarefas"]
            concluidas_item = sum(tarefas_item.values())
            total_item = len(tarefas_item)
            
            relatorio.append(f"{item_num}. {item_data['descricao']} - Responsável: {item_data['responsavel']}")
            relatorio.append(f"   Progresso: {concluidas_item}/{total_item} tarefas")
            
            for tarefa, concluida in tarefas_item.items():
                status = "✅" if concluida else "⬜"
                relatorio.append(f"   {status} {tarefa}")
            
            if item_status["observacoes"]:
                relatorio.append(f"   Observações: {item_status['observacoes']}")
            
            relatorio.append("")
    
    relatorio.append("=" * 60)
    relatorio.append("Assinaturas:")
    relatorio.append("")
    relatorio.append("_________________________          _________________________")
    relatorio.append("Milana Aghara Conde Soares Leite    José Francisco Chao Cabanas")
    relatorio.append("Auditora Interna                     Auditor Interno")
    
    return "\n".join(relatorio)

# Layout principal com abas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 PROGRESSO GERAL",
    "✅ CHECKLISTS",
    "📋 RESUMO DO MÊS",
    "📄 RELATÓRIO",
    "📤 EXPORTAR"
])

# ABA 1: PROGRESSO GERAL
with tab1:
    st.markdown('<p class="sub-header">📊 PROGRESSO DO MÊS</p>', unsafe_allow_html=True)
    
    total_tarefas, tarefas_concluidas = calcular_progresso(chave_mes)
    percentual = (tarefas_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Tarefas", total_tarefas)
    with col2:
        st.metric("Tarefas Concluídas", tarefas_concluidas)
    with col3:
        st.metric("Progresso", f"{percentual:.1f}%")
    
    # Barra de progresso
    st.progress(percentual / 100, text=f"Progresso geral: {percentual:.1f}%")
    
    st.markdown("---")
    
    # Progresso por item
    st.markdown("### 📈 Progresso por Item")
    
    progresso_data = []
    for item_num, item_data in itens_planat.items():
        if item_num in st.session_state.checklists[chave_mes]:
            tarefas_item = st.session_state.checklists[chave_mes][item_num]["tarefas"]
            concluidas = sum(tarefas_item.values())
            total = len(tarefas_item)
            percentual_item = (concluidas / total * 100) if total > 0 else 0
            
            progresso_data.append({
                "Item": item_num,
                "Descrição": item_data["descricao"],
                "Responsável": item_data["responsavel"],
                "Progresso": f"{concluidas}/{total}",
                "%": f"{percentual_item:.0f}%"
            })
    
    df_progresso = pd.DataFrame(progresso_data)
    st.dataframe(df_progresso, use_container_width=True, hide_index=True)
    
    # Gráfico de progresso
    fig = px.bar(
        df_progresso,
        x="Item",
        y=[float(p.strip('%')) for p in df_progresso["%"]],
        title="Progresso por Item (%)",
        labels={"y": "Percentual", "x": "Item"}
    )
    st.plotly_chart(fig, use_container_width=True)

# ABA 2: CHECKLISTS
with tab2:
    st.markdown(f'<p class="sub-header">✅ CHECKLISTS - {meses_pt[mes_selecionado-1]}/{ano_atual}</p>', unsafe_allow_html=True)
    
    # Seleção de item
    item_selecionado = st.selectbox(
        "Selecione o item para preencher",
        list(itens_planat.keys()),
        format_func=lambda x: f"{x} - {itens_planat[x]['descricao']} (Resp: {itens_planat[x]['responsavel']})"
    )
    
    if item_selecionado:
        st.markdown("---")
        
        # Card do item
        with st.container():
            st.markdown(f'<div class="card">', unsafe_allow_html=True)
            st.markdown(f"### {item_selecionado}. {itens_planat[item_selecionado]['descricao']}")
            st.markdown(f"**Responsável:** {itens_planat[item_selecionado]['responsavel']}")
            
            # Tarefas
            st.markdown("#### Tarefas:")
            
            tarefas_atualizadas = {}
            for tarefa in itens_planat[item_selecionado]["tarefas"]:
                valor_atual = st.session_state.checklists[chave_mes][item_selecionado]["tarefas"].get(tarefa, False)
                tarefas_atualizadas[tarefa] = st.checkbox(
                    tarefa,
                    value=valor_atual,
                    key=f"{chave_mes}_{item_selecionado}_{tarefa}"
                )
            
            # Observações
            st.markdown("#### Observações:")
            observacoes = st.text_area(
                "Anotações do item",
                value=st.session_state.checklists[chave_mes][item_selecionado]["observacoes"],
                key=f"{chave_mes}_{item_selecionado}_obs",
                height=100
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Botão salvar
        if st.button(f"💾 Salvar Item {item_selecionado}", type="primary", use_container_width=True):
            st.session_state.checklists[chave_mes][item_selecionado]["tarefas"] = tarefas_atualizadas
            st.session_state.checklists[chave_mes][item_selecionado]["observacoes"] = observacoes
            
            # Verificar se todas as tarefas estão concluídas
            todas_concluidas = all(tarefas_atualizadas.values())
            st.session_state.checklists[chave_mes][item_selecionado]["concluido"] = todas_concluidas
            
            st.success(f"Item {item_selecionado} salvo com sucesso!")
            st.rerun()

# ABA 3: RESUMO DO MÊS
with tab3:
    st.markdown(f'<p class="sub-header">📋 RESUMO - {meses_pt[mes_selecionado-1]}/{ano_atual}</p>', unsafe_allow_html=True)
    
    total_tarefas, tarefas_concluidas = calcular_progresso(chave_mes)
    percentual = (tarefas_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0
    
    # Cards de resumo
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Itens", len(itens_planat))
    with col2:
        itens_concluidos = sum(1 for item in st.session_state.checklists[chave_mes].values() if item["concluido"])
        st.metric("Itens Concluídos", itens_concluidos)
    with col3:
        st.metric("Tarefas", total_tarefas)
    with col4:
        st.metric("Feitas", tarefas_concluidas)
    
    st.markdown("---")
    
    # Lista detalhada por item
    for item_num, item_data in itens_planat.items():
        if item_num in st.session_state.checklists[chave_mes]:
            item_status = st.session_state.checklists[chave_mes][item_num]
            tarefas_item = item_status["tarefas"]
            concluidas_item = sum(tarefas_item.values())
            total_item = len(tarefas_item)
            
            with st.expander(f"{item_num}. {item_data['descricao']} - {concluidas_item}/{total_item} concluídas"):
                for tarefa, concluida in tarefas_item.items():
                    status = "✅" if concluida else "⬜"
                    st.markdown(f"{status} {tarefa}")
                
                if item_status["observacoes"]:
                    st.markdown(f"**Observações:** {item_status['observacoes']}")

# ABA 4: RELATÓRIO
with tab4:
    st.markdown(f'<p class="sub-header">📄 RELATÓRIO DO MÊS</p>', unsafe_allow_html=True)
    
    if st.button("📄 GERAR RELATÓRIO COMPLETO", type="primary", use_container_width=True):
        relatorio_texto = gerar_relatorio_mes(chave_mes)
        
        st.markdown("### 👁️ Visualização do Relatório")
        st.text_area("Prévia", relatorio_texto, height=400)
        
        # Download
        b64 = base64.b64encode(relatorio_texto.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="relatorio_{meses_pt[mes_selecionado-1]}_{ano_atual}.txt" style="background-color: #003366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">📥 BAIXAR RELATÓRIO</a>'
        st.markdown(href, unsafe_allow_html=True)

# ABA 5: EXPORTAR
with tab5:
    st.markdown(f'<p class="sub-header">📤 EXPORTAR DADOS</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Exportar Checklist (JSON)", use_container_width=True):
            dados_export = json.dumps(st.session_state.checklists[chave_mes], indent=2, ensure_ascii=False)
            b64 = base64.b64encode(dados_export.encode()).decode()
            href = f'<a href="data:file/json;base64,{b64}" download="checklist_{meses_pt[mes_selecionado-1]}_{ano_atual}.json">📥 Download JSON</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    with col2:
        if st.button("📥 Exportar Progresso (CSV)", use_container_width=True):
            dados_progresso = []
            for item_num, item_data in itens_planat.items():
                if item_num in st.session_state.checklists[chave_mes]:
                    tarefas_item = st.session_state.checklists[chave_mes][item_num]["tarefas"]
                    concluidas = sum(tarefas_item.values())
                    total = len(tarefas_item)
                    
                    dados_progresso.append({
                        "Item": item_num,
                        "Descrição": item_data["descricao"],
                        "Responsável": item_data["responsavel"],
                        "Tarefas Concluídas": concluidas,
                        "Total Tarefas": total,
                        "Percentual": f"{(concluidas/total*100):.1f}%" if total > 0 else "0%"
                    })
            
            df_export = pd.DataFrame(dados_progresso)
            csv = df_export.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="progresso_{meses_pt[mes_selecionado-1]}_{ano_atual}.csv">📥 Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown('<p class="footer">Sistema de Monitoramento do PLANAT 2026 - Auditoria Interna do IPEM/RJ</p>', unsafe_allow_html=True)
