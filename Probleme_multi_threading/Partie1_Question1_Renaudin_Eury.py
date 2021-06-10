#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 14:14:51 2020

@author: elvinagovendasamy
"""

# =============================================================================
# Question 1
# =============================================================================
import random


class Functions():
    def __init__(self):
        pass

    def run_functions(self,instructions):
        dico={}
        
        # Ici nous avons fait un shuffle des données pour simuler un choix aléatoire.
        random.shuffle(instructions)
        n=len(instructions)
        #On évalue chaque instruction et on enregistre cette évaluation dans un dictionnaire, la clé étant
        #l'instruction à évaluer
        for i in range(n):
            chosen_function=instructions[i]
            dico[chosen_function]=eval(chosen_function)
        return dico
        
                    


if __name__=='__main__':
    
    instruction_list=['1+2','2+10','3**2','4+500','3/30']

    f=Functions()
    result=f.run_functions(instruction_list)
    print(result)
    


