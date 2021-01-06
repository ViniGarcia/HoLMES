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
    __vibPath = "VNF Information Base\\VIB.db"
    __vibConnection = None

    def __init__(self):

        try:
            self.__vibConnection = sqlite3.connect(self.__vibPath, check_same_thread=False)

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

    def operateVibDatabase(self, sqlData):

        try:
            vibCursor = self.__vibConnection.cursor()
            opResult = vibCursor.execute(sqlData[0], sqlData[1])
            self.__vibConnection.commit()
            return opResult
       
        except sqlite3.Error as e:
            raise e

    '''#TEMPORARY
    def vibTesting(self):

        if self.__resetVibDatabase():
            
            classTest = VibModels.VibPlatformInstance().fromData("Click-On-OSv", "CooDriver")
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"Click-On-OSv\";"))
            classTest = VibModels.VibPlatformInstance().fromData("Click-On-OSv-S", "CooSocketDriver")
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"Click-On-OSv-S\";"))

            classTest = VibModels.VibVnfInstance().fromData("VNF01", "127.0.0.1:5000", "Click-On-OSv", ["OP01", "OP02"], True)
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"VNF01\";"))
            classTest = VibModels.VibVnfInstance().fromData("VNF02", "127.0.0.1:5005", "Click-On-OSv-S", ["OP01", "OP02"], True)
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"VNF02\";"))

            classTest = VibModels.VibUserInstance().fromData("USER01", "BatataFrita", None, ["VLMI", "VPMI", "VFMI", "VII", "VCI", "VNF", "VIB", "MS", "AS", "VS"])
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM UserInstance WHERE userId = \"USER01\";"))
            
            classTest = VibModels.VibCredentialInstance().fromData("USER01", "VNF01")
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"USER01\";"))

            classTest = VibModels.VibMaInstance().fromData("CooRunning", "CooRunningAgent", "Click-On-OSv")
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM MaInstance WHERE maId = \"CooRunning\";"))

            vnfIndicatorNotificationsFilter = AsModels.VnfIndicatorNotificationsFilter().fromData(AsModels.VnfInstanceSubscriptionFilter().fromData([], [], ["VNF01"], []), [], ["CooRunningAgent"])
            classTest = VibModels.VibSubscriptionInstance().fromData("SUBS01", vnfIndicatorNotificationsFilter, "http://127.0.0.1:5000/response", {"self":"127.0.0.1:5000"})
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"SUBS01\";"))

            classTest = VibModels.VibVnfmInstance().fromData("DummyVnfmDriver", "DummyVnfmDriver")
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM VnfmInstance WHERE vnfmId = \"DummyVnfmDriver\";"))'''