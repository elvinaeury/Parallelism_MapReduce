#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 14:14:51 2020

@author: elvinagovendasamy
"""


# =============================================================================
# Question 1
# =============================================================================

import time
import threading
import random

class Compte(threading.Thread):
    compte=True

    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        last = -1
        while Compte.compte:
            nb = threading.active_count()
            if last!=nb :
                print(f"{nb} tâche(s) active(s)")
            last = nb
            


class Functions(threading.Thread):

    # création de 2 verrous globaux
    mon_verrou=threading.Lock()
    mon_verrou1=threading.Lock()
    instruction_list=[] # liste globale
    dico={} # dictionnaire global
    k=1

    def __init__(self,numero_processeur):
        threading.Thread.__init__(self)
        self.numero_processeur=numero_processeur

    def run(self):
        while len(Functions.instruction_list)!=0:
            
            Functions.mon_verrou.acquire() # premier verrou
            i=random.randint(0, len(Functions.instruction_list)-1)
            chosen_function=Functions.instruction_list[i]
            Functions.instruction_list.pop(i) # on met le pop pour ajuster la taille de la liste
            Functions.mon_verrou.release()
            
            Functions.mon_verrou1.acquire() # deuxieme verrou
            try:
                result=eval(chosen_function)
                Functions.dico[chosen_function]=(result,self.numero_processeur,Functions.k)
                print(f"{Functions.k} : Résultat de l'expression {chosen_function} = {result}, le numéro du processeur est {self.numero_processeur} ")
                Functions.k+=1
            except Exception as e:
                Functions.dico[chosen_function]=(e,self.numero_processeur,Functions.k)
            Functions.mon_verrou1.release()
    

if __name__=='__main__':
    
    count_=Compte()
    count_.start() # on commence par compter le nombre de tâches: 
    # À partir d'un certain nombre de tâches actives on n'affiche pas les tâches actives

    file_name = input('Nom du fichier à évaluer : ')
    data=open(file_name,'r')
    for lines in data:
        Functions.instruction_list.append(lines.strip('\n'))
        Functions.dico[lines.strip('\n')]=0
    data.close()

    

    threads_active=[]
    n=int(input('Combien de processeurs souhaitez-vous utiliser ? : '))
    for i in range(1,n+1):  
        f=Functions(i)
        threads_active.append(f) # On ajoute les threads dans une liste
    for thread in threads_active: 
        thread.start()
    for thread in threads_active:
        thread.join()
        
    
    
    
    #for items in Functions.dico.keys():
        #print(f"Résultat de l'expression {items} = {Functions.dico[items][0]}, le numéro du processeur est {Functions.dico[items][1]},ID: {threading.current_thread().ident}, nom Thread: {threading.current_thread().name}")
    
    print(Functions.dico)

    print(f"Nombre d'instructions évaluées: {len(Functions.dico)}")
    print('End')
    
