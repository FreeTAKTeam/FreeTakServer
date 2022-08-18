from digitalpy.routing.controller import Controller


class DropPoint(Controller):

    def accept_visitor(self, visitor):
        pass

    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
        
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())

    
    def drop_point_broadcast(self, message, **kwargs):
        self.response.set_values(kwargs)
        domain = _DropPointDomain()
        request = ObjectFactory.get_new_instance('request')
        request.set_action('ParseCoT')
        request.set_value('message', message)
        request.set_value('domain', domain)
        
        actionmapper = ObjectFactory.get_instance('actionMapper')
        response = ObjectFactory.get_new_instance('response')
        
        model_object = domain.create_node(DROP_POINT, BASE_OBJECT_NAME)
        
    def drop_point_recieve(self, **kwargs):
        self.response.set_values(kwargs)
        self.response.set_action("oint_broadcast")