from data_curation.curation.functions import curate_pack_years


def test_curate_pack_years_should_return_empty_value_with_nan():
    # given
    pack_years = float("NaN")
    # when
    result = curate_pack_years(pack_years)
    # then
    assert result == -1


def test_curate_pack_years_should_return_int_value_extracted_from_string():
    # given
    pack_years = "50 packs"
    # when
    result = curate_pack_years(pack_years)
    # then
    assert result == 50


def test_curate_pack_years_should_return_value_if_value_is_valid():
    # given
    pack_years = 48
    # when
    result = curate_pack_years(pack_years)
    # then
    assert result == 48


def test_curate_pack_years_should_return_empty_value_when_no_value_is_extracted_from_string():
    # given
    pack_years = "approximately 50 packs"
    # when
    result = curate_pack_years(pack_years)
    # then
    assert result == -1

