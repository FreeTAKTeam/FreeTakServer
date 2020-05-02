class sql:
    def __init__(self):
        #querys for httpServer
        self.CREATEDPTABLE = ("CREATE TABLE IF NOT EXISTS DataPackages"
        "(PrimaryKey          INTEGER  PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT UNIQUE ON CONFLICT FAIL,"
        "UID                STRING,"
        "Name               STRING,"
        "Hash               VARCHAR(300),"
        "SubmissionDateTime DATETIME DEFAULT (CURRENT_TIMESTAMP),"
        "SubmissionUser     STRING,"
        "CreatorUid         STRING,"
        "Keywords           CHAR     DEFAULT foobar,"
        "MIMEType           STRING   DEFAULT [application/x-zip-compressed],"
        "Size               INTEGER);")

        self.MISSIONUPLOADCALLSIGN = "SELECT Callsign FROM Users WHERE UID=?"
    
        self.INSERTDPINFO = "INSERT INTO DataPackages (UID, Name, Hash, SubmissionUser, CreatorUid, Size) VALUES(?,?,?,?,?,?);"

        self.ROWBYHASH = "SELECT * FROM DataPackages WHERE Hash=?"

        self.SELECTALLDP = "SELECT * FROM DataPackages"
    
        #querys for server
        self.DELETEBYUID = "DELETE FROM Users WHERE UID=?"

        self.CREATEUSERSTABLE = ("CREATE TABLE IF NOT EXISTS Users"
        "(PrimaryKey INTEGER PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT UNIQUE ON CONFLICT FAIL,"
        "UID STRING,"
        "Callsign STRING);")

        self.INSERTNEWUSER = "INSERT INTO users (UID, Callsign) VALUES(?, ?)"