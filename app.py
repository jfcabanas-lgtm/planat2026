import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import base64
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="PLANAT 2026 - IPEM/RJ",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de cores corporativa
cores = {
    "primary": "#003366",      # Azul escuro institucional
    "secondary": "#FFD700",     # Dourado
    "success": "#28a745",       # Verde
    "warning": "#ffc107",        # Amarelo
    "danger": "#dc3545",         # Vermelho
    "light": "#f8f9fa",          # Cinza claro
    "dark": "#343a40",           # Cinza escuro
    "white": "#ffffff"
}

# CSS personalizado para visual corporativo
st.markdown(f"""
<style>
    /* Fonte principal */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Header principal */
    .main-header {{
        background: linear-gradient(90deg, {cores['primary']} 0%, #004c99 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }}
    
    .main-header h1 {{
        font-size: 2.5rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: 1px;
    }}
    
    .main-header p {{
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }}
    
    /* Cards */
    .card {{
        background: {cores['white']};
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    
    .card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    /* Métricas */
    .metric-card {{
        background: linear-gradient(135deg, {cores['primary']} 0%, #004c99 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,51,102,0.2);
    }}
    
    .metric-card h3 {{
        font-size: 1rem;
        font-weight: 400;
        margin: 0;
        opacity: 0.9;
    }}
    
    .metric-card p {{
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0 0 0;
    }}
    
    .metric-card small {{
        font-size: 0.9rem;
        opacity: 0.8;
    }}
    
    /* Status badges */
    .badge {{
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
    }}
    
    .badge-success {{
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }}
    
    .badge-warning {{
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeeba;
    }}
    
    .badge-danger {{
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }}
    
    .badge-info {{
        background: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }}
    
    .badge-secondary {{
        background: #e2e3e5;
        color: #383d41;
        border: 1px solid #d6d8db;
    }}
    
    /* Botões */
    .stButton > button {{
        background: {cores['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s;
        border: 1px solid {cores['primary']};
    }}
    
    .stButton > button:hover {{
        background: #004c99;
        color: white;
        border: 1px solid #004c99;
        box-shadow: 0 2px 4px rgba(0,51,102,0.3);
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2rem;
        background: {cores['light']};
        padding: 0.5rem;
        border-radius: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {cores['primary']};
        color: white !important;
    }}
    
    /* Sidebar */
    .css-1d391kg {{
        background: {cores['light']};
    }}
    
    .sidebar-header {{
        background: {cores['primary']};
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }}
    
    /* Footer */
    .footer {{
        background: {cores['light']};
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: {cores['dark']};
        font-size: 0.9rem;
        margin-top: 2rem;
        border-top: 3px solid {cores['primary']};
    }}
    
    /* Títulos */
    .section-title {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {cores['primary']};
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {cores['secondary']};
    }}
    
    /* Links */
    a {{
        color: {cores['primary']};
        text-decoration: none;
        font-weight: 500;
    }}
    
    a:hover {{
        color: #004c99;
        text-decoration: underline;
    }}
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown(f"""
<div class="main-header">
    <h1>🏛️ PLANAT 2026</h1>
    <p>Plano Anual de Atividades de Auditoria Interna</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem;">Instituto de Pesos e Medidas do Estado do Rio de Janeiro</p>
</div>
""", unsafe_allow_html=True)

# Inicialização do estado da sessão
if 'checklists' not in st.session_state:
    st.session_state.checklists = {}

# Sidebar corporativa
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-header">
        <h3 style="margin:0; color:white;">📅 Controle Mensal</h3>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    st.markdown(f"""
    <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid #003366;">
        <h4 style="margin:0 0 0.5rem 0; color: #003366;">👥 Equipe de Auditoria</h4>
        <p style="margin:0; font-size:0.9rem;">Auditor-Chefe</p>
        <p style="margin:0; font-weight:600;">José Francisco Chao Cabanas</p>
        <p style="margin:0.5rem 0 0 0; font-size:0.9rem;">Auditora</p>
        <p style="margin:0; font-weight:600;">Milana Aghara Conde Soares Leite</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🔄 Nova Sessão", use_container_width=True):
        st.session_state.checklists = {}
        st.rerun()

# Dicionário com todos os itens do PLANAT
itens_planat = {
    1: {
        "descricao": "Atos de Gestão",
        "responsavel": "Auditoria",
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
        "responsavel": "Auditoria",
        "tarefas": [
            "Analisar PPA 2024-2027",
            "Verificar LOA 2026",
            "Acompanhar metas do planejamento"
        ]
    },
    3: {
        "descricao": "Gestão Orçamentária",
        "responsavel": "Auditoria",
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
        "responsavel": "Auditoria",
        "tarefas": [
            "Verificar integração SIAFERIO",
            "Realizar conciliações bancárias",
            "Analisar saldos de caixa",
            "Verificar transferências financeiras"
        ]
    },
    5: {
        "descricao": "Gestão Contábil-Patrimonial",
        "responsavel": "Auditoria",
        "tarefas": [
            "Analisar restos a pagar",
            "Verificar dívida ativa",
            "Acompanhar registros de irregularidades",
            "Conferir bens móveis e imóveis"
        ]
    },
    6: {
        "descricao": "Gestão Previdenciária",
        "responsavel": "Auditoria",
        "tarefas": [
            "Verificar pagamento de GPS",
            "Conferir GFIP",
            "Analisar contribuição patronal"
        ]
    },
    7: {
        "descricao": "Gestão da Descentralização",
        "responsavel": "Auditoria",
        "tarefas": [
            "Analisar convênios vigentes",
            "Verificar prestações de contas",
            "Emitir relatórios de auditoria"
        ]
    },
    8: {
        "descricao": "Bens Móveis e Almoxarifado",
        "responsavel": "Auditoria",
        "tarefas": [
            "Atualizar inventário",
            "Verificar termos de responsabilidade",
            "Conferir estoque do almoxarifado",
            "Identificar bens inservíveis"
        ]
    },
    9: {
        "descricao": "Tomada de Contas",
        "responsavel": "Auditoria",
        "tarefas": [
            "Identificar processos instaurados",
            "Emitir relatórios de auditoria",
            "Encaminhar ao TCE/CGE"
        ]
    },
    10: {
        "descricao": "Prestação de Contas de Adiantamento",
        "responsavel": "Auditoria",
        "tarefas": [
            "Receber prestações de contas",
            "Analisar documentos fiscais",
            "Verificar devolução de saldos",
            "Emitir relatórios"
        ]
    },
    11: {
        "descricao": "PLANAT 2027",
        "responsavel": "Auditoria",
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
        "responsavel": "Auditoria",
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
        "responsavel": "Auditoria",
        "tarefas": [
            "Atender demandas da Presidência",
            "Orientar setores",
            "Emitir notas técnicas"
        ]
    },
    14: {
        "descricao": "Demandas TCE/CGE",
        "responsavel": "Auditoria",
        "tarefas": [
            "Registrar demandas recebidas",
            "Responder dentro do prazo",
            "Arquivar documentação"
        ]
    },
    15: {
        "descricao": "Elaboração de Normativos",
        "responsavel": "Auditoria",
        "tarefas": [
            "Elaborar checklists",
            "Criar manuais",
            "Atualizar instruções normativas"
        ]
    },
    16: {
        "descricao": "Demandas Extraordinárias",
        "responsavel": "Auditoria",
        "tarefas": [
            "Registrar demandas",
            "Emitir notas técnicas",
            "Acompanhar prazos"
        ]
    },
    17: {
        "descricao": "SIAUDI",
        "responsavel": "Auditoria",
        "tarefas": [
            "Registrar recomendações",
            "Anexar evidências",
            "Atualizar status",
            "Monitorar prazos"
        ]
    },
    18: {
        "descricao": "Temas AGE (IN 55/2025)",
        "responsavel": "Auditoria",
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
    relatorio.append("=" * 80)
    relatorio.append(f"RELATÓRIO DE MONITORAMENTO DO PLANAT 2026".center(80))
    relatorio.append("=" * 80)
    relatorio.append(f"Período: {meses_pt[mes_selecionado-1]}/{ano_atual}")
    relatorio.append(f"Data de emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    relatorio.append("=" * 80)
    relatorio.append("")
    
    total_tarefas, tarefas_concluidas = calcular_progresso(mes)
    percentual = (tarefas_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0
    
    relatorio.append("PROGRESSO GERAL")
    relatorio.append("-" * 40)
    relatorio.append(f"Total de Tarefas: {total_tarefas}")
    relatorio.append(f"Tarefas Concluídas: {tarefas_concluidas}")
    relatorio.append(f"Percentual de Conclusão: {percentual:.1f}%")
    relatorio.append("")
    
    relatorio.append("DETALHAMENTO POR ITEM")
    relatorio.append("-" * 40)
    relatorio.append("")
    
    for item_num, item_data in itens_planat.items():
        if item_num in st.session_state.checklists[mes]:
            item_status = st.session_state.checklists[mes][item_num]
            tarefas_item = item_status["tarefas"]
            concluidas_item = sum(tarefas_item.values())
            total_item = len(tarefas_item)
            
            relatorio.append(f"{item_num}. {item_data['descricao']}")
            relatorio.append(f"   Responsável: {item_data['responsavel']}")
            relatorio.append(f"   Progresso: {concluidas_item}/{total_item} ({concluidas_item/total_item*100:.0f}%)")
            relatorio.append("   Tarefas:")
            
            for tarefa, concluida in tarefas_item.items():
                status = "[X]" if concluida else "[ ]"
                relatorio.append(f"      {status} {tarefa}")
            
            if item_status["observacoes"]:
                relatorio.append(f"   Observações: {item_status['observacoes']}")
            
            relatorio.append("")
    
    relatorio.append("=" * 80)
    relatorio.append("ASSINATURAS".center(80))
    relatorio.append("=" * 80)
    relatorio.append("")
    relatorio.append("_" * 35 + "          " + "_" * 35)
    relatorio.append("José Francisco Chao Cabanas" + " " * 20 + "Milana Aghara Conde Soares Leite")
    relatorio.append("Auditor-Chefe" + " " * 27 + "Auditora")
    relatorio.append("")
    relatorio.append("=" * 80)
    
    return "\n".join(relatorio)

# Tabs principais
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 PROGRESSO GERAL",
    "✅ CHECKLISTS OPERACIONAIS",
    "📋 RESUMO EXECUTIVO",
    "📄 RELATÓRIO OFICIAL",
    "📤 EXPORTAR DADOS"
])

# ABA 1: PROGRESSO GERAL
with tab1:
    st.markdown(f'<div class="section-title">📊 PROGRESSO GERAL - {meses_pt[mes_selecionado-1]}/{ano_atual}</div>', unsafe_allow_html=True)
    
    total_tarefas, tarefas_concluidas = calcular_progresso(chave_mes)
    percentual = (tarefas_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0
    
    # Métricas em cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total de Tarefas</h3>
            <p>{total_tarefas}</p>
            <small>18 itens</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Tarefas Concluídas</h3>
            <p>{tarefas_concluidas}</p>
            <small>{percentual:.1f}% do total</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pendentes = total_tarefas - tarefas_concluidas
        st.markdown(f"""
        <div class="metric-card">
            <h3>Tarefas Pendentes</h3>
            <p>{pendentes}</p>
            <small>Aguardando execução</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        itens_concluidos = sum(1 for item in st.session_state.checklists[chave_mes].values() if item["concluido"])
        st.markdown(f"""
        <div class="metric-card">
            <h3>Itens Concluídos</h3>
            <p>{itens_concluidos}/18</p>
            <small>{(itens_concluidos/18*100):.1f}%</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Barra de progresso
    st.markdown("### Progresso Geral")
    st.progress(percentual / 100, text=f"{percentual:.1f}% concluído")
    
    st.markdown("---")
    
    # Tabela de progresso por item
    st.markdown("### 📈 Progresso por Item")
    
    progresso_data = []
    for item_num, item_data in itens_planat.items():
        if item_num in st.session_state.checklists[chave_mes]:
            tarefas_item = st.session_state.checklists[chave_mes][item_num]["tarefas"]
            concluidas = sum(tarefas_item.values())
            total = len(tarefas_item)
            percentual_item = (concluidas / total * 100) if total > 0 else 0
            
            # Determinar badge de status
            if percentual_item == 100:
                badge = '<span class="badge badge-success">Concluído</span>'
            elif percentual_item > 0:
                badge = '<span class="badge badge-warning">Em Andamento</span>'
            else:
                badge = '<span class="badge badge-secondary">Não Iniciado</span>'
            
            progresso_data.append({
                "Item": item_num,
                "Descrição": item_data["descricao"],
                "Progresso": f"{concluidas}/{total}",
                "%": f"{percentual_item:.0f}%",
                "Status": badge
            })
    
    # Criar DataFrame e exibir como HTML para usar badges
    df_progresso = pd.DataFrame(progresso_data)
    
    # Exibir tabela com st.dataframe
    st.dataframe(
        df_progresso,
        column_config={
            "Status": st.column_config.Column("Status", width="medium")
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Gráfico de barras
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_progresso["Item"],
        y=[float(p.strip('%')) for p in df_progresso["%"]],
        marker_color='#003366',
        text=[f"{p}" for p in df_progresso["%"]],
        textposition='outside',
        name="Progresso"
    ))
    
    fig.update_layout(
        title="Progresso por Item (%)",
        xaxis_title="Item",
        yaxis_title="Percentual",
        yaxis_range=[0, 100],
        plot_bgcolor='white',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ABA 2: CHECKLISTS OPERACIONAIS
with tab2:
    st.markdown(f'<div class="section-title">✅ CHECKLISTS OPERACIONAIS - {meses_pt[mes_selecionado-1]}/{ano_atual}</div>', unsafe_allow_html=True)
    
    # Seleção de item em colunas
    col1, col2 = st.columns([1, 1])
    
    with col1:
        item_selecionado = st.selectbox(
            "Selecione o item para preencher",
            list(itens_planat.keys()),
            format_func=lambda x: f"{x} - {itens_planat[x]['descricao']}"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📋 Ver Resumo do Item", use_container_width=True):
            st.session_state.show_resumo = True
    
    if item_selecionado:
        st.markdown("---")
        
        # Card do item
        item_data = itens_planat[item_selecionado]
        tarefas_atual = st.session_state.checklists[chave_mes][item_selecionado]["tarefas"]
        concluidas_item = sum(tarefas_atual.values())
        total_item = len(tarefas_atual)
        
        # Progresso do item
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div class="card">
                <h3 style="margin-top:0; color:#003366;">{item_selecionado}. {item_data['descricao']}</h3>
                <p style="margin-bottom:1rem;"><strong>Responsável:</strong> {item_data['responsavel']}</p>
            """, unsafe_allow_html=True)
            
            st.markdown("**Tarefas:**")
            
            tarefas_atualizadas = {}
            for tarefa in item_data["tarefas"]:
                valor_atual = tarefas_atual.get(tarefa, False)
                tarefas_atualizadas[tarefa] = st.checkbox(
                    tarefa,
                    value=valor_atual,
                    key=f"{chave_mes}_{item_selecionado}_{tarefa}"
                )
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="card" style="text-align:center;">
                <h4 style="margin-top:0;">Progresso</h4>
                <p style="font-size:2rem; margin:0; color:#003366;">{concluidas_item}/{total_item}</p>
                <p>{(concluidas_item/total_item*100):.0f}%</p>
                <div style="background:#e9ecef; height:10px; border-radius:5px;">
                    <div style="background:#003366; width:{(concluidas_item/total_item*100)}%; height:10px; border-radius:5px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Observações
        st.markdown("### 📝 Observações")
        observacoes = st.text_area(
            "Registre observações sobre este item",
            value=st.session_state.checklists[chave_mes][item_selecionado]["observacoes"],
            key=f"{chave_mes}_{item_selecionado}_obs",
            height=100
        )
        
        # Botão salvar
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"💾 SALVAR ITEM {item_selecionado}", type="primary", use_container_width=True):
                st.session_state.checklists[chave_mes][item_selecionado]["tarefas"] = tarefas_atualizadas
                st.session_state.checklists[chave_mes][item_selecionado]["observacoes"] = observacoes
                
                todas_concluidas = all(tarefas_atualizadas.values())
                st.session_state.checklists[chave_mes][item_selecionado]["concluido"] = todas_concluidas
                
                st.success(f"✅ Item {item_selecionado} salvo com sucesso!")
                st.rerun()

# ABA 3: RESUMO EXECUTIVO
with tab3:
    st.markdown(f'<div class="section-title">📋 RESUMO EXECUTIVO - {meses_pt[mes_selecionado-1]}/{ano_atual}</div>', unsafe_allow_html=True)
    
    # Cards de resumo
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <h4 style="margin:0; color:#003366;">Total de Itens</h4>
            <p style="font-size:2rem; margin:0;">18</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        itens_concluidos = sum(1 for item in st.session_state.checklists[chave_mes].values() if item["concluido"])
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <h4 style="margin:0; color:#003366;">Itens Concluídos</h4>
            <p style="font-size:2rem; margin:0;">{itens_concluidos}</p>
            <small>{(itens_concluidos/18*100):.0f}%</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_tarefas, tarefas_concluidas = calcular_progresso(chave_mes)
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <h4 style="margin:0; color:#003366;">Tarefas Realizadas</h4>
            <p style="font-size:2rem; margin:0;">{tarefas_concluidas}</p>
            <small>de {total_tarefas} totais</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        percentual = (tarefas_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <h4 style="margin:0; color:#003366;">Progresso Geral</h4>
            <p style="font-size:2rem; margin:0;">{percentual:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Lista detalhada por item em colunas
    col1, col2 = st.columns(2)
    
    for idx, (item_num, item_data) in enumerate(itens_planat.items()):
        with col1 if idx % 2 == 0 else col2:
            if item_num in st.session_state.checklists[chave_mes]:
                item_status = st.session_state.checklists[chave_mes][item_num]
                tarefas_item = item_status["tarefas"]
                concluidas_item = sum(tarefas_item.values())
                total_item = len(tarefas_item)
                
                # Determinar cor do card baseado no progresso
                if concluidas_item == total_item:
                    border_color = "#28a745"  # Verde
                elif concluidas_item > 0:
                    border_color = "#ffc107"  # Amarelo
                else:
                    border_color = "#dc3545"  # Vermelho
                
                st.markdown(f"""
                <div class="card" style="border-left: 5px solid {border_color};">
                    <h4 style="margin:0; color:#003366;">{item_num}. {item_data['descricao']}</h4>
                    <p style="margin:0.5rem 0;"><strong>Progresso:</strong> {concluidas_item}/{total_item} tarefas</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander(f"Ver detalhes do Item {item_num}"):
                    for tarefa, concluida in tarefas_item.items():
                        if concluida:
                            st.markdown(f"✅ {tarefa}")
                        else:
                            st.markdown(f"⬜ {tarefa}")
                    
                    if item_status["observacoes"]:
                        st.markdown(f"**Observações:** {item_status['observacoes']}")

# ABA 4: RELATÓRIO OFICIAL
with tab4:
    st.markdown(f'<div class="section-title">📄 RELATÓRIO OFICIAL - {meses_pt[mes_selecionado-1]}/{ano_atual}</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <h4 style="margin-top:0;">Gerar Relatório Consolidado</h4>
        <p>Clique no botão abaixo para gerar um relatório completo com todas as atividades do mês, incluindo:</p>
        <ul>
            <li>Progresso geral e por item</li>
            <li>Detalhamento de tarefas</li>
            <li>Observações registradas</li>
            <li>Campo para assinaturas</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 GERAR RELATÓRIO OFICIAL", type="primary", use_container_width=True):
            relatorio_texto = gerar_relatorio_mes(chave_mes)
            
            st.markdown("### 👁️ Prévia do Relatório")
            st.text_area("", relatorio_texto, height=400)
            
            # Download
            b64 = base64.b64encode(relatorio_texto.encode()).decode()
            filename = f"RELATORIO_PLANAT_{meses_pt[mes_selecionado-1]}_{ano_atual}.txt"
            
            st.markdown(f"""
            <div style="text-align:center; margin-top:1rem;">
                <a href="data:file/txt;base64,{b64}" download="{filename}" style="background-color: #003366; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">📥 BAIXAR RELATÓRIO</a>
            </div>
            """, unsafe_allow_html=True)

# ABA 5: EXPORTAR DADOS
with tab5:
    st.markdown(f'<div class="section-title">📤 EXPORTAR DADOS - {meses_pt[mes_selecionado-1]}/{ano_atual}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4 style="margin-top:0;">📋 Exportar Checklist</h4>
            <p>Formato JSON - completo com todas as tarefas e observações</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📥 Exportar JSON", use_container_width=True):
            dados_export = json.dumps(st.session_state.checklists[chave_mes], indent=2, ensure_ascii=False)
            b64 = base64.b64encode(dados_export.encode()).decode()
            filename = f"checklist_{meses_pt[mes_selecionado-1]}_{ano_atual}.json"
            
            st.markdown(f"""
            <a href="data:file/json;base64,{b64}" download="{filename}" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: block; text-align: center;">📥 Download JSON</a>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4 style="margin-top:0;">📊 Exportar Progresso</h4>
            <p>Formato CSV - tabela com progresso por item</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📥 Exportar CSV", use_container_width=True):
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
            filename = f"progresso_{meses_pt[mes_selecionado-1]}_{ano_atual}.csv"
            
            st.markdown(f"""
            <a href="data:file/csv;base64,{b64}" download="{filename}" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: block; text-align: center;">📥 Download CSV</a>
            """, unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="footer">
    <p style="margin:0;"><strong>PLANAT 2026</strong> - Plano Anual de Atividades de Auditoria Interna</p>
    <p style="margin:0.5rem 0 0 0; font-size:0.8rem;">Instituto de Pesos e Medidas do Estado do Rio de Janeiro - IPEM/RJ</p>
    <p style="margin:0; font-size:0.8rem;">Auditoria Interna • Versão 2.0 • {datetime.now().year}</p>
</div>
""", unsafe_allow_html=True)

