class FilterGroup:
    def __init__(self):
        # an array of pipes to receive data from
        self.sources = []

        # an array of pipes to send data too
        self.receivers = []

        # an array of types of CoT which can be received by this group
        self.allowedType = ['*']

        # an array of types of CoT which can't be received by this group
        self.rejectedType = []

    def add_source(self, source):
        self.sources.append(source)
    
    def remove_source(self, source):
        self.sources.remove(source)
        
    def get_sources(self):
        return self.receivers

    def add_receiver(self, source):
        self.receivers.append(source)
    
    def remove_receiver(self, source):
        self.receivers.remove(source)
        
    def get_receivers(self):
        return self.receivers
    
    def add_allowed_type(self, type):
        self.allowedType.append(type)

    def remove_allowed_type(self, type):
        self.allowedType.remove(type)

    def get_allowed_types(self):
        return self.allowedType

    def check_if_type_is_allowed(self, type):
        if type in self.allowedType and type not in self.rejectedType or self.allowedType == ['*'] and type not in self.rejectedType:
            return True

        else:
            return False