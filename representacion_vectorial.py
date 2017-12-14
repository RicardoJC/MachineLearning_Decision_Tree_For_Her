# -*- coding: utf-8 -*-
# Programa que genera representaciones vectoriales de los documentos (tweets)
# usando como medida tf-idf
# Realizado por Ricardo Jimenez Cruz

from __future__ import division
import xml.etree.ElementTree as ET
import re
import sys
import math
import json
import time

reload(sys)
sys.setdefaultencoding('utf8')


def preprocessForText(text):
    return re.sub(u'[^a-zA-Z0-9ñÑÁáÉéÍíÓóÚú ]','',text.lower())

def tf(tweet,collocation):
    tweetNoString = re.subn(collocation,'',preprocessForText(tweet))
    total = len(tweetNoString[0].split())+tweetNoString[1]
    return tweetNoString[1]/total

def dtf(collocation):
    return sum(1 for tweet  in root.iter('tweet') if re.subn(collocation,'',preprocessForText(tweet.find('texto').text))[1])

def idf(collocation):
    return math.log(len(root) / (1+(dtf(collocation))))                   # Mas uno para evitar el denominador con 0

def tfidf(tweet,collocation):
    return tf(tweet,collocation) * idf(collocation)



inicio = time.time()
# Nombre del archivo resultado
TRAINING_DATA = 'training_data.json'



# Regex
# Discriminacion utilitaria  Definicion de las Features
# Hogar
regex_u_1 = re.compile('perdio la cocina')
# Rol de cuidadora
regex_u_2 = re.compile('mujer multiusos|vieja multiusos')
# Servicio
regex_u_3 = re.compile('mujer sirve para|vieja sirve para|puta sirve para')


# Discriminacion encubierta  Definicion de las Features
# Descalificacion
regex_e_1 = re.compile('tenias que ser puta|tenias que ser mujer|tenias que ser vieja')
# Forma de verse
regex_e_2 = re.compile('parece hombre|parece mujer|parece vieja|pareces hombre|pareces mujer|parecer vieja')
# Insinuacion
regex_e_3 = re.compile('andar de puta|pareces puta|parece puta')


# Discriminacion coercitiva  Definicion de las Features
# Violacion normalizada
regex_co_1 = re.compile('se la metio|se la cogio')
# Represion
regex_co_2 = re.compile('neofeminazi|neofeminista|neofeminazis|neofeministas')
# Inferioridad
regex_co_3 = re.compile('por ser mujer|por ser vieja')

# Discriminacion de crisis  Definicion de las Features
# Control
regex_cr_1 = re.compile('matriarcado opresor')
# Exclusion
regex_cr_2 = re.compile('cosa de hombres|cosas de hombres')
# Victimismo
regex_cr_3 = re.compile('estar en sus dias|esta en sus dias')



# Nombre del corpus etiquetado para el entrenamiento
CORPUS = 'formateado.xml'



# Se abre un archivo para su escritura
file_data = open(TRAINING_DATA,'w+')

data=[]
target =list()
# Nombres para cada tipo de definicion de Features
feature_names = ['Hogar','Rol de cuidadora','Servicio','Descalificacion','Forma de verse','Insinuacion','Violacion normalizada','Represion','Inferioridad','Control','Exclusion','Victimismo']
# Clasificaciones para cada una de los tipos de discriminacion
target_names = dict([('Utilitaria',0),('Encubierta',1),('Coercitiva',2),('Crisis',3)])


tree = ET.parse(CORPUS)
root = tree.getroot()

sys.stdout.write('Generando representacion vectorial')
for tweet in root.iter('tweet'):
    sys.stdout.write('.')
    sys.stdout.flush()
    target.append(target_names[tweet.attrib['discriminacion']])
    data.append([tfidf(tweet.find('texto').text,regex_u_1),tfidf(tweet.find('texto').text,regex_u_2),tfidf(tweet.find('texto').text,regex_u_3),
    tfidf(tweet.find('texto').text,regex_e_1),tfidf(tweet.find('texto').text,regex_e_2),tfidf(tweet.find('texto').text,regex_e_3),
    tfidf(tweet.find('texto').text,regex_co_1),tfidf(tweet.find('texto').text,regex_co_2),tfidf(tweet.find('texto').text,regex_co_3),
    tfidf(tweet.find('texto').text,regex_cr_1),tfidf(tweet.find('texto').text,regex_cr_2),tfidf(tweet.find('texto').text,regex_cr_3)])



file_data.write(json.dumps({'training':{'data':data,'target':target,'feature_names':feature_names,'target_names':['Utilitaria','Encubierta','Coercitiva','Crisis']}}))


file_data.close()



fin = time.time()

total = (fin-inicio)/60

print '\nEl programa ha tardado %f segundos' % total
