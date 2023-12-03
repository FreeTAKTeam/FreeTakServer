from flask_httpauth import HTTPTokenAuth
from flask import request
import datetime as dt

auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    from .persistency import dbController
    if token:
        output = dbController.query_APIUser(query=f'token = "{token}"')
        if output:
            return output[0].Username
        else:
            output = dbController.query_systemUser(query=f'token = "{token}"')
            if output:
                output = output[0]
                r = request
                dbController.create_APICall(user_id=output.uid, timestamp=dt.datetime.now(), content=request.data,
                                            endpoint=request.base_url)
                return output.name