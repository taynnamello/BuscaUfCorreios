import requests
from bs4 import BeautifulSoup
import json

def buscapag(uf, pag):
    session = requests.session()
    data = {'UF': uf,
            'qtdrow': 50,
            'pagini': pag - 49,
            'pagfim': pag,
            }
    r = session.post("http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaFaixaCEP.cfm", data)
    content = r.content
 
    soup = BeautifulSoup(content, 'html.parser')

    try:
        if pag > 50:
            items = soup.find_all('table', { 'class' : 'tmptabela' })[0].find_all('td')
        else:
            items = soup.find_all('table', { 'class' : 'tmptabela' })[1].find_all('td')
   
        x = 0;
        data = {}
        for i in range(len(items)): 
            if (i + x) < len(items):
                cidade = items[i + x].string
                faixa = items[i + x + 1].string
                data[cidade] = faixa.strip()
            x = x + 3
    
        return (data)
    except:
        return "Empty"

def gravaArquivoJson(valor):
   with open('cidades.json', 'w') as json_file:
       print("O resultado esta disponível no arquivo cidades.json")
       json.dump(valor, json_file)   

def buscacidades(ufs):
    listaCidades = {}
    for uf in ufs:
        pagina = 50
        finaltabela = 0
        listaCidades[uf] = []
        cod = 1
        print("Iniciando busca pelas cidades de " + uf)
        while (finaltabela == 0):
            resultado = buscapag(uf, pagina)
            if resultado == "Empty":
                finaltabela = 100
                print("Finalizando busca de cidades de " + uf)
            else:
                for key in sorted(resultado):
                    listaCidades[uf].append({'Codigo: ': cod, 'Municipio': key, 'FaixaCep': resultado[key]})
                    cod = cod + 1
                pagina = pagina + 50

    gravaArquivoJson(listaCidades)        

estados = input("Digite os estados que deseja buscar (separados por virgula)")
buscacidades(estado.strip() for estado in estados.split(","))
