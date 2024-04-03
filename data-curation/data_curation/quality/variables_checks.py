import pandas
from pandas import DataFrame


def check_empty_columns(dataset: DataFrame) -> DataFrame:
    for column in dataset.columns:
        dataset[f'{column}-is_empty'] = dataset[column].isna()

    return dataset


def check_duplicated_in_column(dataset: DataFrame, column_name: str) -> DataFrame:
    dataset[f'{column_name}-is_duplicated'] = dataset[column_name].duplicated()

    return dataset


def check_date_format(dataset: DataFrame, column_name: str, date_format: str) -> DataFrame:
    dataset[f'{column_name}_as_iso_8601'] = pandas.to_datetime(dataset[column_name],
                                                               format=date_format,
                                                               errors="coerce")
    dataset[f'{column_name}-is_format_not_compliant'] = dataset[f'{column_name}_as_iso_8601'].isna()

    return dataset


def cast_column_to_numeric(dataset: DataFrame, column_name: str) -> DataFrame:
    dataset[f'{column_name}_as_numeric'] = pandas.to_numeric(dataset[column_name], errors="coerce")
    dataset[f'{column_name}-is_format_not_compliant'] = dataset[f'{column_name}_as_numeric'].isna()

    return dataset


def check_date_is_later_to(dataset: DataFrame, column1_name: str, column2_name: str) -> DataFrame:
    dataset[f'{column1_name}-rules_is_before_than-{column2_name}'] = dataset[f'{column1_name}_as_iso_8601'] < dataset[f'{column2_name}_as_iso_8601']

    return dataset


def check_value_is_not_in_interval(dataset: DataFrame, column_name: str, min_interval, max_interval) -> DataFrame:
    dataset[f'{column_name}-rules_is_not_in_interval'] = ~((dataset[f'{column_name}_as_numeric'] >= min_interval) & (dataset[f'{column_name}_as_numeric'] <= max_interval))

    return dataset


def check_value_is_not_in_enum(dataset: DataFrame, column_name: str, enum: list[str]) -> DataFrame:
    dataset[f'{column_name}-rules_is_in_not_valid_values'] = ~dataset[column_name].str.lower().isin(enum)

    return dataset
