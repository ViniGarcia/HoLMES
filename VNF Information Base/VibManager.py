import sqlite3
import os

import VibTableModels

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

    def _queryVibDatabase(self, sqlQueryRequest):

        try:
            vibCursor = self._vibConnection.cursor()
            vibCursor.execute(sqlQueryRequest)
            return vibCursor.fetchall()
       
        except sqlite3.Error as e:
            raise e

    def _resetVibDatabase(self):

        if self._vibConnection:
            self._vibConnection.close()
            os.remove(self._vibPath)
       
        try:
            self._vibConnection = sqlite3.connect(self._vibPath)
            
            tablesData = VibTableModels.VibSummaryModels()
            for tableName in dir(tablesData):
                if not tableName.startswith("_"):
                    self._queryVibDatabase(getattr(tablesData, tableName))
                
            return True
        
        except sqlite3.Error as e:
            self._vibConnection = None
            return False

    def selectVibDatabase(self, sqlSelect, sqlFrom, sqlWhere):
        pass

    def insertVibDatabase(self, sqlData):

        try:
            vibCursor = self._vibConnection.cursor()
            vibCursor.execute(sqlData[0], sqlData[1])
            self._vibConnection.commit()
            return vibCursor.lastrowid
       
        except sqlite3.Error as e:
            raise e



    #TEMPORARY
    def vibTesting(self):
        #return self._resetVibDatabase()
        
        #return self._queryVibDatabase("SELECT name FROM sqlite_master WHERE type='table';")

        #classTest = VibTableModels.VibVnfInstance("teste1", "teste2", "teste3", "teste4")
        #return self.insertVibDatabase(classTest.toSql())
        return self._queryVibDatabase("SELECT * FROM VnfInstance;")


        return

vibTester = VibManager()
print(vibTester.vibTesting())