
from FreeTAKServer.model.FTSModel.Event import Event
from lxml import etree

class ApplyFullJsonController:
    def __init__(self):
        self.typeDict = {
            'Point': self.point_controller
        }

    def determine_function(self):
        function = self.typeDict[self.type]
        model = function(self.json)
        #model = self.serializeJsonToModel(self.model, json)
        return model

    def point_controller(self, Json):
        JsonFull = self.pointJsonFull
        simpleModelObject = Event.dropPoint(etree.fromstring(JsonFull[1]))
        JsonProcessed = self.serialize_simplified_json_to_comprehensive(Json, JsonFull[0])
        processedModelObject = self.serializeJsonToModel(simpleModelObject, JsonProcessed)
        return processedModelObject

    def serialize_simplified_json_to_comprehensive(self, Json, JsonFull):
        for key, value in Json.items():
            if isinstance(value, dict):
                subJsonFull = JsonFull[key]
                out = self.serialize_simplified_json_to_comprehensive(subJsonFull, value)
                JsonFull[key] = out
            else:
                JsonFull[key] = value
        return JsonFull

    def serializeJsonToModel(self, model, Json):
        for key, value in Json.items():
            if isinstance(value, dict):
                submodel = getattr(model, 'get'+key)
                submodel = submodel()
                out = self.serializeJsonToModel(submodel, value)
                setter = getattr(model, 'set'+key)
                setter(out)
            else:
                setter = getattr(model, 'set' + key)
                setter(value)
        return model

    def serialize_model_to_json(self, modelObject, level = 0):
        json = {}
        for attribName, value in modelObject.__dict__.items():
            if hasattr(value, '__dict__'):
                tagElement = self.serialize_model_to_json(value, level=level + 1)
                # handles instances in which tag name begins with double underscore
                if attribName[0] == '_':
                    tagElement.tag = '_' + tagElement.tag
                    json[attribName] = tagElement
                else:
                    json[attribName] = tagElement

            elif value == None:
                continue

            elif isinstance(value, list):
                for element in value:
                    tagElement = self.serialize_model_to_json(element, attribName, level=level + 1)
                    # handles instances in which tag name begins with double underscore
                    if attribName[0] == '_':
                        tagElement.tag = '_' + tagElement.tag
                        json[attribName] = tagElement
                    else:
                        json[attribName] = tagElement

            # handles text data within tag
            elif attribName == "INTAG":
                json[attribName] = value

            else:
                # handles instances in which attribute name begins with double underscore
                if attribName[0] == '_':
                    json['_' + attribName] = value
                else:
                    json[attribName] = value

        if level == 0:
            return json
        else:
            return json

if __name__ == "__main__":
    ApplyFullJsonController('dwa', 'dwa', 'dwa').determine_function()