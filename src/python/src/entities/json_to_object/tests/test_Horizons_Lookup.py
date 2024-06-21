import pytest
from entities.api_requests import Lookup
from entities.json_to_object.Horizons_Lookup import ObjectLookup

@pytest.fixture
def inject():
    return Lookup(sstr='earth', group='pln')

@pytest.fixture
def Obj(inject):
    return ObjectLookup(inject)

def test_ObjectLookup_isinstance(Obj):
    expected = True
    result = isinstance(Obj, ObjectLookup)

    assert result == expected

