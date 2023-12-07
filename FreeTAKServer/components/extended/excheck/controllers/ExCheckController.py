import os
import hashlib
import uuid
import json
from datetime import datetime
from os import listdir
from pathlib import Path, PurePath
from xml.etree.ElementTree import Element

from defusedxml import ElementTree as etree
from flask import request
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.persistence.DatabaseController import DatabaseController
from FreeTAKServer.core.parsers.templateToJsonSerializer import templateSerializer
from FreeTAKServer.core.parsers.XMLCoTController import XMLCoTController
from FreeTAKServer.model.testobj import testobj
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.RawCoT import RawCoT

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

if not os.path.exists(config.ExCheckMainPath):
    os.mkdir(config.ExCheckMainPath)

if not os.path.exists(config.ExCheckChecklistFilePath):
    os.mkdir(config.ExCheckChecklistFilePath)

if not os.path.exists(config.ExCheckFilePath):
    os.mkdir(config.ExCheckFilePath)

loggingConstants = LoggingConstants(log_name="ExCheckController")
logger = CreateLoggerController("ExCheckController", logging_constants=loggingConstants).getLogger()

# TODO: remove string
XML_TEMPLATE_STR = f'<?xml version="1.0"?><event version="2.0" uid="{uuid.uuid4()}" type="t-x-m-c" time="2020-11-28T17:45:51.000Z" start="2020-11-28T17:45:51.000Z" stale="2020-11-28T17:46:11.000Z" how="h-g-i-g-o"><point lat="0.00000000" lon="0.00000000" hae="0.00000000" ce="9999999" le="9999999" /><detail><mission type="CHANGE" tool="ExCheck" name="exchecktemplates" authorUid="S-1-5-21-2720623347-3037847324-4167270909-1002"><MissionChanges><MissionChange><contentResource><filename>61b01475-ad44-4300-addc-a9474ebf67b0.xml</filename><hash>018cd5786bd6c2e603beef30d6a59987b72944a60de9e11562297c35ebdb7fd6</hash><keywords>test init</keywords><keywords>dessc init</keywords><keywords>FEATHER</keywords><mimeType>application/xml</mimeType><name>61b01475-ad44-4300-addc-a9474ebf67b0</name><size>1522</size><submissionTime>2020-11-28T17:45:47.980Z</submissionTime><submitter>wintak</submitter><tool>ExCheck</tool><uid>61b01475-ad44-4300-addc-a9474ebf67b0</uid></contentResource><creatorUid>S-1-5-21-2720623347-3037847324-4167270909-1002</creatorUid><missionName>exchecktemplates</missionName><timestamp>2020-11-28T17:45:47.983Z</timestamp><type>ADD_CONTENT</type></MissionChange></MissionChanges></mission></detail></event>'

class ExCheckController:
    def __init__(self) -> None:
        self.dbController = DatabaseController()
        self.logger = logger

    def exchecktemplates(self):
        try:
            return templateSerializer().convert_object_to_json(DatabaseController().query_ExCheck())
        except Exception as e:
            self.logger.error(str(e))

    def get_excheck_item(self, hash, uid):
        if hash == None:
            hash_val = "*"
        if uid == None:
            uid_val = "*"
        return templateSerializer().convert_object_to_json(DatabaseController().query_ExCheck(query=f"uid={uid_val} and hash={hash_val}"))

    def template(self, pipe):
        try:
            # this is where the client will post the xmi of a template
            # possibly the uid of the client submitting the template
            uid = request.args.get('clientUid')
            XMI = request.data.decode()
            PIPE = pipe
            serializer = templateSerializer(XMI)
            object = serializer.convert_template_to_object()
            object.timestamp = datetime.strptime(object.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            serializer.create_DB_object(object)
            # TODO add proper sanitation
            # if not sanitize_path_input(object.data.uid):
            #     return "invalid uid sent", 500
            path = str(PurePath(Path(config.ExCheckFilePath), Path(f'{object.data.uid}.xml')))
            with open(path, 'w+') as file:
                file.write(XMI)
                file.close()

            uid = object.data.uid
            temp = etree.fromstring(XMI)
            cot = etree.fromstring(XML_TEMPLATE_STR)
            resources = cot.find('detail').find('mission').find('MissionChanges').find('MissionChange').find(
                'contentResource')
            resources.find('filename').text = temp.find('checklistDetails').find('uid').text + '.xml'
            resources.findall('keywords')[0].text = temp.find('checklistDetails').find('name').text
            resources.findall('keywords')[1].text = temp.find('checklistDetails').find('description').text
            resources.findall('keywords')[2].text = temp.find('checklistDetails').find('creatorCallsign').text
            resources.find('uid').text = temp.find('checklistDetails').find('uid').text
            resources.find('name').text = temp.find('checklistDetails').find('uid').text
            resources.find('size').text = str(len(XMI))
            resources.find('hash').text = str(hashlib.sha256(str(XMI).encode()).hexdigest())
            z = etree.tostring(cot)
            object = testobj()
            object.xmlString = z
            PIPE.put(object)
            return str(uid), 200
        except Exception as e:
            print(str(e))

    def startList(self, subscription):
        uid = str(uuid.uuid4())
        r = request
        # client uid
        request.args.get('clientUid')
        # name of template
        request.args.get('name')
        # description of template
        request.args.get('description')
        # startTime of template
        startTime = request.args.get('startTime')
        # callsign of submission user
        request.args.get('callsign')

        # TODO implement proper sanitation
        # if not sanitize_path_input(subscription):
        #     return "invalid subscription sent", 500

        with open(str(PurePath(Path(config.ExCheckChecklistFilePath), Path(f'{uid}.xml'))), 'w+') as file:
            file.write(str(open(str(PurePath(Path(config.ExCheckFilePath), Path(f'{subscription}.xml'))), 'r').read()))
            file.close()

        xml = etree.parse(
            config.ExCheckChecklistFilePath + '/' + uid + '.xml').getroot()

        starttime = Element('startTime')
        starttime.text = startTime
        details = xml.find('checklistDetails')
        if details.find('startTime') is None:
            details.append(starttime)
        else:
            details.find('startTime').text = startTime
        uids = details.find('uid')
        uids.text = uid
        details.find('description').text = request.args.get('description')
        details.find('name').text = request.args.get('name')

        tasks = xml.find('checklistTasks')
        for task in tasks:
            taskuid = task.find('uid')
            taskuid.text = str(uuid.uuid4())

        with open(
                str(PurePath(Path(config.ExCheckChecklistFilePath), Path(uid + '.xml'))),
                'w+') as file:
            file.write(etree.tostring(xml).decode())
            file.close()

        excheckobj = self.dbController.query_ExCheck(f'ExCheckData.uid = "{subscription}"', verbose=True)[0]
        self.dbController.create_Excheckchecklist(
            startTime=datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S.%fZ'),
            creatorUid=request.args.get('clientUid'),
            description=request.args.get('description'),
            callsign=request.args.get('callsign'),
            name=request.args.get('name'), uid=uid,
            filename=f'{uid}.xml', template=excheckobj
        )

        return str(open(str(PurePath(Path(config.ExCheckChecklistFilePath), Path(uid + '.xml'))), 'r').read()), 200

    def update_checklist(self):
        excheck_xml = etree.fromstring(request.data)
        uid = excheck_xml.find('checklistDetails').find('uid').text

        # client uid
        request.args.get('clientUid')

        # TODO implement proper sanitation
        # if not sanitize_path_input(uid):
        #     return "uid", 500

        with open(str(PurePath(Path(config.ExCheckChecklistFilePath), Path(f'{uid}.xml'))), 'wb+') as file:
            file.write(request.data)
            file.close()

        return str(open(str(PurePath(Path(config.ExCheckChecklistFilePath), Path(uid + '.xml'))), 'r').read()), 200

    def accesschecklist(self, checklistid):
        # TODO implement proper sanitation
        # if not sanitize_path_input(checklistid):
        #     return "invalid checklistid sent", 500
        return str(open(str(PurePath(Path(config.ExCheckChecklistFilePath), Path(checklistid + '.xml'))), 'r').read())

    def updatetemplate(self, checklistid, taskid, pipe):
        data = request.data
        PIPE = pipe
        # TODO implement proper sanitation
        # if not sanitize_path_input(checklistid):
        #     return "invalid checklistid sent", 500
        xml = etree.parse(str(PurePath(Path(config.ExCheckChecklistFilePath), Path(checklistid + '.xml')))).getroot()
        updatedTask = etree.fromstring(data)
        tasks = xml.find('checklistTasks')
        index = 0
        for task in tasks:
            index += 1
            uid = task.find('uid')
            if uid.text == taskid:
                tasks.remove(task)
                tasks.insert(index, updatedTask)
            else:
                pass
        with open(
                str(PurePath(Path(config.ExCheckChecklistFilePath), Path(checklistid + '.xml'))), 'w+') as file:
            file.write(etree.tostring(xml).decode())
            file.close()

        # Create Object to send to client
        object = Event.ExcheckUpdate()
        object.setuid(str(uuid.uuid4()))
        object.setversion('2.0')
        object.detail.mission.settype("CHANGE")
        object.detail.mission.settool("ExCheck")
        object.detail.mission.setname(checklistid)
        object.detail.mission.setauthorUid(request.args.get("clientUid"))
        object.detail.mission.MissionChanges.MissionChange.creatorUid.setINTAG(request.args.get("clientUid"))
        object.detail.mission.MissionChanges.MissionChange.missionName.setINTAG(checklistid)
        object.detail.mission.MissionChanges.MissionChange.type.setINTAG("ADD_CONTENT")
        object.detail.mission.MissionChanges.MissionChange.contentResource.filename.setINTAG(taskid + '.xml')
        object.detail.mission.MissionChanges.MissionChange.contentResource.hash.setINTAG(str(hashlib.sha256(
            str(open(config.ExCheckChecklistFilePath + '/' + checklistid + '.xml', 'r')).encode()).hexdigest()))
        object.detail.mission.MissionChanges.MissionChange.contentResource.keywords.setINTAG('Task')
        object.detail.mission.MissionChanges.MissionChange.contentResource.name.setINTAG(taskid)
        object.detail.mission.MissionChanges.MissionChange.contentResource.size.setINTAG(str(len(data)))
        # TODO: change this value
        object.detail.mission.MissionChanges.MissionChange.contentResource.submitter.setINTAG('atak')
        object.detail.mission.MissionChanges.MissionChange.contentResource.uid.setINTAG(taskid)

        '''object = etree.fromstring(templateex)
        object.uid = uuid.uuid4()
        object.find('detail').find('mission').type= "CHANGE"
        object.find('detail').find('mission').name = taskid
        object.find('detail').find('mission').Uid = request.args.get("clientUid")
        object.find('detail').find('mission').find('MissionChanges').find('MissionChange').find('creatorUid').text = request.args.get("clientUid")
        object.find('detail').find('mission').find('MissionChanges').find('MissionChange').find('missionName').text = taskid
        object.find('detail').find('mission').find('MissionChanges').find('MissionChange').find('filename').text = checklistid+'.xml'
        object.detail.mission.MissionChanges.MissionChange.contentResource.hash.setINTAG(str(hashlib.sha256(str(data).encode()).hexdigest()))
        object.detail.mission.MissionChanges.MissionChange.contentResource.keywords.setINTAG('Task')
        object.detail.mission.MissionChanges.MissionChange.contentResource.name.setINTAG(checklistid)
        object.detail.mission.MissionChanges.MissionChange.contentResource.size.setINTAG(str(len(data)))
        #TODO: change this value
        object.detail.mission.MissionChanges.MissionChange.contentResource.submitter.setINTAG('test')
        object.detail.mission.MissionChanges.MissionChange.contentResource.uid.setINTAG(checklistid)'''
        rawcot = RawCoT()
        xml = XMLCoTController().serialize_model_to_CoT(object)
        rawcot.xmlString = xml

        PIPE.put(rawcot)
        # PIPE.send()

        return '', 200

    def activechecklists(self):
        rootxml = Element('checklists')

        for file in listdir(config.ExCheckChecklistFilePath):
            try:
                checklist = Element('checklist')
                xmldetails = etree.parse(
                    str(PurePath(Path(config.ExCheckChecklistFilePath), Path(file)))
                ).getroot().find('checklistDetails')
                checklist.append(xmldetails)
                checklist.append(Element('checklistColumns'))
                checklist.append(Element('checklistTasks'))
                rootxml.append(checklist)
            except Exception as e:
                logger.info(str(e))
                continue
        xml = etree.tostring(rootxml)
        return xml

    def excheck_table(self, request, pipe):
        try:
            if request.method == "GET":
                jsondata = {"ExCheck": {'Templates': [], 'Checklists': []}}
                excheckTemplates = DatabaseController().query_ExCheck()
                for template in excheckTemplates:
                    templateData = template.data
                    templatejson = {
                        "filename": templateData.filename,
                        "name": templateData.keywords.name,
                        "submissionTime": templateData.submissionTime,
                        "submitter": str(
                            self.dbController.query_user(query=f'uid = "{template.creatorUid}"', column=['callsign'])),
                        "uid": templateData.uid,
                        "hash": templateData.hash,
                        "size": templateData.size,
                        "description": templateData.keywords.description
                    }
                    jsondata["ExCheck"]['Templates'].append(templatejson)
                excheckChecklists = DatabaseController().query_ExCheckChecklist()
                for checklist in excheckChecklists:
                    try:
                        templatename = checklist.template.data.name
                    except AttributeError:
                        templatename = "template removed"
                    checklistjson = {
                        "filename": checklist.filename,
                        "name": checklist.name,
                        "startTime": datetime.strftime(checklist.startTime, "%Y-%m-%dT%H:%M:%S.%fZ"),
                        "submitter": checklist.callsign,
                        "uid": checklist.uid,
                        "description": checklist.description,
                        "template": templatename
                    }
                    jsondata["ExCheck"]['Checklists'].append(checklistjson)
                return json.dumps(jsondata), 200

            elif request.method == "DELETE":
                jsondata = request.data
                ExCheckArray = json.loads(jsondata)["ExCheck"]
                for item in ExCheckArray["Templates"]:
                    templateitem = DatabaseController().query_ExCheck(
                        f'ExCheckData.uid = "{item["uid"]}"', verbose=True)[0]
                    os.remove(str(PurePath(Path(config.ExCheckFilePath),
                            Path(templateitem.data.filename))))
                    DatabaseController().remove_ExCheck(
                        f'PrimaryKey = "{templateitem.PrimaryKey}"')
                for item in ExCheckArray["Checklists"]:
                    checklistitem = DatabaseController().query_ExCheckChecklist(
                        f'uid = "{item["uid"]}"')[0]
                    os.remove(str(
                        PurePath(Path(config.ExCheckChecklistFilePath), Path(checklistitem.filename))))
                    DatabaseController().remove_ExCheckChecklist(
                        f'uid = "{item["uid"]}"')
                return 'success', 200
            elif request.method == "POST":
                try:
                    xmlstring = f'<?xml version="1.0"?><event version="2.0" uid="{uuid.uuid4()}" type="t-x-m-c" time="2020-11-28T17:45:51.000Z" start="2020-11-28T17:45:51.000Z" stale="2020-11-28T17:46:11.000Z" how="h-g-i-g-o"><point lat="0.00000000" lon="0.00000000" hae="0.00000000" ce="9999999" le="9999999" /><detail><mission type="CHANGE" tool="ExCheck" name="exchecktemplates" authorUid="S-1-5-21-2720623347-3037847324-4167270909-1002"><MissionChanges><MissionChange><contentResource><filename>61b01475-ad44-4300-addc-a9474ebf67b0.xml</filename><hash>018cd5786bd6c2e603beef30d6a59987b72944a60de9e11562297c35ebdb7fd6</hash><keywords>test init</keywords><keywords>dessc init</keywords><keywords>FEATHER</keywords><mimeType>application/xml</mimeType><name>61b01475-ad44-4300-addc-a9474ebf67b0</name><size>1522</size><submissionTime>2020-11-28T17:45:47.980Z</submissionTime><submitter>wintak</submitter><tool>ExCheck</tool><uid>61b01475-ad44-4300-addc-a9474ebf67b0</uid></contentResource><creatorUid>S-1-5-21-2720623347-3037847324-4167270909-1002</creatorUid><missionName>exchecktemplates</missionName><timestamp>2020-11-28T17:45:47.983Z</timestamp><type>ADD_CONTENT</type></MissionChange></MissionChanges></mission></detail></event>'
                    # this is where the client will post the xmi of a template
                    # possibly the uid of the client submitting the template
                    authoruid = request.args.get('clientUid')
                    if not authoruid:
                        authoruid = 'server-uid'
                    XMI = request.data.decode()
                    serializer = templateSerializer(XMI)
                    object = serializer.convert_template_to_object()
                    object.timestamp = datetime.strptime(
                        object.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                    serializer.create_DB_object(object)
                    xml = etree.fromstring(XMI)
                    path = str(PurePath(Path(config.ExCheckFilePath),
                            Path(f'{object.data.uid}.xml')))
                    with open(path, 'w+') as file:
                        file.write(XMI)
                        file.close()

                    uid = object.data.uid
                    temp = etree.fromstring(XMI)
                    cot = etree.fromstring(xmlstring)
                    cot.find('detail').find('mission').set("authorUid", authoruid)
                    resources = cot.find('detail').find('mission').find('MissionChanges').find('MissionChange').find(
                        'contentResource')
                    resources.find('filename').text = temp.find(
                        'checklistDetails').find('uid').text + '.xml'
                    resources.findall('keywords')[0].text = temp.find(
                        'checklistDetails').find('name').text
                    resources.findall('keywords')[1].text = temp.find(
                        'checklistDetails').find('description').text
                    resources.findall('keywords')[2].text = temp.find(
                        'checklistDetails').find('creatorCallsign').text
                    resources.find('uid').text = temp.find(
                        'checklistDetails').find('uid').text
                    resources.find('name').text = temp.find(
                        'checklistDetails').find('uid').text
                    resources.find('size').text = str(len(XMI))
                    resources.find('hash').text = str(
                        hashlib.sha256(str(XMI).encode()).hexdigest())
                    z = etree.tostring(cot)
                    object = testobj()
                    object.xmlString = z
                    pipe.put(object)
                    return str(uid), 200
                except Exception as e:
                    print(str(e))
        except Exception as e:
            return str(e), 500
