from lxml import etree
class ExtendedElement(etree.ElementBase):
    def set_parent(self, parent):
        self._parent = parent
        
    def getparent(self):
        if hasattr(self, '_parent'):
            return self._parent
        else:
            return super().getparent()