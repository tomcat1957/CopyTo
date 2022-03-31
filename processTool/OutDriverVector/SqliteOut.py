import os

from .BaseOgrVectorDriver import BaseDriver
from .DlgPersonalDb import DlgDbDrv


class DrvSQLite(BaseDriver):
    def __init__(self,nameDriver="SQLite"):
        BaseDriver.__init__(self,nameDriver)
        self.__isOverWrite=True
    @property
    def extention(self):
        return "sqlite"

    def open(self,path_file,nameLayer,reWrite):

        if not os.path.exists(path_file):
            return super().open(path_file,nameLayer,0)
        isOk=super().open(path_file,nameLayer,1)
        listNamesLayer=super().listLayer
        dlg=DlgDbDrv(path_file,listNamesLayer,nameLayer)
        dlg.show()
        if not dlg.isOk:
            return False
        name_table,isOverWrite=dlg.outNameOverWrite
        super().setActiveName(name_table)
        self.__isOverWrite=isOverWrite
        return True
    def copyLayerFast(self,source_layer,out_name:str,out_srs_wkt,addInExist=False):
        return super().copyLayerFast(source_layer,out_name,out_srs_wkt,not self.__isOverWrite)

