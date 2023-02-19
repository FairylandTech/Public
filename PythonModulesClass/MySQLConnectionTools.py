# coding: utf8
""" 
@File: MySQLConnectionTools.py
@Editor: PyCharm
@Author: Alice(From Chengdu.China)
@HomePage: https://github.com/AliceEngineerPro
@OS: Windows 11 Professional Workstation 22H2
@Envirement: Python3.9 (FairyAdministrator)
@CreatedTime: 2023/2/16 20:58
"""

import pymysql
from loguru import logger


class MySQLConnection(object):
    """MySQL操作工具类"""

    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        """
        
        :param host: 地址 
        :param port: 端口
        :param user: 用户名
        :param password: 密码
        :param database: 数据库
        """
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database

    def info(self) -> dict:
        """
        
        :return: 数据库信息
        """
        return {'MySQLInfo': {
            'Host': self.__host,
            'Port': self.__port,
            'User': self.__user,
            'Password': self.__password,
            'Database': self.__database
        }}

    def __connect(self) -> 1:
        """
        连接数据库
        :return: 1 or 0
        """
        try:
            self.__conn = pymysql.connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                password=self.__password,
                database=self.__database
            )
            logger.info('{}'.format('Connecting to the database succeeded.'))
            self.__cur = self.__conn.cursor()
            logger.info('{}'.format('Creation of database cursor succeeded.'))
            return 1
        except Exception as error:
            logger.error('{}'.format(error))
            return 0

    def query(self, query: str) -> tuple:
        """
        数据查询操作
        :param query: 查询语句 
        :return: 可迭代对象
        """
        if self.__connect() == 1:
            try:
                logger.info('MySQL sentence -> {}'.format(query))
                self.__cur.execute(query=query)
                self.__cur.close()
                self.__conn.close()
                logger.info('{}'.format('Executed successfully.'))
                return self.__cur.fetchall()
            except Exception as error:
                self.__cur.close()
                self.__conn.close()
                logger.error('{}'.format(error))

    def insert(self, insert: str) -> 1:
        if self.__connect() == 1:
            try:
                logger.info('MySQL sentence -> {}'.format(insert))
                self.__cur.execute(query=insert)
                self.__conn.commit()
                logger.info('{}'.format('Executed successfully.'))
                self.__cur.close()
                self.__conn.close()
                return 1
            except Exception as error:
                self.__cur.close()
                self.__conn.close()
                logger.error('{}'.format(error))

    def update(self, update: str):
        self.insert(insert=update)

    def delete(self, delete: str):
        self.insert(insert=delete)
