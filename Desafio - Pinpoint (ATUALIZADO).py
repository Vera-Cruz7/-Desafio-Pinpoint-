import requests
from bs4 import BeautifulSoup
import csv
import time
import os

# Função para consultar o status e salvar em CSV
def consultar_status():
    print("Consultando o status dos serviços NFE...")  # Feedback ao iniciar
    
    # URL do site da NFE
    url = 'http://www.nfe.fazenda.gov.br/portal/disponibilidade.aspx?versao=0.00&tipoConteudo=P2c98tUpxrI='
    
    # Fazendo a requisição HTTP
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tabela = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_gdvDisponibilidade2'})

        if tabela:
            print("Tabela de status encontrada.")
            linhas = tabela.find_all('tr')[1:]  # Ignorar o cabeçalho

            # Abrir o arquivo CSV para gravar
            with open('status_nfe.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                # Escrevendo o cabeçalho (opcional, caso ainda não exista)
                if os.stat('status_nfe.csv').st_size == 0:
                    writer.writerow(['Estado', 'Status', 'Data/Hora'])

                for linha in linhas:
                    colunas = linha.find_all('td')
                    estado = colunas[0].text.strip()
                    status_img = colunas[1].find('img')['src']
                    
                    if 'bola_verde' in status_img:
                        status = 'Operacional'
                    elif 'bola_amarela' in status_img:
                        status = 'Instabilidade'
                    elif 'bola_vermelha' in status_img:
                        status = 'Fora do ar'
                    else:
                        status = 'Desconhecido'
                    
                    print(f"Estado: {estado}, Status: {status}")  # Log adicional para cada estado
                    writer.writerow([estado, status, time.strftime("%Y-%m-%d %H:%M:%S")])
                    
                    # Verificar se algum estado está com problemas e alertar
                    if status != 'Operacional':
                        print(f"Alerta! Estado: {estado} está com status: {status}")
        else:
            print("Tabela de status não encontrada.")
    else:
        print(f"Erro ao acessar a página: {response.status_code}")

# Loop para rodar a cada 30 minutos (1800 segundos)
while True:
    consultar_status()
    time.sleep(1800)  # Intervalo de 30 minutos entre as consultas
