from FreeTAKServer.components.core.abstract_component.domain import Domain
from ..configuration.track_manager_constants import CONFIGURATION_PATH_TEMPLATE
from .. import domain
#protectedstart imports ############################################################################
#protectedend ######################################################################################


#protectedstart classDeclaration ###################################################################
class TrackManagerDomain(Domain):
#protectedend ######################################################################################




	"""This class is to be used for all interactions with the Track Manager
	domain model. This class exposes and handles all domain model functions.
	"""
#protectedstart classComments#######################################################################
#protectedend ######################################################################################


	def __init__(self, request, response, configuration, action_mapper):
#protectedstart classVars ##########################################################################
#protectedend ######################################################################################

		super().__init__(
			# the template of the path to the model configurations
			CONFIGURATION_PATH_TEMPLATE,
			# the module containing all the domain objects
			domain,
			# the request object (passed by constructor)
			request=request,
			# the response object (passed by constructor)
			response=response,
			# the configuration object (passed by constructor)
			configuration=configuration,
			# the action mapper (passed by constructor)
			action_mapper=action_mapper,
		)

#protectedstart functions ##########################################################################
#protectedend ######################################################################################


