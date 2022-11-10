from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

class DatabaseConfiguration:
    DataBasePath = config.DBFilePath
    if config.DataBaseType == "SQLite":
        DataBaseType = str('sqlite:///')
    elif config.DataBaseType == "MySQL":
        DataBaseType = str('mysql://')
    DataBaseConnectionString = str(DataBaseType+DataBasePath)
