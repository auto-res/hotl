# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 21:27:21 2024

@author: Yz
"""

from src.ABS import ABS
from src.concrete import CON


class AplusB:
    def __init__(self, api_key, GPT_id, M_pseudo_code, A_pseudo_code, M_name, A_name):
        self.GPT_id = GPT_id
        self.M_pseudo_code = M_pseudo_code
        self.A_pseudo_code = A_pseudo_code
        self.api_key = api_key
        self.M_name = M_name
        self.A_name = A_name

    def M2_code_gen(self):
        # abs = ABS(self.api_key,self.GPT_id,self.M_pseudo_code,self.M_name)
        # think1,python1_1,python1_2 = abs.abstraction()

        abs = ABS(self.api_key, self.GPT_id, self.A_pseudo_code, self.A_name)
        think2, python2_1, python2_2 = abs.abstraction()

        con = CON(
            self.api_key, self.GPT_id, self.M_pseudo_code, python2_1, python2_2, think2
        )
        mix_python, think = con.concrete()
        return mix_python, think, think2, python2_1, python2_2
