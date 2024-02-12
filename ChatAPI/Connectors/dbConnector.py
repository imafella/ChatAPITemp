# Class for connecting to database.
# Given time, I would have prefered to make an additional service to run
# with a simple API that has no logic other than retrieving and posting to a database

import configparser
import json
import mysql.connector


def loadConfig():
    configParser = configparser.RawConfigParser()
    configFilePath = 'config.txt'
    configParser.read(configFilePath)
    dbConfig = dict(configParser.items('DatabaseDetails'))
    return dbConfig


class chatAPIDBConnector:
    def __init__(self):
        self.dbConfig = loadConfig()
        self.dbConnection = None
        self.cursor = None
        self.connectToDB()
        self.cursor.close()
        self.dbConnection.close()

    # Sets up the config

    def connectToDB(self):
        self.dbConnection = mysql.connector.connect(user=self.dbConfig['user'],
                                                                       password=self.dbConfig['password'],
                                                                       host=self.dbConfig['host'],
                                                                       database=self.dbConfig['database'])
        self.cursor = self.dbConnection.cursor(buffered=True)

    def closeConnectionToDB(self):
        self.cursor.close()
        self.dbConnection.close()

    def selectCall(self, sql):
        self.connectToDB()
        self.cursor.execute(sql)
        desc = self.cursor.description
        column_names = [col[0] for col in desc]
        result = [dict(zip(column_names, row))
                  for row in self.cursor.fetchall()]
        self.closeConnectionToDB()
        return result

    def insertCall(self, sql):
        self.connectToDB()
        self.cursor.execute(sql)
        lastId = self.cursor.lastrowid
        self.dbConnection.commit()
        self.closeConnectionToDB()
        return lastId
