# -*- coding: utf-8 -*-
# Input: Se tiene una base de datos MongoDB con una coleccion llamada sismos
# Output: Corpus etiquetado para el entrenamiento
# Este programa genera un corpus para realizar el entrenamiento de maquina
# Para esto se procesa el texto:
# - - - Se quitan url, emojis, se pasa a minusculas y se lematiza el texto
# Se buscan tokens y colocaciones obtenidas de una hipotesis
# Los tweets encontrados seran asignados a un corpus etiquetado con XML
# Las clasificaciones de Discriminacion son parte del estudio de Luis Bonino
# acerca de los micromachismos
# Creado por Ricardo Jimenez Cruz


import xml.etree.ElementTree as ElementTree
import snowballstemmer as Stemmer
from pymongo import MongoClient
import re
import sys
import time


reload(sys)
sys.setdefaultencoding('utf8')


# ----------------------     Funciones      ----------------------

def tagger(tweet,root,pattern,string,discrimination):                           # Funcion que etiqueta el corpus
    if pattern.search(string.lower()):                                          # Recibe un diccionario tweet
        #cli = MongoClient('mongodb://localhost/tree')
        #db2 = cli.tree
        #db2.tree.insert(tweet)
        print 'Se agrego discriminacion '+discrimination                        # Un objeto root de ElementTree
        tw = ElementTree.SubElement(root,'tweet')                               # El regex compile
        texto = ElementTree.SubElement(tw,'texto')                              # Cadena de texto largo o normal segun el caso
        hashtags = ElementTree.SubElement(tw,'hashtags')                        # Discrimination el tipo de discriminacion
        menciones = ElementTree.SubElement(tw,'menciones')

        tw.set('id',str(tweet['id']))
        tw.set('discriminacion',discrimination)
        tw.set('retweets',str(tweet['retweet_count']))
        tw.set('favoritos',str(tweet['favorite_count']))

        texto.text = string

        if len(tweet['entities']['user_mentions']):
            aux_users = ''
            for user in tweet['entities']['user_mentions']:
                aux_users = aux_users+'@'+user['screen_name']
            hashtags.text = aux_users
        if len(tweet['entities']['hashtags']):
            aux_hashtags = ''
            for tag in tweet['entities']['hashtags']:
                aux_hashtags = aux_hashtags +'#'+tag['text']
            menciones.text = aux_hashtags

# ---------------------- Programa principal ----------------------
# Tiempo de inicio
inicio = time.time()

# Regex
# Discriminacion utilitaria
regex_u = re.compile('perdio la cocina|mujer multiusos|vieja multiusos|mujer sirve para|vieja sirve para|puta sirve para')
# Discriminacion encubierta
regex_e = re.compile('tenias que ser puta|tenias que ser mujer|tenias que ser vieja|parece hombre|parece mujer|parece vieja|pareces hombre|pareces mujer|parecer vieja|andar de puta')
# Discriminacion coercitiva
regex_co = re.compile('se la metio|se la cogio|neofeminazi|neofeminista|neofeminazis|neofeministas|por ser mujer|por ser vieja')
# Discriminacion de crisis
regex_cr = re.compile('matriarcado opresor|cosa de hombres|cosas de hombres|estar en sus dias|esta en sus dias')

MONGO_HOST = 'mongodb://localhost/sismos'                                       # Nombre de la Coleccion y su localizacion
client = MongoClient(MONGO_HOST)
db = client.sismos


root = ElementTree.Element('tweets')                                            # La raiz del xml

for i,tweet in enumerate(db.sismos.find({})):                                   # Iterar toda la coleccion
    print 'Se han procesado %d tweets' % i
    if not tweet['truncated']:                                                  # Buscar textos truncados
        tagger(tweet,root,regex_u,tweet['text'],'Utilitaria')                   # Agrega una entrada al XML con discriminacion Utilitaria
        tagger(tweet,root,regex_e,tweet['text'],'Encubierta')                   # Agrega una entrada al XML con discriminacion Encubierta
        tagger(tweet,root,regex_co,tweet['text'],'Coercitiva')                  # Agrega una entrada al XML con discriminacion Coercitiva
        tagger(tweet,root,regex_cr,tweet['text'],'Crisis')                      # Agrega una entrada al XML con discriminacion Crisis
    else:
        tagger(tweet,root,regex_u,tweet['extended_tweet']['full_text'],'Utilitaria')
        tagger(tweet,root,regex_e,tweet['extended_tweet']['full_text'],'Encubierta')
        tagger(tweet,root,regex_co,tweet['extended_tweet']['full_text'],'Coercitiva')
        tagger(tweet,root,regex_cr,tweet['extended_tweet']['full_text'],'Crisis')


xml = ElementTree.ElementTree(root)                                             # Asignar el root element tree a xml
xml.write('discriminacion.xml',encoding='utf-8',xml_declaration=True)           # Creacion del corpus etiquetado

fin = time.time()
procesamiento = fin - inicio
print 'El programa se tardo %f segundos' % procesamiento
