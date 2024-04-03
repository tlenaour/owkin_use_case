from pandas import DataFrame


def get_patient_ids_with_quality_issues(dataset: DataFrame, quality_check_type: str) -> list[str]:
    quality_columns = dataset.filter(like=quality_check_type)
    patient_ids_with_cross_quality_columns = quality_columns.any(axis=1)
    return patient_ids_with_cross_quality_columns[patient_ids_with_cross_quality_columns].index.to_list()


def get_variables_with_quality_issues(dataset: DataFrame, quality_check_type: str) -> list[str]:
    quality_columns = dataset.filter(like=quality_check_type)
    true_values_count_per_column = quality_columns.sum(axis=0).to_dict()
    return true_values_count_per_column


def get_patients_defect(dataset: DataFrame, quality_check_type: str) -> dict:
    quality_columns = dataset.filter(like=quality_check_type)
    quality_defects_per_patient = {}
    for patient_id, patient_data in quality_columns.iterrows():
        true_columns = patient_data[patient_data].index.tolist()
        quality_defects_per_patient[patient_id] = true_columns
    return quality_defects_per_patient


def build_json_quality_assessment(dataset: DataFrame, quality_check_types: list[str]) -> dict:
    total_patients = len(dataset)
    json_quality_assessment = {}
    global_patient_ids_with_defects = set()
    for quality_check_type in quality_check_types:
        patient_ids_with_defects = get_patient_ids_with_quality_issues(dataset, quality_check_type)
        global_patient_ids_with_defects.update(patient_ids_with_defects)
        defects_by_variables = get_variables_with_quality_issues(dataset, quality_check_type)
        quality_assessment_by_patient = get_patients_defect(dataset, quality_check_type)
        json_quality_assessment[quality_check_type] = {
            "patient_ids_with_defects": patient_ids_with_defects,
            "defects_by_variables": defects_by_variables,
            "quality_assessment_by_patient": quality_assessment_by_patient
        }
    json_quality_assessment["global_patient_ids_with_defects"] = list(global_patient_ids_with_defects)
    json_quality_assessment["total_patients"] = total_patients
    return json_quality_assessment
