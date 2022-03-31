from .BaseOgrVectorDriver import BaseDriver


class Kml(BaseDriver):
    def __init__(self,nameDriver="KML"):
        super().__init__(nameDriver)
        #BaseDriver.__init__(self,nameDriver)
    @property
    def extention(self):
        return "kml"
    def open(self,path_file,nameLayer,reWrite):
        return super().open(path_file,nameLayer,0)

