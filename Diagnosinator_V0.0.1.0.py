import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
from PyQt5.QtCore import Qt as qt
import PyQt5.QtGui as qtg
import time as tm
import datetime as dt
import sqlite3 as sql
import requests as rq

date = tm.strftime('%Y')

conn = sql.connect('patients.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Patient_List(
    ID INT PRIMARY KEY UNIQUE,
    First_Name TEXT,
    Middle_Name TEXT,
    Last_Name TEXT,
    Gender Text,
    Age INTEGER,
    DOB TEXT
    )
""")
c.execute("""SELECT ID FROM Patient_List""")

#-#-# UNCOMMENT TO DROP TABLE #-#-#
#c.execute("DROP TABLE Patient_List")

identity_track = c.fetchall()
conn.commit()
conn.close()

conn = sql.connect('hematology.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Patient_Results(
    ID INT PRIMARY KEY UNIQUE,
    PLT REAL,
    WBC REAL,
    RBC REAL,
    HGB REAL,
    HCT REAL,
    MCV REAL,
    MCH REAL,
    MCHC REAL,
    RDW REAL,
    MPV REAL,
    PER_NEUT REAL,
    PER_LYMPH REAL,
    PER_MONO REAL,
    PER_EOS REAL,
    PER_BASO REAL,
    PER_IG REAL,
    ABS_NEUT REAL,
    ABS_LYMPH REAL,
    ABS_MONO REAL,
    ABS_EOS REAL,
    ABS_BASO REAL,
    ABS_IG REAL
    )
""")

#-#-# UNCOMMENT TO DROP TABLE #-#-#
#c.execute("DROP TABLE Patient_Results")

conn.commit()
conn.close()


def list_columns():
    conn = sql.connect('patients.db')
    c = conn.cursor()
    columns = c.execute('SELECT * FROM Patient_List')
    column_number = 1
    for column in columns.description:
        print('Column # '+str(column_number)+' = '+column[0])
        column_number +=1
 # list_columns()

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        # Initializing.
        self.loaded_patient = '' # Needed for Remove Patient Function when no patient has been loaded.
        self.variable_widget_count = 0
        self.dict_widget_names = {}
        self.dict_widgets = {}

        # Global.
        global identity_track

        self.id_track = identity_track
        if self.id_track == []:
            self.id_track = 1
        else:
            self.id_track = str(((identity_track[-1])[0]+1))

        class Mainscreen:
            self.setWindowTitle('Diagnosinator')
            self.setGeometry(150, 150, 1200, 800)
            self.setMaximumSize(1200,800)
            self.setMinimumSize(1200,800)
            
        class RegExp:

            self.datetime_now = dt.datetime.now()
            year_limit_ones = (self.datetime_now.strftime('%y')[-1])
            year_limit_tens = (self.datetime_now.strftime('%y')[-2])

            self.regexp_input_name = qtc.QRegExp('^[A-Za-z]{1,16}$')
            self.regexp_input_num = qtc.QRegExp('(^\d{1,5}$)|(^\d{1,5}\.\d\d?$)')
            self.regexp_input_date = qtc.QRegExp('(([1-9]|0[1-9]|1[0-2])'
            '/([1-9]|0[1-9]|[1-2]\d|3[0-1])'
            '/((19\d\d|20[0-'+str(int(year_limit_tens)-1)+']\d|20'+str(year_limit_tens)+'[0-'+year_limit_ones+']))|)')

        class tab_set:
            self.tab_bar = qtw.QTabWidget(self)
            self.tab_bar.setFixedSize(self.width(), self.height())

            self.diagnosis_tab = qtw.QWidget()
            self.chemistry_tab = qtw.QWidget() 
            self.hematology_tab = qtw.QWidget()
            self.coagulation_tab = qtw.QWidget()
            self.urinalysis_tab = qtw.QWidget()
            self.bloodbank_tab = qtw.QWidget()
            self.serology_tab = qtw.QWidget()
            self.microbiology_tab = qtw.QWidget()
            
            self.diagnosis_tab.setAutoFillBackground(True)
            self.chemistry_tab.setAutoFillBackground(True)
            self.hematology_tab.setAutoFillBackground(True)
            self.coagulation_tab.setAutoFillBackground(True)
            self.urinalysis_tab.setAutoFillBackground(True)
            self.bloodbank_tab.setAutoFillBackground(True)
            self.serology_tab.setAutoFillBackground(True)
            self.microbiology_tab.setAutoFillBackground(True)

            self.tab_bar.addTab(self.diagnosis_tab,'Diagnosis')
            self.tab_bar.addTab(self.chemistry_tab,'Chemistry')
            self.tab_bar.addTab(self.hematology_tab,'Hematology')
            self.tab_bar.addTab(self.coagulation_tab,'Coagulation')
            self.tab_bar.addTab(self.urinalysis_tab,'Urinalysis')
            self.tab_bar.addTab(self.bloodbank_tab,'Blood Bank')
            self.tab_bar.addTab(self.serology_tab,'Serology')
            self.tab_bar.addTab(self.microbiology_tab,'Microbiology')

            self.p = qtg.QPalette()
            gradient = qtg.QLinearGradient(300, 200, 500, 800)
            gradient.setColorAt(0.0, qtg.QColor('#87bba2'))
            gradient.setColorAt(1.0, qtg.QColor('#55828b'))
            self.p.setBrush(qtg.QPalette.Window, qtg.QBrush(gradient))

            self.diagnosis_tab.setPalette(self.p)
            self.chemistry_tab.setPalette(self.p)   
            self.hematology_tab.setPalette(self.p)
            self.coagulation_tab.setPalette(self.p)
            self.urinalysis_tab.setPalette(self.p)
            self.bloodbank_tab.setPalette(self.p)
            self.serology_tab.setPalette(self.p)
            self.microbiology_tab.setPalette(self.p)


            self.tab_bar.setTabEnabled(1,False)
            self.tab_bar.setTabEnabled(2, False)
            self.tab_bar.setTabEnabled(3, False)
            self.tab_bar.setTabEnabled(4, False)
            self.tab_bar.setTabEnabled(5, False)
            self.tab_bar.setTabEnabled(6, False)
            self.tab_bar.setTabEnabled(7, False)

        class diagnosis: # Diagnosis Tab

            class window_add_patient:  # New Window to Add a Patient to the Database.
                # Creating Widgets.
                self.window_add_patient = qtw.QWidget()
                self.pushbutton_save_patient_info = qtw.QPushButton()
                self.pushbutton_clear_patient_info = qtw.QPushButton()
                 # Label Loop.
                self.list_add_patient_info_label_names = [ 
                    'ID',
                    'First_Name',
                    'Middle_Name',
                    'Last_Name',
                    'Gender',
                    'Date_of_Birth',
                    'Height',
                    'Weight'
                    ]
                # Initializing.
                self.variable_add_patient_info_label_loop_y_coordinate = 15
                
                for pinfowidget in range(len(self.list_add_patient_info_label_names)):
                        pinfo = self.list_add_patient_info_label_names[pinfowidget]

                        label_add_info = 'self.label_add_'+pinfo
                        self.dict_widget_names[self.variable_widget_count] = label_add_info

                        label_add_info = qtw.QLabel()
                        self.dict_widgets[self.variable_widget_count] = label_add_info

                        self.variable_widget_count = self.variable_widget_count + 1
            
                        label_add_info.setText(pinfo+':')
                        label_add_info.setFixedWidth(80)
                        label_add_info.setStyleSheet('text-decoration: underline')
                        label_add_info.setAlignment(qt.AlignRight)
                        label_add_info.move(20,self.variable_add_patient_info_label_loop_y_coordinate)
                        self.variable_add_patient_info_label_loop_y_coordinate = self.variable_add_patient_info_label_loop_y_coordinate+25
                        label_add_info.setParent(self.window_add_patient)

                        if 'Date' in pinfo:
                            lineedit_add_info = 'self.lineedit_add_'+pinfo
                            self.dict_widget_names[self.variable_widget_count] = lineedit_add_info

                            lineedit_add_info = qtw.QLineEdit()
                            self.dict_widgets[self.variable_widget_count] = lineedit_add_info

                            self.variable_widget_count = self.variable_widget_count + 1
                            # self.list_widget_add_patient_info_lineedits.append(lineedit_add_info)

                            lineedit_add_info.move((int(label_add_info.x()+label_add_info.width()+5)),label_add_info.y()-3)
                            lineedit_add_info.setParent(self.window_add_patient)
                            validator = qtg.QRegExpValidator(self.regexp_input_date)
                            lineedit_add_info.setValidator(validator)
                            lineedit_add_info.setFixedWidth(100)
                            lineedit_add_info.setAlignment(qt.AlignLeft)
                            lineedit_add_info.setPlaceholderText('MM/DD/YYYY')
                            lineedit_add_info.textChanged.connect(self.check_dob_input)

                        elif 'eight' in label_add_info.text():
                            doublespinbox_add_info = 'self.doublespinbox_add_'+pinfo
                            self.dict_widget_names[self.variable_widget_count] = doublespinbox_add_info

                            doublespinbox_add_info = qtw.QDoubleSpinBox()
                            self.dict_widgets[self.variable_widget_count] = doublespinbox_add_info

                            self.variable_widget_count = self.variable_widget_count + 1

                            # self.list_widget_add_patient_info_doublespinboxes.append(doublespinbox_add_info)

                            doublespinbox_add_info.move((int(label_add_info.x()+label_add_info.width()+5)),label_add_info.y()-3)
                            doublespinbox_add_info.setParent(self.window_add_patient)

                        elif 'Name'in label_add_info.text():
                            lineedit_add_info = 'self.lineedit_add_'+pinfo
                            self.dict_widget_names[self.variable_widget_count] = lineedit_add_info
                            lineedit_add_info = qtw.QLineEdit()
                            self.dict_widgets[self.variable_widget_count] = lineedit_add_info
                            self.variable_widget_count = self.variable_widget_count + 1
                            # self.list_widget_add_patient_info_lineedits.append(lineedit_add_info)
                            
                            lineedit_add_info.move((int(label_add_info.x()+label_add_info.width()+5)),label_add_info.y()-3)
                            lineedit_add_info.setParent(self.window_add_patient)
                            validator = qtg.QRegExpValidator(self.regexp_input_name)
                            lineedit_add_info.setValidator(validator)
                            lineedit_add_info.setFixedWidth(100)
                            lineedit_add_info.setAlignment(qt.AlignLeft)

                        elif 'ID'in label_add_info.text():
                            lineedit_add_info = 'self.lineedit_add_'+pinfo
                            self.dict_widget_names[self.variable_widget_count] = lineedit_add_info

                            lineedit_add_info = qtw.QLineEdit()
                            self.dict_widgets[self.variable_widget_count] = lineedit_add_info

                            self.variable_widget_count = self.variable_widget_count + 1

                            # self.list_widget_add_patient_info_lineedits.append(lineedit_add_info)

                            lineedit_add_info.move((int(label_add_info.x()+label_add_info.width()+5)),label_add_info.y()-3)
                            lineedit_add_info.setParent(self.window_add_patient)
                            lineedit_add_info.setText(str(self.id_track))
                            lineedit_add_info.setReadOnly(True)
                            lineedit_add_info.setFixedWidth(25)
                            lineedit_add_info.setAlignment(qt.AlignCenter)

                        elif 'Gender' in label_add_info.text():
                            combobox_add_info = 'self.combobox_add_'+pinfo
                            self.dict_widget_names[self.variable_widget_count] = combobox_add_info

                            combobox_add_info = qtw.QComboBox()
                            self.dict_widgets[self.variable_widget_count] = combobox_add_info

                            self.variable_widget_count = self.variable_widget_count + 1

                            # self.list_widget_add_patient_info_comboboxes.append(combobox_add_info)

                            combobox_add_info.move((int(label_add_info.x()+label_add_info.width()+5)),label_add_info.y()-3)
                            combobox_add_info.setParent(self.window_add_patient)
                            combobox_add_info.insertItem(0,'Unknown')
                            combobox_add_info.insertItem(1,'Male')
                            combobox_add_info.insertItem(2,'Female')

                # Set Text.
                self.window_add_patient.setWindowTitle('Add Patient')
                self.pushbutton_save_patient_info.setText('Save')
                self.pushbutton_clear_patient_info.setText('Clear')
                # Set Geometry.
                self.window_add_patient.setGeometry(500,250,500,500)
                # Adjust Size.
                self.pushbutton_save_patient_info.adjustSize()
                self.pushbutton_clear_patient_info.adjustSize()
                # Move.
                self.pushbutton_save_patient_info.move(20,(self.window_add_patient.height()-50))
                self.pushbutton_clear_patient_info.move((self.pushbutton_save_patient_info.x()+self.pushbutton_save_patient_info.width()+20),(self.window_add_patient.height()-50))
                # Set Parent.
                self.pushbutton_save_patient_info.setParent(self.window_add_patient)
                self.pushbutton_clear_patient_info.setParent(self.window_add_patient)
                # Connect
                self.pushbutton_save_patient_info.clicked.connect(self.save_patient_info)
                self.pushbutton_clear_patient_info.clicked.connect(self.clear_patient_info)
                # Other
                self.window_add_patient.setWindowFlags(qt.WindowStaysOnTopHint)
                self.window_add_patient.setPalette(self.p)

            # Creating Widgets.
            self.list_patients = qtw.QListWidget()
            self.groupbox_list_patients = qtw.QGroupBox()
            self.groupbox_high_probability = qtw.QGroupBox()
            self.groupbox_medium_probability = qtw.QGroupBox()
            self.groupbox_low_probability = qtw.QGroupBox()
            self.pushbutton_add_patient = qtw.QPushButton()
            self.pushbutton_edit_patient = qtw.QPushButton()
            self.pushbutton_remove_patient = qtw.QPushButton()
            self.pushbutton_delete_database = qtw.QPushButton()
            self.pushbutton_messagebox_yes = qtw.QPushButton()
            self.pushbutton_messagebox_no = qtw.QPushButton()
            self.messagebox_delete_database_confirmation = qtw.QMessageBox()
            # Set Text.
            self.groupbox_list_patients.setTitle('List of Patients')
            self.groupbox_high_probability.setTitle('High Probability')
            self.groupbox_medium_probability.setTitle('Medium Probability')
            self.groupbox_low_probability.setTitle('Low Probability')
            self.pushbutton_add_patient.setText('Add Patient')
            self.pushbutton_edit_patient.setText('Edit Patient')
            self.pushbutton_remove_patient.setText('Remove Patient')
            self.pushbutton_delete_database.setText('Delete Database')
            self.pushbutton_messagebox_yes.setText('Yes')
            self.pushbutton_messagebox_yes.setText('No')
            self.messagebox_delete_database_confirmation.setText('Are You Sure You Want to Delete The Entire Database?')
            self.messagebox_delete_database_confirmation.setWindowTitle('Confirmation')
            # Adjust Size.
            self.pushbutton_delete_database.adjustSize()
            # Set Fixed Size.
            self.pushbutton_add_patient.setFixedSize(85,25)
            self.pushbutton_edit_patient.setFixedSize(85,25)
            self.pushbutton_remove_patient.setFixedSize(85,25)
            self.messagebox_delete_database_confirmation.setFixedSize(200,200)
            # Set Geometry.
            self.groupbox_list_patients.setGeometry(20,20,200,(self.tab_bar.height()-450))
            self.list_patients.setGeometry(0,20,self.groupbox_list_patients.width(),self.groupbox_list_patients.height()-20)
            self.groupbox_high_probability.setGeometry(500,20,200,300)
            self.groupbox_medium_probability.setGeometry(
                (self.groupbox_high_probability.x()+self.groupbox_high_probability.width()+25),
                self.groupbox_high_probability.y(),
                self.groupbox_high_probability.width(),
                self.groupbox_high_probability.height())
            self.groupbox_low_probability.setGeometry(
                (self.groupbox_medium_probability.x()+self.groupbox_medium_probability.width()+25),
                self.groupbox_high_probability.y(),
                self.groupbox_medium_probability.width(),
                self.groupbox_medium_probability.height())
            # Move.
            self.pushbutton_add_patient.move(self.groupbox_list_patients.x(),(self.groupbox_list_patients.y()+self.groupbox_list_patients.height()+5))
            self.pushbutton_edit_patient.move((self.groupbox_list_patients.x()+self.groupbox_list_patients.width()-self.pushbutton_remove_patient.width()),(self.groupbox_list_patients.y()+self.groupbox_list_patients.height()+5))
            self.pushbutton_remove_patient.move(self.pushbutton_add_patient.x(),(self.pushbutton_add_patient.y()+self.pushbutton_add_patient.height()+5))
            self.pushbutton_delete_database.move((self.width()-self.pushbutton_delete_database.width()-15),(self.height()-self.pushbutton_delete_database.height()-100))
            # Set Parent.
            self.list_patients.setParent(self.groupbox_list_patients)
            self.groupbox_list_patients.setParent(self.diagnosis_tab)
            self.groupbox_high_probability.setParent(self.diagnosis_tab)
            self.groupbox_medium_probability.setParent(self.diagnosis_tab)
            self.groupbox_low_probability.setParent(self.diagnosis_tab)
            self.pushbutton_add_patient.setParent(self.diagnosis_tab)
            self.pushbutton_edit_patient.setParent(self.diagnosis_tab)
            self.pushbutton_remove_patient.setParent(self.diagnosis_tab)
            self.pushbutton_delete_database.setParent(self.diagnosis_tab)
            # Connect.
            self.pushbutton_add_patient.clicked.connect(self.add_patient_info)
            self.pushbutton_edit_patient.clicked.connect(self.edit_patient_info)
            self.pushbutton_remove_patient.clicked.connect(self.remove_patient_info)
            self.pushbutton_delete_database.clicked.connect(self.messagebox_delete_database_confirmation.exec)
            self.list_patients.itemDoubleClicked.connect(self.load_dblclicked_pt)
            self.messagebox_delete_database_confirmation.buttonClicked.connect(self.delete_database)
            # Set Style Sheet.
            self.list_patients.setStyleSheet('border: 2px solid black; border-radius:5px; background-color: #FDF5ED; alternate-background-color: #C0D4D8')
            variable_bg_color_probability_groupbox = '#FDF5ED'
            groupbox_title_font = qtg.QFont()
            groupbox_title_font.setBold(True)
            groupbox_title_font.setPixelSize(14)
            groupbox_title_font.setLetterSpacing(qtg.QFont.AbsoluteSpacing, 2)

            self.groupbox_high_probability.setFont(groupbox_title_font)
            self.groupbox_medium_probability.setFont(groupbox_title_font)
            self.groupbox_low_probability.setFont(groupbox_title_font)
            self.groupbox_list_patients.setFont(groupbox_title_font)

            self.groupbox_high_probability.setStyleSheet("""
            QGroupBox{
                border: 3px solid black;
                border-radius: 10px;
                background-color: """ + variable_bg_color_probability_groupbox + """;
                margin-top: 20px;
                }
                QGroupBox::title{
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 0 3px;
                    }""")
            self.groupbox_medium_probability.setStyleSheet(self.groupbox_high_probability.styleSheet())
            self.groupbox_low_probability.setStyleSheet(self.groupbox_high_probability.styleSheet())
            self.groupbox_list_patients.setStyleSheet(self.groupbox_high_probability.styleSheet())

            # Other.
            self.list_patients.setAlternatingRowColors(True)
            self.list_patients.setSortingEnabled(True)
            self.messagebox_delete_database_confirmation.setIcon(qtw.QMessageBox.Warning)
            self.messagebox_delete_database_confirmation.addButton('Yes',qtw.QMessageBox.YesRole)
            self.messagebox_delete_database_confirmation.addButton('No',qtw.QMessageBox.NoRole)

            # Label Loop.
            self.list_patient_info_label_names = [
                'ID',
                'First_Name',
                'Middle_Name',
                'Last_Name',
                'Gender',
                'Age',
                'DOB',
                'Height',
                'Weight'
                ]

            # self.list_patient_info_labels = []
            # self.list_input_patient_info_labels = []

            self.variable_patient_info_label_loop_y_coordinate = self.groupbox_list_patients.y()+20

            for pinfo in self.list_patient_info_label_names:
                    label_info = 'self.label_'+pinfo
                    self.dict_widget_names[self.variable_widget_count] = label_info
                    label_info = qtw.QLabel()
                    self.dict_widgets[self.variable_widget_count] = label_info
                    self.variable_widget_count = self.variable_widget_count + 1
                    label_input_info = 'self.label_input_'+pinfo
                    self.dict_widget_names[self.variable_widget_count] = label_input_info
                    label_input_info = qtw.QLabel()
                    self.dict_widgets[self.variable_widget_count] = label_input_info
                    self.variable_widget_count = self.variable_widget_count + 1

                    # self.list_patient_info_labels.append(label_info)
                    # self.list_input_patient_info_labels.append(label_input_info)

                    label_info.setText(pinfo+':')
                    label_info.setAlignment(qt.AlignCenter)
                    label_info.setStyleSheet('text-decoration: underline;')
                    label_info.adjustSize()
                    label_info.move(self.groupbox_list_patients.x()+self.groupbox_list_patients.width()+20,self.variable_patient_info_label_loop_y_coordinate)
                    label_input_info.move((label_info.x()+label_info.width()+5),label_info.y())

                    self.variable_patient_info_label_loop_y_coordinate = self.variable_patient_info_label_loop_y_coordinate+25
                    
                    label_info.setParent(self.diagnosis_tab)
                    label_input_info.setParent(self.diagnosis_tab)
  
        class Statusbar:
            self.statusbar = qtw.QStatusBar()
            self.statusbar.setStyleSheet('border: 2px solid black;background-color:gray;')
            self.statusbar.setSizeGripEnabled(False)

            self.statusbar.setFixedSize(self.width(),25)
            self.statusbar.move(0,(self.height()-self.statusbar.height()))
            self.statusbar.setWindowFlags(qt.WindowStaysOnTopHint)
            self.statusbar.setParent(self)

            self.datetime_now = dt.datetime.now()
            statusbar_datetime = self.datetime_now.strftime('%H:%M:%S')
            self.labelstatusbar_datetime = qtw.QLabel(str(statusbar_datetime), self.statusbar)
            self.labelstatusbar_datetime.setFixedSize(55,self.statusbar.height())
            self.labelstatusbar_datetime.setAlignment(qt.AlignCenter)
            self.labelstatusbar_datetime.move((self.statusbar.width()-self.labelstatusbar_datetime.width()),0)
            self.labelstatusbar_datetime.setStyleSheet('background-color:darkgray')

            datetime_font = self.labelstatusbar_datetime.font()
            datetime_font.setBold(True)
            datetime_font = self.labelstatusbar_datetime.setFont(datetime_font) 

        class hematology:
            # Creating Widgets.
            self.pushbutton_save_hematology = qtw.QPushButton()
            self.pushbutton_clear_hematology = qtw.QPushButton()
            # Set Text.
            self.pushbutton_save_hematology.setText('Save')
            self.pushbutton_clear_hematology.setText('Clear')
            # Adjust Size.
            self.pushbutton_save_hematology.adjustSize()
            self.pushbutton_clear_hematology.adjustSize()
            # Move.
            self.pushbutton_save_hematology.move(20,20)
            self.pushbutton_clear_hematology.move((self.pushbutton_save_hematology.x()+self.pushbutton_save_hematology.width()+20),self.pushbutton_save_hematology.y())
            # Set Parent.
            self.pushbutton_save_hematology.setParent(self.hematology_tab)
            self.pushbutton_clear_hematology.setParent(self.hematology_tab)
            # Connect.
            self.pushbutton_save_hematology.clicked.connect(self.save_hematology_info)
            # Initializing.
            start_y = 75
            # Hematology Test List.
            hematology_tests = {
                'PLT':'x10^3/mL',
                'WBC':'x10^3/mL',
                'RBC':'x10^6/mL',
                'HGB':'g/dL',
                'HCT':'%',
                'MCV':'fL',
                'MCH':'pg',
                'MCHC':'g/dL',
                'RDW':'%',
                'MPV':'fL',
                'PER_NEUT':'%',
                'PER_LYMPH':'%',
                'PER_MONO':'%',
                'PER_EOS':'%',
                'PER_BASO':'%',
                'PER_IG':'%',
                'ABS_NEUT':'x10^3/mL',
                'ABS_LYMPH':'x10^3/mL',
                'ABS_MONO':'x10^3/mL',
                'ABS_EOS':'x10^3/mL',
                'ABS_BASO':'x10^3/mL',
                'ABS_IG':'x10^3/mL'}
            # Loop to make Hematology Test Labels and Inputs.
            for test,unit in hematology_tests.items():
                label_test = 'self.label_heme_'+test
                self.dict_widget_names[self.variable_widget_count] = label_test
                label_test = qtw.QLabel()
                self.dict_widgets[self.variable_widget_count] = label_test

                self.variable_widget_count = self.variable_widget_count +1

                lineedit_test = 'self.lineedit_heme_'+test
                self.dict_widget_names[self.variable_widget_count] = lineedit_test
                lineedit_test = qtw.QLineEdit()
                self.dict_widgets[self.variable_widget_count] = lineedit_test

                self.variable_widget_count = self.variable_widget_count + 1

                label_test_unit = 'self.label_heme_'+test+'_unit'
                self.dict_widget_names[self.variable_widget_count] = label_test_unit
                label_test_unit = qtw.QLabel()
                self.dict_widgets[self.variable_widget_count] = label_test_unit

                self.variable_widget_count = self.variable_widget_count + 1
                # Set Text.
                label_test.setText(test)
                label_test_unit.setText(unit)
                # Set Parent.
                label_test.setParent(self.hematology_tab)
                lineedit_test.setParent(self.hematology_tab)
                label_test_unit.setParent(self.hematology_tab)
                # Set Fixed Width.
                label_test.setFixedWidth(60)
                lineedit_test.setFixedWidth(60)
                # Move.
                label_test.move(20,start_y)
                lineedit_test.move((label_test.x()+label_test.width()+10),start_y-3)
                label_test_unit.move((lineedit_test.x()+lineedit_test.width()+5),start_y)
                # Set Alignment.
                label_test.setAlignment(qt.AlignRight)
                lineedit_test.setAlignment(qt.AlignRight)
                # Other.
                validator = qtg.QRegExpValidator(self.regexp_input_num)
                lineedit_test.setValidator(validator)

                
                start_y = start_y + 30

        class exit_button: # Exit Button.
            self.pushbutton_exit = qtw.QPushButton()
            self.pushbutton_exit.setText('- E X I T -')
            self.pushbutton_exit.adjustSize()
            self.pushbutton_exit.move((self.width()-self.pushbutton_exit.width()-25), (self.statusbar.y()-self.pushbutton_exit.height()-35))
            self.pushbutton_exit.setParent(self.diagnosis_tab)
            self.pushbutton_exit.setStyleSheet('background-color: red; font: 13px; font: bold; spacing: 10; border: 2px solid black;')
            self.pushbutton_exit.clicked.connect(self.exit_application)
           
        class timer_statusbar_update: # Status Bar Update Timer
            self.timer_status_bar_update = qtc.QTimer()
            self.timer_status_bar_update.start(1000)
            self.timer_status_bar_update.timeout.connect(self.update_status_bar)

        self.update_id_track()

        def print_widget_list():
            for i in range(len(self.dict_widget_names)):
                print(str(i)+' '+self.dict_widget_names[i])

        print_widget_list()

        self.show()
        # END OF MAINWINDOW INIT.
    
    # START OF SELF FUNCTIONS.

    def load_patient_database(self):
        print('-----LOAD_PATIENT_DATABASE FUNCTION START-----')

        conn = sql.connect('patients.db')
        c = conn.cursor()

        load_patients = c.execute('SELECT ID,First_Name,Last_Name FROM Patient_List')
        database_patients = load_patients.fetchall()
        self.list_widget_patient_list = []
        self.list_patients.clear()

        for patient in database_patients:
            list_patient_widget = 'self.label_ptid_'+str(patient[0]) # Creating the Name of the Widget that will be used to Display each Patient onto the List.
            list_patient = str(patient[0])+' | '+str(patient[1])+' '+str(patient[2]) # The Text to be Displayed for Each Patient. (ID,F_Name,L_Name)
            list_patient_widget = qtw.QLabel()  
            self.list_widget_patient_list.append(list_patient_widget) # Adding the Widget for Each Patient to a List so that it will remain after the Loop.
            list_patient_widget.setText(list_patient)
            self.list_patients.addItem(list_patient)
            
        conn.commit()
        conn.close()

        for num, widget in self.dict_widget_names.items():
            if 'ID' in widget and 'lineedit' in widget:
                self.dict_widgets[num].setText(str(self.id_track))
            else:
                pass

    def update_status_bar(self):
        datetime_now = dt.datetime.now()
        statusbar_datetime = datetime_now.strftime('%H:%M:%S')
        self.labelstatusbar_datetime.setText(str(statusbar_datetime))

    def update_id_track(self):

        print('-----UPDATE_ID_TRACK FUNCTION START-----')

        self.selected_patient = ['cat','mouse']
        self.list_ids =[]

        conn = sql.connect('patients.db')
        c = conn.cursor()

        c.execute("""SELECT ID FROM Patient_List""") # Selecting all patient IDs from Database.
        pt_ids = c.fetchall() # Getting all patient IDs that were selected.
        for id in range(len(pt_ids)):
            self.list_ids.append((pt_ids[id])[0])
        if pt_ids == []:
            self.id_track = 1
        else:
            self.list_ids.append(0)
            for i in range(len(self.list_ids)):
                if (i+1) in self.list_ids:
                    pass
                else:
                    self.id_track = i +1
                    break
        for num,widget in self.dict_widget_names.items():
            if 'ID' in widget and 'lineedit' in widget:
                self.dict_widgets[num].setText(str(self.id_track))
            else:
                pass

        conn.commit()
        conn.close()

        self.load_patient_database()

    def save_patient_info(self):
        print('-----SAVE_PATIENT_INFO FUNCTION START-----')

        conn = sql.connect('patients.db')
        c = conn.cursor()
        
        given_ID = int(self.dict_widgets[1].text())
        given_age = 0

        self.list_save_patient_information = []

        for num,widget in self.dict_widget_names.items():
            if 'add' in widget:
                if 'lineedit' in widget:
                    if 'First_Name' in widget:
                        given_first_name = self.dict_widgets[num].text()
                        self.list_save_patient_information.append((given_first_name))
                    elif 'Middle_Name' in widget:
                        given_middle_name = self.dict_widgets[num].text()
                        self.list_save_patient_information.append(given_middle_name)
                    elif 'Last_Name' in widget:
                        given_last_name = self.dict_widgets[num].text()
                        self.list_save_patient_information.append(given_last_name)
                    elif 'Date_of_Birth' in widget:
                        given_dob = self.dict_widgets[num].text()
                        self.list_save_patient_information.append(given_dob)
                elif 'combobox' in widget:
                    if 'Gender' in widget:
                        given_gender = self.dict_widgets[num].currentText()
                        self.list_save_patient_information.append(given_gender)

        if given_dob != '':
            given_birth_day = int(given_dob.split('/')[1])
            given_birth_month = int(given_dob.split('/')[0])
            given_birth_year = int(given_dob.split('/')[2])
            def calculate_age(born):
                today = dt.date.today()
                return today.year - given_birth_year - ((today.month, today.day) < (given_birth_month, given_birth_day))
            given_age = calculate_age(given_dob)
        else:
            pass
        
        c.execute("""INSERT OR REPLACE INTO Patient_List ('ID','First_Name', 'Middle_Name', 'Last_Name','Gender', 'Age', 'DOB')
                    VALUES (:ID, :First_Name, :Middle_Name, :Last_Name, :Gender, :Age, :DOB) 
                    ON CONFLICT DO UPDATE SET ('ID','First_Name', 'Middle_Name', 'Last_Name','Gender', 'Age', 'DOB') = (:ID, :First_Name, :Middle_Name, :Last_Name, :Gender, :Age, :DOB)""",
            {
                'ID': given_ID,
                'First_Name': given_first_name,
                'Middle_Name': given_middle_name,
                'Last_Name': given_last_name,
                'Gender': given_gender,
                'Age': int(given_age),
                'DOB': given_dob
            }
        )

        conn.commit()
        conn.close()

        self.clear_patient_info()

        self.update_id_track()

    def save_hematology_info(self):
        
        current_selected_id = (self.selected_patient[0][0]) # Patient ID to save the hematology values for.

        patient_hematology_values = [] # List to save the variables with retrieved values.

        for num,widget in self.dict_widget_names.items():
            if 'heme' in widget and 'lineedit' in widget:
                if 'PLT' in widget:
                    given_plt = self.dict_widgets[num].text()
                    if given_plt == '':
                        given_plt = ' - '
                    elif given_plt == ' - ':
                        pass
                    patient_hematology_values.append(given_plt)
                if 'WBC' in widget:
                    given_wbc = self.dict_widgets[num].text()
                    if given_wbc == '':
                        given_wbc = ' - '
                    elif given_wbc == ' - ':
                        pass
                    patient_hematology_values.append(given_wbc)
                if 'RBC' in widget:
                    given_rbc = self.dict_widgets[num].text()
                    if given_rbc == '':
                        given_rbc = ' - '
                    elif given_rbc == ' - ':
                        pass
                    patient_hematology_values.append(given_rbc)
                if 'HCT' in widget:
                    given_hct = self.dict_widgets[num].text()
                    if given_hct == '':
                        given_hct = ' - '
                    elif given_hct == ' - ':
                        pass
                    patient_hematology_values.append(given_hct)
                if 'MCV' in widget:
                    given_mcv = self.dict_widgets[num].text()
                    if given_mcv == '':
                        given_mcv = ' - '
                    elif given_mcv == ' - ':
                        pass
                    patient_hematology_values.append(given_mcv)
                if 'MCH' in widget:
                    given_mch = self.dict_widgets[num].text()
                    if given_mch == '':
                        given_mch = ' - '
                    elif given_mch == ' - ':
                        pass
                    patient_hematology_values.append(given_mch)
                if 'MCHC' in widget:
                    given_mchc = self.dict_widgets[num].text()
                    if given_mchc == '':
                        given_mchc = ' - '
                    elif given_mchc == ' - ':
                        pass
                    patient_hematology_values.append(given_mchc)
                if 'RDW' in widget:
                    given_rdw = self.dict_widgets[num].text()
                    if given_rdw == '':
                        given_rdw = ' - '
                    elif given_rdw == ' - ':
                        pass
                    patient_hematology_values.append(given_rdw)
                if 'MPV' in widget:
                    given_mpv = self.dict_widgets[num].text()
                    if given_mpv == '':
                        given_mpv = ' - '
                    elif given_mpv == ' - ':
                        pass
                    patient_hematology_values.append(given_mpv)
                if 'PER_NEUT' in widget:
                    given_per_neut = self.dict_widgets[num].text()
                    if given_per_neut == '':
                        given_per_neut = ' - '
                    elif given_per_neut == ' - ':
                        pass
                    patient_hematology_values.append(given_per_neut)
                if 'PER_LYMPH' in widget:
                    given_per_lymph = self.dict_widgets[num].text()
                    if given_per_lymph == '':
                        given_per_lymph = ' - '
                    elif given_per_lymph == ' - ':
                        pass
                    patient_hematology_values.append(given_per_lymph)
                if 'PER_MONO' in widget:
                    given_per_mono = self.dict_widgets[num].text()
                    if given_per_mono == '':
                        given_per_mono = ' - '
                    elif given_per_mono == ' - ':
                        pass
                    patient_hematology_values.append(given_per_mono)
                if 'PER_EOS' in widget:
                    given_per_eos = self.dict_widgets[num].text()
                    if given_per_eos == '':
                        given_per_eos = ' - '
                    elif given_per_eos == ' - ':
                        pass
                    patient_hematology_values.append(given_per_eos)
                if 'PER_BASO' in widget:
                    given_per_baso = self.dict_widgets[num].text()
                    if given_per_baso == '':
                        given_per_baso = ' - '
                    elif given_per_baso == ' - ':
                        pass
                    patient_hematology_values.append(given_per_baso)
                if 'PER_IG' in widget:
                    given_per_ig = self.dict_widgets[num].text()
                    if given_per_ig == '':
                        given_per_ig = ' - '
                    elif given_per_ig == ' - ':
                        pass
                    patient_hematology_values.append(given_per_ig)
                if 'ABS_NEUT' in widget:
                    given_abs_neut = self.dict_widgets[num].text()
                    if given_abs_neut == '':
                        given_abs_neut = ' - '
                    elif given_abs_neut == ' - ':
                        pass
                    patient_hematology_values.append(given_abs_neut)
                if 'ABS_LYMPH' in widget:
                    given_abs_lymph = self.dict_widgets[num].text()
                    if given_abs_lymph == '':
                        given_abs_lymph = ' - '
                    elif given_abs_lymph == ' - ':
                        pass
                    patient_hematology_values.append(given_abs_lymph)
                if 'ABS_MONO' in widget:
                    given_abs_mono = self.dict_widgets[num].text()
                    if given_abs_mono == '':
                        given_abs_mono = ' - '
                    elif given_abs_mono == ' - ':
                        pass
                    patient_hematology_values.append(given_abs_mono)
                if 'ABS_EOS' in widget:
                    given_abs_eos = self.dict_widgets[num].text()
                    if given_abs_eos == '':
                        given_abs_eos = ' - '
                    elif given_abs_eos == ' - ':
                        pass
                    patient_hematology_values.append(given_abs_eos)
                if 'ABS_BASO' in widget:
                    given_abs_baso = self.dict_widgets[num].text()
                    if given_abs_baso == '':
                        given_abs_baso = ' - '
                    elif given_abs_baso == ' - ':
                        pass
                    patient_hematology_values.append(given_abs_baso)
                if 'ABS_IG' in widget:
                    given_abs_ig = self.dict_widgets[num].text()
                    if given_abs_ig == '':
                        given_abs_ig = ' - '
                    elif given_abs_ig == ' - ':
                        pass
                    patient_hematology_values.append(given_abs_ig)
                
        print(given_abs_mono)


    def edit_patient_info(self):

        print('-----EDIT_PATIENT_INFO FUNCTION START-----')
        
        current_row = self.list_patients.currentRow()+1
        if current_row == 0:
            print('Select A Patient')
            self.update_id_track()
        else:
            self.window_add_patient.show()
            current_id = (self.list_widget_patient_list[current_row-1].text()[0])
            self.selected_patient = self.selected_patient[0]
            conn = sql.connect('patients.db')
            c = conn.cursor()
            c.execute("SELECT * FROM Patient_List WHERE ID = (?)", (int(current_id),))
            column,selected_pt_info = c.description,c.fetchall()
            conn.commit()
            conn.close()
            
            list_columns = []
            for i in range(len(column[0])):
                list_columns.append(column[i][0])
            # print(list_columns)

            list_patient_info = []
            for i in range(len(selected_pt_info[0])):
                list_patient_info.append(selected_pt_info[0][i])
            # print(list_patient_info)

            for c in range(len(list_patient_info)):
                if 'ID' in list_columns[c]: # Selecting corresponding value from Database.
                    for num,wid in self.dict_widget_names.items(): # looping through the dictionary of input widgets.
                        if 'ID' in wid and 'line' in wid: # finding the corresponding widget in the dictionary.
                            self.dict_widgets[num].setText(str(list_patient_info[c])) # loading the selected database value to the corresponding input widget.
                elif 'First' in list_columns[c]: # Selecting corresponding value from Database.
                    for num,wid in self.dict_widget_names.items(): # looping through the dictionary of input widgets.
                        if 'First' in wid and 'line' in wid: # finding the corresponding widget in the dictionary.
                            self.dict_widgets[num].setText(str(list_patient_info[c])) # loading the selected database value to the corresponding input widget.
                elif 'Middle' in list_columns[c]: # Selecting corresponding value from Database.
                    for num,wid in self.dict_widget_names.items(): # looping through the dictionary of input widgets.
                        if 'Middle' in wid and 'line' in wid: # finding the corresponding widget in the dictionary.
                            self.dict_widgets[num].setText(str(list_patient_info[c])) # loading the selected database value to the corresponding input widget.
                elif 'Last' in list_columns[c]: # Selecting corresponding value from Database.
                    for num,wid in self.dict_widget_names.items(): # looping through the dictionary of input widgets.
                        if 'Last' in wid and 'line' in wid: # finding the corresponding widget in the dictionary.
                            self.dict_widgets[num].setText(str(list_patient_info[c])) # loading the selected database value to the corresponding input widget.
                elif 'Gender' in list_columns[c]: # Selecting corresponding value from Database.
                    for num,wid in self.dict_widget_names.items(): # looping through the dictionary of input widgets.
                        if 'Gender' in wid and 'combo' in wid: # finding the corresponding widget in the dictionary.
                            self.dict_widgets[num].setCurrentIndex(self.dict_widgets[num].findText(list_patient_info[c])) # loading the selected database value to the corresponding input widget.
                elif 'DOB' in list_columns[c]: # Selecting corresponding value from Database.
                    for num,wid in self.dict_widget_names.items(): # looping through the dictionary of input widgets.
                        if 'Date' in wid and 'line' in wid: # finding the corresponding widget in the dictionary.
                            self.dict_widgets[num].setText(str(list_patient_info[c])) # loading the selected database value to the corresponding input widget.
                            print(str(list_patient_info[c]))

    def clear_patient_info(self):
        print('-----CLEAR_PATIENT_INFO FUNCTION START-----')

        for num,widget in self.dict_widget_names.items():
            if 'combobox' in widget:
                self.dict_widgets[num].setCurrentIndex(0)
            elif 'lineedit' in widget and 'ID' not in widget:
                self.dict_widgets[num].clear()
            
    def remove_patient_info(self):
        print('-----REMOVE_PATIENT_INFO FUNCTION START-----')
        current_row = self.list_patients.currentRow()+1
        if current_row == 0:
            print('Select A Patient')
            self.update_id_track()
        else:
            clicked_patient_id = self.list_patients.currentItem().text()[0]

            conn = sql.connect('patients.db')
            c = conn.cursor()
            c.execute("DELETE FROM Patient_List WHERE ID = (?)", (int(clicked_patient_id),))
            conn.commit()
            conn.close()

            if str(self.loaded_patient) == str(clicked_patient_id):
                for num, widget in self.dict_widget_names.items():
                        if 'label' in widget and 'input' in widget and 'add' not in widget:
                            self.dict_widgets[num].setText('')
                self.update_id_track()
            else:
                self.update_id_track()

    def load_dblclicked_pt(self):
        print('-----LOAD_DBLCLICKED_PT FUNCTION START-----')

        clicked_patient_id = self.list_patients.currentItem().text()[0]
        self.loaded_patient = self.list_patients.currentItem().text()[0]

        conn = sql.connect('patients.db')
        c = conn.cursor()

        c.execute("SELECT * FROM Patient_List WHERE (ID = "+str(clicked_patient_id)+")")

        self.selected_patient = c.fetchall()
        print(self.selected_patient)
        conn.commit()
        conn.close()

        dict_selected_patient = {}

        list_database_columns = []
        for column in c.description:
            list_database_columns.append(column[0])

        list_selected_patient_info = []
        for info in range(len(self.selected_patient[0])):
            list_selected_patient_info.append(self.selected_patient[0][info])

        for column in range(len(list_database_columns)):
            dict_selected_patient[list_database_columns[column]] = list_selected_patient_info[column]

        for num,widget in self.dict_widget_names.items():
            for col,value in dict_selected_patient.items():
                if col in widget and 'input' in widget and 'add' not in widget:
                    self.dict_widgets[num].setText(str(value))
                    self.dict_widgets[num].setStyleSheet('text-decoration: underline;')
                    self.dict_widgets[num].adjustSize()

        self.tab_bar.setTabEnabled(1, True)
        self.tab_bar.setTabEnabled(2, True)
        self.tab_bar.setTabEnabled(3, True)
        self.tab_bar.setTabEnabled(4, True)
        self.tab_bar.setTabEnabled(5, True)
        self.tab_bar.setTabEnabled(6, True)
        self.tab_bar.setTabEnabled(7, True)

    def check_dob_input(self):
        for num,widget in self.dict_widget_names.items():
            if 'Date' in widget and 'lineedit' in widget:
                if self.dict_widgets[num].hasAcceptableInput() == False:
                    self.pushbutton_save_patient_info.setDisabled(True)
                    print('unacceptable input')
                elif self.dict_widgets[num].hasAcceptableInput() == True:
                    self.pushbutton_save_patient_info.setEnabled(True)
                    print('acceptable input')

    def add_patient_info(self):
        self.window_add_patient.close()
        self.clear_patient_info()
        self.update_id_track()
        self.window_add_patient.show()


    def delete_database(self,button):
        if 'Yes' in button.text(): # Checks if the Yes Button was clicked.
            self.messagebox_delete_database_confirmation.show()
            conn = sql.connect('patients.db')
            c = conn.cursor()
            c.execute("DELETE FROM Patient_List")
            conn.commit()
            conn.close()
            print('----- DATABASE CLEARED -----')
            self.update_id_track()
        else:
            print('-----CANCELLED-----')

    def exit_application(self):
        self.window_add_patient.close()
        self.close()

    # END OF SELF FUNCTIONS.

app = qtw.QApplication([])
mw = MainWindow()
app.exec_()
# END OF APP.

### TO DO ###
    # Set Input Constraints.
    # When Patient List has >9 Patients, Patient IDs > 10 insert at the wrong place.
    # If a patient is edit while loaded, the loaded info needs to be updated.

# for num,widget in self.dict_widget_names.items():
#   if 'ID' in widget and 'lineedit' in widget:
#       self.dict_widgets[num].setText(some variable)
#   elif 'Name' ....:
#       pass