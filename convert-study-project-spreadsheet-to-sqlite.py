
import sqlite3
import openpyxl
import csv
from difflib import SequenceMatcher


INDIGO_PROJECT_NAME_MATCHING_THRESHOLD = 0.5

###################################################################### Load INDIGO projects

indigo_projects = {}
with open('data/projects.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
       indigo_projects[row[0]] = row[1]


###################################################################### Create database


connection = sqlite3.connect('data/research-projects-database.sqlite')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("BEGIN")

cursor.execute("""CREATE TABLE study (
covidence_number	INTEGER,
study_id  TEXT PRIMARY KEY,	
title	 TEXT,
reviewer_name	 TEXT,
authors	 TEXT,
journal_or_source	 TEXT,
date_publication	 TEXT,
date_publication_year	 INTEGER,
doi	 TEXT,
url	 TEXT,
issn	 TEXT,
study_design_description	 TEXT,
study_design	 TEXT,
initial_research_quality_appraisal	 TEXT,
language	 TEXT,
non_qualitative_casp  TEXT,
more_than_one_social_outcomes_contract  TEXT,
source_spreadsheet_row INTEGER
)""")


cursor.execute("""
CREATE TABLE social_outcomes_contract (
study_id TEXT,
name	 TEXT,
country_intervention	 TEXT,
outcomes_funder_name	 TEXT,
outcomes_funder_type	 TEXT,
primary_policy_sector	 TEXT,
secondary_policy_sectors	 TEXT,
sustainable_development_goals	 TEXT,
target_population	 TEXT,
scale_of_intervention	 TEXT,
incentivised_outcome_measure	 TEXT,
magnitude_of_incentives	 TEXT,
contract_start_date	 TEXT,
contract_end_date	 TEXT,
outcome_validation_method	 TEXT,
agent_service_providers	 TEXT,
agent_type_or_classification	 TEXT,
third_party_investor_involvement	 TEXT,
reports_changes_in_service_delivery_intervention_specific	 TEXT,
reports_changes_in_service_delivery_intervention_specific_details TEXT,
reports_changes_in_utilisation	 TEXT,
reports_changes_in_utilisation_details TEXT,
reports_changes_in_person_level_outcomes	 TEXT,
reports_changes_in_person_level_outcomes_details TEXT,
reports_unintended_effects	 TEXT,
reports_unintended_effects_details TEXT,
reports_auxiliary_resource_or_parallel_reforms_occurring_alongside_soc	 TEXT,
reports_auxiliary_resource_or_parallel_reforms_occurring_alongside_soc_details TEXT,
reports_on_acceptability_of_SOC_political_cultural	 TEXT,
reports_on_acceptability_of_SOC_political_cultural_details TEXT,
reports_on_participant_or_provider_satisfaction	 TEXT,
reports_on_participant_or_provider_satisfaction_details TEXT,
reports_implications_for_management_information_systems TEXT,
reports_implications_for_management_information_systems_details TEXT,
reports_costs_and_resource_implications TEXT,
reports_costs_and_resource_implications_details TEXT,
reports_equity_considerations	 TEXT,
reports_equity_considerations_details TEXT,
reports_development_and_design_process 	 TEXT,
reports_development_and_design_process_details TEXT,
reports_independent_investor_involvement	 TEXT,
reports_independent_investor_involvement_details TEXT,
reports_scalability	 TEXT,
reports_scalability_details TEXT,
reports_relationships_between_contracted_parties	 TEXT,
reports_relationships_between_contracted_parties_details TEXT,
reports_ecosystem_or_system_strengthening_effects	 TEXT,
reports_ecosystem_or_system_strengthening_effects_details TEXT,
reports_changes_in_provider_performance_or_culture	 TEXT,
reports_changes_in_provider_performance_or_culture_details TEXT,
reports_long_term_sustainment_and_legacy_effects 	 TEXT,
reports_long_term_sustainment_and_legacy_effects_details TEXT,
review_beneficial TEXT,
source_spreadsheet_row INTEGER,
possible_indigo_project_id TEXT,
possible_indigo_project_title TEXT,
possible_indigo_project_confidence REAL
)
""")

###################################################################### Open Spreadsheet and insert into database


def stripcellvalue(val):
    return val.strip() if isinstance(val, str) else val


workbook = openpyxl.load_workbook('data/research-projects-spreadsheet.xlsx')
worksheet = workbook['Sheet1']


last_study_id="NA"
for row in range(3, worksheet.max_row + 1):
    study_id = worksheet['B'+str(row)].value
    #print(str(study_id) + "!="+str(last_study_id))
    if study_id and study_id != last_study_id:
        last_study_id = study_id
        cursor.execute(
            """INSERT INTO study (
                covidence_number	,study_id ,title	,reviewer_name	,authors	 ,journal_or_source	,date_publication,date_publication_year,doi	 ,url	,
                issn,study_design_description,study_design	,initial_research_quality_appraisal	,language	,non_qualitative_casp , more_than_one_social_outcomes_contract, source_spreadsheet_row  
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                int(worksheet['A' + str(row)].value),
                worksheet['B' + str(row)].value,
                worksheet['C' + str(row)].value,
                worksheet['D' + str(row)].value,
                worksheet['F' + str(row)].value,
                worksheet['G' + str(row)].value,
                worksheet['H' + str(row)].value if worksheet['H' + str(row)].value != 'n.d.' else None,
                str(worksheet['H' + str(row)].value)[0:4] if worksheet['H' + str(row)].value and worksheet['H' + str(row)].value != 'n.d.' else None,
                worksheet['I' + str(row)].value,
                worksheet['J' + str(row)].value,
                worksheet['K' + str(row)].value,
                worksheet['L' + str(row)].value,
                worksheet['M' + str(row)].value.strip() if worksheet['M' + str(row)].value else None,
                worksheet['N' + str(row)].value,
                worksheet['O' + str(row)].value,
                worksheet['P' + str(row)].value,
                worksheet['Q' + str(row)].value,
                row
            ],
        )

    if worksheet['R' + str(row)].value or worksheet['S' + str(row)].value:
        contract_name = worksheet['R' + str(row)].value,
        if isinstance(contract_name, tuple):
            contract_name = contract_name[0]
        if not contract_name or contract_name == 'N/A':
            contract_name = "ANON STUDY ROW " + str(row)
        # print(str(study_id) + ", "+str(contract_name))

        indigo_projects_for_study = [(k, SequenceMatcher(None, title, contract_name).ratio()) for k, title in indigo_projects.items() ]
        indigo_projects_for_study.sort(key=lambda i: i[1])
        possible_indigo_project_for_study = indigo_projects_for_study.pop()
        insert_data = [
                study_id,
                contract_name,
                worksheet['S' + str(row)].value,
                worksheet['T' + str(row)].value,
                worksheet['U' + str(row)].value,
                worksheet['V' + str(row)].value,
                worksheet['W' + str(row)].value,
                worksheet['X' + str(row)].value,
                worksheet['Y' + str(row)].value,
                worksheet['Z' + str(row)].value,
                worksheet['AA' + str(row)].value,
                worksheet['AB' + str(row)].value,
                worksheet['AC' + str(row)].value,
                worksheet['AD' + str(row)].value,
                worksheet['AE' + str(row)].value,
                worksheet['AF' + str(row)].value,
                worksheet['AG' + str(row)].value,
                worksheet['AH' + str(row)].value,
                stripcellvalue(worksheet['AI' + str(row)].value),
                worksheet['AJ' + str(row)].value,
                worksheet['AK' + str(row)].value,
                worksheet['AL' + str(row)].value,
                stripcellvalue(worksheet['AM' + str(row)].value),
                worksheet['AN' + str(row)].value,
                stripcellvalue(worksheet['AO' + str(row)].value),
                worksheet['AP' + str(row)].value,
                stripcellvalue(worksheet['AQ' + str(row)].value),
                worksheet['AR' + str(row)].value,
                stripcellvalue(worksheet['AS' + str(row)].value),
                worksheet['AT' + str(row)].value,
                worksheet['AU' + str(row)].value,
                worksheet['AV' + str(row)].value,
                stripcellvalue(worksheet['AW' + str(row)].value),
                worksheet['AX' + str(row)].value,
                stripcellvalue(worksheet['AY' + str(row)].value),
                worksheet['AZ' + str(row)].value,
                worksheet['BA' + str(row)].value,
                worksheet['BB' + str(row)].value,
                worksheet['BC' + str(row)].value,
                worksheet['BD' + str(row)].value,
                worksheet['BE' + str(row)].value,
                worksheet['BF' + str(row)].value,
                stripcellvalue(worksheet['BG' + str(row)].value),
                worksheet['BH' + str(row)].value,
                worksheet['BI' + str(row)].value,
                worksheet['BJ' + str(row)].value,
                stripcellvalue(worksheet['BK' + str(row)].value),
                worksheet['BL' + str(row)].value,
                worksheet['BM' + str(row)].value,
                worksheet['BN' + str(row)].value,
                stripcellvalue(worksheet['BO' + str(row)].value),
                worksheet['BP' + str(row)].value,
                worksheet['BQ' + str(row)].value,
                row,
                possible_indigo_project_for_study[0] if possible_indigo_project_for_study[1] > INDIGO_PROJECT_NAME_MATCHING_THRESHOLD else None,
                indigo_projects[possible_indigo_project_for_study[0]] if possible_indigo_project_for_study[1] > INDIGO_PROJECT_NAME_MATCHING_THRESHOLD else None,
                possible_indigo_project_for_study[1] if possible_indigo_project_for_study[1] > INDIGO_PROJECT_NAME_MATCHING_THRESHOLD else None,
            ]
        #print("STUDY===============================================================================================")
        #[print(i) for i in insert_data]
        cursor.execute(
            """INSERT INTO social_outcomes_contract (
                study_id ,name	 ,country_intervention	 ,outcomes_funder_name	 ,outcomes_funder_type	 ,primary_policy_sector	 ,secondary_policy_sectors	 ,
                sustainable_development_goals	 ,target_population	 ,scale_of_intervention	 ,incentivised_outcome_measure	 ,magnitude_of_incentives	 ,contract_start_date	 ,
                contract_end_date	 ,outcome_validation_method	 ,agent_service_providers	 ,agent_type_or_classification	 , third_party_investor_involvement	 ,
                reports_changes_in_service_delivery_intervention_specific	 ,reports_changes_in_service_delivery_intervention_specific_details ,
                reports_changes_in_utilisation	 ,reports_changes_in_utilisation_details ,
                reports_changes_in_person_level_outcomes	 ,reports_changes_in_person_level_outcomes_details ,
                reports_unintended_effects	 ,reports_unintended_effects_details ,
                reports_auxiliary_resource_or_parallel_reforms_occurring_alongside_soc	 ,reports_auxiliary_resource_or_parallel_reforms_occurring_alongside_soc_details ,
                reports_on_acceptability_of_SOC_political_cultural	 ,reports_on_acceptability_of_SOC_political_cultural_details ,
                reports_on_participant_or_provider_satisfaction	 ,reports_on_participant_or_provider_satisfaction_details ,
                reports_implications_for_management_information_systems ,reports_implications_for_management_information_systems_details ,
                reports_costs_and_resource_implications ,reports_costs_and_resource_implications_details ,
                reports_equity_considerations	 ,reports_equity_considerations_details ,
                reports_development_and_design_process 	 ,reports_development_and_design_process_details ,
                reports_independent_investor_involvement	 ,reports_independent_investor_involvement_details ,
                reports_scalability	 ,reports_scalability_details ,
                reports_relationships_between_contracted_parties	 ,reports_relationships_between_contracted_parties_details ,
                reports_ecosystem_or_system_strengthening_effects	 ,reports_ecosystem_or_system_strengthening_effects_details ,
                reports_changes_in_provider_performance_or_culture	 ,reports_changes_in_provider_performance_or_culture_details ,
                reports_long_term_sustainment_and_legacy_effects 	 ,reports_long_term_sustainment_and_legacy_effects_details ,
                review_beneficial , source_spreadsheet_row,
                possible_indigo_project_id, possible_indigo_project_title, possible_indigo_project_confidence
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?
            )""",
            insert_data)

cursor.execute("COMMIT")

