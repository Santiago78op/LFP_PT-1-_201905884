from Analisis.Lexema import *
from Analisis.Error import *
from Analisis.Token import *


class Lexico:
    
    def __init__(self) -> None:
        self.seccion = ''
        self.estado = 0
        self.conteo = 0
        self.fila = 1
        self.col = 1
        self.prefijo = ''
        self.entrada = list()
        self.flujo = list()
        self.tokens = list()
        self.errores = list()
        self.imgs = list()
        self.img = dict()
        self.contenedor = list()
        self.subcont = list()
        self.reserved = [   
                            'FORMULARIO','TIPO',
                            'VALOR','FONDO',
                            'NOMBRE','VALORES',
                            'EVENTO','etiqueta',
                            'texto','grupo-radio',
                            'grupo-option','boton'
                        ]
        
    
    def escanear(self,entrada):
        self.str_to_list(entrada)    
        while len(self.entrada) > 0:
            if self.getSeparador():
                continue
            elif self.getSimbolo():
                continue
            elif self.getSimboloDoble():
                continue
            elif self.getId():
                tipo = 'Palabra Reservada'
                token = Token(tipo,self.getLexema())
                self.addToken(token)
            elif self.getArreglo():
                token = Token('Arreglo',self.getLexema())
                self.addToken(token)
            elif self.getCadena():
                token = Token('Cadena',self.getLexema())
                self.addToken(token)
            elif self.getNumero():
                token = Token('Numero',self.getLexema())
                self.addToken(token)
            else: #Hay un error léxico
                self.error()
        if len(self.errores) == 0:
            self.imgs.append(self.img)
        
    def str_to_list(self,entrada):     
        chars = list()
        for c in entrada:
            chars.append(c)
        self.entrada = chars
        self.entrada.insert(-1,'#')
        self.flujo = chars
    
    def sigChar(self) -> str:
        return self.entrada[0]
    
    def getLexema(self) -> Lexema:
        inicio = self.col - self.conteo
        lexema = Lexema(self.prefijo,self.fila,self.col)
        self.prefijo = ''
        self.conteo = 0
        return lexema
    
    
    def getId(self):
        self.regresar()         
        while 1:
            if self.estado == 0:
                if self.sigChar().isalpha():
                    self.transicion(1) #F
                else:
                    return False
            elif self.estado == 1:
                reservada = self.prefijo
                reservada = reservada.upper()
                if self.sigChar().isalpha():
                    self.transicion(1) #ORMULARIO
                else:
                    if reservada in self.reserved:
                        if reservada == 'TIPO':
                            self.subcont.append(reservada)
                        elif reservada == 'VALOR':
                            self.subcont.append(reservada)
                        elif reservada == 'FONDO':
                            self.subcont.append(reservada)
                        elif reservada == 'NOMBRE':
                            self.subcont.append(reservada)
                        elif reservada == 'VALORES':
                            self.subcont.append(reservada)
                        elif reservada == 'EVENTO':
                            self.subcont.append(reservada)
                        else:
                            self.seccion = reservada
                        return True
                    else:
                        return False
    
    
    def getArreglo(self) -> bool:
        if self.prefijo:
            return False
        else:
            self.regresar()
            while 1:
                if self.estado == 0:
                    if self.sigChar() == ':':
                        tipo = 'Dos Puntos'
                        self.transicion(1)
                        token = Token(tipo,self.getLexema())
                        self.addToken(token)
                        self.transicion(1)
                    else:
                        return False
                elif self.estado == 1:
                    if self.sigChar() == ' ':
                        self.transicion(1)
                    elif self.sigChar() == '[' or self.sigChar() == '<':
                        self.transicion(2)
                    else:
                        return False
                elif self.estado == 2:
                    c = self.sigChar()
                    if c != ']' and c != '\n' and c != ">":
                        self.transicion(2)
                    elif c == ']' or c == '>':
                        self.transicion(3)
                    else:
                        return False
                elif self.estado == 3:
                    self.subcont.append(self.prefijo)
                    return True
            
    
    def getCadena(self) -> bool:
        self.regresar()
        while 1:
            if self.estado == 0:
                if self.sigChar() == '"':
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                c = self.sigChar()
                if c != '"' and c != '\n':
                    self.transicion(1)
                elif c == '"':
                    self.transicion(2)
                else:
                    return False
            elif self.estado == 2:
                self.subcont.append(self.prefijo)
                return True
                
    
    def getNumero(self) -> bool:
        self.regresar()
        while 1:
            if self.estado == 0:
                if self.sigChar().isdigit():
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                if self.sigChar().isdigit():
                    self.transicion(1)
                elif self.getSeparador():
                    self.subcont.append(self.prefijo)
                    return True
                else:
                    self.subcont.append(self.prefijo)
                    return True
            
    
    def getSimboloDoble(self) -> bool:
        self.regresar()
        tipo = ''
        while 1:
            if self.estado == 0:
                if self.sigChar() == '~':
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                if self.sigChar() == '>':
                    self.transicion(2)
                else:
                    return False
            elif self.estado == 2:
                if self.sigChar() == '>':
                    self.transicion(3)
                else:
                    return False
            elif self.estado == 3:
                tipo = 'Indicador Flecha'
                token = Token(tipo,self.getLexema())
                self.addToken(token)
                return True
            

    def getSimbolo(self) -> bool:
        self.regresar()
        tipo = ''
        while 1:
            if self.estado == 0:
                if self.sigChar() == '[':
                    tipo = 'Corchete Apertura'
                    self.transicion(1)
                    self.contenedor = list()
                elif self.sigChar() == ']':
                    tipo = 'Corchete Cierre'
                    self.transicion(1)
                elif self.sigChar() == '<':
                    tipo = 'Menor'
                    self.transicion(1)
                    self.subcont = list()
                elif self.sigChar() == '>':
                    tipo = 'Mayor'
                    self.transicion(1)
                    self.contenedor.append(self.subcont)
                elif self.sigChar() == '#':
                    tipo = 'Numeral'
                    self.transicion(1)
                    self.img[self.seccion] = self.asignarValor()
                elif self.sigChar() == ',':
                    tipo = 'Coma'
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                token = Token(tipo,self.getLexema())
                self.addToken(token)
                return True
            

    def getSeparador(self) -> bool:
        c = self.sigChar()
        if c == ' ' or c == '\t':
            self.consumir()
            return True
        elif self.sigChar() == '\n':
            self.consumir()
            self.updateCount()
            return True
        else:
            return False
        
    def transicion(self,estado:int):
        self.prefijo += self.consumir()
        self.estado = estado
    
    def consumir(self) -> str:
        self.col += 1
        self.conteo += 1
        return self.flujo.pop(0)

    def updateCount(self):
        self.fila += 1
        self.col = 1
        self.conteo = 0

    def addToken(self,t:Token):
        self.tokens.append(t)
        self.entrada = self.flujo
        self.estado = 0

    def regresar(self):
        self.flujo = self.entrada
        self.estado = 0

    def error(self):
        caracter = self.consumir()
        self.entrada = self.flujo
        nuevaCol = self.col - 1
        err = Error(self.fila,nuevaCol,self.prefijo)
        self.errores.append(err)
        self.estado = 0
        self.prefijo = ''
    
    def asignarValor(self):
        if len(self.contenedor) == 0:
            self.contenedor.append(self.subcont)
        elif len(self.contenedor) == 1 and len(self.subcont) == 1:
            valor = self.subcont.pop()
            self.subcont = list()
            self.contenedor = list()
            return valor
        else:
            valor = self.contenedor
            self.subcont = list()
            self.contenedor = list()
            return valor