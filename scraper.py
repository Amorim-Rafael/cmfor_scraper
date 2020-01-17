import requests
from bs4 import BeautifulSoup
import base64
import json
import time
import pathlib
import os
import errno


def crete_folder(dirName):
    if not os.path.exists(dirName):
        try:
            os.makedirs(dirName)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

def get_legislaturas():
    url = 'http://transparencia.cmfor.ce.gov.br/apps/vdp/index.php'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    legislaturas = [option['value'] for option in soup.find(id='legislaturas').find_all('option')]
    return legislaturas
    

def get_vereadores(legislatura):
    url = 'http://transparencia.cmfor.ce.gov.br/apps/vdp/controles/vereadores.php?legislaturas='+str(legislatura)
    page = requests.get(url)
    vereadores = page.json()
    return vereadores
    # for vereador in vereadores:
    #     print(vereador['vereador'].lower().replace(" ", "_"))


def get_pesquisar(legislatura, vereador, mes, ano):
    url = 'http://transparencia.cmfor.ce.gov.br/apps/vdp/controles/resultado_pesquisa_vdp.php'
    page = requests.post(url, data = {'legislaturas': legislatura, 'vereadores': vereador, 'mes': mes, 'ano_legislatura': ano})
    soup = BeautifulSoup(page.content, 'html.parser')
    btns = soup.find('button')
    print(btns)


def get_pdf(legislaturas):
    for legislatura in [l for l in legislaturas if l != '17' and l != '19' and l != '20']:
        for vereador in get_vereadores(legislatura):
            for mes in get_meses():
                for ano in get_anos():
                    name_pdf = vereador['vereador'].lower().replace(" ", "_") + '_' + str(mes) + '_' + str(ano)
                    dirName = 'pdfs/'+str(ano)+'/'+str(mes)+'/'
                    legislatura_decoded, vereador_decoded, mes_decoded, ano_decoded = encode64(str(legislatura).encode(), str(vereador['id_vereador']).encode(), str(mes).encode(), str(ano).encode())
                    url = 'http://transparencia.cmfor.ce.gov.br/apps/vdp/get_files.php?legislatura={}&vereador={}&mes={}&ano={}'.format(legislatura_decoded, vereador_decoded, mes_decoded, ano_decoded)
                    file_pdf = requests.get(url)
                    crete_folder(dirName)
                    with open(dirName+name_pdf+'.pdf', 'wb') as pdf:
                        pdf.write(file_pdf.content)
                        print('salvo '+ name_pdf)


def get_pdf2(legislatura, vereador, mes, ano):
    url = 'http://transparencia.cmfor.ce.gov.br/apps/vdp/get_files.php?legislatura={}&vereador={}&mes={}&ano={}'.format(legislatura, vereador, mes, ano)
    file_pdf = requests.get(url)
    with open('pdfs/teste.pdf', 'wb') as pdf:
        pdf.write(file_pdf.content)


def encode64(legislatura, vereador, mes, ano):
    legislatura_decoded = base64.b64encode(legislatura).decode('utf-8')
    vereador_decoded = base64.b64encode(vereador).decode('utf-8')
    mes_decoded = base64.b64encode(mes).decode('utf-8')
    ano_decoded = base64.b64encode(ano).decode('utf-8')
    return legislatura_decoded, vereador_decoded, mes_decoded, ano_decoded


def get_meses():
    return ['01','02','03','04','05','06','07','08','09','10','11','12']
    # return list(range(1, 13))

def get_anos():
    return [2018,2019,2020]
    # return list(range(2018, 2020))


if __name__ == "__main__":
    get_pdf(get_legislaturas())
    # get_pdf2('MDE=', 'NDY=', 'MQ==', 'MjAxOQ==')