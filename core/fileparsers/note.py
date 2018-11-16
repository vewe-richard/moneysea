from baseparser import BaseParser
import xml.etree.ElementTree as ET

class Note(BaseParser):
    def __init__(self, filepath):
        BaseParser.__init__(self, filepath)
        pass

    def doparse(self):
        tree = ET.parse(self._filepath)
        root = tree.getroot()
        for child in root:
#            print child.tag, child.text
            if child.tag == "adding":
                self._adding = float(child.text)
            elif child.tag == "note":
                self._note = child.text
        pass

    def verify(slef):
        return False
