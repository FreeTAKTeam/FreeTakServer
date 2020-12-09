from FreeTAKServer.controllers.DatabaseControllers.TableController import TableController
from FreeTAKServer.model.SQLAlchemy.DataPackage import DataPackage


class DataPackageTableController(TableController):
		
	def __init__(self):
		self.table = DataPackage
