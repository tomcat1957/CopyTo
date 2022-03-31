

from .DrvKml import Kml
from .DrvXLSX import DrvXlsx
from .GeoJson import GeoJson
from .GpkgOut import Gpkg
from .SqliteOut import DrvSQLite


class ManagerDrivers:
    __list_drivers=None
    def __init__(self):
        self.__list_drivers=[]
    def add(self,driver):
        self.__list_drivers.append(driver)
    @property
    def Extentions(self):
        extentions=[]
        for drv in self.__list_drivers:
            extentions.append(drv.extention)
        return extentions
    @property
    def Names(self):
        names=[]
        for drv in self.__list_drivers:
            names.append(drv.NamedDriver)
        return names
    def getDrvByName(self,name):
        for drv in self.__list_drivers:
            if name==drv.NamedDriver:
                return drv
        return None

def factoryMangerDrivers():
    mngDrvs=ManagerDrivers()
    mngDrvs.add(Gpkg())
    mngDrvs.add(DrvSQLite())
    mngDrvs.add(GeoJson())

    mngDrvs.add(Kml())
    mngDrvs.add(DrvXlsx())
    return mngDrvs