import pytest
from entities.api_requests.NASA.JD_Date_Time_Convert import DateTimeConverter

@pytest.mark.parametrize('input, expected', [('2000-01-01', dict()),
                                             ('2000-01-01.001', dict()),
                                             ('2000-01-01 00:01', dict()),
                                             ('2000-01-01 00:01.01', dict()),
                                             ('2000-01-01 00:01:01', dict()),
                                             ('2000-01-01 00:01:01.01', dict()),
                                             (2451544.5000000, dict())])
def test_get_data_output_type(input, expected) -> None:
    search = DateTimeConverter(input)
    result = search.get_data()
    assert type(result) is type(expected)

@pytest.mark.parametrize('input, expected', 
                         [('2000-01-01 00:01:02', {'cd', 'year', 'month_name', 'doy', 'dow', 'dow_name', 
                                          'day_and_time', 'jd', 'signature'}),

                          (2451544.5000000, {'cd', 'year', 'month', 'month_name', 'doy', 'dow', 
                                             'dow_name', 'day_and_time', 'signature'})])
def test_get_data_output_primary_keys(input, expected) -> None:
    search = DateTimeConverter(input)
    result = (set(search.get_data().keys()))
    assert result == expected



