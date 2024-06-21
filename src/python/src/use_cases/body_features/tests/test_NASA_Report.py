import pytest
from use_cases.body_features.NASA_Report import BodyFeatures

EARTH_SIMULATION = {'body':'earth', 
                    'group':'pln', 
                    'obj_data':True, 
                    'initial_state':True, 
                    'make_ephem':True,
                    'center':True,
                    'out_units':'km-d',
                    'start_time':'2000-jan-01', 
                    'stop_time':'2001-jan-01',
                    'step_size':'30d'}

EARTH_EXEPCTED = ({'mass-(kg)': 5.97219e+24, 'sigma_mass-(kg)': 6e+20},
                 {'GM-(km^3/s^2)': 398600.435436, 'sigma_GM-(km^3/s^2)': 0.0014},
                 {'period-(d)': 1.0000174})

@pytest.mark.parametrize('input, expected', [((EARTH_SIMULATION),(EARTH_EXEPCTED))])
def test_BodyFeatures_works(input, expected):
    obj = BodyFeatures(**input)
    mass_result = obj.mass()
    gmass_result = obj.gmass()
    period_result = obj.period()
    mass_expected, gmass_expected, period_expected = expected
    
    assert mass_result == mass_expected
    assert gmass_result == gmass_expected
    assert period_result == period_expected