#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:35:11 2020

@author: prenaudin, elvinagovendasamy
"""

#Packages
from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np


class PageRank(MRJob):
    
    #cf version 1 
    total_nodes = 0
    dico_nj = {}
    dico_pagerank = {}

    #Permet de stocker la part de masse perdue à cause des pages qui ne citent personne pour la redistribuer à l'ensemble du graphe
    mass_loss = 0
    #Stocke toutes les pages i qui citent au moins une page j
    dico_i = {}
    #Stocke toutes les pages j qui sont au moins citées une fois par une page i
    dico_j = {}
    

    #1. Même chose que la version précédente 
    #2. On stocke toutes les pages qui citent et toutes les pages citées dans les dicos 'dico_i' et 'dico_j' respectivement.
    def mapper_adjacent(self, _, line):
        (i, j) = line.split()
        liste_nodes = np.unique(i)
        liste_nodes2 = np.unique(j)
        for identifiant in liste_nodes:
            PageRank.dico_nj.setdefault(identifiant,0)
            PageRank.dico_i.setdefault(identifiant,0)
        for identifiant in liste_nodes2:
            PageRank.dico_nj.setdefault(identifiant,0)
            PageRank.dico_j.setdefault(identifiant,0)
        PageRank.total_nodes = len(PageRank.dico_nj)
        yield 'in', (j,i)
        yield 'out', (i,j)

    #1. On sauvegarde les pages qui sont citées mais qui ne citent personnes pour pouvoir redistribuer leur masse
    #2. Même chose qu'avant
    #3. On yield les pages qui ne citent personne avec une liste vide comme liste d'adjacence   
    def reducer_adjacent(self, label , values):
        PageRank.pages_no_out = np.setdiff1d(list(PageRank.dico_j.keys()), list(PageRank.dico_i.keys()))
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
            for page in PageRank.pages_no_out:
                yield page, []
        

    # Même chose qu'avant     
    def reducer_adjacent2(self,i,j):
        yield i,(j, 1/PageRank.total_nodes)        
    
    #1. yield le pagerank des pages qui ne citent personne pour pouvoir le récupérer et le redistribuer
    #2. yield toutes les pages avec leur liste d'adjacence et leur pagerank (même les pages qui ne citent personne car leur pagerank
    # doit être mis à jour lui aussi)  
    def mapper_PageRank(self, i, node):
            
        adjacent_list, pagerank = node
        total_neighbours=len(adjacent_list) 

        #pour traiter les pages qui ne citent personne (mass_loss)
        if adjacent_list[0] == []:
            yield 'mass_loss', pagerank               
        
        yield i, node
            

    #1. Enregistre la valeur totale de la masse perdue
    #2. Pour chaque noeud i on yield sa liste d'adjacence et son pagerank
    #3. Chaque pages j de la liste d'adjacence du noeud i reçoit sa part de la masse pagerank du noeud i 
    # (si la liste d'ajacence est vide on ne fait rien, il n'y a pas de masse à distribuer, elle a été stockée dans mass_loss)                   
    def reducer_int(self, key, value):
        if key == 'mass_loss':
            PageRank.mass_loss = sum(value)
        else:
            for val in value:
                adjacent_list, pagerank = val
                total_neighbours=len(adjacent_list)
                
                p=pagerank/total_neighbours # N.PageRank/|N.AdjacencyList|
                
                yield key, ('node',val)
                
                for l in adjacent_list: # yields each neighbour l, and the pagerank of i/nb_neighbors
                    if l != [] : 
                        yield l, ('pagerank', p) # Pass PageRank mass to neighbors, p is float
        

    #1. Récupère la structure de graphe à travers les 'nodes'
    #2. Calcul le nouveau pagerank de chaque noeud (en prenant en compte la masse perdue)
    #3. Enregistre le nouveau pagerank de chaque noeud dans le dictionnaire dico_pagerank
    #4. yield pour chaque noeud sa liste d'adjacence et son nouveau pagerank pour pouvoir repasser dans le mapper_PageRank 
    # et le reducer_int    
    def reducer_PageRank(self, n_id , values):    

            mass_loss = PageRank.mass_loss/PageRank.total_nodes
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
            new_pagerank = c/PageRank.total_nodes + (1-c)*(sum_p + mass_loss)

            #mettre à jour les pageranks dans dico
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
                       reducer=self.reducer_int),
                MRStep(reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_int),
                MRStep(reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                      reducer=self.reducer_int),
                MRStep(reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                        reducer=self.reducer_int),
                MRStep(reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_int),
                MRStep(reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_int),
                MRStep(reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_int),
                MRStep(reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_int),
                MRStep(reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                       reducer=self.reducer_int),
                MRStep(reducer=self.reducer_PageRank),
                MRStep(mapper=self.mapper_PageRank,
                      reducer=self.reducer_int),
                MRStep(reducer=self.reducer_PageRank),
        ]
        

if __name__ == '__main__':
    PageRank.run()
    somme_pagerank = 0
    for val in PageRank.dico_pagerank:
        somme_pagerank += PageRank.dico_pagerank[val]
    
    #Ecriture du fichier de vérfication
    with open ('Pageranks_results_mass.txt','w') as g:
        g.write(f'Nombre de pages:  {PageRank.total_nodes} \n')
        g.write(f'Somme des Pageranks:  {somme_pagerank} \n')
        for k,v in sorted(PageRank.dico_pagerank.items(), key=lambda x : x[1], reverse = True):
            g.write(f'{k}:  {v} \n')
    
    
