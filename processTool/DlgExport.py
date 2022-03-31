import os
from pathlib import Path

import axipy
from PySide2 import QtCore
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialog, QFileDialog


def buildPathOut(path_tab_source,ext_file):
    p = Path(path_tab_source)
    folder=str(p.parent)
    name=p.stem
    out_path=os.path.join(folder,name+"."+ext_file)
    return out_path
def getFilterForSaveAs(namesDrv,extentions):
    outFilter=''
    end_name=namesDrv[-1]
    for name,ext in zip(namesDrv,extentions):
        str_filt=" "+name +" (*."+ext+")"
        if not(name==end_name):
            str_filt=str_filt+";;"
        outFilter=outFilter+str_filt
    return outFilter
class ExportDlg:
    __statusIsOk=False

    __outCoordSys=None
    __curentDrv=None
    def __init__(self,managerDrv):
        self.__mngDrv=managerDrv
        self.__listExtentions=self.__mngDrv.Extentions
        self.__namesDriver=self.__mngDrv.Names
        self.__curentDrv=managerDrv.getDrvByName(self.__namesDriver[0])
        self.__parentWin=axipy.app.mainwindow.qt_object()
        self.load_ui()
    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "ExportTool.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window  = loader.load(ui_file,self.__parentWin)
        ui_file.close()
        #icon=QIcon("save_as_32.png")
        #self.window.pb_saveas.setIcon(QIcon("save_as_32.png"))
        #self.window.setWindowModality(QtCore.Qt.ApplicationModal)
        self.window.setWindowFlags(
            self.window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.__fillListTable()
        self.window.pbClose.clicked.connect(self.__close)
        self.window.pb_run.clicked.connect(self.__run)
        self.window.pb_coordsys.clicked.connect(self.__change_coordSys)
        self.window.pb_saveas.clicked.connect(self.__select_out_path)
        self.window.cb_opentables.currentIndexChanged.connect(self.__changeTable)



    def show(self):
        self.window.exec()
    @property
    def isOk(self):
        return self.__statusIsOk
    def __close(self):
        self.__statusIsOk=False
        self.window.close()
    def __run(self):
        self.__statusIsOk=True
        self.window.close()
    @property
    def getParametrsExport(self):
        params={}
        params['source_tab']=self.window.cb_opentables.currentText()
        params['path_out']=self.window.ln_pathOut.text()
        params['driver']=self.__curentDrv.NamedDriver
        params['out_coordsystem']=self.__outCoordSys
        #params['rewrite']=self.window.ch_rewrite.isChecked()
        params['rewrite']=True

        return params
    def __fillListTable(self):
        self.window.cb_opentables.clear()
        list_table= axipy.app.mainwindow.catalog.tables
        self.__outCoordSys=list_table[0].coordsystem
        path_out=buildPathOut(list_table[0].properties['tabFile'],self.__listExtentions[0])
        self.window.ln_pathOut.setText(path_out)
        self.window.ln_outCoordSys.setText(self.__outCoordSys.description)
        for tab in list_table:
            self.window.cb_opentables.addItem(tab.name)

        self.window.cb_opentables.setCurrentIndex(0)
    def __change_coordSys(self):
        dlgcoordSys= axipy.ChooseCoordSystemDialog(self.__outCoordSys)
        if dlgcoordSys.exec() == QDialog.Accepted:
            self.__outCoordSys=dlgcoordSys.chosenCoordSystem()
            self.window.ln_outCoordSys.setText(self.__outCoordSys.description)
    def __select_out_path(self):
        path_out=self.window.ln_pathOut.text()
        p = Path(path_out)
        folder=str(p.parent)
        filt_extr=getFilterForSaveAs(self.__namesDriver,self.__listExtentions)
        '''
        file_raster_item = QFileDialog.getSaveFileName(self, 'Создать новый файл', os.getenv('HOME'), ' SQlite (*.sqlite);; Gpkg (*.gpkg)')
        '''

        file_exp=QFileDialog.getSaveFileName(self.window, 'Экспортировать файл ', path_out, filt_extr)
        #file_exp=QFileDialog.getSaveFileName(self.window, 'Экспортировать файл ', path_out, ' SQlite (*.sqlite);; Gpkg (*.gpkg)')
        if len(file_exp[0])>0:
            work_ext=file_exp[1]

            list_parm=work_ext.split(' ')
            self.__curentDrv=self.__mngDrv.getDrvByName(list_parm[0])
            new_path=buildPathOut(file_exp[0],self.__curentDrv.extention)
            self.window.ln_pathOut.setText(new_path)
    def __changeTable(self):
        name_tab=self.window.cb_opentables.currentText()
        table=axipy.app.mainwindow.catalog.find(name_tab)
        self.__outCoordSys=table.coordsystem
        self.window.ln_outCoordSys.setText(self.__outCoordSys.description)
        path_out=buildPathOut(table.properties['tabFile'],self.__listExtentions[0])
        self.window.ln_pathOut.setText(path_out)
