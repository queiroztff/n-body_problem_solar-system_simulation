import pytest
from entities.data_mining.NASA.functions import tuple_str_to_float

@pytest.mark.parametrize('input, expected', [(('1', '2', '3'), (1.0, 2.0, 3.0)),
                                             (('1.1', '2.2', '3.3'), (1.1, 2.2, 3.3)),
                                             (('', '', ''), (None, None, None))])
def test_tuple_str_to_float_works(input, expected):
    result = tuple_str_to_float(t=input)
    assert result == expected