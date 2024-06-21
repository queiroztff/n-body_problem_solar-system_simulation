import pytest
from entities.data_mining.NASA.functions.unit_converter import mass_convert_factor

@pytest.mark.parametrize('input, expected', [(('kg', 'g'), 1000.0),
                                             (('g', 'kg'), 0.001),
                                             (('kg', 'hg'), 10.0)])
def test_mass_convert_factor_works(input, expected):
    unit_in, unit_out = input
    result = mass_convert_factor(unit_in=unit_in, unit_out=unit_out)

    assert result == expected
