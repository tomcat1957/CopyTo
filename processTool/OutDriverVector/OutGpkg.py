from osgeo import ogr

from .AbstractOutDriver import AbsOutVector


class Gpkg(AbsOutVector):
    __name_driver="GPKG"
    __ext_file="gpkg"
    def __init__(self):
        self.__drv=ogr.GetDriverByName( self.__name_driver)
    @property
    def extention(self):
        return self.__ext_file
    @property
    def Name(self):
        return self.__name_driver
    @property
    def availableAdd(self):
        return True
    @property
    def listLayers(self):
        pass

