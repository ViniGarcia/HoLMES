import sqlite3
import os

import VibTableModels

'''
CLASS: VibManager
AUTHOR: Vinicius Fulber-Garcia
CREATION: 21 Oct. 2020
L. UPDATE: 02 Nov. 2020 (Fulber-Garcia; Class updates)
DESCRIPTION: Implementation of the VIB manager. In summary, this class control the
             information insertion and retrieving from the VIB. It can also modify
             the VIB internally, reseting the base when necessary.
'''
class VibManager:
    _vibPath = ".\\VIB.db"
    _vibConnection = None

    def __init__(self):

        try:
            self._vibConnection = sqlite3.connect(self._vibPath)
        
        except sqlite3.Error as e:
            self._vibConnection = None

    def __del__(self):

        if self._vibConnection:
            self._vibConnection.close()

    def _resetVibDatabase(self):

        if self._vibConnection:
            self._vibConnection.close()
            os.remove(self._vibPath)
       
        try:
            self._vibConnection = sqlite3.connect(self._vibPath)
            
            tablesData = VibTableModels.VibSummaryModels()
            for tableName in dir(tablesData):
                if not tableName.startswith("_"):
                    self.queryVibDatabase(getattr(tablesData, tableName))
                
            return True
        
        except sqlite3.Error as e:
            self._vibConnection = None
            return False

    def queryVibDatabase(self, sqlQueryRequest):

        try:
            vibCursor = self._vibConnection.cursor()
            vibCursor.execute(sqlQueryRequest)
            return vibCursor.fetchall()
       
        except sqlite3.Error as e:
            raise e

    def insertVibDatabase(self, sqlData):

        try:
            vibCursor = self._vibConnection.cursor()
            vibCursor.execute(sqlData[0], sqlData[1])
            self._vibConnection.commit()
            return vibCursor.lastrowid
       
        except sqlite3.Error as e:
            raise e

    '''#TEMPORARY
    def vibTesting(self):
        #return self._resetVibDatabase()
        
        #return self._queryVibDatabase("SELECT name FROM sqlite_master WHERE type='table';")

        #classTest = VibTableModels.VibVnfInstance("teste1", "teste2", "teste3", "teste4")
        #return self.insertVibDatabase(classTest.toSql())
        return self.queryVibDatabase("SELECT * FROM VnfInstance WHERE ID = 1;")

        return'''
'''
vibTester = VibManager()
ret = vibTester.vibTesting()
print(ret)
'''