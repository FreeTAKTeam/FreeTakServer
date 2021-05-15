from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModel.Filename import Filename
from FreeTAKServer.model.FTSModel.Hash import Hash
from FreeTAKServer.model.FTSModel.Keywords import Keywords
from FreeTAKServer.model.FTSModel.MimeType import MimeType
from FreeTAKServer.model.FTSModel.Name import Name
from FreeTAKServer.model.FTSModel.Size import Size
from FreeTAKServer.model.FTSModel.SubmissionTime import SubmissionTime
from FreeTAKServer.model.FTSModel.Submitter import Submitter
from FreeTAKServer.model.FTSModel.Tool import Tool
from FreeTAKServer.model.FTSModel.Uid import Uid

class ContentResource(FTSProtocolObject):

    def __init__(self):
        pass

    @staticmethod
    def ExcheckUpdate():
        contentresource = ContentResource()
        contentresource.filename = Filename.ExcheckUpdate()
        contentresource.hash = Hash.ExcheckUpdate()
        contentresource.keywords = Keywords.ExcheckUpdate()
        contentresource.mimeType = MimeType.ExcheckUpdate()
        contentresource.name = Name.ExcheckUpdate()
        contentresource.size = Size.ExcheckUpdate()
        contentresource.submissionTime = SubmissionTime.ExcheckUpdate()
        contentresource.submitter = Submitter.ExcheckUpdate()
        contentresource.tool = Tool.ExcheckUpdate()
        contentresource.uid = Uid.ExcheckUpdate()
        return contentresource

