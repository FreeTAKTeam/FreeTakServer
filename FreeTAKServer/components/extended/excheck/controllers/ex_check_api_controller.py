import connexion
import six

from swagger_server.models.checklist import Checklist  # noqa: E501
from swagger_server.models.checklist_task import ChecklistTask  # noqa: E501
from swagger_server import util


def add_edit_checklist_task(body, client_uid, checklist_uid, task_uid):  # noqa: E501
    """add_edit_checklist_task

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param client_uid: 
    :type client_uid: str
    :param checklist_uid: 
    :type checklist_uid: str
    :param task_uid: 
    :type task_uid: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = ChecklistTask.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def add_edit_template_task(body, client_uid, template_uid, task_uid):  # noqa: E501
    """add_edit_template_task

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param client_uid: 
    :type client_uid: str
    :param template_uid: 
    :type template_uid: str
    :param task_uid: 
    :type task_uid: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = ChecklistTask.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def add_mission_reference_to_checklist(checklist_uid, mission_name, client_uid, password=None):  # noqa: E501
    """add_mission_reference_to_checklist

     # noqa: E501

    :param checklist_uid: 
    :type checklist_uid: str
    :param mission_name: 
    :type mission_name: str
    :param client_uid: 
    :type client_uid: str
    :param password: 
    :type password: str

    :rtype: str
    """
    return 'do some magic!'


def create_checklist(body, client_uid, default_role=None):  # noqa: E501
    """create_checklist

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param client_uid: 
    :type client_uid: str
    :param default_role: 
    :type default_role: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = Checklist.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_checklist(checklist_uid, client_uid):  # noqa: E501
    """delete_checklist

     # noqa: E501

    :param checklist_uid: 
    :type checklist_uid: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def delete_checklist_task(checklist_uid, task_uid, client_uid):  # noqa: E501
    """delete_checklist_task

     # noqa: E501

    :param checklist_uid: 
    :type checklist_uid: str
    :param task_uid: 
    :type task_uid: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def delete_template(template_uid, client_uid):  # noqa: E501
    """delete_template

     # noqa: E501

    :param template_uid: 
    :type template_uid: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def delete_template_task(template_uid, task_uid, client_uid):  # noqa: E501
    """delete_template_task

     # noqa: E501

    :param template_uid: 
    :type template_uid: str
    :param task_uid: 
    :type task_uid: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def get_checklist(checklist_uid, client_uid=None, secago=None, token=None):  # noqa: E501
    """get_checklist

     # noqa: E501

    :param checklist_uid: 
    :type checklist_uid: str
    :param client_uid: 
    :type client_uid: str
    :param secago: 
    :type secago: int
    :param token: 
    :type token: str

    :rtype: str
    """
    return 'do some magic!'


def get_checklist1(client_uid):  # noqa: E501
    """get_checklist1

     # noqa: E501

    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def get_checklist_status(checklist_uid, token=None, client_uid=None):  # noqa: E501
    """get_checklist_status

     # noqa: E501

    :param checklist_uid: 
    :type checklist_uid: str
    :param token: 
    :type token: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def get_checklist_task(checklist_uid, task_uid, client_uid):  # noqa: E501
    """get_checklist_task

     # noqa: E501

    :param checklist_uid: 
    :type checklist_uid: str
    :param task_uid: 
    :type task_uid: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def get_template(template_uid, client_uid):  # noqa: E501
    """get_template

     # noqa: E501

    :param template_uid: 
    :type template_uid: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def get_template_task(template_uid, task_uid, client_uid):  # noqa: E501
    """get_template_task

     # noqa: E501

    :param template_uid: 
    :type template_uid: str
    :param task_uid: 
    :type task_uid: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def post_template(client_uid, callsign=None, name=None, description=None):  # noqa: E501
    """post_template

     # noqa: E501

    :param client_uid: 
    :type client_uid: str
    :param callsign: 
    :type callsign: str
    :param name: 
    :type name: str
    :param description: 
    :type description: str

    :rtype: str
    """
    return 'do some magic!'


def remove_mission_reference_from_checklist(checklist_uid, mission_name, client_uid):  # noqa: E501
    """remove_mission_reference_from_checklist

     # noqa: E501

    :param checklist_uid: 
    :type checklist_uid: str
    :param mission_name: 
    :type mission_name: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def start_checklist(template_uid, client_uid, callsign, name, description, start_time, default_role=None):  # noqa: E501
    """start_checklist

     # noqa: E501

    :param template_uid: 
    :type template_uid: str
    :param client_uid: 
    :type client_uid: str
    :param callsign: 
    :type callsign: str
    :param name: 
    :type name: str
    :param description: 
    :type description: str
    :param start_time: 
    :type start_time: str
    :param default_role: 
    :type default_role: str

    :rtype: str
    """
    return 'do some magic!'


def stop_checklist(checklist_uid, client_uid):  # noqa: E501
    """stop_checklist

     # noqa: E501

    :param checklist_uid: 
    :type checklist_uid: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'

def parseTemplate(templateCsv):
    """
        converts a CSV template into a XML template
    """
    checklist = Checklist()
    # assign a uid for the template
    checklist.setChecklistDetails(ChecklistDetails())
    checklist.getChecklistDetails().setUid(str(uuid.uuid4()))

    templateCsv = templateCsv.replace("\r", "")
    rows = templateCsv.split("\n", -1)
    if len(rows) < 3:
        return None

    # parse the labels from the header row containing the Col definition
    header = parseHeaderRow(rows[0])

    # parse the format instructions, add them to the header row
    header = parseFormatRow(rows[1], header)

    # create the ChecklistColumns and add them to the header
    checklistColumns = ChecklistColumns()
    checklistColumns.getChecklistColumn().extend(header)
    checklist.setChecklistColumns(checklistColumns)

    # parse the remainder of the rows
    checklistTasks = ChecklistTasks()
    for i in range(2, len(rows)):
        if len(rows[i]) == 0:
            continue

        checklistTask = parseChecklistTask(rows[i], len(header))
        checklistTasks.getChecklistTask().append(checklistTask)
    checklist.setChecklistTasks(checklistTasks)

    checklist = copyNotes(checklist)

    return checklist