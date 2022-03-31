import axipy

from .BaseOgrVectorDriver import BaseDriver
from ... import factoryMangerDrivers


def run(param_copy):
    mng_drvs=factoryMangerDrivers()
    table_source=axipy.app.mainwindow.catalog.find(param_copy['source_tab'])
    path_source=table_source.properties['tabFile']
    source_ds=BaseDriver()
    is_ok_open=source_ds.open(path_source)
    out_drv=mng_drvs.getDrvByName(param_copy['driver'])
    out_coordSys=param_copy['out_coordsystem']
    out_wkt=out_coordSys.wkt
    source_cs_wkt=table_source.coordsystem.wkt
    if out_coordSys==table_source.coordsystem:
        out_wkt=source_cs_wkt
    path_out=param_copy['path_out']
    reWrite=param_copy['rewrite']
    list_layer=source_ds.listLayer
    is_ok_open=out_drv.open(path_out,list_layer[0],reWrite)
    if is_ok_open:
        #out_ds=out_drv.activeGdalDataSource

        layer_source=source_ds.getLayer(list_layer[0])
        outName=out_drv.NameActive
        out_layer=out_drv.copyLayerFast(layer_source,outName,out_wkt,reWrite)
        layer_source=None
        out_layer=None
        out_drv.close()
        source_ds.close()


