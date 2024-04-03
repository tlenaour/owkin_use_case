import pandas
from data_curation.quality.variables_checks import check_duplicated_in_column, check_empty_columns
from data_curation.quality.variables_checks import check_date_format, check_date_is_later_to
from data_curation.quality.variables_checks import check_value_is_not_in_enum, check_value_is_not_in_interval
from data_curation.quality.variables_checks import cast_column_to_numeric
from data_curation.quality.measure import build_json_quality_assessment
import json
import click


@click.command()
@click.option('--dataset-path',
              required=True,
              type=click.Path(exists=True))
@click.option('--output-directory',
              required=True,
              type=click.Path(exists=True))
def main(dataset_path: str, output_directory: str):
    analyzed_variables = ['Patient ID', 'Date of Birth', 'date of diagnosis', 'Smoking history', 'Pack years (PA)']
    na_values = ['unk', 'unknow', 'None', 'Uk']

    dataset = pandas.read_csv(dataset_path,
                              sep=";",
                              keep_default_na=True,
                              na_values=na_values,
                              )

    referential_values = {
        "Smoking history": ["heavy", "former"],
    }

    intervals_values = {
        "Pack years (PA)": {
            "min": 5,
            "max": 85
        }
    }

    default_date_format = "%d/%m/%Y"

    dataset = dataset[analyzed_variables]

    # flag empty values
    dataset = check_empty_columns(dataset=dataset)

    # check Patient Id column
    column_name = "Patient ID"
    dataset = check_duplicated_in_column(dataset,
                                         column_name=column_name)

    # check Date of birth
    column_name = "Date of Birth"
    dataset = check_date_format(dataset=dataset,
                                date_format=default_date_format,
                                column_name=column_name)

    # check date of diagnosis
    column_name = "date of diagnosis"
    anterior_column = "Date of Birth"
    dataset = check_date_format(dataset=dataset,
                                date_format=default_date_format,
                                column_name=column_name)

    dataset = check_date_is_later_to(dataset=dataset,
                                     column1_name=column_name,
                                     column2_name=anterior_column)

    # check Smoking history
    column_name = "Smoking history"
    dataset = check_value_is_not_in_enum(dataset=dataset,
                                         column_name=column_name,
                                         enum=referential_values[column_name])

    # check Pack years (PA)
    column_name = "Pack years (PA)"
    dataset = cast_column_to_numeric(dataset=dataset,
                                     column_name=column_name)

    min_interval = intervals_values[column_name]["min"]
    max_interval = intervals_values[column_name]["max"]
    dataset = check_value_is_not_in_interval(dataset=dataset,
                                             column_name=column_name,
                                             min_interval=min_interval,
                                             max_interval=max_interval)
    dataset = dataset.set_index('Patient ID')

    quality_checks = ['is_empty', 'is_format_not_compliant', 'rules']
    json_quality_assessment = build_json_quality_assessment(dataset=dataset,
                                                            quality_check_types=quality_checks)
    metadata = {
        "analyzed_variables": analyzed_variables,
        "na_values_used": na_values,
        "referential_values_used": referential_values,
        "intervals_values_used": intervals_values,
        "date_format_used": default_date_format
    }
    json_quality_assessment["metadata"] = metadata
    with open(f'{output_directory}/quality_assessment.json', 'w') as f:
        json.dump(json_quality_assessment, f)


if __name__ == "__main__":
    main()