import streamlit as st
from funcoes import (
    carregar_produtos,
    buscar_produto,
    normalize,
)

# --- Configurações Iniciais ---
st.set_page_config(page_title="SmartVendas - Chat", layout="centered")

# Mock para carregar dados (substitua pela sua importação real se necessário)
@st.cache_data
def carregar_dados():
    try:
        return carregar_produtos()
    except:
        return [] 

banco = carregar_dados()

# --- Estados da Conversa ---
if "chat" not in st.session_state:
    st.session_state.chat = []
    st.session_state.conversa_state = 'INITIAL'
    st.session_state.current_product = None

if not st.session_state.chat:
    st.session_state.chat.append({"role": "assistant", "content": "Olá! Sou o SmartBot.\nSobre o que você deseja falar?"})

# --- Funções de Resposta ---
def get_greeting_response():
    return "Olá! Sou o Smartbot do time de vendas. Como posso ajudar?"

def get_product_query_response():
    return "Qual seria o produto que você procura?"

def get_delivery_response(product_name):
    return f"Certo, achei o seu **{product_name.title()}**.\n\nDeseja saber sobre o prazo de entrega?"

def get_transfer_query_response():
    return "O prazo é de 2 a 5 dias úteis.\n\nDeseja que te transfira para um de nossos vendedores?"

def get_transfer_confirmation():
    return "Certo, vou te transferir para o atendimento humano."

# --- Layout e Estilização (CSS Atualizado e Compacto) ---
st.markdown("""
<style>
    :root {
        --primary-blue: #1565C0;
        --bg-gray: #F5F5F5;
        --chat-user: #1565C0;
        --chat-bot: #FFFFFF;
        --phone-width: 360px;  /* Largura fixa compacta */
        --phone-height: 640px; /* Altura fixa compacta (16:9) */
    }

    /* Centraliza tudo na página */
    .block-container {
        padding-top: 2rem;
        display: flex;
        justify-content: center;
    }

    /* O CORPO do Celular */
    .mobile-container {
        width: var(--phone-width);
        height: var(--phone-height);
        background-color: var(--bg-gray);
        border-radius: 30px; /* Bordas bem arredondadas */
        box-shadow: 0 15px 35px rgba(0,0,0,0.2); /* Sombra para dar profundidade */
        border: 8px solid #222; /* Moldura preta do celular */
        display: flex;
        flex-direction: column;
        overflow: hidden;
        position: relative;
        margin-bottom: 50px; /* Espaço para o input não cobrir o pé do celular */
    }

    /* Cabeçalho Azul */
    .app-header {
        background-color: var(--primary-blue);
        color: white;
        padding: 25px 15px 15px 15px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        z-index: 10;
    }
    
    .icon-circle {
        background: rgba(255,255,255,0.2);
        width: 50px; height: 50px;
        border-radius: 50%;
        margin: 0 auto 8px auto;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px;
    }

    /* Área de Scroll do Chat */
    .chat-scroll-area {
        flex-grow: 1;
        overflow-y: auto;
        padding: 15px;
        padding-bottom: 60px; /* Espaço extra no final */
        scrollbar-width: thin; /* Scrollbar fina */
    }

    /* --- Balões de Chat --- */
    
    /* Removemos o estilo padrão do Streamlit */
    .stChatMessage {
        background-color: transparent !important;
        padding: 0 !important;
        margin-bottom: 10px;
        border: none !important;
    }
    .stChatMessage .stChatMessageAvatar { display: none; }

    /* Conteúdo do Balão */
    .stChatMessageContent {
        padding: 10px 14px !important;
        border-radius: 18px !important;
        font-size: 13px;
        line-height: 1.4;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        max-width: 80%;
        display: inline-block;
    }

    /* Bot (Esquerda) */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        text-align: left;
    }
    div[data-testid="stChatMessage"]:nth-child(odd) .stChatMessageContent {
        background-color: var(--chat-bot) !important;
        color: #333 !important;
        border-top-left-radius: 4px !important;
    }

    /* Usuário (Direita) */
    div[data-testid="stChatMessage"]:nth-child(even) {
        text-align: right; /* Alinha o bloco à direita */
    }
    div[data-testid="stChatMessage"]:nth-child(even) .stChatMessageContent {
        background-color: var(--chat-user) !important;
        color: white !important;
        border-top-right-radius: 4px !important;
        text-align: left; /* Texto dentro do balão continua legível */
    }

    /* --- Truque para o Input do Chat --- */
    /* Força o input a ter a largura do celular e centralizar */
    .stChatInput {
        position: fixed;
        bottom: 20px;
        width: var(--phone-width) !important;
        max-width: var(--phone-width) !important;
        left: 50%;
        transform: translateX(-50%);
        z-index: 100;
    }
    
    .stChatInputContainer {
        background-color: white;
        border-radius: 25px !important;
        border: 1px solid #ddd;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }

    /* Esconder header/footer padrão */
    header, footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- Estrutura Visual ---

# Inicia container do "Celular"
st.markdown('<div class="mobile-container">', unsafe_allow_html=True)

# Cabeçalho
st.markdown("""
    <div class="app-header">
        <div class="icon-circle">🛒</div>
        <div style="font-weight:bold; font-size:18px;">SmartVendas</div>
        <div style="font-size:12px; opacity:0.9;">Assistente Virtual</div>
    </div>
""", unsafe_allow_html=True)

# Área de Chat
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-scroll-area">', unsafe_allow_html=True)
    
    # Renderiza mensagens
    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Fim do container mobile


# --- Lógica de Input e Processamento ---

if prompt := st.chat_input("Digite sua dúvida..."):
    
    st.session_state.chat.append({"role": "user", "content": prompt})
    prompt_norm = normalize(prompt)
    resposta = None
    
    # --- LÓGICA DE ESTADOS (Mantida igual) ---
    if st.session_state.conversa_state == 'INITIAL':
        saudacoes = ["oi", "ola", "bom dia", "boa tarde", "boa noite", "e ai"]
        if any(s in prompt_norm for s in saudacoes):
            resposta = get_greeting_response()
            st.session_state.conversa_state = 'AWAITING_QUERY'
        else:
            resposta = "Olá! Diga 'Quero consultar um produto' para iniciarmos."

    elif st.session_state.conversa_state == 'AWAITING_QUERY':
        if ("consultar" in prompt_norm and "produto" in prompt_norm) or "quero" in prompt_norm:
            resposta = get_product_query_response()
            st.session_state.conversa_state = 'AWAITING_PRODUCT'
        else:
            resposta = "Para ver nosso catálogo, diga: 'Quero consultar um produto'."

    elif st.session_state.conversa_state == 'AWAITING_PRODUCT':
        produto_encontrado, dados = buscar_produto(prompt, banco)
        if produto_encontrado:
            st.session_state.current_product = produto_encontrado
            resposta = get_delivery_response(produto_encontrado)
            st.session_state.conversa_state = 'AWAITING_DELIVERY_CONFIRMATION'
        else:
            resposta = "Produto não encontrado. Tente outro nome."

    elif st.session_state.conversa_state == 'AWAITING_DELIVERY_CONFIRMATION':
        if any(x in prompt_norm for x in ["sim", "quero", "pode", "ok"]):
            resposta = get_transfer_query_response()
            st.session_state.conversa_state = 'AWAITING_TRANSFER_CONFIRMATION'
        else:
            resposta = "Tudo bem. Posso te transferir para um vendedor humano?"
            st.session_state.conversa_state = 'AWAITING_TRANSFER_CONFIRMATION'

    elif st.session_state.conversa_state == 'AWAITING_TRANSFER_CONFIRMATION':
            if any(x in prompt_norm for x in ["sim", "quero", "pode", "ok"]):
                resposta = get_transfer_confirmation()
                st.session_state.conversa_state = 'TRANSFERRING'
            else:
                resposta = "Certo. Digite 'oi' para reiniciar."
                st.session_state.conversa_state = 'INITIAL'

    elif st.session_state.conversa_state == 'TRANSFERRING':
        resposta = "Aguarde um momento..."

    if resposta:
        st.session_state.chat.append({"role": "assistant", "content": resposta})
    
    st.rerun()