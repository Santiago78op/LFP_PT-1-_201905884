from json import tool
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os

#Flask Components
import requests
import json

#Directorios
from Analisis import Lexico

class GUI():
    
    
    def __init__(self) -> None:
        raiz = Tk()
        raiz.title("Reading Form")
        raiz.geometry("835x450")
        raiz.rowconfigure(0, weight=1)
        raiz.columnconfigure(0, weight=1)
        
        
        
        mainframe = ttk.Frame(raiz)
        mainframe.grid(row=0, column=0, sticky=NSEW)
        mainframe.columnconfigure(1, weight=1)
        mainframe.rowconfigure(2, weight=1)
 

        
        #contenedor botones Superior
        panel_superior = ttk.Frame(mainframe, borderwidth=5, relief="ridge")
        panel_superior.grid(row=1, column=1, sticky=NSEW)
        panel_superior.columnconfigure(1, weight=1)
        panel_superior.columnconfigure(2, weight=1)
        panel_superior.columnconfigure(3, weight=1)
       
       
        Button_Cargar = ttk.Button(panel_superior,text="Cargar Archivo", command=self.cargar_archivo)
        Button_Cargar.grid(row=0, column=1, sticky=NSEW)

        
        Button_Analizar = ttk.Button(panel_superior,text="Analizar", command=self.readfile)
        Button_Analizar.grid(row=0, column=2, sticky=NSEW)

        def checkifireland():
            accion = combobox1.get()
            ruta = ''
            if accion == "Formulario":
                ruta = 'app\\Reports\\Forms\\forms.html'
                os.startfile(ruta)
            elif accion == "Reporte Errores":
                ruta = 'app\\Reports\\Errors\\errores.html'
                os.startfile(ruta)
            elif accion == "Reporte Tokens":
                ruta = 'app\\Reports\\Tokens\\tokens.html'
                os.startfile(ruta)
            
        opcion=tk.StringVar()
        OptionList = [
        "Formulario",
        "Reporte Tokens",
        "Reporte Errores",
        "Manual Usuario",
        "Manual Técnico"
        ] 
        combobox1=ttk.Combobox(panel_superior,state="readonly",text="-- Select Team --", 
                                  width=10, 
                                  textvariable=opcion, 
                                  values=OptionList)
        combobox1.current(0)
        combobox1.set("Reportes")
        combobox1.grid(row=0, column=3, sticky=NSEW)
        
        
        Button_Visualizar = ttk.Button(panel_superior,text="Generar", command=checkifireland)
        Button_Visualizar.grid(row=0, column=4, sticky=NSEW)


        #contenedor Text Medio
        panel_medio = ttk.Frame(mainframe, borderwidth=5, relief="ridge")
        panel_medio.grid(row=2, column=1, sticky=NSEW)
        panel_medio.rowconfigure(1,weight=1)
        panel_medio.columnconfigure(1,weight=1)
        

        def take_input():
            entrada = ''
            file = open('app//Data//form.txt','r')
            for line in file:
                entrada += line
            file.close()
            textEditor.insert(END, entrada)

        def getTextInput():
            result=textEditor.get("1.0","end")
            nueva_ruta = 'app//Data//form.txt'
            archivo = open(f'{nueva_ruta}', 'w')
            archivo.write(result)
            self.route = 'app//Data//form.txt'
            
        def clearToTextInput():
            textEditor.delete("1.0","end")
            
        textEditor = Text(panel_medio)
        textEditor.pack(expand=True)
        textEditor.grid(row=1,column=1,sticky=NSEW)

        
        
        #Contendor Inferior
        panel_inferior = ttk.Frame(mainframe, borderwidth=5, relief="ridge")
        panel_inferior.columnconfigure(1, weight=1)
        panel_inferior.columnconfigure(2, weight=1)
        panel_inferior.columnconfigure(3, weight=1)
        panel_inferior.grid(row=3, column=1, sticky=NSEW)

        buttonForm = ttk.Button(panel_inferior,text="Form", command=take_input)
        buttonForm.grid(row=0, column=1, sticky=NSEW)
        
        buttonReescribir = ttk.Button(panel_inferior,text="Modificar Form", command=getTextInput)
        buttonReescribir.grid(row=0, column=2, sticky=NSEW)
        
        clear = ttk.Button(panel_inferior,text="Limpiar", command=clearToTextInput)
        clear.grid(row=0, column=3, sticky=NSEW)

        raiz.mainloop()
    

    
    def cargar_archivo(self,*args):
        fileChooser = Tk()
        fileChooser.withdraw()
        self.route = askopenfilename()
        fileChooser.destroy()
        print(self.route)
    
    
    def readfile(self,*args):
        entrada = ''
        tokens = dict()
        errores = dict()
        try:
            file = open(self.route,'r')
            for line in file:
                entrada += line
            file.close()
            self.take_output(entrada)
            self.lex = Lexico.Lexico()
            self.lex.escanear(entrada)
            if len(self.lex.errores) == 0:
                for img in self.lex.imgs:
                    form =self.convertDict(img)
                    print(json.dumps(form, indent=4))
                    self.sendFom(form)
                lista_tokens = list()
                for elemento in self.lex.tokens:
                    id = elemento.id
                    lex = elemento.valor
                    valor = lex.valor
                    fila = lex.fila
                    columna = lex.col
                    lista_tokens.append([id,valor,fila,columna])   
                tokens['tokens']=lista_tokens
                print(json.dumps(tokens, indent=4))
                self.sendTokens(tokens)
                lista_tokens.clear()
            else:
                print('\t---ERRORES---')
                lista_errores = list()
                for e in self.lex.errores:
                    print(">",e.toString(),sep=" ")
                    Error = 'Error'
                    fil = e.fila
                    col = e.col
                    caracter = e.caracter
                    lista_errores.append([Error,fil,col,caracter])   
                errores['errores']=lista_errores      
                print(json.dumps(errores, indent=4))         
                self.sendErrores(errores)
                lista_errores.clear()
        except FileNotFoundError:
            print('> No se encontró ningun archivo')
            
    
    def take_output(self,contenido):
        nueva_ruta = 'app//Data//form.txt'
        archivo = open(f'{nueva_ruta}', 'w')
        archivo.write(contenido)
        
    def convertDict(self,imgs):
        nuevoForm=dict()
        lista_contenedor = []
        for token in imgs['FORMULARIO']:
            lista = []
            for element in token:
                element = element.strip()
                element = element.replace('"','')
                element = element.replace('<','')
                element = element.replace('>','')
                element = element.lower()
                lista.append(element)  
            lista_contenedor.append(lista)
            nuevoForm['FORMULARIO']=lista_contenedor

        tipos = dict()
        contenedor = dict()
        lista_etiquetas=list()
        lista_textos=list()
        lista_grupo_radios=list()
        lista_grupo_options=list()
        lista_botons = list()
        for token in nuevoForm['FORMULARIO']:
            nuevoToken = token 
            if ('etiqueta') in nuevoToken:
                longitud = len(nuevoToken)/2       
                for i in range(int(longitud)):
                    variable = nuevoToken.pop(0)
                    if variable == 'tipo':
                        variable_1 = nuevoToken.pop(0)
                        variable_1 = 'label'
                        tipos[variable]=variable_1
                                    
                    else:
                        variable_1 = nuevoToken.pop(0)
                        tipos[variable]=variable_1
                        
                lista_etiquetas.append([tipos])
                tipos=dict()
            elif ('texto') in nuevoToken:
                longitud = len(nuevoToken)/2
                for i in range(int(longitud)):
                    variable = nuevoToken.pop(0)
                    if variable == 'tipo':
                        variable_1 = nuevoToken.pop(0)
                        variable_1 = 'input'
                        tipos[variable]=variable_1
                        
                    else:
                        variable_1 = nuevoToken.pop(0)
                        tipos[variable]=variable_1
                        
                lista_textos.append([tipos])
                tipos=dict()   
            elif ('grupo-radio') in nuevoToken:
                longitud = len(nuevoToken)/2
                nuevalista=[]
                for i in range(int(longitud)):
                    variable = nuevoToken.pop(0)
                    if variable == 'tipo':
                        variable_1 = nuevoToken.pop(0)
                        variable_1 = 'radio'
                        tipos[variable]=variable_1
                        
                    elif variable == 'valores':
                        variable_1 = nuevoToken.pop(0)
                        variable_1=variable_1.replace('[','')
                        variable_1=variable_1.replace(']','')
                        variable_1=variable_1.replace("'",'')
                        variable_1 = variable_1.split(',')

                        for data in variable_1:
                            data = data.strip()
                            nuevalista.append(data)
                        tipos[variable]=nuevalista
                        
                    else:
                        variable_1 = nuevoToken.pop(0)
                        tipos[variable]=variable_1
                
                lista_grupo_radios.append([tipos])
                tipos=dict()     

            elif ('grupo-option') in nuevoToken:
                longitud = len(nuevoToken)/2
                nuevalista=[]
                for i in range(int(longitud)):
                    variable = nuevoToken.pop(0)
                    if variable == 'tipo':
                        variable_1 = nuevoToken.pop(0)
                        variable_1 = 'select'
                        tipos[variable]=variable_1
                    elif variable == 'valores':
                        variable_1 = nuevoToken.pop(0)
                        variable_1=variable_1.replace('[','')
                        variable_1=variable_1.replace(']','')
                        variable_1=variable_1.replace("'",'')
                        variable_1 = variable_1.split(',')

                        for data in variable_1:
                            data = data.strip()
                            nuevalista.append(data)
                        tipos[variable]=nuevalista
                        
                    else:
                        variable_1 = nuevoToken.pop(0)
                        tipos[variable]=variable_1
                
                lista_grupo_options.append([tipos])
                tipos=dict()     

            elif ('boton') in nuevoToken:
                longitud = len(nuevoToken)/2
                for i in range(int(longitud)):
                    variable = nuevoToken.pop(0)
                    if variable == 'tipo':
                        variable_1 = nuevoToken.pop(0)
                        variable_1 = 'button'
                        tipos[variable]=variable_1
                    else:
                        variable_1 = nuevoToken.pop(0)
                        tipos[variable]=variable_1        
                lista_botons.append([tipos])
                tipos=dict()  
                
        #Contenedores
        contenedor['etiquetas']=lista_etiquetas
        contenedor['textos']=lista_textos
        contenedor['grupo_radios']=lista_grupo_radios
        contenedor['grupo_options']=lista_grupo_options
        contenedor['botons']=lista_botons
        return contenedor
        

    def sendFom(self,img):
        r = requests.post('http://127.0.0.1:5000/postForm', json=img)
        print('> Server devolvio: ',r.status_code)
        

    def sendTokens(self,tokens):
        r = requests.post('http://127.0.0.1:5000/postTokens',json=tokens)
        print('> Server devolvio: ',r.status_code)
        
    def sendErrores(self,errores):
        requests.post('http://127.0.0.1:5000/postErrores',json=errores)





    
        
        
    
        