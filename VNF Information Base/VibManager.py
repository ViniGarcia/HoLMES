import sqlite3
import os

import VibModels
import AsModels

'''
CLASS: VibManager
AUTHOR: Vinicius Fulber-Garcia
CREATION: 21 Oct. 2020
L. UPDATE: 28 Jul. 2021 (Fulber-Garcia; Included vnfmAdrress into DummyVnfmDriver register)
DESCRIPTION: Implementation of the VIB manager. In summary, this class control the
             information insertion and retrieving from the VIB. It can also modify
             the VIB internally, reseting the base when necessary.
'''
class VibManager:
    __vibPath = os.path.abspath(__file__).replace("VibManager.py", "VIB.db")
    __vibConnection = None

    def __init__(self):

        try:
            self.__vibConnection = sqlite3.connect(self.__vibPath, check_same_thread=False)
            self.__vibConnection.execute("PRAGMA foreign_keys = 1")
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
            
            standardUser = VibModels.VibUserInstance().fromData("admin", "admin", None, ["VLMI", "VPMI", "VFMI", "VII", "VCI", "VNF", "VIB", "MS", "AS", "VS"])
            self.operateVibDatabase(standardUser.toSql())
            vinesVnfmDriver = VibModels.VibVnfmDriverInstance().fromData("StdVinesVnfmDriver", "VinesVnfmDriver")
            self.operateVibDatabase(vinesVnfmDriver.toSql())
            standardVnfmDriver = VibModels.VibVnfmDriverInstance().fromData("StdDummyVnfmDriver", "DummyVnfmDriver")
            self.operateVibDatabase(standardVnfmDriver.toSql())
            standardVnfm = VibModels.VibVnfmInstance().fromData("DummyVnfm", "StdDummyVnfmDriver", "127.0.0.1", "")
            self.operateVibDatabase(standardVnfm.toSql())
            for standardPlatform in [{"platformId": "Click-On-OSv", "platformDriver": "ClickOnOSvDriver"}, {"platformId": "COVEN-HTTP", "platformDriver": "HttpCovenDriver"}, {"platformId": "COVEN-Socket", "platformDriver": "SocketCovenDriver"}, {"platformId": "Leaf", "platformDriver": "LeafDriver"}]:
                self.operateVibDatabase(VibModels.VibPlatformInstance().fromDictionary(standardPlatform).toSql())

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
            return e

    def operateVibDatabase(self, sqlData):

        try:
            vibCursor = self.__vibConnection.cursor()
            opResult = vibCursor.execute(sqlData[0], sqlData[1])
            self.__vibConnection.commit()
            return opResult
       
        except sqlite3.Error as e:
            return e

    #TEMPORARY
    '''def vibTesting(self):

        if self.__resetVibDatabase():

            print(self.queryVibDatabase("SELECT * FROM PlatformInstance;"))
            classTest = VibModels.VibPlatformInstance().fromData("PLATFORM01", "CooDriver")
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"PLATFORM01\";"))
            classTest = VibModels.VibPlatformInstance().fromData("PLATFORM02", "CooSocketDriver")
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"PLATFORM02\";"))

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

            classTest = VibModels.VibMaInstance().fromData("MONITOR01", "CooRunningAgent", "Click-On-OSv")
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM MaInstance WHERE maId = \"MONITOR01\";"))

            vnfIndicatorNotificationsFilter = AsModels.VnfIndicatorNotificationsFilter().fromData(AsModels.VnfInstanceSubscriptionFilter().fromData([], [], ["VNF01"], []), [], ["CooRunningAgent"])
            classTest = VibModels.VibSubscriptionInstance().fromData("SUBS01", vnfIndicatorNotificationsFilter, "http://127.0.0.1:5000/response", {"self":"127.0.0.1:5000"})
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"SUBS01\";"))

            classTest = VibModels.VibVnfmDriverInstance().fromData("VNFMNAME01", "VNFDRIVER01")
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM VnfmDriverInstance WHERE vnfmId = \"VNFMNAME01\";"))

            classTest = VibModels.VibVnfmInstance().fromData("VNFM01", "VNFMNAME01", "127.0.0.1", "APIKey;APIPasswd")
            self.operateVibDatabase(classTest.toSql())
            print(self.queryVibDatabase("SELECT * FROM VnfmInstance WHERE vnfmId = \"VNFM01\";"))

            self.__resetVibDatabase()'''