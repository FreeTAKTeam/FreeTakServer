import connexion
import six

from swagger_server import util


def get_all_cot_events(uid, secago=None, start=None, end=None):  # noqa: E501
    """get_all_cot_events

     # noqa: E501

    :param uid: 
    :type uid: str
    :param secago: 
    :type secago: int
    :param start: 
    :type start: str
    :param end: 
    :type end: str

    :rtype: str
    """
    start = util.deserialize_datetime(start)
    end = util.deserialize_datetime(end)
    return 'do some magic!'


def get_cot_event(uid):  # noqa: E501
    """get_cot_event

     # noqa: E501

    :param uid: 
    :type uid: str

    :rtype: str
    """
    return 'do some magic!'


def get_cot_events(uids):  # noqa: E501
    """get_cot_events

     # noqa: E501

    :param uids: 
    :type uids: List[str]

    :rtype: str
    """
    return 'do some magic!'


def get_cot_events_by_time_and_bbox(start, end, left=None, bottom=None, right=None, top=None):  # noqa: E501
    """get_cot_events_by_time_and_bbox

     # noqa: E501

    :param start: 
    :type start: str
    :param end: 
    :type end: str
    :param left: 
    :type left: float
    :param bottom: 
    :type bottom: float
    :param right: 
    :type right: float
    :param top: 
    :type top: float

    :rtype: str
    """
    start = util.deserialize_datetime(start)
    end = util.deserialize_datetime(end)
    return 'do some magic!'
