from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

class DatabaseConfiguration:
    DataBasePath = MainConfig.DBFilePath
    DataBaseType = str('sqlite:///')
    DataBaseConnectionString = str(DataBaseType+DataBasePath)
    #DataBaseConnectionString = str('sqlite:////home/ghost/FTSTesting/FreeTAKServer/controllers/testing.db')
