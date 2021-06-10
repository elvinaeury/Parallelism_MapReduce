#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 18:24:56 2020

@author: prenaudin, elvinagovendasamy
"""
# Packages
from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np

class PageRank(MRJob):
    #Nombre de noeud dans le graphe (= nombre de pages web différentes) 
    total_nodes = 0
    #Dictionnaire de contrôle 
    dico_nj = {}
    #Dictionnaire stockant les pageranks de chaque page pour pouvoir les écrire dans un fichier .txt à la fin des itérations.
    #plus lisible que dans la console
    dico_pagerank = {}
            
    
    #1. Initialisation à 0 du nombre de voisin de chaque noeud du graphe
    #2. Récupération du nombre total de noeud dans le graphe
    #3. Envoi des couples de noeuds ayant un lien entrant (in) ou sortant (out) de l'un vers l'autre  
    def mapper_adjacent(self, _, line):
        (i, j) = line.split()
        liste_nodes = np.unique(i)
        liste_nodes2 = np.unique(j)
        for identifiant in liste_nodes:
            PageRank.dico_nj.setdefault(identifiant,0)
        for identifiant in liste_nodes2:
            PageRank.dico_nj.setdefault(identifiant,0)
        PageRank.total_nodes = len(PageRank.dico_nj) #ça marche
        yield 'in', (j,i)
        yield 'out', (i,j)


    #1. Initialisation du pagerank initial pour chaque noeud du graphe
    #2. Calcul du nombre de pages citées par un noeud i  
    #3. Envoi des noeuds i et des pages j qu'ils citent
    def reducer_adjacent(self, label , values):
        if label == 'in':
            for val in values:
                j,i = val
                PageRank.dico_pagerank[j] = 1/PageRank.total_nodes
        else:
            for val in values:
                i,j = val
                PageRank.dico_nj[i]+=1
                PageRank.dico_pagerank[i] = 1/PageRank.total_nodes
                yield i,j


    # Création de la liste d'adjacence des noeuds i (pages citées par le noeud i)
    # On yield aussi le pagerank initial des noeuds i pour la structure de l'algorithme 
    def reducer_adjacent2(self,i,j):
        yield i,(j, 1/PageRank.total_nodes)
        
        
    #1. Pour chaque noeud i, on yield sa liste d'adjacence et son pagerank
    #2. Chaque pages j de la liste d'adjacence du noeud i reçoit sa part de la masse pagerank du noeud i
    def mapper_PageRank(self, i, node):
            
        adjacent_list, pagerank = node
        total_neighbours=len(adjacent_list)
        
        p=pagerank/total_neighbours

        yield i, ('node',node)

        for l in adjacent_list: # yields each neighbour l, and the pagerank of i/nb_neighbors
            yield l, ('pagerank', p) # Pass PageRank mass to neighbors, p is float
                    
        
    #1. Récupère la structure de graphe à travers les 'nodes'
    #2. Calcul le nouveau pagerank de chaque noeud  
    #3. Enregistre le nouveau pagerank de chaque noeud dans le dictionnaire dico_pagerank
    #4. yield pour chaque noeud sa liste d'adjacence et son nouveau pagerank pour pouvoir repasser dans le mapper_PageRank      
    def reducer_PageRank(self, n_id , values):    
            
            c = 0.15 # provided
            sum_p = 0
            node = ([], sum_p)
            
            for val in values:
                label, content = val

                # If it's a node, save the node
                if label == 'node':
                    node = content

                # If it's a pagerank, sum the pagerank
                elif label == 'pagerank':
                    sum_p += content

            #update the pagerank
            new_pagerank = c/PageRank.total_nodes + (1-c)*sum_p

            #mettre à jour les pageranks dans le dico
            PageRank.dico_pagerank[n_id] = new_pagerank

            #Update the node with the new pagerank
            if node[0] != []:
                node = (node[0],new_pagerank)
                yield(n_id, node)   


    def steps(self):
        return [MRStep(mapper=self.mapper_adjacent,
                       reducer=self.reducer_adjacent),
                MRStep(reducer=self.reducer_adjacent2),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_PageRank),
        ]
        

if __name__ == '__main__':
    PageRank.run()
    somme_pagerank = 0
    for val in PageRank.dico_pagerank:
        somme_pagerank += PageRank.dico_pagerank[val]
    
    #Ecriture du fichier de vérfication
    with open ('Pageranks_results.txt','w') as g:
        g.write(f'Nombre de pages:  {PageRank.total_nodes} \n')
        g.write(f'Somme des Pageranks:  {somme_pagerank} \n')
        for k,v in sorted(PageRank.dico_pagerank.items(), key=lambda x : x[1], reverse = True):
            g.write(f'{k}:  {v} \n')
    
    
