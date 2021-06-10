#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 14:14:51 2020

@author: elvinagovendasamy
"""

# =============================================================================
# Question 2
# =============================================================================

import random

class Functions():
    def __init__(self):
        pass
        
    def read_file(self, file_name):
        f=open(file_name,'r')
        instruction_list=[]
        for lines in f:
            instruction_list.append(lines.strip('\n'))
        f.close()
        return instruction_list
        
    
    def run_functions(self, file_name):
        dico={}
        instruction_list=Functions.read_file(self,file_name)
        random.shuffle(instruction_list)
        
        n=len(instruction_list)
        for i in range(n):
            chosen_function=instruction_list[i]
            dico[chosen_function]=eval(chosen_function)
            
        return dico


if __name__=='__main__':

    file_name = input('Nom du fichier à évaluer : ')
    f=Functions()
    result=f.run_functions(file_name)
    print(result)
    