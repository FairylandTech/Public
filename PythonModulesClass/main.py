# coding: utf8
""" 
@File: main.py
@Editor: PyCharm
@Author: Alice(From Chengdu.China)
@HomePage: https://github.com/AliceEngineerPro
@OS: Windows 11 Professional Workstation 22H2
@Envirement: Python3.9 (FairyAdministrator)
@CreatedTime: 2023/2/20 1:33
"""

from PythonModulesClass.Utils.PublicTools import Public


def public():
    return Public()

if __name__ == '__main__':
    print(public().abs_path())
