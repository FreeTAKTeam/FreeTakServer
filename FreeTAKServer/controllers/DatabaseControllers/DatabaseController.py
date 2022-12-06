import FreeTAKServer.controllers.DatabaseControllers.table_controllers
from FreeTAKServer.controllers.DatabaseControllers import DataPackageTableController, system_user_table_controller
from FreeTAKServer.controllers.DatabaseControllers import VideoStreamTableController
from FreeTAKServer.controllers.DatabaseControllers import EventTableController
from FreeTAKServer.controllers.persistence import ActiveEmergencysController
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import make_transient
from sqlalchemy.exc import IntegrityError
from FreeTAKServer.model.SQLAlchemy.Root import Base
from FreeTAKServer.controllers.configuration.DatabaseConfiguration import DatabaseConfiguration
from FreeTAKServer.controllers.DatabaseControllers import APIUsersController
from FreeTAKServer.controllers.DatabaseControllers import ExCheckController
from FreeTAKServer.controllers.DatabaseControllers import ExCheckChecklistController
from FreeTAKServer.controllers.DatabaseControllers import API_call_controller
from FreeTAKServer.controllers.persistence import _VideoTableController
from FreeTAKServer.controllers.DatabaseControllers.table_controllers import ActiveFederationsController, UserTableController, FederationsController
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
from FreeTAKServer.model.SQLAlchemy.User import User
import FreeTAKServer.model.SQLAlchemy.APIUsers
import FreeTAKServer.model.SQLAlchemy.system_user
import FreeTAKServer.model.SQLAlchemy.ActiveEmergencys
import FreeTAKServer.model.SQLAlchemy.ExCheckKeywords
import FreeTAKServer.model.SQLAlchemy.ExCheckData
import FreeTAKServer.model.SQLAlchemy.ExCheck
import FreeTAKServer.model.SQLAlchemy.ExCheckChecklist
import FreeTAKServer.model.SQLAlchemy.APICalls

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
        self.UserTableController = UserTableController()
        self.SystemUserTableController = system_user_table_controller.SystemUserTableController()
        self.VideoStreamTableController = VideoStreamTableController.VideoStreamTableController()
        self._VideoTableController = _VideoTableController._VideoTableController()
        self.EventTableController = EventTableController.EventTableController()
        self.APIUserController = APIUsersController.APIUsersController()
        self.ActiveEmergencysController = ActiveEmergencysController.ActiveEmergencysController()
        self.ExCheckController = ExCheckController.ExCheckController()
        self.ExCheckChecklistController = ExCheckChecklistController.ExCheckChecklistController()
        self.ActiveFederationController = ActiveFederationsController()
        self.FederationController = FederationsController()
        self.APICallController = API_call_controller.APICallController()

    def create_engine(self):
        """
        this function creates the engine and applies all the metadata
        of classes which inherit the base class and applies it to the database
        to create tables.
        :arg
        """
        engine = create_engine(DatabaseConfiguration().DataBaseConnectionString, echo=False)
        if engine.dialect.has_table(engine, 'SystemUser') == False:
            Base.metadata.create_all(engine)
            tempsession = sessionmaker(bind=engine)()
            tempsession.add(FreeTAKServer.model.SQLAlchemy.system_user.SystemUser(uid="1", name="admin", password="password", token="token", device_type="mobile"))
            tempsession.commit()
            tempsession.close()
            return engine
        else:
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

    def remove_datapackage(self, query="1=1"):
        '''
        :param query: this parameter will be used to select which datapackages are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.DataPackageController, query=query)

    def query_datapackage(self, query="1=1", column=['*']):
        return self._query(controller=self.DataPackageController, query=query, columns=column)

    def update_datapackage(self, column_value=None, query="1=1"):
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
        except IntegrityError as e:
            if str(e) == """(sqlite3.IntegrityError) UNIQUE constraint failed: User.uid
[SQL: INSERT INTO "User" (uid, callsign, "CN", "IP", "CoT_id") VALUES (?, ?, ?, ?, ?)]
[parameters: ('S-1-5-21-2720623347-3037847324-4167270909-1002', 'FEAR', None, '192.168.2.75', 'S-1-5-21-2720623347-3037847324-4167270909-1002')]
(Background on this error at: http://sqlalche.me/e/13/gkpj)""":
                self.session.rollback()
                user2 = User(**args)
                self.session.merge(user2)
                self.session.commit()
                """ self.session.rollback()
                self.session.close()
                self.session = self.create_Session()
                obj = self.query_user(f'uid == "{args["uid"]}"')[0]
                self.session.delete(obj)
                self.session.expire(obj)
                self.session.commit()
                del obj
                self.session.close()
                self.session = self.create_Session()
                return self._create(controller=self.UserTableController, **args)"""
            else:
                self.session.rollback()
                user2 = User(**args)
                self.session.merge(user2.CoT)
                self.session.commit()
                """print(e)
                self.session.rollback()
                self.session.close()
                self.session = self.create_Session()
                obj = self.query_CoT(f'uid == "{args["CoT"].uid}"')[0]
                self.session.delete(obj)
                self.session.commit()
                del obj
                return self._create(controller=self.UserTableController, **args)"""
        except Exception as e:
            print(e)
            try:
                self.session.rollback()
                self.session.close()
                self.session = self.create_Session()
                obj = self.query_CoT(f'uid = "{args["CoT"].uid}"')[0]
                self.session.delete(obj)
                self.session.commit()
                return self._create(controller=self.UserTableController, **args)
            except Exception as e:
                self.session.rollback()
                self.session.close()
                self.session = self.create_Session()
                raise Exception(e)
    def remove_user(self, query="1=1"):
        '''
        :param query: this parameter will be used to select which datapackages are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.UserTableController, query=query)

    def query_user(self, query="1=1", column=['*']):
        return self._query(controller=self.UserTableController, query=query, columns=column)

    def update_user(self, column_value=dict(), query="1=1"):
        return self._update(controller=self.UserTableController, query=query, column_value=column_value)

    def create_systemUser(self, **args):
        try:
            return self._create(controller=self.SystemUserTableController, **args)
        except Exception as e:
            print(e)
            self.session.rollback()
            self.session.commit()
            raise Exception(e)
    def remove_systemUser(self, query="1=1"):
        return self._remove(controller=self.SystemUserTableController, query=query)

    def query_systemUser(self, query="1=1", column=['*']):
        return self._query(controller=self.SystemUserTableController, query=query, columns=column)

    def update_systemUser(self, column_value=dict, query="1=1"):
        return self._update(controller=self.SystemUserTableController, query=query, column_value=column_value)

    def create_videostream(self, **args):
        return self._create(controller=self.VideoStreamTableController, **args)

    def remove_videostream(self, query="1=1"):
        '''
        :param query: this parameter will be used to select which datapackages are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self._VideoTableController, query=query)

    def query_videostream(self, query="1=1", column=['*']):
        return self._query(controller=self._VideoTableController, query=query, columns=column)

    def update_videostream(self, column_value=dict(), query="1=1"):
        return self._update(controller=self._VideoTableController, query=query, column_value=column_value)

    def create_vide(self, **args):
        return self._create(controller=self._VideoTableController, **args)

    def remove_vide(self, query="1=1"):
        '''
        :param query: this parameter will be used to select which datapackages are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.VideoStreamTableController, query=query)

    def query_video(self, query="1=1", column=['*']):
        return self._query(controller=self._VideoTableController, query=query, columns=column)

    def update_video(self, column_value=dict(), query="1=1"):
        return self._update(controller=self.VideoStreamTableController, query=query, column_value=column_value)

    def create_CoT(self, object):
        try:
            session = self.create_Session()
            output = self.EventTableController.create(session, object)
            session.close()
            return output
        except IntegrityError as e:
            try:
                session.rollback()
                session.close()
                obj = self.query_CoT(f'uid = "{object.uid}"')[0]
                newobj = self.EventTableController.convert_model_to_row(object)
                self.session.delete(obj)
                self.session.commit()
                make_transient(obj)
                newobj.User = obj.User

                self.session.add(newobj)
                self.session.commit()
            except Exception as e:
                raise e
        except Exception as e:
            self.session.rollback()
    def remove_CoT(self, query="1=1"):
        '''
        :param query: this parameter will be used to select which datapackages are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.EventTableController, query=query)

    def query_CoT(self, query="1=1", column=['*']):
        return self._query(controller=self.EventTableController, query=query, columns=column)

    def update_CoT(self, column_value=dict(), query="1=1"):
        return self._update(controller=self.EventTableController, query=query, column_value=column_value)

    def create_APIUser(self, **args):
        return self._create(self.APIUserController, **args)

    def remove_APIUser(self, query="1=1"):
        '''
        :param query: this parameter will be used to select which datapackages are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.APIUserController, query=query)

    def query_APIUser(self, query="1=1", column=['*']):
        return self._query(controller=self.APIUserController, query=query, columns=column)

    def update_APIUser(self, column_value=None, query="1=1"):
        return self._update(controller=self.APIUserController, query=query, column_value=column_value)

    def create_ActiveEmergency(self, object):
        try:
            session = self.create_Session()
            self.ActiveEmergencysController.create(session, object)
        except Exception as e:
            print(e)
            session.rollback()
            session.close()
            raise Exception(e)

    def remove_ActiveEmergency(self, query="1=1"):
        return self._remove(controller=self.ActiveEmergencysController, query=query)

    def query_ActiveEmergency(self, query="1=1", column=['*']):
        return self._query(controller=self.ActiveEmergencysController, query=query, columns=column)

    def update_ActiveEmergency(self, column_value=None, query="1=1"):
        return self._update(controller=self.ActiveEmergencysController, query=query, column_value=column_value)


    def create_ExCheck(self, object):
        try:
            session = self.create_Session()
            output = self.ExCheckController.create(session, object)
            session.close()
            return output
        except Exception as e:
            session.rollback()
            session.close()

    def remove_ExCheck(self, query="1=1"):
        return self._remove(controller=self.ExCheckController, query=query)

    def query_ExCheck(self, query = "1=1", column=["*"], verbose = False):
        if verbose == False:
            return self._query(controller=self.ExCheckController, query=query, columns=column)
        else:
            return self.ExCheckController.queryChildren(query, column, self.session)
    def update_ExCheck(self, query="1=1", column_value=None):
        return self._update(controller=self.ExCheckController, query=query, column_value=column_value)

    def create_Excheckchecklist(self, **args):
        return self._create(self.ExCheckChecklistController, **args)

    def remove_ExCheckChecklist(self, query="1=1"):
        '''
        :param query: this parameter will be used to select which exCheckChecklists are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.ExCheckChecklistController, query=query)

    def query_ExCheckChecklist(self, query="1=1", column=['*']):
        return self._query(controller=self.ExCheckChecklistController, query=query, columns=column)

    def update_ExCheckChecklist(self, column_value=None, query="1=1"):
        return self._update(controller=self.ExCheckChecklistController, query=query, column_value=column_value)

    def create_ActiveFederation(self, **args):
        return self._create(self.ActiveFederationController, **args)

    def remove_ActiveFederation(self, query="1=1"):
        '''
        :param query: this parameter will be used to select which exCheckChecklists are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.ActiveFederationController, query=query)

    def query_ActiveFederation(self, query="1=1", column=['*']):
        return self._query(controller=self.ActiveFederationController, query=query, columns=column)

    def update_ActiveFederation(self, column_value=None, query="1=1"):
        return self._update(controller=self.ActiveFederationController, query=query, column_value=column_value)

    def create_Federation(self, **args):
        return self._create(self.FederationController, **args)

    def remove_Federation(self, query="1=1"):
        '''
        :param query: this parameter will be used to select which exCheckChecklists are deleted
        :return: 1 on success
        '''
        return self._remove(controller=self.FederationController, query=query)

    def query_Federation(self, query="1=1", column=['*']):
        return self._query(controller=self.FederationController, query=query, columns=column)

    def update_Federation(self, column_value=None, query="1=1"):
        return self._update(controller=self.FederationController, query=query, column_value=column_value)

    def create_APICall(self, **args):
        return self._create(self.APICallController, **args)

    def remove_APICall(self, query="1=1"):
        return self._remove(controller = self.APICallController, query = query)

    def query_APICall(self, query="1=1", column=["*"]):
        return self._query(controller=self.APICallController, query=query, columns=column)

    def update_APICall(self, column_value = None, query="1=1"):
        return self._update(controller=self.APICallController, query=query, column_value=column_value)

    def shutdown_Connection(self):
        self.session.close()
        self.engine.dispose()
