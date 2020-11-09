from FreeTAKServer.controllers.DatabaseControllers import UserTableController, DataPackageTableController
from FreeTAKServer.controllers.DatabaseControllers import VideoStreamTableController
from FreeTAKServer.controllers.DatabaseControllers import EventTableController
from FreeTAKServer.controllers.DatabaseControllers import ActiveEmergencysController
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from FreeTAKServer.model.SQLAlchemy.Root import Base
from FreeTAKServer.controllers.configuration.DatabaseConfiguration import DatabaseConfiguration
from FreeTAKServer.controllers.DatabaseControllers import APIUsersController
import FreeTAKServer.model.SQLAlchemy.CoTTables.Archive
import FreeTAKServer.model.SQLAlchemy.CoTTables._Group
import FreeTAKServer.model.SQLAlchemy.CoTTables.Chat
import FreeTAKServer.model.SQLAlchemy.CoTTables.Color
import FreeTAKServer.model.SQLAlchemy.CoTTables.Contact
import FreeTAKServer.model.SQLAlchemy.CoTTables.Dest
import FreeTAKServer.model.SQLAlchemy.CoTTables.Emergency
import FreeTAKServer.model.SQLAlchemy.CoTTables.Link
import FreeTAKServer.model.SQLAlchemy.CoTTables.Marti
import FreeTAKServer.model.SQLAlchemy.CoTTables.Precisionlocation
import FreeTAKServer.model.SQLAlchemy.CoTTables.Remarks
import FreeTAKServer.model.SQLAlchemy.CoTTables.Serverdestination
import FreeTAKServer.model.SQLAlchemy.CoTTables.Status
import FreeTAKServer.model.SQLAlchemy.CoTTables.Summary
import FreeTAKServer.model.SQLAlchemy.CoTTables.Takv
import FreeTAKServer.model.SQLAlchemy.CoTTables.Track
import FreeTAKServer.model.SQLAlchemy.CoTTables.Uid
import FreeTAKServer.model.SQLAlchemy.CoTTables.Usericon
import FreeTAKServer.model.SQLAlchemy.DataPackage
import FreeTAKServer.model.SQLAlchemy.VideoStream
import FreeTAKServer.model.SQLAlchemy.User
import FreeTAKServer.model.SQLAlchemy.APIUsers
import FreeTAKServer.model.SQLAlchemy.ActiveEmergencys


class DatabaseController:
    """
    this controller should only be instantiated once for
    each database connection to be established. this
    function is the entry point for any classes attempting
    to access the database
    """

    def __init__(self):
        self.engine = self.create_engine()
        self.SessionMaker = self.create_Sessionmaker()
        self.session = self.create_Session()
        self.DataPackageController = DataPackageTableController.DataPackageTableController()
        self.UserTableController = UserTableController.UserTableController()
        self.VideoStreamTableController = VideoStreamTableController.VideoStreamTableController()
        self.EventTableController = EventTableController.EventTableController()
        self.APIUserController = APIUsersController.APIUsersController()
        self.ActiveEmergencysController = ActiveEmergencysController.ActiveEmergencysController()

    def create_engine(self):
        """
        this function creates the engine and applies all the metadata
        of classes which inherit the base class and applies it to the database
        to create tables.
        TODO: move database path to constants
        :arg
        """
        engine = create_engine(DatabaseConfiguration().DataBaseConnectionString, echo=False)
        Base.metadata.create_all(engine)
        return engine

    def create_Sessionmaker(self):
        SessionMaker = sessionmaker(bind=self.engine)
        return SessionMaker

    def create_Session(self):
        """
        this function creates the session with the server
        via the engine
        :param engine:
        :return:
        """
        session = self.SessionMaker()
        return session

    def create_datapackage(self, **args):
        return self._create(self.DataPackageController, **args)

    def remove_datapackage(self, query="1 == 1"):
        '''
        :param query: this parameter will be used to select which datapackages are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.DataPackageController, query=query)

    def query_datapackage(self, query="1 == 1", column=['*']):
        return self._query(controller=self.DataPackageController, query=query, columns=column)

    def update_datapackage(self, column_value=None, query="1 == 1"):
        return self._update(controller=self.DataPackageController, query=query, column_value=column_value)

    def _create(self, controller, **args):
        controller.create(session=self.session, **args)
        return 1

    def _remove(self, controller, query):
        return controller.delete(session=self.session, query=query)

    def _query(self, controller, query, columns):
        return controller.query(session=self.session, query=query, columns = columns)

    def _update(self, controller, column_value, query):
        return controller.update(session = self.session, column_value=column_value, query=query)

    def create_user(self, **args):
        try:
            return self._create(controller=self.UserTableController, **args)
        except Exception as e:
            self.session.rollback()
            self.session.commit()
    def remove_user(self, query="1 == 1"):
        '''
        :param query: this parameter will be used to select which datapackages are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.UserTableController, query=query)

    def query_user(self, query="1 == 1", column=['*']):
        return self._query(controller=self.UserTableController, query=query, columns=column)

    def update_user(self, column_value=dict(), query="1 == 1"):
        return self._update(controller=self.UserTableController, query=query, column_value=column_value)

    def create_videostream(self, **args):
        return self._create(controller=self.VideoStreamTableController, **args)

    def remove_videostream(self, query="1 == 1"):
        '''
        :param query: this parameter will be used to select which datapackages are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.VideoStreamTableController, query=query)

    def query_videostream(self, query="1 == 1", column=['*']):
        return self._query(controller=self.VideoStreamTableController, query=query, columns=column)

    def update_videostream(self, column_value=dict(), query="1 == 1"):
        return self._update(controller=self.VideoStreamTableController, query=query, column_value=column_value)

    def create_CoT(self, object):
        try:
            session = self.create_Session()
            output = self.EventTableController.create(session, object)
            session.close()
            return output
        except Exception as e:
            session.rollback()
            session.close()
    def remove_CoT(self, query="1 == 1"):
        '''
        :param query: this parameter will be used to select which datapackages are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.EventTableController, query=query)

    def query_CoT(self, query="1 == 1", column=['*']):
        return self._query(controller=self.EventTableController, query=query, columns=column)

    def update_CoT(self, column_value=dict(), query="1 == 1"):
        return self._update(controller=self.EventTableController, query=query, column_value=column_value)

    def create_APIUser(self, **args):
        return self._create(self.APIUserController, **args)

    def remove_APIUser(self, query="1 == 1"):
        '''
        :param query: this parameter will be used to select which datapackages are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.APIUserController, query=query)

    def query_APIUser(self, query="1 == 1", column=['*']):
        return self._query(controller=self.APIUserController, query=query, columns=column)

    def update_APIUser(self, column_value=None, query="1 == 1"):
        return self._update(controller=self.APIUserController, query=query, column_value=column_value)

    def create_ActiveEmergency(self, object):
        try:
            session = self.create_Session()
            self.ActiveEmergencysController.create(session, object)
        except Exception as e:
            session.rollback()
            session.close()
    def remove_ActiveEmergency(self, query="1 == 1"):
        return self._remove(controller=self.ActiveEmergencysController, query=query)

    def query_ActiveEmergency(self, query="1 == 1", column=['*']):
        return self._query(controller=self.ActiveEmergencysController, query=query, columns=column)

    def update_ActiveEmergency(self, column_value=None, query="1 == 1"):
        return self._update(controller=self.ActiveEmergencysController, query=query, column_value=column_value)

    def shutdown_Connection(self):
        self.session.close()
        self.engine.dispose()

if __name__ == "__main__":
    contr = DatabaseController().query_ActiveEmergency()
    x = contr[0]
    y = x.event
    z = y.__dict__
    b = y.detail
    from sqlalchemy.inspection import inspect

    g = y.__mapper__.relationships
    import datetime as dt
    #contr.create_datapackage(uid='9', CreatorUid='abc123', Hash='36e4506f4d6a9582fc60529525c55f3ebd42b887b5164d24e44b85d7ea686a3d', Keywords="foobar", MIMEType="aaa/bbb", Name="other", Privacy=1, Size=32, SubmissionDateTime=dt.datetime.utcnow(), SubmissionUser="blue")
    #contr.remove_APIUser(query='Username == "admin"')
    #contr.remove_datapackage('Hash == "36e4506f4d6a9582fc60529525c55f3ebd42b887b5164d24e44b85d7ea686a3d"')
    #UID = 123
    #callsign = contr.query_user(query=f'uid == "{UID}"', column=['callsign'])
    '''contr.(uid='9', CreatorUid='abc123', Hash='1bc21o', Keywords="foobar", MIMEType="aaa/bbb", Name="other", Privacy=1, Size=32, SubmissionDateTime=dt.datetime.utcnow(), SubmissionUser="blue")
    from FreeTAKServer.controllers.SpecificCoTControllers.SendDropPointController import SendDropPointController
    m = RawCoT()
    m.dbController = contr
    m.xmlString = "<event version='2.0' uid='4oh2-4265fe-83cb-9bd3442e6de0' type='a-h-G' time='2020-05-06T13:29:25.146Z' start='2020-05-06T13:29:25.146Z' stale='2020-05-06T13:34:25.146Z' how='h-g-i-g-o'><point lat='44.22054348420014' lon='-66.14146066424053' hae='9999999.0' ce='9999999.0' le='9999999.0' /><detail><status readiness='true'/><archive/><precisionlocation altsrc='???'/><archive/><usericon iconsetpath='COT_MAPPING_2525B/a-h/a-h-G'/><contact callsign='Bob'/><color argb='-1'/><link uid='ANDROID-352614100054990' production_time='2020-01-20T00:15:03.281Z' type='a-f-G-U-C' parent_callsign='Peregrin' relation='p-p'/><marti><dest callsign = 'abc'/></marti></detail></event>"
    # m.xmlString = "<event version='2.0' uid='87f64797-4ae2-42ce-83cb-9bd3442e6dd0' type='a-h-G' time='2020-05-06T13:29:25.146Z' start='2020-05-06T13:29:25.146Z' stale='2020-05-06T13:34:25.146Z' how='h-g-i-g-o'><point lat='44.22054348420014' lon='-66.14146066424053' hae='9999999.0' ce='9999999.0' le='9999999.0' /><detail/></event>"
    x = SendDropPointController(m)
    b = RawCoT()
    b.dbController = contr
    b.xmlString = '<event version="2.0" uid="5bbka076-caea-4766-a390-1c9ac3f58d00" type="a-n-G" how="h-g-i-g-o" start="2020-09-30T00:56:29.71Z" time="2020-07-18T13:38:31.220Z" stale="2020-10-07T00:56:29.71Z"><detail><status readiness="true"/><usericon iconsetpath="COT_MAPPING_2525B/a-n/a-n-G"/><link uid="ANDROID-359975090666199" relation="p-p" production_time="2020-07-11T17:31:36.007Z" type="a-f-G-U-C" parent_callsign="NOVA"/><color argb="-1"/><precisionlocation altsrc="???"/><contact callsign="N.11.143136"/><remarks time="2020-09-30T00:56:12Z">DEFAULT</remarks><summary/></detail><point le="9999999.0" ce="9999999.0" hae="9999999.0" lon="-61.137312737751884" lat="-11.005735933018565"/></event>'
    x = SendDropPointController(b)
    #y = x.getObject()
    #contr.create_CoT(y.modelObject)
    x = contr.session.query(Event).all()[-1]
    #contr.create_user(callsign = 'abc')
    #import operator
    #a = contr.query_datapackage("uid == 423")'''
