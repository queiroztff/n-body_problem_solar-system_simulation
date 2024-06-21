import pytest
from use_cases.body_features.functions import date_to_jd

@pytest.mark.parametrize('input, expected', [(('2000-01-01 00:00'),(2451544.5)),
                                             (('2020-01-01 00:00.20'),(2458849.5001389)),
                                             ((2451544.5),(2451544.5)),
                                             ((2458849.5001389),(2458849.5001389))])
def test_date_to_jd_works(input, expected):
    date = date_to_jd(date=input)
    result = date
    assert result == expected
