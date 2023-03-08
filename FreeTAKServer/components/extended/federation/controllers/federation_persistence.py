from federation.configuration.federation_constants import PERSISTENCE_PATH
from digitalpy.routing.controller import Controller
import json
import os
import pickle


class FederationPersistence(Controller):
	"""this class is responsible for managing saved components"""

	def __init__(self, request, response, action_mapper, configuration):
		super().__init__(
		request=request,
		response=response,
		action_mapper=action_mapper,
		configuration=configuration,
	)
	self._persistence = {
		"federation": {},
	}

	# create the mapping persistence if it doesn't exist already
		if not os.path.exists(PERSISTENCE_PATH):
			with open(PERSISTENCE_PATH, mode="w+", encoding="utf-8") as f:
				json.dump(self._persistence, f)

	# load the mapping persistence into memory
	with open(PERSISTENCE_PATH, mode="r+", encoding="utf-8") as f:
		self._persistence = json.load(f)
		self.components = self._persistence["components"]

	def execute(self, method=None):
		getattr(self, method)(**self.request.get_values())
		return self.response

	def save_component(self, model_object, **kwargs) -> None:
		"""this method adds a new component to the list of components
		Args:
		 model_object (Event): the new Component model object
		"""
		try:
			component_uid = model_object.uid
			self.components[component_uid] = codecs.encode(
			 pickle.dumps(model_object), "base64"
			).decode()

			self.request.get_value("logger").debug(
			f"added component: {component_uid} to components: {self.components}"
			)
			self._update_persistence()
			except Exception as error:
				self.request.get_value("logger").error(
				f"error adding component to components {error}"
				)

	def delete_component(self, model_object, **kwargs) -> None:
		"""this method removes the specified component from the list of components
		Args:
		component (Event): the Component delete model object
		"""
		del self.components[model_object.uid]
		self._update_persistence()

	def get_all_components(self, **kwargs) -> None:
		"""this method is gets all the saved component objects and returns them
		as a list of component objects"""
		self._sync_persistence()
		components = [
		pickle.loads(codecs.decode(component.encode(), "base-64"))
		for component in self.components.values()
		]
		self.response.set_value("components", list(components))

	def _sync_persistence(self):
		"""synchronize the current, in-memory state, with the persistence"""
		with open(PERSISTENCE_PATH, mode="r", encoding="utf-8") as f:
			self._persistence = json.load(f)

	def _update_persistence(self):
		"""update the persistence with the in memory state"""
		# TODO: this form of persistence runs the risk of causing deletions
		# if it is being written to at the same time, to avoid this we
		# should be using a real database or at least a recognized
		# (preferably ACID) persistence mechanism
		with open(PERSISTENCE_PATH, mode="w", encoding="utf-8") as f:
			json.dump(self._persistence, f)

