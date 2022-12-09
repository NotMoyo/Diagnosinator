import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
from PyQt5.QtCore import Qt as qt
from PyQt5.QtCore import QRect as qr
import PyQt5.QtGui as qtg
import time as tm
import datetime as dt
import sqlite3 as sql
import requests as rq
import json as js

class Class_Patient_Information:
    def __init__(self, ID, First_Name, Middle_Name, Last_Name, Gender, DOB):
        self.ID = ID
        self.First_Name = First_Name
        self.Middle_Name = Middle_Name
        self.Last_Name = Last_Name
        self.Gender = Gender
        self.DOB = DOB
        
        def Age_Calculation(self):
            if self.DOB != '':
                given_birth_day = int(self.DOB.split('/')[1])
                given_birth_month = int(self.DOB.split('/')[0])
                given_birth_year = int(self.DOB.split('/')[2])
                def calculate_age(born):
                    today = dt.date.today()
                    return today.year - given_birth_year - ((today.month, today.day) < (given_birth_month, given_birth_day))
                self.Age = calculate_age(self.DOB)
                return self.Age
            else:
                return 0
        self.Age = Age_Calculation(self)

class Class_Patient_Heme_Results:
    def __init__(self, ID, PLT, WBC, RBC, HCT, MCV, MCH, MCHC, RDW, MPV, PER_NEUT, PER_LYMPH, PER_MONO, PER_EOS, PER_BASO, PER_IG, ABS_NEUT, ABS_LYMPH, ABS_MONO, ABS_EOS, ABS_BASO, ABS_IG):
        self.ID = ID
        self.PLT = PLT
        self.WBC = WBC
        self.RBC = RBC
        self.HCT = HCT
        self.MCV = MCV
        self.MCH = MCH
        self.MCHC = MCHC
        self.RDW = RDW
        self.MPV = MPV
        self.PER_NEUT = PER_NEUT
        self.PER_LYMPH = PER_LYMPH
        self.PER_MONO = PER_MONO
        self.PER_EOS = PER_EOS
        self.PER_BASO = PER_BASO
        self.PER_IG = PER_IG
        self.ABS_NEUT = ABS_NEUT
        self.ABS_LYMPH = ABS_LYMPH
        self.ABS_MONO = ABS_MONO
        self.ABS_EOS = ABS_EOS
        self.ABS_BASO = ABS_BASO
        self.ABS_IG = ABS_IG

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
        self.new_dict_widgets = {}

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
                        self.new_dict_widgets['save_'+pinfo+'_label'] = label_add_info # Adding the Save pinfo Label to Dict.

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
                            self.new_dict_widgets['save_'+pinfo+'_lineedit'] = lineedit_add_info # Adding the Save pinfo Lineedit to Dict.

                            self.variable_widget_count = self.variable_widget_count + 1
                            

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
                            self.new_dict_widgets['save_'+pinfo+'_doublespinbox'] = doublespinbox_add_info # Adding the Save pinfo Doublespinbox to Dict.
                            
                            self.variable_widget_count = self.variable_widget_count + 1

                            doublespinbox_add_info.move((int(label_add_info.x()+label_add_info.width()+5)),label_add_info.y()-3)
                            doublespinbox_add_info.setParent(self.window_add_patient)

                        elif 'Name'in label_add_info.text():
                            lineedit_add_info = 'self.lineedit_add_'+pinfo
                            self.dict_widget_names[self.variable_widget_count] = lineedit_add_info
                            lineedit_add_info = qtw.QLineEdit()
                            self.dict_widgets[self.variable_widget_count] = lineedit_add_info
                            self.new_dict_widgets['save_'+pinfo+'_lineedit'] = lineedit_add_info # Adding the Save pinfo Lineedit to Dict.

                            self.variable_widget_count = self.variable_widget_count + 1
                            
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
                            self.new_dict_widgets['save_'+pinfo+'_lineedit'] = lineedit_add_info # Adding the Save pinfo Lineedit to Dict.

                            self.variable_widget_count = self.variable_widget_count + 1

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
                            self.new_dict_widgets['save_'+pinfo+'_combobox'] = combobox_add_info

                            self.variable_widget_count = self.variable_widget_count + 1

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

                uhcloseevent = qtg.QCloseEvent()

                uhcloseevent.accept()


                self.window_add_patient.closeEvent(uhcloseevent)

            # Creating Widgets.
            self.list_patients = qtw.QListWidget()
            self.list_symptom_search = qtw.QListWidget()
            self.groupbox_list_patients = qtw.QGroupBox()
            self.groupbox_high_probability = qtw.QGroupBox()
            self.groupbox_medium_probability = qtw.QGroupBox()
            self.groupbox_low_probability = qtw.QGroupBox()
            self.groupbox_patient_symptoms = qtw.QGroupBox()
            self.lineedit_symptom_search = qtw.QLineEdit()
            self.pushbutton_add_patient = qtw.QPushButton()
            self.pushbutton_edit_patient = qtw.QPushButton()
            self.pushbutton_remove_patient = qtw.QPushButton()
            self.pushbutton_delete_database = qtw.QPushButton()
            self.pushbutton_messagebox_yes = qtw.QPushButton()
            self.pushbutton_messagebox_no = qtw.QPushButton()
            self.pushbutton_symptom_search = qtw.QPushButton()
            self.messagebox_delete_database_confirmation = qtw.QMessageBox()
            # Set Text.
            self.groupbox_list_patients.setTitle('List of Patients')
            self.groupbox_high_probability.setTitle('High Probability')
            self.groupbox_medium_probability.setTitle('Medium Probability')
            self.groupbox_low_probability.setTitle('Low Probability')
            self.groupbox_patient_symptoms.setTitle('Symptoms')
            self.pushbutton_add_patient.setText('Add Patient')
            self.pushbutton_edit_patient.setText('Edit Patient')
            self.pushbutton_remove_patient.setText('Remove Patient')
            self.pushbutton_delete_database.setText('Delete Database')
            self.pushbutton_messagebox_yes.setText('Yes')
            self.pushbutton_messagebox_yes.setText('No')
            self.pushbutton_symptom_search.setText('Search')
            self.messagebox_delete_database_confirmation.setText('Are You Sure You Want to Delete The Entire Database?')
            self.messagebox_delete_database_confirmation.setWindowTitle('Confirmation')
            # Set Style Sheet.
            self.list_patients.setStyleSheet('border: 3px solid black; border-radius:5px; background-color: #FDF5ED; alternate-background-color: #C0D4D8')
            self.lineedit_symptom_search.setStyleSheet('border: 2px solid black; border-radius:2px; background-color: #FDF5ED')
            self.list_symptom_search.setStyleSheet('border: 3px solid black; border-radius:5px; background-color: #FDF5ED; alternate-background-color: #C0D4D8')
            self.pushbutton_add_patient.setStyleSheet('border: 3px solid #CAC6D7; border-radius:3px; background-color: #EAE6FA; font: bold')
            self.pushbutton_edit_patient.setStyleSheet(self.pushbutton_add_patient.styleSheet())
            self.pushbutton_remove_patient.setStyleSheet(self.pushbutton_add_patient.styleSheet())
            self.pushbutton_delete_database.setStyleSheet(self.pushbutton_add_patient.styleSheet())
            self.groupbox_high_probability.setStyleSheet("""
            QGroupBox{
                border: 3px solid black;
                border-radius: 10px;
                background-color: #FDF5ED;
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
            self.groupbox_patient_symptoms.setStyleSheet(self.groupbox_high_probability.styleSheet())
            # Set Fixed Size.
            self.groupbox_list_patients.setFixedSize(200,(self.tab_bar.height()-450))
            self.pushbutton_remove_patient.setFixedSize((self.pushbutton_delete_database.sizeHint().width()),25)
            self.pushbutton_add_patient.setFixedSize(self.pushbutton_remove_patient.width(),self.pushbutton_remove_patient.height())
            self.pushbutton_edit_patient.setFixedSize(self.pushbutton_remove_patient.width(),self.pushbutton_remove_patient.height())
            self.pushbutton_delete_database.setFixedSize(self.pushbutton_remove_patient.width(),self.pushbutton_remove_patient.height())
            self.list_patients.setFixedSize(self.groupbox_list_patients.width(),self.groupbox_list_patients.height()-20)
            self.messagebox_delete_database_confirmation.setFixedSize(200,200)
            self.groupbox_high_probability.setFixedSize(200,300)
            self.groupbox_medium_probability.setFixedSize(self.groupbox_high_probability.width(),self.groupbox_high_probability.height())
            self.groupbox_low_probability.setFixedSize(self.groupbox_high_probability.width(),self.groupbox_high_probability.height())
            self.lineedit_symptom_search.setFixedSize(200,25)
            self.list_symptom_search.setFixedSize(475,300)
            self.groupbox_patient_symptoms.setFixedSize(self.groupbox_high_probability.width(),self.list_symptom_search.height()+20)
            self.pushbutton_symptom_search.setFixedSize(75,25)
            # Move.
            self.groupbox_list_patients.move(20,20)
            self.pushbutton_remove_patient.move(((self.groupbox_list_patients.frameGeometry().right())+20),((self.groupbox_list_patients.frameGeometry().bottom()))-25)
            self.pushbutton_add_patient.move(self.pushbutton_remove_patient.x(),(self.pushbutton_remove_patient.frameGeometry().top()-40))
            self.pushbutton_edit_patient.move(((self.pushbutton_add_patient.frameGeometry().right())+20),(self.pushbutton_add_patient.y()))
            self.pushbutton_delete_database.move(self.pushbutton_edit_patient.x(),self.pushbutton_remove_patient.y())
            self.list_patients.move(0,20)
            self.groupbox_high_probability.move(500,20)
            self.groupbox_medium_probability.move((self.groupbox_high_probability.x()+self.groupbox_high_probability.width()+25),self.groupbox_high_probability.y())
            self.groupbox_low_probability.move((self.groupbox_medium_probability.x()+self.groupbox_medium_probability.width()+25),self.groupbox_high_probability.y())
            self.lineedit_symptom_search.move(20,((self.groupbox_list_patients.frameGeometry().bottom())+25))
            self.list_symptom_search.move(self.lineedit_symptom_search.x(),(self.lineedit_symptom_search.y()+self.lineedit_symptom_search.height())+20)
            self.groupbox_patient_symptoms.move(self.groupbox_high_probability.x(),self.list_symptom_search.y()-20)
            self.pushbutton_symptom_search.move((self.lineedit_symptom_search.frameGeometry().right()+20),self.lineedit_symptom_search.y())
            # Set Parent.
            self.list_patients.setParent(self.groupbox_list_patients)
            self.list_symptom_search.setParent(self.diagnosis_tab)
            self.groupbox_list_patients.setParent(self.diagnosis_tab)
            self.groupbox_high_probability.setParent(self.diagnosis_tab)
            self.groupbox_medium_probability.setParent(self.diagnosis_tab)
            self.groupbox_low_probability.setParent(self.diagnosis_tab)
            self.groupbox_patient_symptoms.setParent(self.diagnosis_tab)
            self.lineedit_symptom_search.setParent(self.diagnosis_tab)
            self.pushbutton_add_patient.setParent(self.diagnosis_tab)
            self.pushbutton_edit_patient.setParent(self.diagnosis_tab)
            self.pushbutton_remove_patient.setParent(self.diagnosis_tab)
            self.pushbutton_delete_database.setParent(self.diagnosis_tab)
            self.pushbutton_symptom_search.setParent(self.diagnosis_tab)
            # Connect.
            self.pushbutton_add_patient.clicked.connect(self.add_patient_info)
            self.pushbutton_edit_patient.clicked.connect(self.edit_patient_info)
            self.pushbutton_remove_patient.clicked.connect(self.remove_patient_info)
            self.pushbutton_delete_database.clicked.connect(self.messagebox_delete_database_confirmation.exec)
            self.pushbutton_symptom_search.clicked.connect(self.update_symptom_search)
            self.list_patients.itemDoubleClicked.connect(self.load_dblclicked_pt)
            self.list_symptom_search.itemDoubleClicked.connect(self.add_selected_symptom)
            self.messagebox_delete_database_confirmation.buttonClicked.connect(self.delete_database)
            
            
            # Set Font.
            groupbox_title_font = qtg.QFont()
            groupbox_title_font.setBold(True)
            groupbox_title_font.setPixelSize(14)
            groupbox_title_font.setLetterSpacing(qtg.QFont.AbsoluteSpacing, 2)

            self.groupbox_high_probability.setFont(groupbox_title_font)
            self.groupbox_medium_probability.setFont(groupbox_title_font)
            self.groupbox_low_probability.setFont(groupbox_title_font)
            self.groupbox_list_patients.setFont(groupbox_title_font)
            self.groupbox_patient_symptoms.setFont(groupbox_title_font)

            

            # Other.
            self.list_patients.setAlternatingRowColors(True)
            self.list_symptom_search.setAlternatingRowColors(True)
            self.list_patients.setSortingEnabled(True)
            self.list_symptom_search.hide()
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

            self.variable_patient_info_label_loop_y_coordinate = self.groupbox_list_patients.y()+20

            for pinfo in self.list_patient_info_label_names:
                    label_info = 'self.label_'+pinfo
                    self.dict_widget_names[self.variable_widget_count] = label_info
                    label_info = qtw.QLabel()
                    self.dict_widgets[self.variable_widget_count] = label_info
                    self.new_dict_widgets['selected_'+pinfo+'_label'] = label_info # Adding Widget to Dictionary.
                    self.variable_widget_count = self.variable_widget_count + 1
                    lineedit_input_info = 'self.label_input_'+pinfo
                    self.dict_widget_names[self.variable_widget_count] = lineedit_input_info
                    lineedit_input_info = qtw.QLineEdit()
                    self.dict_widgets[self.variable_widget_count] = lineedit_input_info
                    self.new_dict_widgets['selected_'+pinfo+'_lineedit'] = lineedit_input_info
                    self.variable_widget_count = self.variable_widget_count + 1

                    # Set Text.
                    label_info.setText(pinfo+':')
                    # Set Alignment.
                    label_info.setAlignment(qt.AlignCenter)
                    # Set Style Sheet.
                    label_info.setStyleSheet('text-decoration: underline;')
                    lineedit_input_info.setStyleSheet('background-color: darkgray;')
                    # Adjust Size.
                    label_info.adjustSize()
                    # Move.
                    label_info.move(
                        ((self.groupbox_list_patients.x()+self.groupbox_list_patients.width()+75)-label_info.width()),
                        self.variable_patient_info_label_loop_y_coordinate)
                    lineedit_input_info.move((label_info.x()+label_info.width()+5),label_info.y())
                    # Set Parent
                    label_info.setParent(self.diagnosis_tab)
                    lineedit_input_info.setParent(self.diagnosis_tab)
                    # Other
                    lineedit_input_info.setReadOnly(True)
                    lineedit_input_info.setDisabled(True)
                    # Variable Edit.
                    self.variable_patient_info_label_loop_y_coordinate = self.variable_patient_info_label_loop_y_coordinate+25
                    
        
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
                self.new_dict_widgets['heme_'+test+'_label'] = label_test # Adding the heme test label to Dict.

                self.variable_widget_count = self.variable_widget_count +1

                lineedit_test = 'self.lineedit_heme_'+test
                self.dict_widget_names[self.variable_widget_count] = lineedit_test
                lineedit_test = qtw.QLineEdit()
                self.dict_widgets[self.variable_widget_count] = lineedit_test
                self.new_dict_widgets['heme_'+test+'_lineedit'] = lineedit_test # Adding the heme test lineedit to Dict.

                self.variable_widget_count = self.variable_widget_count + 1

                label_test_unit = 'self.label_heme_'+test+'_unit'
                self.dict_widget_names[self.variable_widget_count] = label_test_unit
                label_test_unit = qtw.QLabel()
                self.dict_widgets[self.variable_widget_count] = label_test_unit
                self.new_dict_widgets['heme_'+test+'_unit_label'] = label_test_unit # Adding the heme test unit label to Dict.

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
            for i in self.new_dict_widgets.keys():
                print(i)
            #for i in range(len(self.dict_widget_names)):
            #    print(str(i)+' '+self.dict_widget_names[i])

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

        self.new_dict_widgets['save_ID_lineedit'].setText(str(self.id_track))

        conn.commit()
        conn.close()

        self.load_patient_database()
    
    def update_symptom_search(self):
        if self.lineedit_symptom_search.text() == '':
            print('Enter a Search Term')
        else:
            print('searches symptom lol')
            self.list_symptom_search.clear()
            self.list_symptom_search.show()

            token_endpoint = 'https://icdaccessmanagement.who.int/connect/token'
            client_id = 'cc8be595-994e-41ca-b324-6fff4af501e3_74492fea-f0aa-4935-a2cf-751681707925'
            client_secret = 'o6a4IAjrvmmTgcSxRmaFTqzUxDFtHnKzgr0fjuP/NN4='
            scope = 'icdapi_access'
            grant_type = 'client_credentials'

            # set data to post
            payload = {'client_id': client_id,
               'client_secret': client_secret,
               'scope': scope,
               'grant_type': grant_type}

            # make request
            r = rq.post(token_endpoint, data=payload, verify=False).json()
            token = r['access_token']

            # access ICD API
            search_term = self.lineedit_symptom_search.text()
            uri = 'https://id.who.int/icd/release/11/2022-02/mms/search?q='+search_term

            # HTTP header fields to set
            headers = {'Authorization': 'Bearer ' + token,
                       'Accept': 'application/json',
                       'Accept-Language': 'en',
                       'API-Version': 'v2'}
        
            # make request
            r = rq.get(uri, headers=headers, verify=False)

            # filter and print result(s).
            dict_results = {}

            list_filtered_results_1 = []
            list_filtered_results_2 = []

            def result_filter_1(obj):
                filtered_result_1 = js.dumps(obj, sort_keys=True, indent=8, separators=(',',':')).split(',')
                for i in filtered_result_1:
                    list_filtered_results_1.append(i)
                
            result_filter_1(r.json())

            list_titles = []
            list_codes = []


            for i in range(len(list_filtered_results_1)):
                if 'title' in list_filtered_results_1[i]:
                    if 'Is' in list_filtered_results_1[i]: pass
                    else:
                        list_filtered_results_1[i] = str(list_filtered_results_1[i]).replace("<em class='found'>",'')
                        list_filtered_results_1[i] = str(list_filtered_results_1[i]).replace("</em>", '')
                        list_filtered_results_1[i] = str(list_filtered_results_1[i]).replace("  ", '')
                        list_filtered_results_1[i] = str(list_filtered_results_1[i]).replace('"','')
                        list_filtered_results_1[i] = str(list_filtered_results_1[i]).replace('title:','')
                        list_filtered_results_1[i] = str(list_filtered_results_1[i]).replace('\n','')
                        list_titles.append(list_filtered_results_1[i])
                if 'Code' in list_filtered_results_1[i]:
                    list_filtered_results_1[i] = str(list_filtered_results_1[i]).replace("  ", '')
                    list_filtered_results_1[i] = str(list_filtered_results_1[i]).replace('"','')
                    list_filtered_results_1[i] = str(list_filtered_results_1[i]).replace('theCode:','')
                    list_filtered_results_1[i] = str(list_filtered_results_1[i]).replace('\n','')
                    list_codes.append(list_filtered_results_1[i])

            # Adding Symptom Code and Symptom Title to Search Results Dictionary.
            for result in range(len(list_codes)):
                dict_results[list_codes[result]] = list_titles[result]

            
            for code,title in dict_results.items():
                self.list_symptom_search.addItem(str(code)+' | '+str(title))
                self.list_symptom_search.adjustSize()

    def add_selected_symptom(self):
        print('ooO symptom selected')

        print((self.list_symptom_search.currentItem().text()))

    def save_patient_info(self):
        print('-----SAVE PATIENT INFO FUNCTION START-----')

        conn = sql.connect('patients.db')
        c = conn.cursor()

        var_save_patient_info = Class_Patient_Information(
            ID = self.new_dict_widgets['save_ID_lineedit'].text(),
            First_Name = self.new_dict_widgets['save_First_Name_lineedit'].text(),
            Middle_Name = self.new_dict_widgets['save_Middle_Name_lineedit'].text(),
            Last_Name = self.new_dict_widgets['save_Last_Name_lineedit'].text(),
            Gender = self.new_dict_widgets['save_Gender_combobox'].currentText(),
            DOB = self.new_dict_widgets['save_Date_of_Birth_lineedit'].text()
            )

        c.execute("""INSERT OR REPLACE INTO Patient_List ('ID','First_Name', 'Middle_Name', 'Last_Name','Gender', 'Age', 'DOB')
                    VALUES (:ID, :First_Name, :Middle_Name, :Last_Name, :Gender, :Age, :DOB) 
                    ON CONFLICT DO UPDATE SET ('ID','First_Name', 'Middle_Name', 'Last_Name','Gender', 'Age', 'DOB') = (:ID, :First_Name, :Middle_Name, :Last_Name, :Gender, :Age, :DOB)""",
            {
                'ID': var_save_patient_info.ID,
                'First_Name': var_save_patient_info.First_Name,
                'Middle_Name': var_save_patient_info.Middle_Name,
                'Last_Name': var_save_patient_info.Last_Name,
                'Gender': var_save_patient_info.Gender,
                'Age': int(var_save_patient_info.Age),
                'DOB': var_save_patient_info.DOB
            }
        )

        conn.commit()
        conn.close()

        var_save_patient_heme = Class_Patient_Heme_Results(
            ID = self.new_dict_widgets['save_ID_lineedit'].text(),
            PLT = self.new_dict_widgets['heme_PLT_lineedit'].text(),
            WBC = self.new_dict_widgets['heme_WBC_lineedit'].text(),
            RBC = self.new_dict_widgets['heme_RBC_lineedit'].text(),
            HCT = self.new_dict_widgets['heme_HCT_lineedit'].text(),
            MCV = self.new_dict_widgets['heme_MCV_lineedit'].text(),
            MCH = self.new_dict_widgets['heme_MCH_lineedit'].text(),
            MCHC = self.new_dict_widgets['heme_MCHC_lineedit'].text(),
            RDW = self.new_dict_widgets['heme_RDW_lineedit'].text(),
            MPV = self.new_dict_widgets['heme_MPV_lineedit'].text(),
            PER_NEUT = self.new_dict_widgets['heme_PER_NEUT_lineedit'].text(),
            PER_LYMPH = self.new_dict_widgets['heme_PER_LYMPH_lineedit'].text(),
            PER_MONO = self.new_dict_widgets['heme_PER_MONO_lineedit'].text(),
            PER_EOS = self.new_dict_widgets['heme_PER_EOS_lineedit'].text(),
            PER_BASO = self.new_dict_widgets['heme_PER_BASO_lineedit'].text(),
            PER_IG = self.new_dict_widgets['heme_PER_IG_lineedit'].text(),
            ABS_NEUT = self.new_dict_widgets['heme_ABS_NEUT_lineedit'].text(),
            ABS_LYMPH = self.new_dict_widgets['heme_ABS_LYMPH_lineedit'].text(),
            ABS_MONO = self.new_dict_widgets['heme_ABS_MONO_lineedit'].text(),
            ABS_EOS = self.new_dict_widgets['heme_ABS_EOS_lineedit'].text(),
            ABS_BASO = self.new_dict_widgets['heme_ABS_BASO_lineedit'].text(),
            ABS_IG = self.new_dict_widgets['heme_ABS_IG_lineedit'].text()
            )
       
        conn = sql.connect('hematology.db')
        c = conn.cursor()

        c.execute("""INSERT INTO Patient_Results (
            'ID','PLT', 'WBC', 'RBC', 'HCT', 'MCV', 'MCH', 'MCHC', 'RDW', 'MPV', 
            'PER_NEUT', 'PER_LYMPH', 'PER_MONO', 'PER_EOS', 'PER_BASO', 'PER_IG', 
            'ABS_NEUT', 'ABS_LYMPH', 'ABS_MONO', 'ABS_EOS', 'ABS_BASO', 'ABS_IG'
            )
            VALUES (
            :ID,:PLT, :WBC, :RBC, :HCT, :MCV, :MCH, :MCHC, :RDW, :MPV, 
            :PER_NEUT, :PER_LYMPH, :PER_MONO, :PER_EOS, :PER_BASO, :PER_IG, 
            :ABS_NEUT, :ABS_LYMPH, :ABS_MONO, :ABS_EOS, :ABS_BASO, :ABS_IG
            )""",
            {
                'ID': var_save_patient_heme.ID,
                'PLT': var_save_patient_heme.PLT,
                'WBC': var_save_patient_heme.WBC,
                'RBC': var_save_patient_heme.RBC,
                'HCT': var_save_patient_heme.HCT,
                'MCV': var_save_patient_heme.MCV,
                'MCH': var_save_patient_heme.MCH,
                'MCHC': var_save_patient_heme.MCHC,
                'RDW': var_save_patient_heme.RDW,
                'MPV': var_save_patient_heme.MPV,
                'PER_NEUT': var_save_patient_heme.PER_NEUT,
                'PER_LYMPH': var_save_patient_heme.PER_LYMPH,
                'PER_MONO': var_save_patient_heme.PER_MONO,
                'PER_EOS': var_save_patient_heme.PER_EOS,
                'PER_BASO': var_save_patient_heme.PER_BASO,
                'PER_IG': var_save_patient_heme.PER_IG,
                'ABS_NEUT': var_save_patient_heme.ABS_NEUT,
                'ABS_LYMPH': var_save_patient_heme.ABS_LYMPH,
                'ABS_MONO': var_save_patient_heme.ABS_MONO,
                'ABS_EOS': var_save_patient_heme.ABS_EOS,
                'ABS_BASO': var_save_patient_heme.ABS_BASO,
                'ABS_IG': var_save_patient_heme.ABS_IG
            })
        conn.commit()
        conn.close()

        
        self.clear_patient_info()

        self.update_id_track()

    def save_hematology_info(self):
        print('-----SAVE PATIENT HEMATOLOGY RESULTS FUNCTION START-----')

        var_save_patient_heme = Class_Patient_Heme_Results(
            ID = self.new_dict_widgets['selected_ID_lineedit'].text(),
            PLT = self.new_dict_widgets['heme_PLT_lineedit'].text(),
            WBC = self.new_dict_widgets['heme_WBC_lineedit'].text(),
            RBC = self.new_dict_widgets['heme_RBC_lineedit'].text(),
            HCT = self.new_dict_widgets['heme_HCT_lineedit'].text(),
            MCV = self.new_dict_widgets['heme_MCV_lineedit'].text(),
            MCH = self.new_dict_widgets['heme_MCH_lineedit'].text(),
            MCHC = self.new_dict_widgets['heme_MCHC_lineedit'].text(),
            RDW = self.new_dict_widgets['heme_RDW_lineedit'].text(),
            MPV = self.new_dict_widgets['heme_MPV_lineedit'].text(),
            PER_NEUT = self.new_dict_widgets['heme_PER_NEUT_lineedit'].text(),
            PER_LYMPH = self.new_dict_widgets['heme_PER_LYMPH_lineedit'].text(),
            PER_MONO = self.new_dict_widgets['heme_PER_MONO_lineedit'].text(),
            PER_EOS = self.new_dict_widgets['heme_PER_EOS_lineedit'].text(),
            PER_BASO = self.new_dict_widgets['heme_PER_BASO_lineedit'].text(),
            PER_IG = self.new_dict_widgets['heme_PER_IG_lineedit'].text(),
            ABS_NEUT = self.new_dict_widgets['heme_ABS_NEUT_lineedit'].text(),
            ABS_LYMPH = self.new_dict_widgets['heme_ABS_LYMPH_lineedit'].text(),
            ABS_MONO = self.new_dict_widgets['heme_ABS_MONO_lineedit'].text(),
            ABS_EOS = self.new_dict_widgets['heme_ABS_EOS_lineedit'].text(),
            ABS_BASO = self.new_dict_widgets['heme_ABS_BASO_lineedit'].text(),
            ABS_IG = self.new_dict_widgets['heme_ABS_IG_lineedit'].text()
            )
       
        conn = sql.connect('hematology.db')
        c = conn.cursor()

        c.execute("""INSERT OR REPLACE INTO Patient_Results (
            'ID','PLT', 'WBC', 'RBC', 'HCT', 'MCV', 'MCH', 'MCHC', 'RDW', 'MPV', 
            'PER_NEUT', 'PER_LYMPH', 'PER_MONO', 'PER_EOS', 'PER_BASO', 'PER_IG', 
            'ABS_NEUT', 'ABS_LYMPH', 'ABS_MONO', 'ABS_EOS', 'ABS_BASO', 'ABS_IG'
            )
            VALUES (
            :ID,:PLT, :WBC, :RBC, :HCT, :MCV, :MCH, :MCHC, :RDW, :MPV, 
            :PER_NEUT, :PER_LYMPH, :PER_MONO, :PER_EOS, :PER_BASO, :PER_IG, 
            :ABS_NEUT, :ABS_LYMPH, :ABS_MONO, :ABS_EOS, :ABS_BASO, :ABS_IG
            ) 
            ON CONFLICT DO UPDATE SET (
            'ID','PLT', 'WBC', 'RBC', 'HCT', 'MCV', 'MCH', 'MCHC', 'RDW', 'MPV', 
            'PER_NEUT', 'PER_LYMPH', 'PER_MONO', 'PER_EOS', 'PER_BASO', 'PER_IG', 
            'ABS_NEUT', 'ABS_LYMPH', 'ABS_MONO', 'ABS_EOS', 'ABS_BASO', 'ABS_IG'
            ) = (
            :ID,:PLT, :WBC, :RBC, :HCT, :MCV, :MCH, :MCHC, :RDW, :MPV, 
            :PER_NEUT, :PER_LYMPH, :PER_MONO, :PER_EOS, :PER_BASO, :PER_IG, 
            :ABS_NEUT, :ABS_LYMPH, :ABS_MONO, :ABS_EOS, :ABS_BASO, :ABS_IG
            )""",
            {
                'ID': var_save_patient_heme.ID,
                'PLT': var_save_patient_heme.PLT,
                'WBC': var_save_patient_heme.WBC,
                'RBC': var_save_patient_heme.RBC,
                'HCT': var_save_patient_heme.HCT,
                'MCV': var_save_patient_heme.MCV,
                'MCH': var_save_patient_heme.MCH,
                'MCHC': var_save_patient_heme.MCHC,
                'RDW': var_save_patient_heme.RDW,
                'MPV': var_save_patient_heme.MPV,
                'PER_NEUT': var_save_patient_heme.PER_NEUT,
                'PER_LYMPH': var_save_patient_heme.PER_LYMPH,
                'PER_MONO': var_save_patient_heme.PER_MONO,
                'PER_EOS': var_save_patient_heme.PER_EOS,
                'PER_BASO': var_save_patient_heme.PER_BASO,
                'PER_IG': var_save_patient_heme.PER_IG,
                'ABS_NEUT': var_save_patient_heme.ABS_NEUT,
                'ABS_LYMPH': var_save_patient_heme.ABS_LYMPH,
                'ABS_MONO': var_save_patient_heme.ABS_MONO,
                'ABS_EOS': var_save_patient_heme.ABS_EOS,
                'ABS_BASO': var_save_patient_heme.ABS_BASO,
                'ABS_IG': var_save_patient_heme.ABS_IG
            }
        )
        conn.commit()
        conn.close()

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

        for lineedit,widget in self.new_dict_widgets.items():
            if 'heme' in lineedit and 'lineedit' in lineedit:
                widget.clear()

        clicked_patient_id = self.list_patients.currentItem().text()[0]
        self.loaded_patient = self.list_patients.currentItem().text()[0]

        conn = sql.connect('patients.db')
        c = conn.cursor()

        c.execute("SELECT * FROM Patient_List WHERE (ID = "+str(clicked_patient_id)+")")

        self.selected_patient = c.fetchall()
        self.columns = c.description
        dict_selected_patient = {}
        list_selected_patient_info = []
        list_database_columns = []
        for column in self.columns:
            list_database_columns.append(column[0])
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

        conn.commit()
        conn.close()

        conn = sql.connect('hematology.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM Patient_Results WHERE (ID = "+str(clicked_patient_id)+")")
        self.selected_patient = c.fetchall()
        self.selected_patient = self.selected_patient[0]
        print(str(self.selected_patient))


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
    # When Heme Index "Loses Focus" Calculate.
    # Set Input Constraints.
    # When Patient List has >9 Patients, Patient IDs > 10 insert at the wrong place.
    # If a patient is edit while loaded, the loaded info needs to be updated.
    # In future, maybe delay loading selected pt results in tabs until they are opened.

# for num,widget in self.dict_widget_names.items():
#   if 'ID' in widget and 'lineedit' in widget:
#       self.dict_widgets[num].setText(some variable)
#   elif 'Name' ....:
#       pass