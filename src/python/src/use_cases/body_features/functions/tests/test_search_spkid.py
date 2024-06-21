import pytest
from use_cases.body_features.functions.search_spkid import search_spkid

SUN_SPKID = 10
MERCURY_SPKID = 199
VENUS_SPKID = 299
EARTH_SPKID = 399
MARS_SPKID = 499
JUPITER_SPKID = 599
SATURN_SPKID = 699
URANUS_SPKID = 799
NEPTUNE_SPKID = 899
MOON_SPKID = 301

@pytest.mark.parametrize('input, expected', [(('Sun', 'pln'),(10)),
                                             (('Mercury', 'pln'),(199)),
                                             (('Venus', 'pln'),(299)),
                                             (('Earth', 'pln'),(399)),
                                             (('Mars', 'pln'),(499)),
                                             (('Jupiter', 'pln'),(599)),
                                             (('Saturn', 'pln'),(699)),
                                             (('Uranus', 'pln'),(799)),
                                             (('Neptune', 'pln'),(899)),
                                             (('moon', 'sat'),(301))])
def test_search_spkid_works(input, expected):
    body, group = input
    id = search_spkid(body=body, group=group)
    result = id
    assert result == expected
