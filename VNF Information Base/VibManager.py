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
    __vibPath = "C:\\Users\\55559\\Desktop\\EMSPlatform\\VNF Information Base\\VIB.db"
    __vibConnection = None

    def __init__(self):

        try:
            self.__vibConnection = sqlite3.connect(self.__vibPath)
        
        except sqlite3.Error as e:
            self.__vibConnection = None

    def __del__(self):

        if self.__vibConnection:
            self.__vibConnection.close()

    def _resetVibDatabase(self):

        if self.__vibConnection:
            self.__vibConnection.close()
            os.remove(self.__vibPath)
       
        try:
            self.__vibConnection = sqlite3.connect(self.__vibPath)
            
            tablesData = VibTableModels.VibSummaryModels()
            for tableName in dir(tablesData):
                if not tableName.startswith("_"):
                    self.queryVibDatabase(getattr(tablesData, tableName))
                
            return True
        
        except sqlite3.Error as e:
            self.__vibConnection = None
            return False

    def queryVibDatabase(self, sqlQueryRequest):

        try:
            vibCursor = self.__vibConnection.cursor()
            vibCursor.execute(sqlQueryRequest)
            return vibCursor.fetchall()
       
        except sqlite3.Error as e:
            raise e

    def insertVibDatabase(self, sqlData):

        try:
            vibCursor = self.__vibConnection.cursor()
            vibCursor.execute(sqlData[0], sqlData[1])
            self.__vibConnection.commit()
            return vibCursor.lastrowid
       
        except sqlite3.Error as e:
            raise e

'''    #TEMPORARY
    def vibTesting(self):
        self._resetVibDatabase()
        #return self.queryVibDatabase("SELECT name FROM sqlite_master WHERE type='table';")
        
        classTest = VibTableModels.VibVnfInstance("VNF01", "COO", "Regras;Ações", True)
        self.insertVibDatabase(classTest.toSql())
        self.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"VNF01\";")
        
        classTest = VibTableModels.VibAuthInstance("USER01", "VNF01", "BatataFrita", None)
        self.insertVibDatabase(classTest.toSql())
        return self.queryVibDatabase("SELECT * FROM AuthInstance WHERE userId = \"USER01\";")
        return

vibTester = VibManager()
ret = vibTester.vibTesting()
print(ret)'''