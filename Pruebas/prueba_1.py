
form = dict()
form['FORMULARIO']=[['TIPO', ' "etiqueta"', 'VALOR', ' "Apellido:"'], ['TIPO', ' "texto"', 'VALOR', ' "Apellido"', 'FONDO', ' "Ingrese apellido"'],['TIPO', ' "etiqueta"', 'VALOR', ' "Nombre:"'], ['TIPO', ' "texto"', 'VALOR', ' "Nombre"', 'FONDO', ' "Ingrese nombre"'], ['TIPO', ' "grupo-radio"', 'NOMBRE', ' "Sexo"', 'VALORES', " ['Masculino', 'Femenino']"], ['TIPO', ' "grupo-option"', 'NOMBRE', ' "pais"', 'VALORES', " ['Guatemala', 'El Salvador', 'Honduras']"], ['TIPO', ' "boton"', 'VALOR', ' "valor"', 'EVENTO', ' <EVENTO>']]

# form['FORMULARIO']=[['TIPO', ' "etiqueta"', 'VALOR', ' "Nombre:"'], ['TIPO', ' "texto"', 'VALOR', ' "Nombre"', 'FONDO', ' "Ingrese nombre"'], ['TIPO', ' "grupo-radio"', 'NOMBRE', ' "Sexo"', 'VALORES', " ['Masculino', 'Femenino']"], ['TIPO', ' "grupo-option"', 'NOMBRE', ' "pais"', 'VALORES', " ['Guatemala', 'El Salvador', 'Honduras']"], ['TIPO', ' "boton"', 'VALOR', ' "valor"', 'EVENTO', ' <EVENTO>']]---, ['TIPO', ' "grupo-radio"', 'NOMBRE', ' "Sexo"', 'VALORES', " ['Masculino', 'Femenino']"], ['TIPO', ' "grupo-option"', 'NOMBRE', ' "pais"', 'VALORES', " ['Guatemala', 'El Salvador', 'Honduras']"], ['TIPO', ' "boton"', 'VALOR', ' "valor"', 'EVENTO', ' <EVENTO>']

nuevoForm=dict()
lista_contenedor = []
for token in form['FORMULARIO']:
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
                variable_1 = 'selected'
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


jsonp = contenedor

if 'etiquetas' in jsonp:
     etiquetas = jsonp['etiquetas']
if 'textos' in jsonp:
     textos = jsonp['textos']
     
for etiquetado in etiquetas:
    for etiqueta in etiquetado:
        if textos != None:
            for texteado in textos:
                for texto in texteado:
                    if (texto.get('valor')+":") == etiqueta.get('valor') or (texto.get('valor')) == etiqueta.get('valor'):
                        print(etiqueta.get('valor'),texto.get('valor'))


# s = contenedor
# s['tipo'] = 'label'

# print(s['tipo'])        
        



# listOfDicts = [
#      { "name": "Tommy", "age": 20 },
#      { "name": "Markus", "age": 25 },
#      { "name": "Pamela", "age": 27 },
#      { "name": "Richard", "age": 22 }
# ]

# print(next((x for x in listOfDicts if x["etiqueta"]==None), None))

# dic =  {'a' : 1, 'b' : 2, 'c' : 3 , 'd' : 4}
# if 'a' not in dic:
#     print("No hay")
# else:
#     print("Si")
    
#     <
#         tipo: "etiqueta",
#         valor: "Nombre:"
#     >,
# print(nuevoDict_2)

# jsonp = nuevoDict_2['etiqueta']

# for elemento in jsonp:
#     if 'label' == jsonp.get(elemento):
#         print("label")
#     else:
#         print(jsonp.get(elemento))

# <link rel="stylesheet" href="../..{{ url_for('static', filename='css/bootstrap.min.css') }}">
#     <script src="../..{{ url_for('static', filename='js/bootstrap.min.js') }}"> </script>


#!importante
        

# radio = contenedor['grupo-radio']

# valores = radio['valores']


# valores=valores.replace('[','')
# valores=valores.replace(']','')
# valores=valores.replace("'",'')
# valores = valores.split(',')

# nuevalista=[]
# for elemento in valores:
#     elemento = elemento.strip()
#     nuevalista.append(elemento)
# radio['valores'] = nuevalista

# print(radio)

# nuevalista.clear()

    # <section class="Master">
    #     <div class="child">
    #         <h1>Reporte Fomulario</h1>
    #     <section class="child_etiqueta">
    #     {% if etiqueta != None %}
    #         <{{etiqueta.get('tipo')}}>{{etiqueta.get('valor')}}</{{etiqueta.get('tipo')}}>
    #     {% endif %}
    #     </section>
    #     <section class="child_texto">
    #     {% if texto != None %}
    #         <{{texto.get('tipo')}} type="text" placeholder="{{texto.get('fondo')}}" >
    #     {% endif %}
    #     </section>
    #     <section class="child_grupo_radio">
    #         {% if grupo_radio != None %}
    #         <p>{{grupo_radio.get('nombre')}}:</p>
    #             {% for elemento in grupo_radio.get('valores')%}
    #             <div>
    #                 <input type="{{grupo_radio.get('tipo')}}" name="{{grupo_radio.get('nombre')}}" value="{{elemento}}">
    #                 <label for="{{elemento}}">{{elemento}}</label>
    #             </div> 
    #             {% endfor %}
    #         {% endif %}
    #     </section>
    #     <section class="grupo_option">
    #         {% if grupo_option != None %}
    #             <{{grupo_option.get('tipo')}}>
    #                 <option selected disabled>{{grupo_option.get('nombre')}}</option>
    #                 {% for element in grupo_option.get('valores') %}
    #                     <option value="{{element}}">{{element}}</option>
    #                 {% endfor %}    
    #             </{{grupo_option.get('tipo')}}>
    #         {% endif %}
    #     </section> 
    #     <section class="boton">
    #         {% if boton != None %}
    #             <{{boton.get('tipo')}} name="button">{{boton.get('valor')}}</{{boton.get('tipo')}}>
    #         {% endif %}
    #     </section> 
    #     </div>
    # </section>
    
'''
    formulario ~>> [
    <
        tipo: "etiqueta",
        valor: "Nombre:"
    >,
    <
        tipo: "texto",
        valor: "Nombre",
        fondo: "Ingrese nombre"
    >,
    <
        tipo: "grupo-radio",
        nombre: "Sexo",
        valores: ['Masculino', 'Femenino']

    >,
    <
        tipo: "grupo-option",
        nombre: "pais",
        valores: ['Guatemala', 'El Salvador', 'Honduras']
    >,
    <
        tipo: "boton",
        valor: "valor",
        evento: <EVENTO>
    >
]

'''
# html, body {
#     margin:0;
#     height:100%;
# }

# body{
#     background-image: url("..//img//fondo_body.jpg");   
#     background-size: cover;
#     background-repeat: no-repeat;
#     background-position: center;
#     margin:0;
#     width:100%;
#     height:100%;
# }

# .main-section{
#     margin:0 auto;
#     margin-top:15%;
#     padding: 0;
# }

# .modal-content{
#     background-color: #3b4652;
#     opacity: .85;
#     padding: 0 20px;
#     box-shadow: 0px 0px 3px #848484;
# }

# .form-group input{
#     height: 42px;
#     font-size: 18px;
#     border: 1px solid black;
#     padding-left: 54px;
#     border-radius: 5px;
# }

# .form-group::before{
#     font-family: "Font Awesome\ 5 Free";
#     position: absolute;
#     left: 28px;
#     font-size: 22px;
#     padding-top:4px;
# }

# .form-group#user-group::before{
#     content: "\f007";
# }

# .form-group#contrasena-group::before{
#     content: "\f023";
# }

# .form-check {
#     margin:0 auto;
#     margin-top:5%;
#     padding: 0;
# }

# .form-select {
#     margin:0 auto;
#     margin-top:5%;
#     padding: 5;
# }


# .btn-primary{
#     margin:0 auto;
#     margin-top:5%;
#     margin-bottom: 10px;
# }

# cadena = " "
# # Comprobar con la forma idiomática
# if not cadena:
# 	print("La cadena está vacía")
# else:
#     print("La cadena NO está vacía")

