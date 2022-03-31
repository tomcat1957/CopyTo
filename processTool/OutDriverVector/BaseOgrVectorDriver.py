import os

from osgeo import ogr


class BaseDriver:
    __drv=None
    __ds=None
    def __init__(self,nameDriver=None):
        self.__name_drv=nameDriver
        if nameDriver is not None:
            self.__drv=ogr.GetDriverByName(nameDriver)
    @property
    def availableAdd(self):
        return False
    def open(self,name_source,nameLayer=None,open_read=1):
        self.__activeName=nameLayer
        if self.__drv is None:
            self.__ds=ogr.Open(name_source,open_read)
        else:
            if open_read==1 and os.path.exists(name_source):
                self.__ds=ogr.Open(name_source,open_read)
            else:
                self.__ds=self.__drv.CreateDataSource(name_source)
        if self.__ds is not None:
            return True
        return False
    @property
    def activeGdalDataSource(self):
        return self.__ds
    @property
    def NamedDriver(self):
        return self.__drv.GetName()
    @property
    def extantion(self):
        return None
    @property
    def listLayer(self):
        if self.__ds is None:
            return None
        list_layer=[]
        for i in range(self.__ds.GetLayerCount()):
            list_layer.append(self.__ds.GetLayerByIndex(i).GetName())
        list_layer.sort()
        return list_layer
    def delLayer(self,name):
        if self.__ds is not None:
            self.__ds.DeleteLayer(name)
    def existLayer(self,name:str):
        list_layer=self.listLayer
        if list_layer is None:
            return False
        if name in list_layer :
            return True
        if name.lower() in list_layer :
            return True
        return False

    def getLayer(self,name):
        return self.__ds.GetLayerByName(name)
    def copyLayerFast(self,source_layer,out_name:str,out_srs_wkt,addInExist=False):
        options=[]
        str_over="NO"
        if addInExist:
            str_over="YES"
        options.append("OVERWRITE="+str_over)
        '''
        if addInExist:
            self.__ds.CopyLayer(source_layer,out_name,['OVERWRITE=YES'])
        else:
            self.__ds.CopyLayer(source_layer,out_name,['OVERWRITE=NO'])
        '''
        if out_srs_wkt is not None:
            options.append("DST_SRSWKT="+out_srs_wkt)
        self.__ds.CopyLayer(source_layer,out_name,options)
    def copyLayer(self,source_layer,out_name:str,addInExist=False,class_progress=None):
        layer_exist=self.existLayer(out_name)
        if layer_exist and not addInExist:
            self.delLayer(out_name.lower())
    def setActiveName(self,name):
        self.__activeName=name
    @property
    def NameActive(self):
        return self.__activeName
    def close(self):
        if self.__ds is not None:
            self.__ds=None







