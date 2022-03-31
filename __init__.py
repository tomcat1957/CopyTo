import axipy

from .processTool.DlgExport import ExportDlg
from .processTool.OutDriverVector.ManagerDrivers import factoryMangerDrivers
from .processTool.OutDriverVector.RunCopy import run


class Plugin:
    def __init__(self, iface):
        self.iface = iface
        menubar = iface.menubar
        tr = iface.tr
        local_file=iface.local_file
        self.__action = menubar.create_button(iface.tr('"Экспорт в .."'),
                                              icon=local_file('processTool', 'saveas.png'), on_click=self.run_tools)
        #position = menubar.get_position(tr('Таблица'), tr('Действие Операции'))
        position = menubar.get_position(tr('Таблица'), tr('Действие'))
        position.add(self.__action, size=2)

        self.__catalog=axipy.app.mainwindow.catalog
        if self.__catalog is None:
            print("axipy.app.mainwindow.catalog is None")
        self.__selection=axipy.gui.selection_manager

        self.__catalog.updated.connect(self.__tryInReady)

        self.__tryInReady()
        #self.__selection.changed.connect(self.__changeSelection)
    def unload(self):
        self.__catalog.updated.disconnect(self.__tryInReady)
        #self.__viewService.countChanged.disconnect(self.__tyrIsReadyForMapAndSelection)
        self.iface.menubar.remove(self.__action)
    def run_tools(self):
        dlg=ExportDlg(factoryMangerDrivers())
        dlg.show()
        if dlg.isOk:
            propertyRun=dlg.getParametrsExport
            run(propertyRun)
            #BuildCatalog(propertyRun)
    def __changeSelection(self):
        print("run select")
    def __tryInReady(self):
        '''
        Проверяем условия для готовности инструмента к работе
        Должна быть открыта хотя бы одна пространственная таблица
        :return:
        '''
        tables=self.__catalog.tables
        for table in tables:
            if table.is_spatial and table.count()>0:
                self.__action.action.setEnabled(True)
                return

        self.__action.action.setEnabled(False)