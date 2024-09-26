import streamlit as st
from bs4 import BeautifulSoup
import re

# Caminho para o arquivo HTML local
caminho_arquivo = '/workspaces/Funcoes2/blob/pagina/teste.html'

def carregar_espacos(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            conteudo = file.read()
            soup = BeautifulSoup(conteudo, 'html.parser')

            espacos = {}
            # Procurar por elementos `span` que contêm links `a`
            for span in soup.find_all('span', class_='plugin_pagetree_children_span'):
                link_element = span.find('a')
                if link_element:
                    nome_espaco = link_element.get_text(strip=True)
                    link_espaco = link_element['href']
                    espacos[nome_espaco] = link_espaco
            return espacos
    except FileNotFoundError:
        st.error("Arquivo não encontrado. Verifique o caminho do arquivo.")
        return {}
    except Exception as e:
        st.error(f"Erro ao processar o HTML: {e}")
        return {}

def buscar_espaco(pergunta, espacos):
    pergunta_lower = pergunta.lower()
    resultados = []
    for chave, link in espacos.items():
        if re.search(pergunta_lower, chave.lower()):
            resultados.append((chave, link))
    
    if resultados:
        return resultados
    return "Desculpe, não encontrei palavra correspondente."

# Configuração do Streamlit
st.title("Procura de funções")
#st.write("Faça uma pergunta sobre o que deseja consultar.")

# Carregar os espaços do arquivo local
espacos = carregar_espacos(caminho_arquivo)

# Entrada do usuário
pergunta = st.text_input("Digite o nome do que você está procurando:")

# Quando o usuário enviar uma pergunta
if pergunta:
    resposta = buscar_espaco(pergunta, espacos)
    if isinstance(resposta, list):
        for nome_espaco, link_espaco in resposta:
            st.write(f"Espaço: {nome_espaco}, Link: {link_espaco}")
    else:
        st.write("Resposta:", resposta)
