# coding: utf8
""" 
@File: ReadExcelTools.py
@Editor: PyCharm
@Author: Alice(From Chengdu.China)
@HomePage: https://github.com/AliceEngineerPro
@OS: Windows 11 Professional Workstation 22H2
@Envirement: Python3.9 (FairyAdministrator)
@CreatedTime: 2023/2/16 21:45
"""
import logging

import xlrd
from loguru import logger


class ReadExcel(object):
    """读取Excel操作工具类"""
    
    def __init__(self, excel_path: str):
        self.__excel_path = excel_path
        
    def read(self) -> xlrd.book.Book:
        """
        读取Excel
        :return: xlrd.book.Book Object 
        """
        logger.info('Excel file path: {}'.format(self.__excel_path))
        return xlrd.open_workbook(filename=self.__excel_path)


