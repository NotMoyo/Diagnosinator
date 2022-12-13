# Cleaning Code.
import json as js
import requests as rq
import sqlite3 as sql
import datetime as dt
import PyQt5.QtGui as qtg
from PyQt5.QtCore import Qt as qt
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw


class Class_Patient_Information:
    def __init__(self, ID: int, First_Name: str, Middle_Name: str, Last_Name: str, Gender: str, DOB: str):
        self.ID = ID
        self.First_Name = First_Name
        self.Middle_Name = Middle_Name
        self.Last_Name = Last_Name
        self.Gender = Gender
        self.DOB = DOB

        def Age_Calculation(self: 'Class_Patient_Information'):
            if self.DOB != '':
                given_birth_day = int(self.DOB.split('/')[1])
                given_birth_month = int(self.DOB.split('/')[0])
                given_birth_year = int(self.DOB.split('/')[2])

                def calculate_age(born: str):
                    today = dt.date.today()
                    return today.year - given_birth_year - ((today.month, today.day) < (given_birth_month, given_birth_day))
                self.Age = calculate_age(self.DOB)
                return self.Age
            else:
                return ''
        self.Age = Age_Calculation(self)


class Class_Patient_Symptoms:
    def __init__(self, ID: int, sym_code: str, sym_name: str):
        self.ID = ID
        self.sym_code = sym_code
        self.sym_name = sym_name


class Class_Patient_Heme_Results:
    def __init__(self, ID: int, PLT: int, WBC: int, RBC: int, HGB: int, HCT: int, MCV: int, MCH: int, MCHC: int, RDW: int, MPV: int, PER_NEUT: int, PER_LYMPH: int, PER_MONO: int, PER_EOS: int, PER_BASO: int, PER_IG: int, ABS_NEUT: int, ABS_LYMPH: int, ABS_MONO: int, ABS_EOS: int, ABS_BASO: int, ABS_IG: int):
        self.ID = ID
        self.PLT = PLT
        self.WBC = WBC
        self.RBC = RBC
        self.HGB = HGB
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


def initialize_database():
    global identity_track
    global var_sym_col_track
    var_sym_col_track = 1
    conn = sql.connect('patients.db')
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS [Patient_List](
                ID INT PRIMARY KEY UNIQUE,
                First_Name TEXT,
                Middle_Name TEXT,
                Last_Name TEXT,
                Gender Text,
                Age NUMERIC,
                DOB TEXT)""")
    c.execute(
        """CREATE TABLE IF NOT EXISTS [Patient_Symptoms](
                [ID] INT,
                [SYM_CODE] TEXT PRIMARY KEY,
                [SYM_NAME] TEXT,
                FOREIGN KEY (ID) REFERENCES [Patient_List](ID))""")
    c.execute(
        """CREATE TABLE IF NOT EXISTS [Hematology_Values](
                ID INT PRIMARY KEY UNIQUE,
                PLT NUMERIC,
                WBC NUMERIC,
                RBC NUMERIC,
                HGB NUMERIC,
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
                ABS_IG REAL,
                FOREIGN KEY (ID) REFERENCES [Patient_List](ID))""")

    c.execute("""SELECT ID FROM Patient_List""")
    identity_track = c.fetchall()
    # -#-# UNCOMMENT TO DROP TABLE #-#-#
    # c.execute("DROP TABLE Patient_List")
    # c.execute("DROP TABLE Hematology_Values")
    conn.commit()
    conn.close()
    print('----- FINISHED <')


initialize_database()


class MainWindow(qtw.QMainWindow):

    def __init__(self):

        super().__init__()
        # Initializing.
        # Needed for Remove Patient Function when no patient has been loaded.
        self.loaded_patient = ''
        self.variable_add_patient_info_label_loop_y_coordinate = 15
        self.dict_diag_widgets = {}
        self.dict_diag_add_pt_widgets = {}
        self.dict_heme_table_test_row_widgets = {}

        self.list_patient_info_label_names = (
            'ID',
            'First_Name',
            'Middle_Name',
            'Last_Name',
            'Gender',
            'Age',
            'DOB',
            'Height',
            'Weight')
        self.list_add_patient_info_label_names = (
            'ID',
            'First_Name',
            'Middle_Name',
            'Last_Name',
            'Gender',
            'Date_of_Birth',
            'Height',
            'Weight')
        self.list_hematology_tests = {
            'PLT': 'x10^3/mL',
            'WBC': 'x10^3/mL',
            'RBC': 'x10^6/mL',
            'HGB': 'g/dL',
            'HCT': '%',
            'MCV': 'fL',
            'MCH': 'pg',
            'MCHC': 'g/dL',
            'RDW': '%',
            'MPV': 'fL',
            'PER_NEUT': '%',
            'PER_LYMPH': '%',
            'PER_MONO': '%',
            'PER_EOS': '%',
            'PER_BASO': '%',
            'PER_IG': '%',
            'ABS_NEUT': 'x10^3/mL',
            'ABS_LYMPH': 'x10^3/mL',
            'ABS_MONO': 'x10^3/mL',
            'ABS_EOS': 'x10^3/mL',
            'ABS_BASO': 'x10^3/mL',
            'ABS_IG': 'x10^3/mL'}

        # Global.
        global identity_track

        self.id_track = identity_track
        if self.id_track == []:
            self.id_track = 1
        else:
            self.id_track = str(((identity_track[-1])[0]+1))

        self.mainscreen()

    def mainscreen(self):
        # ---START---#
        self.setWindowTitle('Diagnosinator')
        self.setGeometry(150, 150, 1200, 800)
        self.setMaximumSize(1200, 800)
        self.setMinimumSize(1200, 800)

        self.regexp()

    def regexp(self):

        self.datetime_now = dt.datetime.now()
        year_limit_ones = (self.datetime_now.strftime('%y')[-1])
        year_limit_tens = (self.datetime_now.strftime('%y')[-2])

        self.regexp_input_name = qtc.QRegExp('^[A-Za-z]{1,16}$')
        self.regexp_input_num = qtc.QRegExp(
            '(^\d{1,5}$)|(^\d{1,5}\.\d\d?$)')  # 0-99999.99
        self.regexp_input_date = qtc.QRegExp('(([1-9]|0[1-9]|1[0-2])'
                                             '/([1-9]|0[1-9]|[1-2]\d|3[0-1])'
                                             '/((19\d\d|20[0-'+str(int(year_limit_tens)-1)+']\d|20'+str(year_limit_tens)+'[0-'+year_limit_ones+']))|)')

        self.tab_set()

    def tab_set(self):

        self.tab_bar = qtw.QTabWidget(parent=self)
        self.tab_bar.setFixedSize(self.width(), self.height())

        self.tab_diagnosis = qtw.QWidget()
        self.tab_chemistry = qtw.QWidget()
        self.tab_hematology = qtw.QWidget()
        self.tab_coagulation = qtw.QWidget()
        self.tab_urinalysis = qtw.QWidget()
        self.tab_bloodbank = qtw.QWidget()
        self.tab_serology = qtw.QWidget()
        self.tab_microbiology = qtw.QWidget()

        self.tab_diagnosis.setAutoFillBackground(True)
        self.tab_chemistry.setAutoFillBackground(True)
        self.tab_hematology.setAutoFillBackground(True)
        self.tab_coagulation.setAutoFillBackground(True)
        self.tab_urinalysis.setAutoFillBackground(True)
        self.tab_bloodbank.setAutoFillBackground(True)
        self.tab_serology.setAutoFillBackground(True)
        self.tab_microbiology.setAutoFillBackground(True)

        self.tab_bar.addTab(self.tab_diagnosis, 'Diagnosis')
        self.tab_bar.addTab(self.tab_chemistry, 'Chemistry')
        self.tab_bar.addTab(self.tab_hematology, 'Hematology')
        self.tab_bar.addTab(self.tab_coagulation, 'Coagulation')
        self.tab_bar.addTab(self.tab_urinalysis, 'Urinalysis')
        self.tab_bar.addTab(self.tab_bloodbank, 'Blood Bank')
        self.tab_bar.addTab(self.tab_serology, 'Serology')
        self.tab_bar.addTab(self.tab_microbiology, 'Microbiology')

        self.p = qtg.QPalette()
        gradient = qtg.QLinearGradient(300, 200, 500, 800)
        gradient.setColorAt(0.0, qtg.QColor('#62646A'))
        gradient.setColorAt(1.0, qtg.QColor('#010314'))
        self.p.setBrush(qtg.QPalette.Window, qtg.QBrush(gradient))

        self.tab_diagnosis.setPalette(self.p)
        self.tab_chemistry.setPalette(self.p)
        self.tab_hematology.setPalette(self.p)
        self.tab_coagulation.setPalette(self.p)
        self.tab_urinalysis.setPalette(self.p)
        self.tab_bloodbank.setPalette(self.p)
        self.tab_serology.setPalette(self.p)
        self.tab_microbiology.setPalette(self.p)

        self.tab_bar.setTabEnabled(1, False)
        self.tab_bar.setTabEnabled(2, False)
        self.tab_bar.setTabEnabled(3, False)
        self.tab_bar.setTabEnabled(4, False)
        self.tab_bar.setTabEnabled(5, False)
        self.tab_bar.setTabEnabled(6, False)
        self.tab_bar.setTabEnabled(7, False)

        self.diagnosis_tab()

    def diagnosis_tab(self):  # Diagnosis Tab

        # Creating Widgets.
        self.table_patients = qtw.QTableWidget()

        self.list_symptom_search = qtw.QListWidget()

        self.lineedit_symptom_search = qtw.QLineEdit()

        self.pushbutton_add_patient = qtw.QPushButton()
        self.pushbutton_edit_patient = qtw.QPushButton()
        self.pushbutton_remove_patient = qtw.QPushButton()
        self.pushbutton_delete_database = qtw.QPushButton()
        self.pushbutton_messagebox_yes = qtw.QPushButton()
        self.pushbutton_messagebox_no = qtw.QPushButton()
        self.pushbutton_symptom_search = qtw.QPushButton()
        self.pushbutton_add_symptom = qtw.QPushButton()
        self.pushbutton_remove_symptom = qtw.QPushButton()

        self.messagebox_delete_database_confirmation = qtw.QMessageBox()

        self.label_patient_symptoms = qtw.QLabel()
        # Table Configuration.
        list_patients_table_columns = ['ID', 'First Name', 'Last Name', 'Age']
        self.table_patients.setColumnCount(len(list_patients_table_columns))
        self.table_patients.setHorizontalHeaderLabels(
            list_patients_table_columns)
        self.table_patients.setAlternatingRowColors(True)
        self.table_patients.setShowGrid(True)
        self.table_patients.resizeColumnsToContents()
        self.table_patients.resizeRowsToContents()
        self.table_patients.horizontalHeader().setSectionResizeMode(
            qtw.QHeaderView.ResizeToContents)
        self.table_patients.verticalHeader().setSectionResizeMode(
            qtw.QHeaderView.ResizeToContents)
        self.table_patients.setSizeAdjustPolicy(
            qtw.QAbstractScrollArea.AdjustToContents)
        self.table_patients.setEditTriggers(
            qtw.QAbstractItemView.NoEditTriggers)
        self.table_patients.setSelectionBehavior(
            qtw.QAbstractItemView.SelectRows)
        self.table_patients.horizontalHeader().setStretchLastSection(True)
        self.table_patients.verticalHeader().setMinimumWidth(25)
        self.table_patients.horizontalHeader().setMinimumHeight(30)
        # Set Text.
        self.pushbutton_add_patient.setText('Add Patient')
        self.pushbutton_edit_patient.setText('Edit Patient')
        self.pushbutton_remove_patient.setText('Remove Patient')
        self.pushbutton_delete_database.setText('Delete Database')
        self.pushbutton_messagebox_yes.setText('Yes')
        self.pushbutton_messagebox_yes.setText('No')
        self.pushbutton_symptom_search.setText('Search')
        self.pushbutton_add_symptom.setText('Add Symptom')
        self.pushbutton_remove_symptom.setText('Remove Symptom')

        self.messagebox_delete_database_confirmation.setText(
            'Are You Sure You Want to Delete The Entire Database?')
        self.messagebox_delete_database_confirmation.setWindowTitle(
            'Confirmation')
        # Size Variables.
        self.button_width, self.button_height = self.pushbutton_remove_symptom.sizeHint().width(), 20
        # Set Style Sheet.

        self.lineedit_symptom_search.setStyleSheet(
            'border: 2px solid black; border-radius:2px; background-color: #FDF5ED')

        # Set Fixed Size.

        self.messagebox_delete_database_confirmation.setFixedSize(200, 200)
        self.pushbutton_add_patient.setFixedSize(
            self.button_width, self.button_height)
        self.pushbutton_edit_patient.setFixedSize(
            self.button_width, self.button_height)
        self.pushbutton_remove_patient.setFixedSize(
            self.button_width, self.button_height)
        self.pushbutton_delete_database.setFixedSize(
            self.button_width, self.button_height)
        self.lineedit_symptom_search.setFixedSize(200, 25)
        self.list_symptom_search.setFixedSize(200, 200)
        self.table_patients.setFixedSize(475, 275)

        # Move.
        self.table_patients.move(10, 10)

        self.pushbutton_add_patient.move(self.table_patients.x(
        ), self.table_patients.y() + self.table_patients.height() + 10)
        self.pushbutton_edit_patient.move(self.pushbutton_add_patient.x(
        ), self.pushbutton_add_patient.y() + self.pushbutton_add_patient.height() + 10)
        self.pushbutton_remove_patient.move(self.pushbutton_edit_patient.x(
        ), self.pushbutton_edit_patient.y() + self.pushbutton_edit_patient.height() + 10)
        self.pushbutton_delete_database.move(self.pushbutton_remove_patient.x(
        ), self.pushbutton_remove_patient.y() + self.pushbutton_remove_patient.height() + 10)
        self.pushbutton_add_symptom.move(self.lineedit_symptom_search.x(
        ), self.lineedit_symptom_search.y() + self.lineedit_symptom_search.height() + 10)
        self.pushbutton_remove_symptom.move(self.pushbutton_add_symptom.x(
        ) + self.pushbutton_add_symptom.width() + 10, self.pushbutton_add_symptom.y())

        self.lineedit_symptom_search.move(self.pushbutton_add_patient.x(
        ) + self.pushbutton_add_patient.width() + 50, self.pushbutton_add_patient.y())
        self.list_symptom_search.move(self.pushbutton_add_patient.x(
        ) + self.pushbutton_add_patient.width() + 10, self.pushbutton_remove_patient.y())
        self.pushbutton_symptom_search.move(self.lineedit_symptom_search.x(
        ) + self.lineedit_symptom_search.width() + 10, self.lineedit_symptom_search.y())

        # Set Parent.
        self.table_patients.setParent(self.tab_diagnosis)

        self.list_symptom_search.setParent(self.tab_diagnosis)
        self.lineedit_symptom_search.setParent(self.tab_diagnosis)
        self.pushbutton_add_patient.setParent(self.tab_diagnosis)
        self.pushbutton_edit_patient.setParent(self.tab_diagnosis)
        self.pushbutton_remove_patient.setParent(self.tab_diagnosis)
        self.pushbutton_delete_database.setParent(self.tab_diagnosis)
        self.pushbutton_symptom_search.setParent(self.tab_diagnosis)
        self.pushbutton_add_symptom.setParent(self.tab_diagnosis)
        self.pushbutton_remove_symptom.setParent(self.tab_diagnosis)

        # Connect.
        self.pushbutton_add_patient.clicked.connect(self.add_patient_info)
        self.pushbutton_edit_patient.clicked.connect(self.edit_patient_info)
        self.pushbutton_remove_patient.clicked.connect(
            self.remove_patient_info)
        self.pushbutton_delete_database.clicked.connect(
            self.messagebox_delete_database_confirmation.exec)
        self.pushbutton_symptom_search.clicked.connect(self.search_symptom)
        self.pushbutton_add_symptom.clicked.connect(self.add_selected_symptom)
        self.pushbutton_remove_symptom.clicked.connect(
            self.remove_selected_symptom)
        self.messagebox_delete_database_confirmation.buttonClicked.connect(
            self.delete_database)
        # Other.
        self.list_symptom_search.setAlternatingRowColors(True)
        self.list_symptom_search.hide()
        self.pushbutton_add_symptom.hide()
        self.pushbutton_remove_symptom.hide()
        self.messagebox_delete_database_confirmation.setIcon(
            qtw.QMessageBox.Warning)
        self.messagebox_delete_database_confirmation.addButton(
            'Yes', qtw.QMessageBox.YesRole)
        self.messagebox_delete_database_confirmation.addButton(
            'No', qtw.QMessageBox.NoRole)

        self.tab_bar.show()
        self.window_add_patient()

    # New Window to Add a Patient to the Database.
    def window_add_patient(self):
        # Creating Widgets.
        self.window_add_patient = qtw.QWidget()
        self.pushbutton_save_patient_info = qtw.QPushButton()
        self.pushbutton_clear_patient_info = qtw.QPushButton()
        # Label Loop.
        for pinfowidget in range(len(self.list_add_patient_info_label_names)):
            pinfo = self.list_add_patient_info_label_names[pinfowidget]
            # Create Label.
            diag_add_pt_label_add_info = 'self.label_add_'+pinfo
            diag_add_pt_label_add_info = qtw.QLabel()
            # Adding Widget to Dictionary.
            self.dict_diag_add_pt_widgets[
                'save_' + pinfo+'_label'] = diag_add_pt_label_add_info
            # Set Text.
            diag_add_pt_label_add_info.setText(pinfo+':')
            # Set Fixed Width.
            diag_add_pt_label_add_info.setFixedWidth(80)
            # Set Style Sheet.
            diag_add_pt_label_add_info.setStyleSheet(
                'text-decoration: underline')
            # Set Alignment.
            diag_add_pt_label_add_info.setAlignment(qt.AlignRight)
            # Move.
            diag_add_pt_label_add_info.move(
                20, self.variable_add_patient_info_label_loop_y_coordinate)
            # Increment Y Coordinate. (For Next Label)
            self.variable_add_patient_info_label_loop_y_coordinate = self.variable_add_patient_info_label_loop_y_coordinate+25
            diag_add_pt_label_add_info.setParent(self.window_add_patient)

            if 'Date' in pinfo:
                # Create Line Edit.
                diag_add_pt_lineedit_add_info = 'self.lineedit_add_'+pinfo
                diag_add_pt_lineedit_add_info = qtw.QLineEdit()
                # Adding Widget to Dictionary.
                self.dict_diag_add_pt_widgets[
                    'save_'+pinfo + '_lineedit'] = diag_add_pt_lineedit_add_info
                # Move.
                diag_add_pt_lineedit_add_info.move(
                    (int(diag_add_pt_label_add_info.x()+diag_add_pt_label_add_info.width()+5)), diag_add_pt_label_add_info.y()-3)
                # Set Parent.
                diag_add_pt_lineedit_add_info.setParent(
                    self.window_add_patient)
                # Set Validator.
                validator = qtg.QRegExpValidator(self.regexp_input_date)
                diag_add_pt_lineedit_add_info.setValidator(validator)
                # Set Fixed Width.
                diag_add_pt_lineedit_add_info.setFixedWidth(100)
                # Set Alignment.
                diag_add_pt_lineedit_add_info.setAlignment(qt.AlignLeft)
                # Set Placeholder Text.
                diag_add_pt_lineedit_add_info.setPlaceholderText('MM/DD/YYYY')
                # Connect to Function.
                diag_add_pt_lineedit_add_info.textChanged.connect(
                    self.check_dob_input)
            elif 'eight' in diag_add_pt_label_add_info.text():
                # Create Double Spin Box.
                doublespinbox_add_info = 'self.doublespinbox_add_'+pinfo
                doublespinbox_add_info = qtw.QDoubleSpinBox()
                # Adding Widget to Dictionary.
                self.dict_diag_add_pt_widgets[
                    'save_'+pinfo + '_doublespinbox'] = doublespinbox_add_info
                # Move.
                doublespinbox_add_info.move(
                    (int(diag_add_pt_label_add_info.x()+diag_add_pt_label_add_info.width()+5)), diag_add_pt_label_add_info.y()-3)
                # Set Parent.
                doublespinbox_add_info.setParent(self.window_add_patient)
            elif 'Name' in diag_add_pt_label_add_info.text():
                # Create Line Edit.
                diag_add_pt_lineedit_add_info = 'self.lineedit_add_'+pinfo
                diag_add_pt_lineedit_add_info = qtw.QLineEdit()
                # Adding Widget to Dictionary.
                self.dict_diag_add_pt_widgets[
                    'save_'+pinfo + '_lineedit'] = diag_add_pt_lineedit_add_info
                # Move.
                diag_add_pt_lineedit_add_info.move(
                    (int(diag_add_pt_label_add_info.x()+diag_add_pt_label_add_info.width()+5)), diag_add_pt_label_add_info.y()-3)
                # Set Parent.
                diag_add_pt_lineedit_add_info.setParent(
                    self.window_add_patient)
                # Set Validator.
                validator = qtg.QRegExpValidator(self.regexp_input_name)
                diag_add_pt_lineedit_add_info.setValidator(validator)
                # Set Fixed Width.
                diag_add_pt_lineedit_add_info.setFixedWidth(100)
                # Set Alignment.
                diag_add_pt_lineedit_add_info.setAlignment(qt.AlignLeft)
            elif 'ID' in diag_add_pt_label_add_info.text():
                # Create Line Edit.
                diag_add_pt_lineedit_add_info = 'self.lineedit_add_'+pinfo
                diag_add_pt_lineedit_add_info = qtw.QLineEdit()
                # Adding Widget to Dictionary.
                self.dict_diag_add_pt_widgets[
                    'save_'+pinfo + '_lineedit'] = diag_add_pt_lineedit_add_info
                # Move.
                diag_add_pt_lineedit_add_info.move(
                    (int(diag_add_pt_label_add_info.x()+diag_add_pt_label_add_info.width()+5)), diag_add_pt_label_add_info.y()-3)
                # Set Parent.
                diag_add_pt_lineedit_add_info.setParent(
                    self.window_add_patient)
                # Set Text.
                diag_add_pt_lineedit_add_info.setText(str(self.id_track))
                # Set ReadOnly.
                diag_add_pt_lineedit_add_info.setReadOnly(True)
                # Set Fixed Width.
                diag_add_pt_lineedit_add_info.setFixedWidth(25)
                # Set Alignment.
                diag_add_pt_lineedit_add_info.setAlignment(qt.AlignCenter)
            elif 'Gender' in diag_add_pt_label_add_info.text():
                # Create Combo Box.
                combobox_add_info = 'self.combobox_add_'+pinfo
                combobox_add_info = qtw.QComboBox()
                # Adding Widget to Dictionary.
                self.dict_diag_add_pt_widgets[
                    'save_'+pinfo + '_combobox'] = combobox_add_info
                # Move.
                combobox_add_info.move(
                    (int(diag_add_pt_label_add_info.x()+diag_add_pt_label_add_info.width()+5)), diag_add_pt_label_add_info.y()-3)
                # Set Parent.
                combobox_add_info.setParent(self.window_add_patient)
                # Insert Items.
                combobox_add_info.insertItem(0, 'Unknown')
                combobox_add_info.insertItem(1, 'Male')
                combobox_add_info.insertItem(2, 'Female')
        # Set Text.
        self.window_add_patient.setWindowTitle('Add Patient')
        self.pushbutton_save_patient_info.setText('Save')
        self.pushbutton_clear_patient_info.setText('Clear')
        # Set Geometry.
        self.window_add_patient.setGeometry(500, 250, 500, 500)
        # Adjust Size.
        self.pushbutton_save_patient_info.adjustSize()
        self.pushbutton_clear_patient_info.adjustSize()
        # Move.
        self.pushbutton_save_patient_info.move(
            20, (self.window_add_patient.height()-50))
        self.pushbutton_clear_patient_info.move((self.pushbutton_save_patient_info.x(
        )+self.pushbutton_save_patient_info.width()+20), (self.window_add_patient.height()-50))
        # Set Parent.
        self.pushbutton_save_patient_info.setParent(self.window_add_patient)
        self.pushbutton_clear_patient_info.setParent(self.window_add_patient)
        # Connect
        self.pushbutton_save_patient_info.clicked.connect(
            self.save_patient_info)
        self.pushbutton_clear_patient_info.clicked.connect(
            self.clear_patient_info)
        # Other
        self.window_add_patient.setWindowFlags(qt.WindowStaysOnTopHint)
        self.window_add_patient.setPalette(self.p)

        uhcloseevent = qtg.QCloseEvent()

        uhcloseevent.accept()

        self.window_add_patient.closeEvent(uhcloseevent)

        self.statusbar()

    def statusbar(self):

        self.statusbar = qtw.QStatusBar()
        # Set Size Grip Enabled.
        self.statusbar.setSizeGripEnabled(False)
        # Set Window Flags.
        self.statusbar.setWindowFlags(qt.WindowStaysOnTopHint)
        # Set Parent.
        self.statusbar.setParent(self)

        self.datetime_now = dt.datetime.now()

        statusbar_datetime = self.datetime_now.strftime('%H:%M:%S')

        self.labelstatusbar_datetime = qtw.QLabel(
            str(statusbar_datetime), self.statusbar)
        # Set Fixed Size.
        self.statusbar.setFixedSize(self.width(), 25)
        self.labelstatusbar_datetime.setFixedSize(55, self.statusbar.height())
        # Set Alignment.
        self.labelstatusbar_datetime.setAlignment(qt.AlignCenter)
        # Move.
        self.statusbar.move(0, (self.height()-self.statusbar.height()))
        self.labelstatusbar_datetime.move(
            (self.statusbar.width()-self.labelstatusbar_datetime.width()), 0)
        # Set Style Sheet.
        self.statusbar.setStyleSheet(
            'border: 2px solid gray;background-color:lightgray;')
        self.labelstatusbar_datetime.setStyleSheet(
            'background-color:lightgray')
        # Font.
        datetime_font = self.labelstatusbar_datetime.font()
        # Set Bold.
        datetime_font.setBold(True)
        # Set Font.
        datetime_font = self.labelstatusbar_datetime.setFont(datetime_font)

        self.chemistry_tab()

    def chemistry_tab(self):
        self.hematology_tab()

    def hematology_tab(self):
        # Creating Widgets.
        self.table_heme_values = qtw.QTableWidget()
        self.pushbutton_save_hematology = qtw.QPushButton()
        self.pushbutton_clear_hematology = qtw.QPushButton()
        # Set Text.
        self.pushbutton_save_hematology.setText('Save')
        self.pushbutton_clear_hematology.setText('Clear')
        # Hematology Values Table Configuration.
        list_heme_values_table_columns = (
            'Test', 'Result', 'Units', 'Reference Range')
        self.table_heme_values.setColumnCount(
            len(list_heme_values_table_columns))
        self.table_heme_values.setHorizontalHeaderLabels(
            list_heme_values_table_columns)
        self.table_heme_values.horizontalHeader().setSectionResizeMode(
            qtw.QHeaderView.ResizeToContents)
        self.table_heme_values.verticalHeader().setSectionResizeMode(
            qtw.QHeaderView.ResizeToContents)
        self.table_heme_values.setSizeAdjustPolicy(
            qtw.QAbstractScrollArea.AdjustToContents)
        self.table_heme_values.setAlternatingRowColors(True)
        self.table_heme_values.setFrameStyle(qtw.QFrame.Panel)
        self.table_heme_values.setFrameShadow(qtw.QFrame.Sunken)
        # Adjust Size.
        self.pushbutton_save_hematology.adjustSize()
        self.pushbutton_clear_hematology.adjustSize()
        # Move.
        self.pushbutton_save_hematology.move(20, 20)
        self.pushbutton_clear_hematology.move((self.pushbutton_save_hematology.x(
        )+self.pushbutton_save_hematology.width()+50), self.pushbutton_save_hematology.y())
        self.table_heme_values.move(20, self.pushbutton_save_hematology.y(
        )+self.pushbutton_save_hematology.height()+20)
        # Set Parent.
        self.table_heme_values.setParent(self.tab_hematology)
        self.pushbutton_save_hematology.setParent(self.tab_hematology)
        self.pushbutton_clear_hematology.setParent(self.tab_hematology)
        # Connect.
        self.pushbutton_save_hematology.clicked.connect(
            self.save_hematology_info)
        self.pushbutton_clear_hematology.clicked.connect(
            self.clear_hematology_info)
        # Set Style Sheet.
        # self.table_heme_values.setStyleSheet(
        #     'border: 1px outset black;background-color:#A0A1A7; alternate-background-color:#55828B;gridline-color: black; ')
        # Increment Variable.
        start_y = 75
        # Heme Validators.
        self.regexp_input_PLT = qtc.QRegExp(  # 0-9999.99
            '\d?\d?\d?\d?(\.\d\d?)?')
        self.regexp_input_WBC = qtc.QRegExp(  # 0-1999.99
            '^(0|1\d?\d?\d?|[1-9]\d?\d?)?(\.\d\d?)?$')
        self.regexp_input_RBC = qtc.QRegExp('[0-9]?(\.\d\d?)?')  # 0-9.99
        self.regexp_input_HGB = qtc.QRegExp(  # 0-39.99
            '([0-9]|[1-3]\d?)?(\.\d\d?)?')
        self.regexp_input_HCT = qtc.QRegExp('[1-8]\d?')  # 10-89
        self.regexp_input_MCV = qtc.QRegExp(  # 50-139.99
            '((1[1-3]|[5-9])\d)?(\.\d\d?)?')
        self.regexp_input_MCH = qtc.QRegExp(  # 0-59.99
            '([0-9]|[1-5]\d?)?(\.\d\d?)?')
        self.regexp_input_MCHC = qtc.QRegExp(  # 0-59.99
            '(\d|[1-5]\d?)?(\.\d\d?)?')
        self.regexp_input_RDW = qtc.QRegExp(  # 0-39.99
            '(\d|[1-3]\d?)?(\.\d\d?)?')
        self.regexp_input_MPV = qtc.QRegExp(  # 0-39.99
            '(\d|[1-3]\d?)?(\.\d\d?)?')
        self.regexp_input_PER_NEUT = qtc.QRegExp(  # 0-100
            '(100|(\d?\d?)?)?(\.\d\d?)?')
        self.regexp_input_PER_LYMPH = qtc.QRegExp(  # 0-100
            '100|(\d?\d?)?(\.\d\d?)?')
        self.regexp_input_PER_MONO = qtc.QRegExp(  # 0-100
            '100|(\d?\d?)?(\.\d\d?)?')
        self.regexp_input_PER_EOS = qtc.QRegExp(  # 0-100
            '100|(\d?\d?)?(\.\d\d?)?')
        self.regexp_input_PER_BASO = qtc.QRegExp(  # 0-100
            '100|(\d?\d?)?(\.\d\d?)?')
        self.regexp_input_PER_IG = qtc.QRegExp(  # 0-100
            '100|(\d?\d?)?(\.\d\d?)?')
        self.regexp_input_ABS_NEUT = qtc.QRegExp(  # 0-1999.99
            '^(0|1\d?\d?\d?|[1-9]\d?\d?)?(\.\d\d?)?$')
        self.regexp_input_ABS_LYMPH = qtc.QRegExp(  # 0-1999.99
            '^(0|1\d?\d?\d?|[1-9]\d?\d?)?(\.\d\d?)?$')
        self.regexp_input_ABS_MONO = qtc.QRegExp(  # 0-1999.99
            '^(0|1\d?\d?\d?|[1-9]\d?\d?)?(\.\d\d?)?$')
        self.regexp_input_ABS_EOS = qtc.QRegExp(  # 0-1999.99
            '^(0|1\d?\d?\d?|[1-9]\d?\d?)?(\.\d\d?)?$')
        self.regexp_input_ABS_BASO = qtc.QRegExp(  # 0-1999.99
            '^(0|1\d?\d?\d?|[1-9]\d?\d?)?(\.\d\d?)?$')
        self.regexp_input_ABS_IG = qtc.QRegExp(  # 0-1999.99
            '^(0|1\d?\d?\d?|[1-9]\d?\d?)?(\.\d\d?)?$')
        # Hematology Test & Unit Dict.

        # Heme Values Table Configuration.

        # Loop to make Hematology Test Labels and Inputs.
        for test, unit in self.list_hematology_tests.items():
            # Set Row Number.
            row_number = self.table_heme_values.rowCount()
            # Insert New Row.
            self.table_heme_values.insertRow(row_number)
            # Set Item.
            the_test_widget = qtw.QTableWidgetItem(test)
            the_test_widget.setFlags(qtc.Qt.ItemIsEnabled)  # Disable Editing.
            self.table_heme_values.setItem(  # Set Item.
                row_number, 0, the_test_widget)

            the_result_widget = qtw.QLineEdit()
            the_result_widget.setFrame(False)
            the_result_widget.setText('')
            self.table_heme_values.setCellWidget(
                row_number, 1, the_result_widget)

            the_unit_widget = qtw.QTableWidgetItem(unit)
            the_unit_widget.setFlags(qtc.Qt.ItemIsEnabled)
            self.table_heme_values.setItem(
                row_number, 2, the_unit_widget)
            validator = qtg.QRegExpValidator(self.regexp_input_num)

            # Validators.
            if 'PLT' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_PLT)
                the_result_widget.setValidator(validator)
            elif 'WBC' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_WBC)
                the_result_widget.setValidator(validator)
            elif 'RBC' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_RBC)
                the_result_widget.setValidator(validator)
            elif 'HGB' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_HGB)
                the_result_widget.setValidator(validator)
            elif 'HCT' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_HCT)
                the_result_widget.setValidator(validator)
            elif 'MCV' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_MCV)
                the_result_widget.setValidator(validator)
            elif 'MCH' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_MCH)
                the_result_widget.setValidator(validator)
            elif 'MCHC' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_MCHC)
                the_result_widget.setValidator(validator)
            elif 'RDW' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_RDW)
                the_result_widget.setValidator(validator)
            elif 'MPV' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_MPV)
                the_result_widget.setValidator(validator)
            elif 'PER_NEUT' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_PER_NEUT)
                the_result_widget.setValidator(validator)
            elif 'PER_LYMPH' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_PER_LYMPH)
                the_result_widget.setValidator(validator)
            elif 'PER_MONO' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_PER_MONO)
                the_result_widget.setValidator(validator)
            elif 'PER_EOS' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_PER_EOS)
                the_result_widget.setValidator(validator)
            elif 'PER_BASO' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_PER_BASO)
                the_result_widget.setValidator(validator)
            elif 'PER_IG' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_PER_IG)
                the_result_widget.setValidator(validator)
            elif 'ABS_NEUT' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_ABS_NEUT)
                the_result_widget.setValidator(validator)
            elif 'ABS_LYMPH' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_ABS_LYMPH)
                the_result_widget.setValidator(validator)
            elif 'ABS_MONO' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_ABS_MONO)
                the_result_widget.setValidator(validator)
            elif 'ABS_EOS' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_ABS_EOS)
                the_result_widget.setValidator(validator)
            elif 'ABS_BASO' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_ABS_BASO)
                the_result_widget.setValidator(validator)
            elif 'ABS_IG' in test:
                validator = qtg.QRegExpValidator(self.regexp_input_ABS_IG)
                the_result_widget.setValidator(validator)
            # Incrementing Y Position.
            start_y = start_y + 30
        # Resizing Columns.
        self.table_heme_values.resizeColumnsToContents()
        # Resizing Rows.
        self.table_heme_values.resizeRowsToContents()
        # Next Tab.
        self.coagulation_tab()

    def coagulation_tab(self):
        self.urinalysis_tab()

    def urinalysis_tab(self):
        self.bloodbank_tab()

    def bloodbank_tab(self):
        self.serology_tab()

    def serology_tab(self):
        self.microbiology_tab()

    def microbiology_tab(self):
        self.set_dict_all_widgets()

    def set_dict_all_widgets(self):
        self.dict_all_widgets = {
            **self.dict_diag_widgets, **self.dict_diag_add_pt_widgets, **self.dict_heme_table_test_row_widgets}
        self.exit_button()

    def exit_button(self):  # Exit Button.

        self.pushbutton_exit = qtw.QPushButton()

        self.pushbutton_exit.setText('- E X I T -')

        self.pushbutton_exit.adjustSize()

        self.pushbutton_exit.move((self.width()-self.pushbutton_exit.width()-50),
                                  (self.statusbar.y()-self.pushbutton_exit.height()-35))

        self.pushbutton_exit.setParent(self.tab_diagnosis)

        self.pushbutton_exit.setStyleSheet(
            'background-color: #D81A16; font: 13px; font: bold; spacing: 10; border: 2px solid #F5F5F5;')

        self.pushbutton_exit.clicked.connect(self.exit_application)

        self.set_style_sheet()

    def set_style_sheet(self):
        self.setStyleSheet("""
            QListWidget{
                border: 3px solid black;
                border-radius:5px;
                background-color:#f1f8f9;}
            QPushButton{
                min-width:"""+str(self.button_width)+""";
                max-width:"""+str(self.button_width)+""";
                min-height:"""+str(self.button_height)+""";
                max-height:"""+str(self.button_height)+""";
                border: 3px solid #CAC6D7;
                border-radius:3px;
                background-color: #EAE6FA;}
            QTableWidget QFrame{border: 2px outset black; background-color:#55828b;}
            QTableWidget QHeaderView::section{background-color:#55828b;}
            QTableWidget QTableCornerButton::section{background-color:#55828b; border: 2px inset black;}
            QTableWidget {
                alternate-background-color: #EAE6FA; gridline-color: black;
            }""")
        self.timer_statusbar_update()

    def timer_statusbar_update(self):  # Status Bar Update Timer.

        self.timer_status_bar_update = qtc.QTimer()
        self.timer_status_bar_update.start(1000)
        self.timer_status_bar_update.timeout.connect(self.update_status_bar)

        self.show()
        self.print_widget_list()
        self.load_patient_database()

    def print_widget_list(self):

        for i in self.dict_all_widgets.keys():
            print(i)


##        ##        ##        ##        ##        ##        ##        ##        ##        ##        ##        ##        ##        ##        ##        ##        ##        ##        ##
####    ######    ######    ######    ######    ######    ######    ######    ######    ######    ######    ######    ######    ######    ######    ######    ######    ######    ######
# | START OF SELF FUNCTIONS |##########| START OF SELF FUNCTIONS |##########| START OF SELF FUNCTIONS |##########| START OF SELF FUNCTIONS |##########| START OF SELF FUNCTIONS \
 #########  ########  ########  ########  ########  ########  ########  ########  ########  ########  ########  ########  ########  ########  ########  ########  ########  ########  #####
   #####      ####      ####      ####      ####      ####      ####      ####      ####      ####      ####      ####      ####      ####      ####      ####      ####      ####      #####

    def load_patient_database(self):  # Loading the Patient Database.

        conn = sql.connect('patients.db')  # Connecting to the Database.
        c = conn.cursor()  # Creating a Cursor.

        load_patients = c.execute(  # Loading the Patients from the Database.
            'SELECT ID,First_Name,Last_Name FROM Patient_List')

        # Fetching the Patients from the Database.
        database_patients = load_patients.fetchall()

        conn.commit()  # Committing the Changes to the Database.
        conn.close()  # Closing the Connection to the Database.

        for row, patient in enumerate(database_patients):
            self.table_patients.setRowCount(row)  # Setting the Row Count.
            var_id = patient[0]  # Setting the ID.
            var_first_name = patient[1]  # Setting the First Name.
            var_last_name = patient[2]  # Setting the Last Name.

            self.table_patients.insertRow(row)  # Inserting a Row.
            self.table_patients.setItem(
                row, 0, qtw.QTableWidgetItem(str(var_id)))
            # Disabling Editing of the ID.
            qtw.QTableWidgetItem(str(var_id)).setFlags(qtc.Qt.ItemIsEnabled)
            self.table_patients.setItem(
                row, 1, qtw.QTableWidgetItem(str(var_first_name)))
            # Disabling Editing of the First Name.
            qtw.QTableWidgetItem(str(var_first_name)).setFlags(
                qtc.Qt.ItemIsEnabled)
            self.table_patients.setItem(
                row, 2, qtw.QTableWidgetItem(str(var_last_name)))
            # Disabling Editing of the Last Name.
            qtw.QTableWidgetItem(str(var_last_name)).setFlags(
                qtc.Qt.ItemIsEnabled)
        print('database_patients', database_patients)

    def update_status_bar(self):  # Updating the Status Bar.
        datetime_now = dt.datetime.now()  # Getting the Current Date and Time.
        # Formatting the Current Date and Time.
        statusbar_datetime = datetime_now.strftime('%H:%M:%S')
        # Updating the Status Bar with the Current Date and Time.
        self.labelstatusbar_datetime.setText(str(statusbar_datetime))

    def update_id_track(self):  # Updating the ID Track.
        # Setting the Selected Patient to a Placeholder.
        self.selected_patient = ['placeholder']
        self.list_ids = []

        conn = sql.connect('patients.db')  # Connecting to the Database.
        c = conn.cursor()  # Creating a Cursor.

        c.execute(
            """SELECT ID FROM Patient_List""")  # Selecting the Patient IDs from the Database.

        pt_ids = c.fetchall()  # Fetching all patient IDs from Database.

        conn.commit()  # Committing the Changes to the Database.
        conn.close()  # Closing the Connection to the Database.

        for id in range(len(pt_ids)):
            # Adding the Patient IDs to the List of IDs.
            self.list_ids.append((pt_ids[id])[0])
        if pt_ids == []:  # If there are no Patient IDs in the Database.
            self.id_track = 1  # Set the ID Track to 1.
        else:  # If there are Patient IDs in the Database.
            # Add a 0 to the List of IDs to prevent an Index Error.
            self.list_ids.append(0)
            # Looping through the List of IDs.
            for i in range(len(self.list_ids)):
                if (i+1) in self.list_ids:  # If the ID is in the List of IDs.
                    pass  # Do Nothing.
                else:  # If the ID is not in the List of IDs.
                    self.id_track = i + 1  # Set the ID Track to the ID.
                    break  # Break the Loop.

        # Set the ID Line Edit to the ID Track.
        self.dict_diag_add_pt_widgets['save_ID_lineedit'].setText(
            str(self.id_track))
        self.load_patient_database()  # Load the Patient Database.

    def search_symptom(self):
        if self.lineedit_symptom_search.text() == '':
            messagebox_enter_search_term = qtw.QMessageBox()
            messagebox_enter_search_term.setIcon(qtw.QMessageBox.Information)
            messagebox_enter_search_term.setText(
                'Please enter a search term')
            messagebox_enter_search_term.setWindowTitle('Search Term Error')
            messagebox_enter_search_term.exec_()
            print('Enter a Search Term')
        else:
            try:
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

                self.r_json = r.json()

                destination_entities = self.r_json['destinationEntities']

                for i in range(len(destination_entities)):
                    print(destination_entities[i]['title'])

                # for i in range(len(destination_entities)):
                #     print(destination_entities[i])
                #     print('-----------------------')
                #     print('-----------------------')

                # for key, value in destination_entities.items():
                #     print('key = ' + str(key))
                #     print('value = ' + str(value))

                # for key,value in self.r_json.items():
                #     print('key = ' + str(key))
                #     print('value = ' + str(value))

                def result_filter_1(obj):

                    filtered_result_1 = js.dumps(
                        obj, sort_keys=True, indent=8, separators=(',', ':')).split(',')
                    for i in filtered_result_1:

                        list_filtered_results_1.append(i)

                result_filter_1(r.json())
                list_titles = []
                list_codes = []

                for i in range(len(list_filtered_results_1)):
                    if 'title' in list_filtered_results_1[i]:
                        if 'Is' in list_filtered_results_1[i]:
                            pass
                        else:
                            list_filtered_results_1[i] = str(
                                list_filtered_results_1[i]).replace("<em class='found'>", '')
                            list_filtered_results_1[i] = str(
                                list_filtered_results_1[i]).replace("</em>", '')
                            list_filtered_results_1[i] = str(
                                list_filtered_results_1[i]).replace("  ", '')
                            list_filtered_results_1[i] = str(
                                list_filtered_results_1[i]).replace('"', '')
                            list_filtered_results_1[i] = str(
                                list_filtered_results_1[i]).replace('title:', '')
                            list_filtered_results_1[i] = str(
                                list_filtered_results_1[i]).replace('\n', '')
                            list_titles.append(list_filtered_results_1[i])
                    if 'Code' in list_filtered_results_1[i]:
                        list_filtered_results_1[i] = str(
                            list_filtered_results_1[i]).replace("  ", '')
                        list_filtered_results_1[i] = str(
                            list_filtered_results_1[i]).replace('"', '')
                        list_filtered_results_1[i] = str(
                            list_filtered_results_1[i]).replace('theCode:', '')
                        list_filtered_results_1[i] = str(
                            list_filtered_results_1[i]).replace('\n', '')
                        list_codes.append(list_filtered_results_1[i])
                # Adding Symptom Code and Symptom Title to Search Results Dictionary.
                for result in range(len(list_codes)):
                    dict_results[list_codes[result]] = list_titles[result]

                for code, title in dict_results.items():
                    self.list_symptom_search.addItem(
                        str(code)+' | '+str(title))
                    self.list_symptom_search.adjustSize()
                # Only show add symptom button if a patient is selected and the ID is displayed.
                if self.dict_all_widgets[selected_ID_lineedit] != '':
                    self.pushbutton_add_symptom.show()
                    self.pushbutton_remove_symptom.show()
                else:
                    pass

            except:
                if len(self.list_symptom_search) == 0:
                    self.list_symptom_search.clear()
                    self.list_symptom_search.addItem('No Results Found')
                    self.list_symptom_search.adjustSize()
                    self.pushbutton_add_symptom.hide()
                    self.pushbutton_remove_symptom.hide()
                else:
                    pass

    # Add Selected Symptom to Patient Symptoms List

    def add_selected_symptom(self):
        self.list_patient_symptoms.addItem(
            self.list_symptom_search.currentItem().text())  # Add Selected Symptom to Patient Symptoms List
        self.save_patient_symptoms()  # Save Patient Symptoms to Database

    # Remove Selected Symptom from Patient Symptoms List
    def remove_selected_symptom(self):
        try:  # Try to Remove Selected Symptom from Patient Symptoms List
            sel_sym_code, sel_sym_name = (
                self.list_patient_symptoms.currentItem().text()).split(' | ')  # Split Symptom Code and Symptom Name

            conn = sql.connect('patients.db')  # Connect to Database
            c = conn.cursor()  # Create Cursor
            c.execute(
                "DELETE FROM [Patient_Symptoms] WHERE SYM_CODE = (?)", (str(sel_sym_code),))  # Delete Selected Symptom from Database
            conn.commit()  # Commit Changes
            conn.close()  # Close Connection

            self.load_pt_symptoms()  # Load Patient Symptoms from Database
        except:  # If No Symptom is Selected
            print('Select a Symptom')  # Print Error Message

    def save_patient_info(self):  # Save Patient Information to Database
        conn = sql.connect('patients.db')  # Connect to Database
        c = conn.cursor()  # Create Cursor

        var_save_patient_info = Class_Patient_Information(  # Create Class_Patient_Information Object
            ID=self.dict_diag_add_pt_widgets['save_ID_lineedit'].text(),
            First_Name=self.dict_diag_add_pt_widgets['save_First_Name_lineedit'].text(
            ),
            Middle_Name=self.dict_diag_add_pt_widgets['save_Middle_Name_lineedit'].text(
            ),
            Last_Name=self.dict_diag_add_pt_widgets['save_Last_Name_lineedit'].text(
            ),
            Gender=self.dict_diag_add_pt_widgets['save_Gender_combobox'].currentText(
            ),
            DOB=self.dict_diag_add_pt_widgets['save_Date_of_Birth_lineedit'].text())  # Create Class_Patient_Information Object

        c.execute(  # Insert Patient Information into Database
            """INSERT OR REPLACE INTO Patient_List (
                'ID','First_Name', 'Middle_Name', 'Last_Name','Gender', 'Age', 'DOB')
            VALUES (
                :ID, :First_Name, :Middle_Name, :Last_Name, :Gender, :Age, :DOB)
            ON CONFLICT DO UPDATE SET (
                'ID','First_Name', 'Middle_Name', 'Last_Name','Gender', 'Age', 'DOB') = (:ID, :First_Name, :Middle_Name, :Last_Name, :Gender, :Age, :DOB)""",
            {
                'ID': var_save_patient_info.ID,
                'First_Name': var_save_patient_info.First_Name,
                'Middle_Name': var_save_patient_info.Middle_Name,
                'Last_Name': var_save_patient_info.Last_Name,
                'Gender': var_save_patient_info.Gender,
                'Age': var_save_patient_info.Age,
                'DOB': var_save_patient_info.DOB})

        conn.commit()  # Commit Changes
        conn.close()  # Close Connection

        # INITIAL BLANK VALUE SETTING.
        var_save_patient_heme = Class_Patient_Heme_Results(  # Create Class_Patient_Heme_Results Object
            ID=self.dict_all_widgets['save_ID_lineedit'].text(),
            PLT=self.table_heme_values.cellWidget(0, 1).text(),
            WBC=self.table_heme_values.cellWidget(1, 1).text(),
            RBC=self.table_heme_values.cellWidget(2, 1).text(),
            HGB=self.table_heme_values.cellWidget(3, 1).text(),
            HCT=self.table_heme_values.cellWidget(4, 1).text(),
            MCV=self.table_heme_values.cellWidget(5, 1).text(),
            MCH=self.table_heme_values.cellWidget(6, 1).text(),
            MCHC=self.table_heme_values.cellWidget(7, 1).text(),
            RDW=self.table_heme_values.cellWidget(8, 1).text(),
            MPV=self.table_heme_values.cellWidget(9, 1).text(),
            PER_NEUT=self.table_heme_values.cellWidget(10, 1).text(),
            PER_LYMPH=self.table_heme_values.cellWidget(11, 1).text(),
            PER_MONO=self.table_heme_values.cellWidget(12, 1).text(),
            PER_EOS=self.table_heme_values.cellWidget(13, 1).text(),
            PER_BASO=self.table_heme_values.cellWidget(14, 1).text(),
            PER_IG=self.table_heme_values.cellWidget(15, 1).text(),
            ABS_NEUT=self.table_heme_values.cellWidget(16, 1).text(),
            ABS_LYMPH=self.table_heme_values.cellWidget(17, 1).text(),
            ABS_MONO=self.table_heme_values.cellWidget(18, 1).text(),
            ABS_EOS=self.table_heme_values.cellWidget(19, 1).text(),
            ABS_BASO=self.table_heme_values.cellWidget(20, 1).text(),
            ABS_IG=self.table_heme_values.cellWidget(21, 1).text())

        conn = sql.connect('patients.db')  # Connect to Database
        c = conn.cursor()  # Create Cursor

        c.execute(  # Insert Blank Initializing Patient Hematology Results into Database
            """INSERT INTO Hematology_Values (
                'ID','PLT', 'WBC', 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'RDW', 'MPV',
                'PER_NEUT', 'PER_LYMPH', 'PER_MONO', 'PER_EOS', 'PER_BASO', 'PER_IG',
                'ABS_NEUT', 'ABS_LYMPH', 'ABS_MONO', 'ABS_EOS', 'ABS_BASO', 'ABS_IG')
            VALUES (
                :ID,:PLT, :WBC, :RBC, :HGB, :HCT, :MCV, :MCH, :MCHC, :RDW, :MPV,
                :PER_NEUT, :PER_LYMPH, :PER_MONO, :PER_EOS, :PER_BASO, :PER_IG,
                :ABS_NEUT, :ABS_LYMPH, :ABS_MONO, :ABS_EOS, :ABS_BASO, :ABS_IG)""",
            {
                'ID': var_save_patient_heme.ID,
                'PLT': var_save_patient_heme.PLT,
                'WBC': var_save_patient_heme.WBC,
                'RBC': var_save_patient_heme.RBC,
                'HGB': var_save_patient_heme.HGB,
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
                'ABS_IG': var_save_patient_heme.ABS_IG})

        conn.commit()  # Commit Changes
        conn.close()  # Close Connection

        self.clear_patient_info()  # Clear Patient Info
        self.update_id_track()  # Update ID_Track

    def save_patient_symptoms(self):  # Save Patient Symptoms to Database
        sel_sym_code, sel_sym_name = (  # Get Selected Symptom Code and Name
            self.list_symptom_search.currentItem().text()).split(' | ')  # Split Code and Name

        try:  # Try to Save Patient Symptoms
            var_save_patient_sym = Class_Patient_Symptoms(  # Create Class_Patient_Symptoms Object
                ID=self.dict_all_widgets['selected_ID_lineedit'].text(),
                sym_code=sel_sym_code,
                sym_name=sel_sym_name)

            conn = sql.connect('patients.db')
            c = conn.cursor()

            c.execute(
                """INSERT INTO [Patient_Symptoms] (
                        'ID', 'SYM_CODE', 'SYM_NAME')
                   VALUES (
                   :ID, :SYM_CODE, :SYM_NAME)""",
                {
                    'ID': var_save_patient_sym.ID,
                    'SYM_CODE': var_save_patient_sym.sym_code,
                    'SYM_NAME': var_save_patient_sym.sym_name})

            conn.commit()
            conn.close()
        except:  # If Patient Symptoms Already Saved, Print Error Message
            print('Symptom Already Added.')

    def save_hematology_info(self):  # Save Hematology Info to Database
        # check for '.' in input.
        # for each row in table.
        for i in range(self.table_heme_values.rowCount()):
            # if acceptable input.
            if self.table_heme_values.cellWidget(i, 1).hasAcceptableInput():
                # if input starts with '.'.
                if (self.table_heme_values.cellWidget(i, 1).text()).startswith('.'):
                    self.table_heme_values.cellWidget(i, 1).setText(  # replace '.' with '0.'.
                        '0' + self.table_heme_values.cellWidget(i, 1).text())  # add '0' to beginning of input.
            else:  # if not acceptable input, replace '.' with blank.
                self.table_heme_values.cellWidget(i, 1).setText(  # replace '.' with blank.
                    self.table_heme_values.cellWidget(i, 1).text().replace('.', ''))  # replace '.' with blank.

        var_save_patient_heme = Class_Patient_Heme_Results(  # Create Class_Patient_Heme_Results Object
            ID=self.dict_diag_widgets['selected_ID_lineedit'].text(),
            PLT=self.table_heme_values.cellWidget(0, 1).text(),
            WBC=self.table_heme_values.cellWidget(1, 1).text(),
            RBC=self.table_heme_values.cellWidget(2, 1).text(),
            HGB=self.table_heme_values.cellWidget(3, 1).text(),
            HCT=self.table_heme_values.cellWidget(4, 1).text(),
            MCV=self.table_heme_values.cellWidget(5, 1).text(),
            MCH=self.table_heme_values.cellWidget(6, 1).text(),
            MCHC=self.table_heme_values.cellWidget(7, 1).text(),
            RDW=self.table_heme_values.cellWidget(8, 1).text(),
            MPV=self.table_heme_values.cellWidget(9, 1).text(),
            PER_NEUT=self.table_heme_values.cellWidget(10, 1).text(),
            PER_LYMPH=self.table_heme_values.cellWidget(11, 1).text(),
            PER_MONO=self.table_heme_values.cellWidget(12, 1).text(),
            PER_EOS=self.table_heme_values.cellWidget(13, 1).text(),
            PER_BASO=self.table_heme_values.cellWidget(14, 1).text(),
            PER_IG=self.table_heme_values.cellWidget(15, 1).text(),
            ABS_NEUT=self.table_heme_values.cellWidget(16, 1).text(),
            ABS_LYMPH=self.table_heme_values.cellWidget(17, 1).text(),
            ABS_MONO=self.table_heme_values.cellWidget(18, 1).text(),
            ABS_EOS=self.table_heme_values.cellWidget(19, 1).text(),
            ABS_BASO=self.table_heme_values.cellWidget(20, 1).text(),
            ABS_IG=self.table_heme_values.cellWidget(21, 1).text())

        conn = sql.connect('patients.db')  # Connect to Database
        c = conn.cursor()  # Create Cursor

        c.execute(  # Insert or Replace Hematology Values
            """INSERT OR REPLACE INTO Hematology_Values (
                'ID','PLT', 'WBC', 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'RDW', 'MPV',
                'PER_NEUT', 'PER_LYMPH', 'PER_MONO', 'PER_EOS', 'PER_BASO', 'PER_IG',
                'ABS_NEUT', 'ABS_LYMPH', 'ABS_MONO', 'ABS_EOS', 'ABS_BASO', 'ABS_IG')
            VALUES (
                :ID,:PLT, :WBC, :RBC, :HGB, :HCT, :MCV, :MCH, :MCHC, :RDW, :MPV,
                :PER_NEUT, :PER_LYMPH, :PER_MONO, :PER_EOS, :PER_BASO, :PER_IG,
                :ABS_NEUT, :ABS_LYMPH, :ABS_MONO, :ABS_EOS, :ABS_BASO, :ABS_IG)
            ON CONFLICT DO UPDATE SET (
                'ID','PLT', 'WBC', 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'RDW', 'MPV',
                'PER_NEUT', 'PER_LYMPH', 'PER_MONO', 'PER_EOS', 'PER_BASO', 'PER_IG',
                'ABS_NEUT', 'ABS_LYMPH', 'ABS_MONO', 'ABS_EOS', 'ABS_BASO', 'ABS_IG') = (
                :ID,:PLT, :WBC, :RBC, :HGB, :HCT, :MCV, :MCH, :MCHC, :RDW, :MPV,
                :PER_NEUT, :PER_LYMPH, :PER_MONO, :PER_EOS, :PER_BASO, :PER_IG,
                :ABS_NEUT, :ABS_LYMPH, :ABS_MONO, :ABS_EOS, :ABS_BASO, :ABS_IG)""",
            {
                'ID': var_save_patient_heme.ID,
                'PLT': var_save_patient_heme.PLT,
                'WBC': var_save_patient_heme.WBC,
                'RBC': var_save_patient_heme.RBC,
                'HGB': var_save_patient_heme.HGB,
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
                'ABS_IG': var_save_patient_heme.ABS_IG})

        conn.commit()  # Commit Changes
        conn.close()  # Close Connection

    def clear_hematology_info(self):
        # for each row in table.
        for i in range(self.table_heme_values.rowCount()):
            # clear the text in the cell.
            self.table_heme_values.cellWidget(i, 1).clear()

    def edit_patient_info(self):

        current_row = self.list_patients.currentRow()+1

        if current_row == 0:
            print('Select A Patient')
            self.update_id_track()
        else:
            self.window_add_patient.set
            self.window_add_patient.show()

            current_id = (
                self.list_widget_patient_list[current_row-1].text()[0])
            self.selected_patient = self.selected_patient[0]

            conn = sql.connect('patients.db')
            c = conn.cursor()

            c.execute("SELECT * FROM Patient_List WHERE ID = (?)",
                      (int(current_id),))

            column, selected_pt_info = c.description, c.fetchall()

            conn.commit()
            conn.close()

            list_columns = []

            for i in range(len(column[0])):
                list_columns.append(column[i][0])

            list_patient_info = []

            for i in range(len(selected_pt_info[0])):
                list_patient_info.append(selected_pt_info[0][i])

            # for c in range(len(list_patient_info)):
            #     # Selecting corresponding value from Database.
            #     if 'ID' in list_columns[c]:
            #         # looping through the dictionary of input widgets.
            #         for num, wid in self.dict_widget_names.items():
            #             # finding the corresponding widget in the dictionary.
            #             if 'ID' in wid and 'line' in wid:
            #                 # loading the selected database value to the corresponding input widget.
            #                 pass
            #                 # Selecting corresponding value from Database.
            #     elif 'First' in list_columns[c]:
            #         # looping through the dictionary of input widgets.
            #         for num, wid in self.dict_widget_names.items():
            #             # finding the corresponding widget in the dictionary.
            #             if 'First' in wid and 'line' in wid:
            #                 # loading the selected database value to the corresponding input widget.
            #                 self.dict_widgets[num].setText(
            #                     str(list_patient_info[c]))
            #     # Selecting corresponding value from Database.
            #     elif 'Middle' in list_columns[c]:
            #         # looping through the dictionary of input widgets.
            #         for num, wid in self.dict_widget_names.items():
            #             # finding the corresponding widget in the dictionary.
            #             if 'Middle' in wid and 'line' in wid:
            #                 # loading the selected database value to the corresponding input widget.
            #                 self.dict_widgets[num].setText(
            #                     str(list_patient_info[c]))
            #     # Selecting corresponding value from Database.
            #     elif 'Last' in list_columns[c]:
            #         # looping through the dictionary of input widgets.
            #         for num, wid in self.dict_widget_names.items():
            #             # finding the corresponding widget in the dictionary.
            #             if 'Last' in wid and 'line' in wid:
            #                 # loading the selected database value to the corresponding input widget.
            #                 self.dict_widgets[num].setText(
            #                     str(list_patient_info[c]))
            #     # Selecting corresponding value from Database.
            #     elif 'Gender' in list_columns[c]:
            #         # looping through the dictionary of input widgets.
            #         for num, wid in self.dict_widget_names.items():
            #             # finding the corresponding widget in the dictionary.
            #             if 'Gender' in wid and 'combo' in wid:
            #                 # loading the selected database value to the corresponding input widget.
            #                 self.dict_widgets[num].setCurrentIndex(
            #                     self.dict_widgets[num].findText(list_patient_info[c]))
            #     # Selecting corresponding value from Database.
            #     elif 'DOB' in list_columns[c]:
            #         # looping through the dictionary of input widgets.
            #         for num, wid in self.dict_widget_names.items():
            #             # finding the corresponding widget in the dictionary.
            #             if 'Date' in wid and 'line' in wid:
            #                 # loading the selected database value to the corresponding input widget.
            #                 self.dict_widgets[num].setText(
            #                     str(list_patient_info[c]))

    def clear_patient_info(self):
        print('> CLEARING PATIENT INFO -----')
        for name, widget in self.dict_all_widgets.items():
            if 'save' in name:
                if 'ID' in name:
                    pass
                elif 'lineedit' in name:
                    widget.clear()
                elif 'combobox' in name:
                    widget.setCurrentIndex(0)
                else:
                    pass
            else:
                pass
        print('----- FINISHED <')

    def remove_patient_info(self):
        print('> REMOVING PATIENT INFO -----')
        current_row = self.table_patients.currentRow()+1

        if current_row == 0:
            print('Select A Patient')
            self.update_id_track()
        else:
            self.clicked_patient_id = self.table_patients.item(
                current_row-1, 0).text()

            conn = sql.connect('patients.db')
            c = conn.cursor()

            c.execute("DELETE FROM Patient_List WHERE ID = (?)",
                      (int(self.clicked_patient_id),))

            c.execute("DELETE FROM Hematology_Values WHERE ID = (?)",
                      (int(self.clicked_patient_id),))

            conn.commit()
            conn.close()

            if str(self.loaded_patient) == str(self.clicked_patient_id):
                for name, widget in self.dict_all_widgets.items():
                    if 'selected' in name and 'lineedit' in name:
                        widget.setText('')
                self.update_id_track()
            else:
                self.update_id_track()

    def load_dblclicked_pt(self):
        self.clicked_patient_id = self.list_patients.currentItem().text()[0]
        self.loaded_patient = self.list_patients.currentItem().text()[0]

        self.load_pt_info()
        self.load_pt_symptoms()
        self.label_patient_symptoms.show()
        self.load_pt_heme()

        self.selected_patient = self.selected_patient[0]

        self.tab_bar.setTabEnabled(1, True)
        self.tab_bar.setTabEnabled(2, True)
        self.tab_bar.setTabEnabled(3, True)
        self.tab_bar.setTabEnabled(4, True)
        self.tab_bar.setTabEnabled(5, True)
        self.tab_bar.setTabEnabled(6, True)
        self.tab_bar.setTabEnabled(7, True)

        self.list_patient_symptoms.show()
        self.pushbutton_remove_symptom.show()

        try:  # if the list of symptoms is visible, then show the add symptom button.
            # if the list of symptoms is visible, then show the add symptom button.
            if self.list_symptom_search.isVisible() == True:
                # if the list of symptoms is visible, then show the add symptom button.
                self.pushbutton_add_symptom.show()

            else:  # if the list of symptoms is not visible, then hide the add symptom button.
                pass
        except:
            print('except1')

    def load_pt_info(self):
        conn = sql.connect('patients.db')  # connecting to the database.
        c = conn.cursor()  # creating a cursor object.

        c.execute("SELECT * FROM Patient_List WHERE (ID = " +
                  str(self.clicked_patient_id)+")")  # selecting the patient from the database.

        # fetching the selected patient from the database.
        self.selected_patient_info = c.fetchall()
        self.selected_patient_info = self.selected_patient_info[0]
        self.columns = c.description
        self.columns = [column[0] for column in self.columns]
        self.dict_selected_patient_info = {
            **dict(zip(self.columns, self.selected_patient_info))}
        conn.commit()
        conn.close()

    def load_pt_symptoms(self):
        self.list_patient_symptoms.clear()

        conn = sql.connect('patients.db')
        c = conn.cursor()

        c.execute("SELECT * FROM Patient_Symptoms WHERE (ID = " +
                  str(self.clicked_patient_id)+")")

        self.selected_patient = c.fetchall()
        self.columns = c.description

        dict_selected_patient_symptoms = {}
        list_sym_codes = []
        list_sym_names = []

        for symptoms in range(len(self.selected_patient)):
            dict_selected_patient_symptoms[self.selected_patient[symptoms]
                                           [1]] = self.selected_patient[symptoms][2]

        for sym_code, sym_name in dict_selected_patient_symptoms.items():
            self.list_patient_symptoms.addItem(sym_code + ' | '+sym_name)

        conn.commit()
        conn.close()

    def load_pt_heme(self):

        self.clear_hematology_info()

        conn = sql.connect('patients.db')  # connect to database
        c = conn.cursor()  # create cursor

        c.execute("SELECT * FROM Hematology_Values WHERE (ID = " +
                  str(self.clicked_patient_id)+")")  # select all values from Hematology_Values table where ID = clicked_patient_id

        # fetch all values from Hematology_Values table where ID = clicked_patient_id
        self.selected_patient = c.fetchall()

        list_selected_patient_heme_values = []
        for info in range(len(self.selected_patient[0])):
            list_selected_patient_heme_values.append(
                self.selected_patient[0][info])

       # self.table_heme_values.cellWidget(0, 1).setText('kitten')
        for value in range(len(list_selected_patient_heme_values)-1):
            self.table_heme_values.cellWidget(value, 1).setText(
                str(list_selected_patient_heme_values[value+1]))
        conn.commit()
        conn.close()

    def check_dob_input(self):

        if self.dict_all_widgets['save_Date_of_Birth_lineedit'].hasAcceptableInput() == False:
            self.pushbutton_save_patient_info.setDisabled(True)
        elif self.dict_all_widgets['save_Date_of_Birth_lineedit'].hasAcceptableInput() == True:
            self.pushbutton_save_patient_info.setEnabled(True)

    def add_patient_info(self):

        self.window_add_patient.close()
        self.clear_patient_info()
        self.update_id_track()
        self.window_add_patient.show()

    def delete_database(self, button):

        if 'Yes' in button.text():  # Checks if the Yes Button was clicked.

            self.messagebox_delete_database_confirmation.show()
            conn = sql.connect('patients.db')
            c = conn.cursor()
            # c.execute("DELETE FROM Patient_List")
            c.execute("DROP TABLE Hematology_Values")
            c.execute("DROP TABLE Patient_Symptoms")
            c.execute("DROP TABLE Patient_List")

            conn.commit()
            conn.close()

            initialize_database()

            print('----- DATABASE CLEARED -----')
            self.table_patients.clear()
            self.table_patients.setRowCount(0)

            self.load_patient_database()
            self.update_id_track()
        else:
            messagebox_decline_database_deletion = qtw.QMessageBox()
            messagebox_decline_database_deletion.setWindowTitle(
                'No Database Deleted')
            messagebox_decline_database_deletion.setText('No Database Deleted')
            messagebox_decline_database_deletion.exec_()

    def exit_application(self):
        # -==BEGINNING---#
        self.window_add_patient.close()
        self.close()


if __name__ == '__main__':

    app = qtw.QApplication([])
    mw = MainWindow()
    app.exec_()


##########     ###      ###     ######
##########     ####     ###     ###  ###
###            #####    ###     ###    ###
###            ######   ###     ###      ###
######         ### ###  ###     ###      ###
######         ###  ### ###     ###      ###
###            ###   ######     ###      ###
###            ###    #####     ###    ###
##########     ###     ####     ###  ###
##########     ###      ###     ######
