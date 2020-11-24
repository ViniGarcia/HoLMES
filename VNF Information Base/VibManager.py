import sqlite3
import os

import VibModels
import AsModels

'''
CLASS: VibManager
AUTHOR: Vinicius Fulber-Garcia
CREATION: 21 Oct. 2020
L. UPDATE: 10 Nov. 2020 (Fulber-Garcia; Delete method)
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

    def __resetVibDatabase(self):

        if self.__vibConnection:
            self.__vibConnection.close()
            os.remove(self.__vibPath)
       
        try:
            self.__vibConnection = sqlite3.connect(self.__vibPath)
            
            tablesData = VibModels.VibSummaryModels()
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

    def deleteVibDatabase(self, sqlDeleteRequest):

        try:
            vibCursor = self.__vibConnection.cursor()
            delResult = vibCursor.execute(sqlDeleteRequest).rowcount
            self.__vibConnection.commit()
            return delResult
       
        except sqlite3.Error as e:
            print(e)
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
        if self.__resetVibDatabase():
            return self.queryVibDatabase("SELECT name FROM sqlite_master WHERE type='table';")
            
            #classTest = VibModels.VibPlatformInstance().fromData("COO", {"START":"/START", "STOP":"/STOP"}, {"CPU":"/CPU", "MEMORY":"/MEMORY"}, {"FUNCTION":"/FUNCTION"})
            #self.insertVibDatabase(classTest.toSql())
            #print(self.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"COO\";"))

            #classTest = VibModels.VibVnfInstance().fromData("VNF01", "127.0.0.1:5000", "Click-On-OSv", ["OP01", "OP02"], True)
            #self.insertVibDatabase(classTest.toSql())
            #print(self.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"VNF01\";"))
            
            #classTest = VibModels.VibAuthInstance().fromData("USER01", "VNF01", "BatataFrita", None)
            #self.insertVibDatabase(classTest.toSql())
            #print(self.queryVibDatabase("SELECT * FROM AuthInstance WHERE userId = \"USER01\";"))

            #classTest = VibModels.VibVnfIndicatorSubscription().fromData("SUBS01", AsModels.VnfIndicatorNotificationsFilter(), "192.168.0.100:8000", {"self":"192.168.0.100:8000"})
            #self.insertVibDatabase(classTest.toSql())
            #print(self.queryVibDatabase("SELECT * FROM VnfIndicatorSubscription WHERE visId = \"SUBS01\";"))
'''