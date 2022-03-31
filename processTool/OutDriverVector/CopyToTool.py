import time

import axipy
from axipy import Table
from osgeo import ogr

from .BaseOgrVectorDriver import BaseDriver
from .ToolProgressBar.AddProgress import BasicProcess

def calcProcent(count,curent_value):
    proc_val=(curent_value/count)*100.0
    return int(proc_val)
class RunCopy(BasicProcess):
    def __init__(self,ds_source,name_layer_source,ds_out,name_layer_out,out_srs=None,addExist=False):
        super().__init__()
        self.__ds_source=ds_source
        self.__name_layer_source=name_layer_source
        self.__ds_out=ds_out
        self.__name_out_layer=name_layer_out
        self.__out_srs=out_srs
        self.__layer_add_exist=addExist

        self.__prepare()
    def __prepare(self):
        self.__source_layer=self.__ds_source.GetLayerByName(self.__name_layer_source)
        self.__count=self.__source_layer.GetFeatureCount()


    @property
    def Count(self):
        return self.__count
    def run(self):
        if self.__out_srs is None:
            self.__out_srs= self.__source_layer.GetSpatialRef()
        self.ClsProgressBar().processUpdateProcessName("Копирование структуры")
        if self.__layer_add_exist:
            self.__out_layer=self.__ds_out.CreateLayer(self.__name_out_layer, self.__out_srs, geom_type=ogr.wkbUnknown,options=['OVERWRITE=YES'])
        else:
            self.__out_layer=self.__ds_out.CreateLayer(self.__name_out_layer, self.__out_srs, geom_type=ogr.wkbUnknown,options=['OVERWRITE=NO'])
            inLayerDefn = self.__source_layer.GetLayerDefn()
            for i in range(0, inLayerDefn.GetFieldCount()):
                fieldDefn = inLayerDefn.GetFieldDefn(i)
                self.__out_layer.CreateField(fieldDefn)
        '''
        if self.__reproject:
            inSpatialRef=self.__source_layer.GetSpatialRef()
        '''

        last_proc=0
        index=0
        outLayerDefn=self.__out_layer.GetLayerDefn()

        for i in range(self.__count):
            #outFeature = ogr.Feature(outLayerDefn)

            inFeature=self.__source_layer.GetFeature(i+1)
            outFeature=inFeature.Clone()
            '''
            for ifield in range(0, outLayerDefn.GetFieldCount()):
                fieldDefn = outLayerDefn.GetFieldDefn(ifield)
                fieldName = fieldDefn.GetName()
                print(fieldName)
                outFeature.SetField(fieldDefn.GetNameRef(),inFeature.GetField(ifield))
            '''
            geom = inFeature.GetGeometryRef()
            outFeature.SetGeometry(geom.Clone())
            # Add new feature to output Layer
            self.__out_layer.CreateFeature(outFeature)
            outFeature=None
            inFeature=None
            index += 1
            time.sleep(0.00000005)
            cur_proc=calcProcent(self.__count,index)
            if cur_proc>last_proc:
                last_proc=cur_proc
                self.countChanged.emit(cur_proc)
            #QCoreApplication.processEvents()
            if self.ClsProgressBar().isCancel:
                break
        self.endProcess.emit(0)
        self.__source_layer=None
        self.__out_layer=None
        self.__ds_out=None
        self.__ds_source=None





