import pytest
from entities.data_mining.NASA.mass import Mass

MERCURY_MASS = 'Mass x10^23 (kg)      =     3.302'
VENUS_MASS = 'Mass x10^23 (kg)      =    48.685 '
EARTH_MASS = 'Mass x10^24 (kg)= 5.97219+-0.0006'
MOON_MASS = 'Mass, x10^22 kg       =    7.349'
MARS_MASS = 'Mass x10^23 (kg)      =    6.4171'
JUPITER_MASS = 'Mass x 10^22 (g)      = 189818722 +- 8817'
SATURN_MASS = 'Mass x10^26 (kg)      = 5.6834'
URANUS_MASS = 'Mass x10^24 (kg)      = 86.813'
TITAN_MASS = ' Mass (10^19 kg)        = 13455.3'

@pytest.mark.parametrize('input, expected', [((MERCURY_MASS), ({'mass-(kg)':3.302E23, 'sigma_mass-(kg)':None})),
                                             ((VENUS_MASS), ({'mass-(kg)':48.685E23, 'sigma_mass-(kg)':None})),
                                             ((EARTH_MASS), ({'mass-(kg)':5.97219E24, 'sigma_mass-(kg)':0.0006E24})),
                                             ((MOON_MASS), ({'mass-(kg)':7.349E22, 'sigma_mass-(kg)':None})),
                                             ((MARS_MASS), ({'mass-(kg)':6.4171E23, 'sigma_mass-(kg)':None})),
                                             ((JUPITER_MASS), ({'mass-(kg)':189818722E19, 'sigma_mass-(kg)':8817E19})),
                                             ((SATURN_MASS), ({'mass-(kg)':5.6834E26, 'sigma_mass-(kg)':None})),
                                             ((URANUS_MASS), ({'mass-(kg)':86.813E24, 'sigma_mass-(kg)':None})),
                                             ((TITAN_MASS), ({'mass-(kg)':13455.3E19, 'sigma_mass-(kg)':None}))])
def test_Mass_works(input, expected):
    obj = Mass(report=input)
    result = obj.mass()
    assert ((abs(result['mass-(kg)'] - expected['mass-(kg)'])/result['mass-(kg)']) < 1E-5)
