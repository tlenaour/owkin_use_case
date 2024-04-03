from data_curation.quality.variables_checks import cast_column_to_numeric
from data_curation.curation.functions import curate_pack_years
import pandas
import click


@click.command()
@click.option('--dataset-path',
              required=True,
              type=click.Path(exists=True))
@click.option('--smoking-history-referential-path',
              required=True,
              type=click.Path(exists=True))
@click.option('--output-directory',
              required=True,
              type=click.Path(exists=True))
def main(dataset_path: str, smoking_history_referential_path: str, output_directory: str):
    curated_columns = ['Patient ID', 'Smoking history', 'Pack years (PA)']
    output_columns = ['patient_id', 'smoking_history', 'smoking_history_has_been_fixed', 'pack_years', 'pack_years_has_been_fixed']

    dataset = pandas.read_csv(filepath_or_buffer=dataset_path,
                              sep=";",
                              keep_default_na=True,
                              na_values=["unk", "unknow", "None", "Uk"],
                              )

    dataset = dataset[curated_columns]
    dataset = cast_column_to_numeric(dataset=dataset,
                                     column_name='Pack years (PA)')
    dataset['pack_years'] = dataset['Pack years (PA)'].apply(curate_pack_years)
    dataset['pack_years_has_been_fixed'] = dataset['Pack years (PA)_as_numeric'] != dataset['pack_years']

    dataset['normalized_raw_smoking_history'] = dataset['Smoking history'].str.lower()
    smoking_history_referential = pandas.read_csv(filepath_or_buffer=smoking_history_referential_path)
    dataset = dataset.merge(smoking_history_referential,
                            left_on='normalized_raw_smoking_history',
                            right_on='old_value',
                            how='left')
    dataset['smoking_history'] = dataset['new_value']
    dataset['smoking_history_has_been_fixed'] = dataset['smoking_history'] != dataset['Smoking history']
    dataset['patient_id'] = dataset['Patient ID']

    dataset[output_columns].to_csv(f"{output_directory}/dataset_with_better_quality.csv",
                                   index=False)


if __name__ == "__main__":
    main()
