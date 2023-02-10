import os
import requests
from flask import Flask, flash, request, redirect, url_for, session, render_template, send_from_directory, abort
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import warnings
warnings.filterwarnings(action='ignore')
from beckendSearch import *


app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'

MAX_SIZE = 15
        
#Rota principal da consulta, ao realizar o get é chamada a função scraper() que preenche a lista vazia.
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        all_texts.clear()
        processar_pagina()
        return render_template('scrap.html')

artigos = []       
#rota de pesquisa, retorna os dados de url, titulo e resumo encontrados para os termos buscados na pesquisa                  
@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        search = request.form['text'].strip().lower()
        #Acessar os termos relacionados e colocar na pasta artigos
        for item in all_texts:
            if search and search in item.get('Titulo').lower():
                artigos.append(item)       
        if artigos:
            return render_template('output.html', nome=artigos)
                  
        
if __name__=="__main__":
    app.run(port=4000,debug=True)