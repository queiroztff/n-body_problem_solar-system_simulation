import pytest
from entities.data_mining.NASA.period import Period

MERCURY_PERIOD = 'Sidereal orb. per.    = 87.969257  d'
VENUS_PERIOD = 'Sidereal orb. per., d = 224.70079922 d'
EARTH_PERIOD = 'Sidereal orb period  = 365.25636 d'
MOON_PERIOD = 'Orbit period          = 27.321582 d'
MARS_PERIOD = 'Mean sidereal orb per =  686.98 d'
JUPITER_PERIOD = 'Sidereal orbit period = 4332.589 d'
SATURN_PERIOD = 'Sidereal orbit period  = 10755.698 d'
URANUS_PERIOD = 'Sidereal orbit period  = 30685.4 d'
TITAN_PERIOD = 'Orbital period     = 15.945421 d'

@pytest.mark.parametrize('input, expected', [((MERCURY_PERIOD), ({'period-(d)':87.969257})),
                                             ((VENUS_PERIOD), ({'period-(d)':224.70079922})),
                                             ((EARTH_PERIOD), ({'period-(d)':365.25636})),
                                             ((MOON_PERIOD), ({'period-(d)':27.321582})),
                                             ((MARS_PERIOD), ({'period-(d)':686.98})),
                                             ((JUPITER_PERIOD), ({'period-(d)':4332.589})),
                                             ((SATURN_PERIOD), ({'period-(d)':10755.698})),
                                             ((URANUS_PERIOD), ({'period-(d)':30685.4})),
                                             ((TITAN_PERIOD), ({'period-(d)':15.945421}))])
def test_Period_works(input, expected):
    obj = Period(report=input)
    result = obj.period()
    assert result == expected