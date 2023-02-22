# coding: utf8
""" 
@File: PublicTools.py
@Editor: PyCharm
@Author: Alice(From Chengdu.China)
@HomePage: https://github.com/AliceEngineerPro
@OS: Windows 11 Professional Workstation 22H2
@Envirement: Python3.9 (FairyAdministrator)
@CreatedTime: 2023/2/16 22:14
"""

import os
import datetime
from loguru import logger

class Public(object):
    
    def __init__(self):
        self.__abspath = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
    def abs_path(self):
        return self.__abspath
    
    def now_data(self):
        return datetime.datetime.today().date()




