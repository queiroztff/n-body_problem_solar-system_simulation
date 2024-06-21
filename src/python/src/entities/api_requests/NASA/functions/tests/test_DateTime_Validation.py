import pytest
from entities.api_requests.NASA.functions.DateTime_Validation import datetime_validation

@pytest.mark.parametrize('input, expected', [('xxxx-02-01', ValueError),
                                             ('2000-xx-01', ValueError),
                                             ('2000-01-xx', ValueError),
                                             ('2000-01-01 xx:01:01', ValueError), 
                                             ('2000/01/01', ValueError), 
                                             ('2451544.5000000', ValueError), 
                                             ('2000-01-01   00:01:01.01', ValueError),
                                             (24515445000000, ValueError)])
def test_datetimevalidation_exception_datetime(input, expected) -> None:
    with pytest.raises(expected_exception=expected):
        datetime_validation(input)

@pytest.mark.parametrize('input', [('2000-jan-01'),
                                   ('2000-feb-01'),
                                   ('2000-mar-01'),
                                   ('2000-01-01'), 
                                   ('2000-01-01.001'), 
                                   ('2000-01-01 00:01'), 
                                   ('2000-01-01 00:01.01'), 
                                   ('2000-01-01 00:01:01.01'), 
                                   (2451544.5000000)])
def test_datetimevalidation_no_exception_datetime(input) -> None:
    datetime_validation(input)
    assert True