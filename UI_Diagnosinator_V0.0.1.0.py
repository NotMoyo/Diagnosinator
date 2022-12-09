import sys
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('Diagnosinator.ui', self)
        self.move(100,100)
        self.setWindowTitle('Diagnosinator')

        self.tabs = self.findChild(QTabWidget,'tabWidget')

        table_hematology_row_headers = [
                    'WBC','RBC','HGB','HCT','MCV','MCH','MCHC','RDW','PLT','MPV',
                    '%NEUT','%LYMPH','%MONO','%EOS','%BASO','%IG',
                    'ABS.NEUT','ABS.LYMPH','ABS.MONO','ABS.EOS','ABS.BASO','ABS.IG'
                ]
        print(len(table_hematology_row_headers))

        # def table_hematology():
        #     table_hematology_column_headers = ['Results','Unit']
        #     table_hematology_row_headers = [
        #         'WBC','RBC','HGB','HCT','MCV','MCH','MCHC','RDW','PLT','MPV',
        #         '%NEUT','%LYMPH','%MONO','%EOS','%BASO','%IG',
        #         'ABS.NEUT','ABS.LYMPH','ABS.MONO','ABS.EOS','ABS.BASO','ABS.IG'
        #     ]
        #     self.hematology_table = self.findChild(QTableWidget, 'tableWidget_hematology')
        #     self.hematology_table.move(20,20)
        #     self.hematology_table.setColumnCount(len(table_hematology_column_headers))
        #     self.hematology_table.setRowCount(len(table_hematology_row_headers))
        #     self.hematology_table.setHorizontalHeaderLabels(table_hematology_column_headers)
        #     self.hematology_table.setVerticalHeaderLabels(table_hematology_row_headers)

            # self.hematology_table.setItem(1,1,QTableWidgetItem('Test'))
        # def table_chemistry():
        #     table_chemistry_column_headers = ['Results', 'Unit']
        #     table_chemistry_row_headers = [
        #         'Na+','K+','Cl-','CO2',
        #         'ALB','CREAT','BUN','TP','T.Bili','D.Bili',
        #         'ALT','ALP','AST','GGT',
        #         'TROPT','PROBNP','CKMB','CK',
        #         'Ca','Mg','PHOS',
        #         'Fe','TIBC','B12','FOL','VITD','FERR',
        #         'GLUC','A1C','CRP','UA',
        #         'LACT','AMM',
        #         'TRIG','CHOL','HDL','VLDL',
        #         'BHCG','CEA','PSA','PCT',
        #         'TSH','FT4','T4','T3U','PTH',
        #         'TESTO','ETOH','LDH','LIP',
        #         'DIG','Li','ACET','VANC','GENT','TOBRA','BHYD'
        #
        #     ]
        #     self.chemistry_table = self.findChild(QTableWidget, 'tableWidget_chemistry')
        #     self.chemistry_table.move(20, 20)
        #     self.chemistry_table.setColumnCount(len(table_chemistry_column_headers))
        #     self.chemistry_table.setRowCount(len(table_chemistry_row_headers))
        #     self.chemistry_table.setHorizontalHeaderLabels(table_chemistry_column_headers)
        #     self.chemistry_table.setVerticalHeaderLabels(table_chemistry_row_headers)
        # table_chemistry()
        # table_hematology()
        class hematology:
            def __init__(self,test_name,unit,lower_ref,upper_ref):
                self.test = test_name
                self.unit = unit
                self.lower = lower_ref
                self.upper = upper_ref
        self.show()



app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
