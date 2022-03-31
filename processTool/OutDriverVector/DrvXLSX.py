from .BaseOgrVectorDriver import BaseDriver


class DrvXlsx(BaseDriver):
    def __init__(self,nameDriver="XLSX"):
        BaseDriver.__init__(self,nameDriver)
    @property
    def extention(self):
        return "xlsx"

    def open(self,path_file,nameLayer,reWrite):
        return super().open(path_file,nameLayer,0)