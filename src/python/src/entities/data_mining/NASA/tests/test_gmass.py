import pytest
from entities.data_mining.NASA.gmass import Gmass

MERCURY_GMASS = 'GM (km^3/s^2) = 22031.86855  \n  GM 1-sigma (km^3/s^2) = '
VENUS_GMASS = 'GM (km^3/s^2) = 324858.592 \n GM 1-sigma (km^3/s^2) = +-0.006'
EARTH_GMASS = 'GM, km^3/s^2 = 398600.435436 \n  GM 1-sigma, km^3/s^2 = 0.0014'
MOON_GMASS = 'GM, km^3/s^2          = 4902.800066 \n GM 1-sigma, km^3/s^2  =  +-0.0001'
MARS_GMASS = 'GM (km^3/s^2)         = 42828.375214 \n GM 1-sigma (km^3/s^2) = +- 0.00028'
JUPITER_GMASS = 'GM (km^3/s^2)         = 126686531.900     GM 1-sigma (km^3/s^2) =  +- 1.2732'
SATURN_GMASS = 'GM (km^3/s^2)         = 37931206.234    GM 1-sigma (km^3/s^2)  = +- 98'
URANUS_GMASS = 'GM (km^3/s^2)         = 5793951.256     GM 1-sigma (km^3/s^2)  = +-4.3'
TITAN_GMASS = 'GM (km^3/s^2)          = 8978.14  +-  0.06'

@pytest.mark.parametrize('input, expected', [((MERCURY_GMASS), ({'GM-(km^3/s^2)':22031.86855, 'sigma_GM-(km^3/s^2)':None})),
                                             ((VENUS_GMASS),({'GM-(km^3/s^2)':324858.592, 'sigma_GM-(km^3/s^2)':0.006})),
                                             ((EARTH_GMASS),({'GM-(km^3/s^2)':398600.435436, 'sigma_GM-(km^3/s^2)':0.0014})),
                                             ((MOON_GMASS),({'GM-(km^3/s^2)':4902.800066, 'sigma_GM-(km^3/s^2)':0.0001})),
                                             ((MARS_GMASS),({'GM-(km^3/s^2)':42828.375214, 'sigma_GM-(km^3/s^2)':0.00028})),
                                             ((JUPITER_GMASS),({'GM-(km^3/s^2)':126686531.900, 'sigma_GM-(km^3/s^2)':1.2732})),
                                             ((SATURN_GMASS),({'GM-(km^3/s^2)':37931206.234, 'sigma_GM-(km^3/s^2)':98})),
                                             ((URANUS_GMASS),({'GM-(km^3/s^2)':5793951.256, 'sigma_GM-(km^3/s^2)':4.3})),
                                             ((TITAN_GMASS),({'GM-(km^3/s^2)':8978.14, 'sigma_GM-(km^3/s^2)':0.06}))])
def test_gmass_works(input, expected):
    obj = Gmass(report=input)
    result = obj.gmass()
    assert result == expected

