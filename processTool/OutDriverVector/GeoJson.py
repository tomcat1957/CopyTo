from .BaseOgrVectorDriver import BaseDriver


class GeoJson(BaseDriver):
    def __init__(self,nameDriver="GeoJSON"):
        BaseDriver.__init__(self,nameDriver)
    @property
    def extention(self):
        return "json"

    def open(self,path_file,nameLayer,reWrite):
        return super().open(path_file,nameLayer,0)