import json
import re
from difflib import get_close_matches

# ---------------------------
# CARREGAR PRODUTOS (JSON)
# ---------------------------
def carregar_produtos():
    """Carrega os dados do arquivo produtos.json."""
    try:
        # A função espera encontrar 'produtos.json' na mesma pasta.
        with open("produtos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERRO: Arquivo 'produtos.json' não encontrado!")
        return {}
    except Exception as e:
        print(f"Erro ao carregar produtos: {e}")
        return {}

# ---------------------------
# NORMALIZA TEXTO
# ---------------------------
def normalize(texto):
    """Normaliza o texto para facilitar a busca (minúsculas, sem acentos e caracteres especiais)."""
    # Simplificado, apenas minúsculas e remoção de pontuação
    texto = texto.lower()
    texto = texto.replace("-", " ")
    texto = re.sub(r"[^\w\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

# ---------------------------
# BUSCAR PRODUTO
# ---------------------------
def buscar_produto(mensagem, banco):
    """Busca um produto no banco de dados com base na mensagem."""
    if not mensagem:
        return None

    msg_norm = normalize(mensagem)

    # Cria um dicionário achatado com todos os nomes de produtos
    todos_produtos = {}
    for categoria in banco.values():
        for nome, dados in categoria.items():
            todos_produtos[nome] = dados

    chaves_produtos = todos_produtos.keys()

    # 1 — Match exato ou aproximado
    # Usamos o get_close_matches para procurar o produto mais provável
    similar = get_close_matches(msg_norm, chaves_produtos, n=1, cutoff=0.65)
    
    if similar:
        return similar[0], todos_produtos[similar[0]] # Retorna o nome e os dados

    return None, None # Se não encontrar