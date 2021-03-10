import os
from pathlib import PurePath
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
class LoggingConstants:
    LOGDIRECTORY = 'logs'
    def __init__(self):
        #main logging config
        self.CURRENTPATH = os.path.dirname(os.path.realpath(__file__))
        self.CURRENTPATH = PurePath(self.CURRENTPATH)
        self.PARENTPATH = str(self.CURRENTPATH.parents[0])
        self.LOGFORMAT = '%(levelname)s : %(asctime)s : %(filename)s:%(lineno)d : %(message)s'
        self.LOGNAME = 'FTS'
        self.ERRORLOG = str(PurePath(MainConfig.MainPath, f"{self.LOGDIRECTORY}/{self.LOGNAME}_error.log"))
        self.DEBUGLOG = str(PurePath(MainConfig.MainPath, f"{self.LOGDIRECTORY}/{self.LOGNAME}_debug.log"))
        self.INFOLOG = str(PurePath(MainConfig.MainPath, f"{self.LOGDIRECTORY}/{self.LOGNAME}_info.log"))
        self.HTTPLOG = str(PurePath(MainConfig.MainPath, f"{self.LOGDIRECTORY}/{self.LOGNAME}_http.log"))
        self.DELIMITER = ' ? '
        self.MAXFILESIZE = 100000
        self.BACKUPCOUNT = 5
        #orchestrator logs
        
        #clientConnected
        self.CLIENTCONNECTED = 'client has connected'
        self.CREATE = 'create'
        self.ADD = 'add'
        self.CLIENTCONNECTEDFINISHED = 'finished establishing connection'
        self.CLIENTCONNECTEDERROR = 'there has been an error in a clients connection'
        
        #emergencyReceived
        self.ON = 'on'
        self.OFF = 'off'
        self.EMERGENCYCREATED = 'emergency has been created'
        self.EMERGENCYREMOVED = 'emergency has now been removed'
        self.EMERGENCY = "emergency"
        self.EMERGENCYRECEIVEDERROR = 'there has been an error in a clients connection'

        #dataReceived
        self.DATARECEIVEDERROR = 'there has been an error in the reception of generic data'

        #clientDisconnected
        self.CLIENTDISCONNECTSTART = 'initiating client disconnection'
        self.REMOVE = "remove"
        self.DESTROY = 'destroy'
        self.CLIENTDISCONNECTEND = 'client disconnection has concluded '
        self.CLIENTDISCONNECTERROR = 'there has been an error in the reception of generic data'

        #monitorRawCoT
        self.MONITORRAWCOTERRORA = 'there has been an error in the reception of data in the monitoring of pipes A'
        self.MONITORRAWCOTERRORB = 'there has been an error in the reception of data in the monitoring of pipes B'
        self.MONITORRAWCOTERRORC = 'there has been an error in the reception of data in the monitoring of pipes C'
        self.MONITORRAWCOTERRORD = 'there has been an error in the reception of data in the monitoring of pipes D'
        self.MONITORRAWCOTERRORINTERNALSCANERROR = 'there has been an error in the scanning of the internal CoT array'

        #start
        self.LOADING = 'loading ...'
        self.SERVERSTARTED = 'server has started'
        self.STARTERROR = 'there has been a critical error in the startup of FTS'
        
        #arguments
        self.ARGUMENTDESCRIPTION = 'FreeTAKServer startup settings'
        self.ARGUMENTCOTPORTDESCRIPTION = 'the port you would like FreeTAKServer to run receive connections on'
        self.ARGUMENTCOTPORT = '-CoTPort'
        self.ARGUMENTCOTPORTDEFAULT = 8087

        self.ARGUMENTCoTIPDESCRIPTION = "the IP you would like FreeTAKServer to run receive connections on ONLY CHANGE IF YOU KNOW WHAT YOU'RE DOING"
        self.ARGUMENTCOTIP = '-CoTIP'
        self.ARGUMENTCoTIPDEFAULT = '0.0.0.0'

        self.ARGUMENTDATAIPDESCRIPTION = 'the ip address you would like FreeTAKServer to run receive datapackages on this is necesarry if its not set correctly data packages will fail'
        self.ARGUMENTDATAIP = '-DataIP'
        self.ARGUMENTDATAIPDEFAULT = '0.0.0.0'

        self.ARGUMENTDATAPORTDESCRIPTION = 'the port you would like FreeTAKServer to run receive connections on'
        self.ARGUMENTDATAPORT = '-DataPort'
        self.ARGUMENTDATAPORTDEFAULT = 8080

        #ClientInformationController
        self.CLIENTINFORMATIONCONTROLLERERROR = 'another exception'

        #ClientReceptionHandler
        #Startup
        self.CLIENTRECEPTIONHANDLERSTART = "client reception handler has finished startup"
        self.CLIENTRECEPTIONHANDLERSTARTUPERROR = 'there has been an error in client reception startup'
       
        #Monitor event pipe
        self.CLIENTRECEPTIONHANDLERMONITOREVENTPIPEERROR = 'there has been an error in a client reception Event Pipe'
        
        #Return data to orchestrator
        self.CLIENTRECEPTIONHANDLERRETURNDATATOORCHESTRATORERROR = 'there has been an error in client reception returning data to the orchestrator'
        
        #create client monitor
        self.CLIENTRECEPTIONHANDLERCREATECLIENTMONITORERROR = 'there has been an error in client reception with the creation of a client monitor'
        self.CLIENTRECEPTIONHANDLERCREATECLIENTMONITORINFO = 'client reception handler thread has finished being created'

        #destroy client monitor
        self.CLIENTRECEPTIONHANDLERDESTROYCLIENTMONITORINFO = 'client reception handler thread has finished being terminated'
        self.CLIENTRECEPTIONHANDLERDESTROYCLIENTMONITORERROR = 'there has been an error in client reception with the destruction of a clients thread '

        #monitorForData
        self.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORA = 'there has been an error in a clients reception thread section A '
        self.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORB = 'there has been an error in a clients reception thread section B '
        self.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORC = 'there has been an error in a clients reception thread section C '
        self.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORD = 'there has been an error in a clients reception thread section D '

        #return Received Data
        self.CLIENTRECEPTIONHANDLERRETURNRECEIVEDDATAERROR = 'there has been an error in a clients reception thread with the returning of received data '

        #data package server

        #ReceiveConnections
        #listen
        self.RECEIVECONNECTIONSLISTENINFO = 'client connected'
        self.RECEIVECONNECTIONSLISTENERROR = 'error in Receive connections listen function '

        #send client data
        #send data in queue

        self.SENDCLIENTDATASENDDATAINQUEUEINFO = 'send data in queue started'

        #Send data controller
        #Send data in queue
        self.SENDDATACONTROLLERSENDDATAINQUEUEERROR = "error send data controller in send data in queue"

        #XMLCoTController
        #determine CoT general
        self.XMLCOTCONTROLLERDETERMINECOTGENERALERRORA = "exception XMLCoTController in determining general CoT type A "
        self.XMLCOTCONTROLLERDETERMINECOTGENERALERRORB = "exception XMLCoTController in determining general CoT type B "