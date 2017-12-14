# -*- coding: utf-8 -*-
# Programa que implementa el metodo de aprendizaje por arbol de decision
# Realizado por Ricardo Jimenez Cruz

from sklearn import tree
import graphviz
import json

CORPUS = 'training_data.json'

data_set = json.load(open(CORPUS))

data = data_set.get('training').get('data')
target = data_set.get('training').get('target')
feature_names = data_set.get('training').get('feature_names')
target_names = data_set.get('training').get('target_names')

clasificador = tree.DecisionTreeClassifier()
clasificador  = clasificador.fit(data, target)


dot_data = tree.export_graphviz(clasificador, out_file=None,
                         feature_names=feature_names,
                         class_names=target_names,  
                         filled=True, rounded=True,
                         special_characters=True)
graph = graphviz.Source(dot_data)
graph.render("Arbol")
