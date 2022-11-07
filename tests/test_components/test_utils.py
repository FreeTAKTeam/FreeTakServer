from digitalpy.core.object_factory import ObjectFactory


def execute_action(action: str, values: dict) -> dict:
    """execute a specific action given a list of values to be in the request object."""
    request = ObjectFactory.get_new_instance("request")
    request.set_action(action)
    request.set_values(values)

    actionmapper = ObjectFactory.get_instance("sync_actionMapper")
    response = ObjectFactory.get_new_instance("response")

    actionmapper.process_action(request, response)

    return response.get_values()


def execute_async_action(action: str, values: dict) -> dict:
    """execute a specific async action given a list of values to be in the request object"""
    request = ObjectFactory.get_new_instance("request")
    request.set_action(action)
    request.set_values(values)

    actionmapper = ObjectFactory.get_instance("actionMapper")
    response = ObjectFactory.get_new_instance("response")

    request.set_format("pickled")
    response.set_format("pickled")

    listener = actionmapper.process_action(request, response, True)

    actionmapper.get_response(response, request, listener)

    return response.get_values()
