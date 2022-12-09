:::mermaid
flowchart TB
    subgraph self.mainwindow[Main Window]
        direction TB
        __init__[/__init__/]
        self.mainscreen[/"self.mainscreen()"/]
        self.regexp[/"self.regex()"/]
        self.tab_set[/"self.tab_set()"/]
        self.diagnosis_tab[/"self.diagnosis_tab()"/]
        self.window_add_patient[/"self.window_add_patient()"/]
        self.window_add_patient.close[/"self.window_add_patient.close()"/]
        self.window_add_patient.show[/"self.window_add_patient.show()"/]
        self.statusbar[/"self.statusbar()"/]
        self.hematology[/"self.hematology()"/]
        self.exit_button[/"self.exit_button()"/]
        self.exit_application[/"self.exit_application()"/]
        self.timer_statusbar_update[/"self.timer_statusbar_update()"/]
        self.tab_bar.show[/"self.tab_bar.show()"/]
        self.mainwindow.show[/"self.mainwindow.show()"/]
        self.mainwindow.close[/"self.mainwindow.close()"/]
        self.update_id_track[/"self.update_id_track()"/]
        self.search_symptoms[/"self.search_symptoms()"/]
        self.add_selected_symptom[/"self.add_selected_symptom()"/]
        self.add_patient_info[/"self.add_patient_info()"/]
        self.edit_patient_info[/"self.edit_patient_info()"/]
        self.clear_hematology_info[/"self.clear_hematology_info()"/]
        self.clear_patient_info[/"self.clear_patient_info()"/]
        self.remove_selected_symptom[/"self.remove_selected_symptom()"/]
        self.remove_patient_info[/"self.remove_patient_info()"/]
        self.delete_database[/"self.delete_database()"/]
        self.save_patient_info[/"self.save_patient_info()"/]
        self.save_patient_symptoms[/"self.save_patient_symptoms()"/]
        self.save_hematology_info[/"self.save_hematology_info()"/]
        self.load_patient_database[/"self.load_patient_database()"/]
        self.load_dblclicked_pt[/"self.load_dblclicked_pt()"/]
        self.load_pt_info[/"self.load_pt_info()"/]
        self.load_pt_symptoms[/"self.load_pt_symptoms()"/]
        self.load_pt_heme[/"self.load_pt_heme()"/]
        self.label_patient_symptoms.show[/"self.label_patient_symptoms.show()"/]
        self.list_patients_clear[/"self.list_patients_clear()"/]
        self.list_patient_symptoms.show[/"self.list_patient_symptoms.show()"/]
        self.list_patient_symptoms.clear[/"self.list_patient_symptoms.clear()"/]
        self.pushbutton_remove_symptom.show[/"self.pushbutton_remove_symptom.show()"/]
        self.check_heme_input[/"self.check_heme_input()"/]
        self.check_dob_input[/"self.check_dob_input()"/]
        %%
        %%
        __init__ --> self.mainscreen --> self.regexp --> self.tab_set --> self.diagnosis_tab --> self.tab_bar.show & self.window_add_patient
        %%
        self.window_add_patient --> self.statusbar --> self.hematology --> self.exit_button --> self.timer_statusbar_update --> self.mainwindow.show & self.load_patient_database
        end
        %%
        self.load_patient_database --> self.list_patients_clear
        self.update_id_track --> self.load_patient_database
        self.add_selected_symptom --> self.save_patient_symptoms
        self.save_patient_info --> self.clear_patient_info & self.update_id_track
        %%
        self.load_dblclicked_pt --> self.load_pt_info & self.load_pt_symptoms & self.load_pt_heme & self.label_patient_symptoms.show & self.list_patient_symptoms.show & self.pushbutton_remove_symptom.show
        %%
        self.load_pt_symptoms --> self.list_patient_symptoms.clear
        %%
        self.add_patient_info --> self.window_add_patient.close & self.clear_patient_info & self.update_id_track & self.window_add_patient.show
        %%
        self.exit_application --> self.window_add_patient.close & self.mainwindow.close
    
:::


:::mermaid 
subgraph self.tab_bar[Tab Bar]
        direction TB
        self.tab_diagnosis
        self.chemistry_tab
        self.hematology_tab
        self.coagulation_tab
        self.urinalysis_tab
        self.bloodbank_tab
        self.serology_tab
        self.microbiology_tab
        self.tab_set --> self.tab_diagnosis & self.chemistry_tab & self.hematology_tab & self.coagulation_tab & self.urinalysis_tab & self.bloodbank_tab & self.serology_tab & self.microbiology_tab
        end
:::