from flask import Flask, request, Response
from flask import render_template
import pathlib


#app = raiz
app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)
    

@app.route('/')
def index():
    return '<h1>Hola Mundo!</h1>'


@app.route('/postForm',methods=['POST'])
def start():
    json = request.json
    
    if 'etiquetas' not in json:
        etiquetas = None
    else:
        etiquetas = json['etiquetas']

    
    if 'textos' not in json:
        textos = None
    else:
        textos = json['textos']

    
    if 'grupo_radios' not in json:
        grupo_radios = None
    else:
        grupo_radios = json['grupo_radios']


    if 'grupo_options' not in json:
        grupo_options = None
    else:
        grupo_options = json['grupo_options']
    

    if 'botons' not in json:
        botons = None
    else:
        botons = json['botons']


    JsonImg = {
        'etiquetas':etiquetas,
        'textos':textos,
        'grupo_radios':grupo_radios,
        'grupo_options':grupo_options,
        'botons':botons
        }    

    #Hacer un dict/json que tenga los datos de la tabla a crear
   
    saveHtmlForm('forms',render_template('Form.html',**JsonImg))
    return Response()

def saveHtmlForm(filtro,html):
    pathlib.Path(f'Reports/Forms').mkdir(parents=True,exist_ok=True)
    with open(f'Reports/Forms/{filtro}.html','w') as f:
        f.write(html)
        f.close
    
@app.route('/postTokens',methods=['POST'])
def link():
    
    json = request.json
    lista = json['tokens']
    
    
    JsonImg = {
        'lista':lista
        }    

    #Hacer un dict/json que tenga los datos de la tabla a crear
    saveHtmlTokens('tokens',render_template('Tokens.html',**JsonImg))

    return Response()

def saveHtmlTokens(filtro,html):
    pathlib.Path(f'Reports/Tokens').mkdir(parents=True,exist_ok=True)
    with open(f'Reports/Tokens/{filtro}.html','w') as f:
        f.write(html)
        f.close


@app.route('/postErrores',methods=['POST'])
def end():
    
    json = request.json
    lista = json['errores']
    
    
    JsonImg = {
        'lista':lista
        }    

    #Hacer un dict/json que tenga los datos de la tabla a crear
    saveHtmlErrors('errores',render_template('Errores.html',**JsonImg))

    return Response()

def saveHtmlErrors(filtro,html):
    pathlib.Path(f'Reports/Errors').mkdir(parents=True,exist_ok=True)
    with open(f'Reports/Errors/{filtro}.html','w') as f:
        f.write(html)
        f.close