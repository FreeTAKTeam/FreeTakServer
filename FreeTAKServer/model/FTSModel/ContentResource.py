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

class ContentResource:

    def __init__(self):
        pass

    @staticmethod
    def CreateExCheckTemplate():
        contentresource = ContentResource()
        contentresource.filename = Filename.CreateExCheckTemplate()
        contentresource.hash = Hash.CreateExCheckTemplate()
        contentresource.keywords = Keywords.CreateExCheckTemplate()
        contentresource.mimetype = MimeType.CreateExCheckTemplate()
        contentresource.name = Name.CreateExCheckTemplate()
        contentresource.size = Size.CreateExCheckTemplate()
        contentresource.submissiontime = SubmissionTime.CreateExCheckTemplate()
        contentresource.submitter = Submitter.CreateExCheckTemplate()
        contentresource.tool = Tool.CreateExCheckTemplate()
        contentresource.uid = Uid.CreateExCheckTemplate()
        return contentresource

