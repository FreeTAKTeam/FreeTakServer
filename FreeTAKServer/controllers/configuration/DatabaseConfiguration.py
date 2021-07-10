from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

class DatabaseConfiguration:
    DataBasePath = MainConfig.DBFilePath
    if MainConfig.DataBaseType == "SQLite":
        DataBaseType = str('sqlite:///')
    elif MainConfig.DataBaseType == "MySQL":
        DataBaseType = str('mysql://')
    DataBaseConnectionString = str(DataBaseType+DataBasePath)
