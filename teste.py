import requests
from bs4 import BeautifulSoup

# URL da página principal
url = "http://www.nfe.fazenda.gov.br/portal/disponibilidade.aspx?versao=0.00&tipoConteudo=P2c98tUpxrI="

# Cabeçalhos HTTP para simular um navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extrair_dados(url):
    try:
        # Fazer a solicitação HTTP para obter o conteúdo da página
        response = requests.get(url, headers=headers, verify=False)  # Ignora verificação SSL para depuração

        # Verificar se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Obter o conteúdo HTML da página
            html_content = response.content

            # Analisar o conteúdo HTML usando BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Imprimir o HTML para verificar a estrutura
            print(soup.prettify())

            # Encontrar a tabela relevante na página
            table = soup.find('table', {'class': 'tabelaListagemDados'})  # Ajuste o seletor se necessário

            # Verificar se a tabela foi encontrada
            if table:
                rows = table.find_all('tr')  # Encontra todas as linhas da tabela

                # Definir o mapeamento das imagens para valores numéricos
                status_mapping = {
                    'bola_verde_P.png': '2',
                    'bola_amarela_P.png': '1',
                    'bola_vermelho_P.png': '0'
                }

                # Iterar sobre as linhas da tabela, ignorando o cabeçalho
                for row in rows[1:]:
                    cols = row.find_all('td')  # Encontra todas as colunas (células)

                    if len(cols) >= 9:
                        autorizador = cols[0].text.strip()

                        # Tradução dos status das colunas "Autorização4" e "Status Serviço4"
                        autorizacao4_status = 'N/A'
                        status_servico4 = 'N/A'

                        # Verifica a imagem na coluna "Autorização4"
                        img_autorizacao4 = cols[1].find('img')
                        if img_autorizacao4:
                            img_src = img_autorizacao4['src']
                            autorizacao4_status = status_mapping.get(img_src.split('/')[-1], 'N/A')

                        # Verifica a imagem na coluna "Status Serviço4"
                        img_status_servico4 = cols[5].find('img')
                        if img_status_servico4:
                            img_src = img_status_servico4['src']
                            status_servico4 = status_mapping.get(img_src.split('/')[-1], 'N/A')

                        # Exibe os dados extraídos
                        print(f'{autorizador}\t{autorizacao4_status}\t{status_servico4}')

                print("Script finalizado com sucesso!")
            else:
                print("Tabela não encontrada na página.")
        else:
            print(f"Falha ao acessar a página. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a solicitação: {e}")

def main():
    try:
        # Fazer a solicitação HTTP para a página principal
        response = requests.get(url, headers=headers, verify=False)  # Ignora verificação SSL para depuração

        if response.status_code == 200:
            # Obter o conteúdo HTML da página principal
            html_content = response.content

            # Analisar o conteúdo HTML usando BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Imprimir o HTML para verificar a estrutura
            print(soup.prettify())

            # Encontrar todos os links na página
            links = soup.find_all('a', href=True)

            # Iterar sobre todos os links encontrados
            for link in links:
                # Obter a URL completa para o link
                page_url = link['href']
                # Verificar se o link é relativo e criar uma URL absoluta
                if not page_url.startswith('http'):
                    page_url = requests.compat.urljoin(url, page_url)

                print(f"Acessando: {page_url}")
                # Chamar a função para extrair dados de cada link
                extrair_dados(page_url)
        else:
            print(f"Falha ao acessar a página principal. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a solicitação: {e}")

# Executa a função principal
main()
