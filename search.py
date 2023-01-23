import os
import requests
from flask import Flask, flash, request, redirect, url_for, session, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.exceptions import RequestEntityTooLarge
from wtforms.validators import InputRequired
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
from glob import glob
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd

from typing import Dict
import warnings
warnings.filterwarnings(action='ignore')
import csv


es = Elasticsearch(
        hosts="https://localhost:9200",
        ca_certs="C:/Users/adria/Documents/Trabalho - Central/codigos/http_ca.crt",
        http_auth=("elastic", "WTDxSVLE0Wx-EK4Ngoh="),
        verify_certs=True
        )


app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'

   
all_texts = []
def scrapper():
    try:
        global all_texts
        if all_texts == []:
            option = Options()
            option.add_argument('--headless')
            navegador = webdriver.Chrome(options=option) #definir o navegador utilizado
            navegador.get('https://sac.sefaz.mt.gov.br/citsmart/pages/knowledgeBasePortal/knowledgeBasePortal.load#/list/1')
            sleep(50) 
            texto1 = navegador.find_element(By.CLASS_NAME,"knowledge-base-list-items") #Localizar a class que contém todos os textos
            sleep(2)
            page = navegador.page_source #tirar um print da página pegando o html
            search_area = BeautifulSoup(page, 'html.parser')
            hospedagens = search_area.find_all('div', attrs={'class':'knowledge-base-list-item clearfix ng-scope'})
            
            for hospedagem in hospedagens:
                all = {}
                u = 'https://sac.sefaz.mt.gov.br/citsmart/pages/knowledgeBasePortal/knowledgeBasePortal.load'
                a = hospedagem.find('a', attrs={'ui-sref':'knowledgeBase.knowledge({idKnowledge: knowledge.idBaseConhecimento})'})
                url = u+a['href']
                all['URL'] = url
                
                t = hospedagem.find('span', attrs={'ng-bind-html':'knowledge.titulo'}).get_text()
                all['Titulo'] = t
                
                e = hospedagem.find('div', attrs={'ng-bind-html':'knowledge.conteudoReduzido'}).get_text().strip()
                all['Resumo'] = e
                all_texts.append(all)            
    except Exception as e:
        return e
        
          
#Criar a busca
@app.route('/', methods=['GET'])
def index():
    return render_template('scrap.html')
        
                   
@app.route('/search', methods=['GET','POST' ])
def searched():
    if request.method == 'POST':
        try:
            search = scrapper(request.form['text'].strip().lower())
            for row in range(len(all_texts)):
                books = all_texts[row]
            if search in books:
                data = all_texts[books.index(search)]
                return render_template('output.html', nome = data)
        except:
            return render_template('output.html')
        
        
if __name__=="__main__":
    app.run(port=4000,debug=True)