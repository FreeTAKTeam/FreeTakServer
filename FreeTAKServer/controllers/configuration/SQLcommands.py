class SQLcommands:
    def __init__(self):
        # Statements for Data Package records. Accessed from HTTP server
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
                              "Size               INTEGER,"
                              "Privacy            INTEGER  DEFAULT 0);")
        self.MISSIONUPLOADCALLSIGN = "SELECT Callsign FROM Users WHERE UID=?"
        self.INSERTDPINFO = "INSERT INTO DataPackages (UID, Name, Hash, SubmissionUser, CreatorUid, Size) VALUES (?,?,?,?,?,?);"
        self.ROWBYHASH = "SELECT * FROM DataPackages WHERE Hash=?"
        self.SELECTALLDP = "SELECT * FROM DataPackages WHERE Privacy = 0"
        self.RETRIEVECALLSIGNFROMUID = "SELECT Callsign FROM Users WHERE Uid = ?"

        # Statements to work with storing/retrieving video links. Accessed from HTTP server
        self.CREATEVIDEOTABLE = ("CREATE TABLE IF NOT EXISTS VideoLinks"
                                 "(PrimaryKey         INTEGER PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT UNIQUE ON CONFLICT FAIL,"
                                 "FullXmlString       STRING,"
                                 "Timestamp           DATETIME DEFAULT (CURRENT_TIMESTAMP),"
                                 "Protocol            STRING,"
                                 "Alias               STRING,"
                                 "Uid                 STRING,"
                                 "Address             STRING,"
                                 "Port                INTEGER DEFAULT -1,"
                                 "RoverPort           INTEGER DEFAULT -1,"
                                 "IgnoreEmbeddedKlv   STRING DEFAULT false,"
                                 "PreferredMacAddress STRING DEFAULT NULL,"
                                 "Path                STRING DEFAULT NULL,"
                                 "Buffer              INTEGER DEFAULT -1,"
                                 "Timeout             INTEGER,"
                                 "RtspReliable        INTEGER DEFAULT 0);")
        self.INSERTVIDEO = "INSERT INTO VideoLinks (FullXmlString,Protocol,Alias,Uid,Address,Port,RoverPort,IgnoreEmbeddedKlv,PreferredMacAddress,Path,Buffer,Timeout,RtspReliable) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.GETALLVIDEOS = "SELECT FullXmlString FROM VideoLinks"
        self.GETVIDEOSWITHUID = "SELECT FullXmlString from VideoLinks WHERE Uid=?"

        # Statements for User records accessed from HTTP server
        self.CREATEUSERTABLE = ("CREATE TABLE IF NOT EXISTS Users"
                                "(PrimaryKey         INTEGER PRIMARY KEY ON CONFLICT FAIL AUTOINCREMENT UNIQUE ON CONFLICT FAIL,"
                                "Uid                 STRING,"
                                "Callsign             STRING)")
        self.ADDUSER = ("INSERT INTO Users (Uid, Callsign) VALUES (?, ?)")
        self.REMOVEUSER = ("DELETE FROM Users WHERE Uid = ?")
