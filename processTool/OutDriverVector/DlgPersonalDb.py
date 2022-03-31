import os

import axipy
from PySide2 import QtCore
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class DlgDbDrv:
    __statusIsOk=False
    def __init__(self,path_db,list_table,name_new_tab):
        self.__path_db=path_db
        self.__list_in_db=list_table
        self.__name_add_tab=name_new_tab
        self.__parentWin=axipy.app.mainwindow.qt_object()
        self.load_ui()
        self.__initUi()
    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "DlgPersonalDb.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.window  = loader.load(ui_file,self.__parentWin)
        ui_file.close()
        self.window.setWindowFlags(
            self.window.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint & ~QtCore.Qt.WindowContextHelpButtonHint)
    def __initUi(self):
        self.window.lst_table.addItems(self.__list_in_db)
        self.window.lb_path_file.setText(self.__name_add_tab)
        '''
        if self.__name_add_tab in self.__list_in_db:
            self.window.gpb_options.setEnabled(True)
        '''
        self.window.ln_name_new_tab.setText(self.__name_add_tab)
        self.window.pb_cancel.clicked.connect(self.__close)
        self.window.pb_run.clicked.connect(self.__run)
        self.window.ln_name_new_tab.textChanged.connect(self.__change_new_name_tab)
    def __change_new_name_tab(self):
        new_name=self.window.ln_name_new_tab.text()
        '''
        if new_name in self.__list_in_db:
            self.window.gpb_options.setEnabled(True)
        else:
            self.window.gpb_options.setEnabled(False)
        '''
        if len(new_name)==0:
            self.window.pb_run.setEnabled(False)
        else:
            self.window.pb_run.setEnabled(True)
    def show(self):
        self.window.exec()
    @property
    def isOk(self):
        return self.__statusIsOk
    @property
    def outNameOverWrite(self):
        name_table=self.window.ln_name_new_tab.text()
        overWrite=True
        '''
        if not self.window.gpb_options.isEnabled():
            return name_table,overWrite
        
        return name_table,self.window.rb_replace.isChecked()
        '''
        return name_table,overWrite
    def __close(self):
        self.__statusIsOk=False
        self.window.close()
    def __run(self):
        self.__statusIsOk=True
        self.window.close()
