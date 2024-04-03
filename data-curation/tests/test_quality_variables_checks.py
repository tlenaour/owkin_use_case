from data_curation.quality.variables_checks import check_empty_columns
from data_curation.quality.variables_checks import check_duplicated_in_column
from data_curation.quality.variables_checks import check_value_is_not_in_enum
from data_curation.quality.variables_checks import check_date_format
from data_curation.quality.variables_checks import check_date_is_later_to
from data_curation.quality.variables_checks import check_value_is_not_in_interval
from data_curation.quality.variables_checks import cast_column_to_numeric
from pandas import DataFrame, to_datetime
from pandas.testing import assert_frame_equal


def test_check_empty_columns_should_create_a_column_with_boolean_as_true_for_empty_columns():
    # given
    dataframe = DataFrame({'smoking_status': ['heavy', float('NaN'), 'former']})
    # when
    result = check_empty_columns(dataframe)
    # then
    expected = DataFrame({'smoking_status': ['heavy', float('NaN'), 'former'],
                          'smoking_status-is_empty': [False, True, False]})

    assert_frame_equal(result, expected)


def test_check_duplicated_in_column_should_create_a_column_with_boolean_as_true_for_duplicated_columns():
    # given
    dataframe = DataFrame({'patient_id': [1, 2, 3, 4, 3]})
    # when
    result = check_duplicated_in_column(dataframe, 'patient_id')
    # then
    expected = DataFrame({'patient_id': [1, 2, 3, 4, 3],
                          'patient_id-is_duplicated': [False, False, False, False, True]})
    assert_frame_equal(result, expected)


def test_check_value_is_in_enum_should_create_a_column_with_boolean_if_record_is_not_in_given_enum():
    # given
    dataframe = DataFrame({'smoking_status': ['heavy', float('NaN'), 'former', 'Former smoker']})
    enum = ['heavy', 'former']
    # when
    result = check_value_is_not_in_enum(dataframe, 'smoking_status', enum)
    # then
    expected = DataFrame({'smoking_status': ['heavy', float('NaN'), 'former', 'Former smoker'],
                          'smoking_status-rules_is_in_not_valid_values': [False, True, False, True]})
    assert_frame_equal(result, expected)


def test_check_date_format_should_create_a_column_with_boolean_if_record_does_not_respect_date_format():
    # given
    dataframe = DataFrame({'date_of_birth': ['03/04/2024', '.', '2024-04-03', '11/28/2024']})
    # when
    result = check_date_format(dataframe, 'date_of_birth', '%d/%m/%Y')
    # then
    expected = DataFrame({'date_of_birth': ['03/04/2024', '.', '2024-04-03', '11/28/2024'],
                          'date_of_birth-is_format_not_compliant': [False, True, True, True]})
    assert_frame_equal(result[['date_of_birth', 'date_of_birth-is_format_not_compliant']], expected)


def test_check_date_is_later_to_should_create_a_column_with_boolean_if_date1_is_later_than_date2():
    # given
    dataframe = DataFrame({'date_of_birth': ['03/04/2024', '03/04/2023', '04/05/1992', '12/12/1998'],
                           'date_of_diagnosis': ['11/04/2022', '12/01/2024', '28/08/2004', '08/09/1978']}
                          )
    dataframe['date_of_diagnosis_as_iso_8601'] = to_datetime(dataframe['date_of_diagnosis'],
                                                             format="%d/%m/%Y",
                                                             errors="coerce")
    dataframe['date_of_birth_as_iso_8601'] = to_datetime(dataframe['date_of_birth'],
                                                         format="%d/%m/%Y",
                                                         errors="coerce")
    # when
    result = check_date_is_later_to(dataframe, 'date_of_diagnosis', 'date_of_birth')
    # then
    expected = DataFrame({'date_of_diagnosis-rules_is_before_than-date_of_birth': [True, False, False, True]})
    assert_frame_equal(result['date_of_diagnosis-rules_is_before_than-date_of_birth'].to_frame(), expected)


def test_check_value_is_not_in_interval_should_create_a_column_with_boolean_as_true_if_record_is_not_in_interval():
    # given
    dataframe = DataFrame({'packet_year_as_numeric': [10, 12, 2, 35, 48]})
    # when
    result = check_value_is_not_in_interval(dataframe, 'packet_year', min_interval=9, max_interval=37)
    # then
    expected = DataFrame({'packet_year_as_numeric': [10, 12, 2, 35, 48],
                          'packet_year-rules_is_not_in_interval': [False, False, True, False, True]})
    assert_frame_equal(result, expected)


def test_cast_column_to_numeric_should_create_a_column_with_boolean_as_true_if_cast_has_failed():
    # given
    dataframe = DataFrame({'packet_year': [10, '12 pks', 'unk', 35, 48]})
    # when
    result = cast_column_to_numeric(dataframe, 'packet_year')
    # then
    expected = DataFrame({'packet_year-is_format_not_compliant': [False, True, True, False, False]})
    assert_frame_equal(result['packet_year-is_format_not_compliant'].to_frame(), expected)