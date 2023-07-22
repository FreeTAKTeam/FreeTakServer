from digitalpy.core.component_management.impl.default_facade import DefaultFacade

from FreeTAKServer.components.extended.federation.controllers.federation_general_controller import FederationGeneralController
#protectedstart imports ############################################################################
#protectedend ######################################################################################


#protectedstart classDeclaration ###################################################################
class FederationFacade(DefaultFacade):
#protectedend ######################################################################################




	"""Facade class for the this component. Responsible for handling all public
	routing. Forwards all requests to the internal router.
	WHY:
	<ul>
	<li><b>Isolation</b>: We can easily isolate our code from the complexity of
	a subsystem.</li>
	<li><b>Testing Process</b>: Using Facade Method makes the process of testing
	comparatively easy since it has convenient methods for common testing tasks.
	</li>
	<li><b>Loose Coupling</b>: Availability of loose coupling between the
	clients and the Subsystems.</li>
	</ul>
	"""
#protectedstart classComments#######################################################################
#protectedend ######################################################################################



#	default constructor  def __init__(self):
#protectedstart classVars ##########################################################################
#protectedend ######################################################################################


	def __init__(self):
#protectedstart classVars ##########################################################################
#protectedend ######################################################################################

		self.federation_chat_121 = FederationGeneralController()
		self.federation_chat_all = FederationGeneralController()
		self.federation_connection = FederationGeneralController()
		self.federation_create_presence = FederationGeneralController()
		self.federation_delete_presence = FederationGeneralController()
		self.federation_send_cot = FederationGeneralController()
		self.federation_share_files = FederationGeneralController()
		self.federation_update_presence = FederationGeneralController()
		self.federation_connection_legacy_tak_server = FederationGeneralController()
		self.federation_disconnect_from_server = FederationGeneralController()
		self.federation_delete_presence = FederationGeneralController()
		self.federation_chat_all = FederationGeneralController()
		self.federation_connection = FederationGeneralController()
		self.federation_share_files = FederationGeneralController()
		self.federation_disconnect_from_server = FederationGeneralController()
		self.federation_chat_121 = FederationGeneralController()
		self.federation_broadcast_cot = FederationGeneralController()
		self.federation_send_cot = FederationGeneralController()
		self.federation_create_presence = FederationGeneralController()
		self.federation_update_presence = FederationGeneralController()
		self.federation_connection_legacy_tak_server = FederationGeneralController()

#protectedstart functions ##########################################################################
#protectedend ######################################################################################


