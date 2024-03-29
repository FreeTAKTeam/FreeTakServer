#######################################################
# 
# Remarks.py
# Python implementation of the Class Remarks
# Generated by Enterprise Architect
# Created on:      26-Sep-2020 9:41:41 PM
# Original author: natha
# 
#######################################################
from sqlalchemy import Column, ForeignKey
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Remarks(Base):
# default constructor  def __init__(self):
    __tablename__ = "Remarks"
    PrimaryKey = Column(ForeignKey("Detail.PrimaryKey"), primary_key=True)
    Detail = relationship("Detail", back_populates="remarks")
    # Used to track a conversation thread.  The format is a comma-separated list of
    # freetext keywords.
    # 
    #               ex. keywords="debriefing"            - Describes a conversation
    # about debriefing
    #               ex. keywords="mission-A"             - Describes a conversation
    # about mission-A
    #               ex. keywords="tasking_B, subject_C"  - Describes a conversation
    # about tasking_B and subject_C
    keywords = Column(String(100))
    # Source specifies the sender�s UID � this is what is parsed by recipients to
    # determine the sender, with the UID format being the fallback.
    source = Column(String(100))
    # the time of the remark was added to the CoT object
    time = Column(String(100))
    # Intended recipeint(s) of this remark information. Tentative field coding as
    # follows: The to attribute may contain the UID of the entity to whom the message
    # is addressed.  (Implementors should expect that future versions of this sub
    # schema will allow a comma separated list of UIDs.)  Absense of an explict
    # addressee means the message is broadcast.
    # e.g. ANDROID-359975090666199
    to = Column(String(100))
    # Version tag for this sub schema.  Neccessary to ensure upward compatibility
    # with future revisions.
    version = Column(String(100))
    INTAG = Column(String(1000))