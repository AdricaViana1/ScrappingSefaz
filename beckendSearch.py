from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from elasticsearch import Elasticsearch


###############################################################################
## Pesquisa dos temas
###############################################################################

#Função para ler a página, extrair os campos com as urls, o título do artigo e o resumo do conteúdo      
   
all_texts = []

def acessar_pagina():
    option = Options()
    option.add_argument('--headless')
    acesso_pagina = webdriver.Chrome(options=option) #definir o navegador utilizado
    acesso_pagina.get('https://sac.sefaz.mt.gov.br/citsmart/pages/knowledgeBasePortal/knowledgeBasePortal.load#/list/1')
    
    sleep(52)
    
    return acesso_pagina    


def processar_pagina(pagina = [],contador = 1):    
    if contador > 4:
        return all_texts     
    
    if not pagina:
        pagina = acessar_pagina()
               
    page = pagina.page_source #tirar um print da página pegando o html  
    search_area = BeautifulSoup(page, 'html.parser')    
    hospedagens = search_area.find_all('div', attrs={'class':'knowledge-base-list-item clearfix ng-scope'})
        
    for hospedagem in hospedagens:
        all = {}
        try:
            u = 'https://sac.sefaz.mt.gov.br/citsmart/pages/knowledgeBasePortal/knowledgeBasePortal.load'
            a = hospedagem.find('a', attrs={'ui-sref':'knowledgeBase.knowledge({idKnowledge: knowledge.idBaseConhecimento})'})
            url = u+a['href']
            all['URL'] = url    
        except:
            all['URL'] = ["Vazio"]
        try:
            t = hospedagem.find('span', attrs={'ng-bind-html':'knowledge.titulo'}).get_text()
            all['Titulo'] = t
        except:
            all['Titulo'] = ["Vazio"]                         
        try:
            e = hospedagem.find('div', attrs={'ng-bind-html':'knowledge.conteudoReduzido'}).get_text().strip()
            all['Resumo'] = e
        except:
            all['Resumo'] = ["Vazio"]
        all_texts.append(all)
    
    print(len(all_texts))
                        
    ultima_pagina = pagina.find_element(By.CSS_SELECTOR, 'div.knowledge-base-pagination.margin-top.clearfix > ul > li.pagination-next.ng-scope > a')
    ultima_pagina.click()
            
    sleep(52)
        
    contador = contador + 1
                  
    return processar_pagina(pagina, contador)