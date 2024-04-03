from pandas import DataFrame
import pandas
import json
import click


def describe_variable(dataset: DataFrame, column_name: str) -> dict:
    column = dataset[column_name]
    description = {
        'count': (count := int(column.count())),
        'missing': int(dataset.shape[0] - count),
        'unique': column.nunique()
    }
    if pandas.api.types.is_numeric_dtype(column):
        description |= {
            'min': column.min(),
            '25%': column.quantile(0.25),
            '50%': column.median(),
            '75%': column.quantile(0.75),
            'max': column.max(),
            'mean': column.mean(),
            'std': column.std(),
            'variance': column.var()
        }

    elif pandas.api.types.is_datetime64_any_dtype(column):
        description['min'] = str(column.min())
        description['max'] = str(column.max())
    else:
        value_counts = column.value_counts().to_dict()
        description['value_counts'] = {key: int(value) for key, value in value_counts.items()}
        description['top_value'] = column.mode().iloc[0]
        description['top_value_count'] = int(column.value_counts().iloc[0])
    return description


@click.command()
@click.option('--dataset-path',
              required=True,
              type=click.Path(exists=True))
@click.option('--output-directory',
              required=True,
              type=click.Path(exists=True))
def main(dataset_path: str, output_directory: str):
    default_dateformat = "%d/%m/%Y"
    dataset = pandas.read_csv(filepath_or_buffer=dataset_path,
                              sep=";",
                              na_values=["unk", "unknow", "None", "Uk"],
                              )
    dataset['Patient ID'] = dataset['Patient ID'].astype("str")
    dataset['Date of Birth'] = pandas.to_datetime(dataset['Date of Birth'],
                                                  format=default_dateformat,
                                                  errors="coerce")
    dataset['date of diagnosis'] = pandas.to_datetime(dataset['date of diagnosis'],
                                                      format=default_dateformat,
                                                      errors="coerce")
    dataset["Pack years (PA)"] = pandas.to_numeric(dataset["Pack years (PA)"],
                                                   errors='coerce')
    dataset["Line Of Treatment"] = pandas.to_numeric(dataset["Line Of Treatment"],
                                                     errors='coerce')
    dataset['Date of PSA level'] = pandas.to_datetime(dataset['Date of PSA level'],
                                                      format=default_dateformat,
                                                      errors="coerce")
    dataset['PSA level'] = pandas.to_numeric(dataset['PSA level'],
                                             errors="coerce")
    dataset['ab Value 1'] = pandas.to_numeric(dataset['ab Value 1'],
                                              errors="coerce")
    dataset['Lab Value 2'] = pandas.to_numeric(dataset['Lab Value 2'],
                                               errors="coerce")
    dataset['Lab Value 3'] = pandas.to_numeric(dataset['Lab Value 3'],
                                               errors="coerce")
    dataset['Date of biobsy'] = pandas.to_datetime(dataset['Date of biobsy'],
                                                   format=default_dateformat,
                                                   errors="coerce")
    dict_dataset_description = {column: describe_variable(dataset, column) for column in dataset.columns}
    with open(f'{output_directory}/dataset_description.json', 'w') as f:
        json.dump(dict_dataset_description, f)


if __name__ == "__main__":
    main()
