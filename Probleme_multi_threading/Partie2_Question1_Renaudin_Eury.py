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

class Functions(threading.Thread):

    # création de 2 verrous globaux
    mon_verrou=threading.Lock()
    mon_verrou1=threading.Lock()
    instruction_list=[] # liste globale
    dico={} # dictionnaire global

    def __init__(self):
        threading.Thread.__init__(self)
        

    def run(self):
        while len(Functions.instruction_list)!=0:
            
            Functions.mon_verrou.acquire() # premier verrou
            i=random.randint(0, len(Functions.instruction_list)-1)
            chosen_function=Functions.instruction_list[i]
            Functions.instruction_list.pop(i) # on met le pop pour ajuster la taille de la liste
            Functions.mon_verrou.release()

            Functions.mon_verrou1.acquire()
            try:
                result=eval(chosen_function)
                Functions.dico[chosen_function]=result
            except Exception as e:
                Functions.dico[chosen_function]=e
            Functions.mon_verrou1.release()   
                
            
    

if __name__=='__main__':

    file_name = input('Nom du fichier à évaluer : ')
    data=open(file_name,'r')
    for lines in data:
        Functions.instruction_list.append(lines.strip('\n'))
        Functions.dico[lines.strip('\n')]=0
        
    data.close()
   

    threads_active=[]
    n=int(input('Combien de processeurs souhaitez-vous utiliser ? : '))
    for i in range(1,n+1):  
        f=Functions()
        threads_active.append(f) # On ajoute les threads dans une liste
    for thread in threads_active: 
        thread.start()
    for thread in threads_active:
        thread.join()
    
    
    #for items in Functions.dico.keys():
        #print(f"Résultat de l'expression {items} = {Functions.dico[items][0]}, le numéro du processeur est {Functions.dico[items][1]}")

    print(Functions.dico)
    print(f"Nombre d'instructions évaluées: {len(Functions.dico)}")
    print('End')
    
