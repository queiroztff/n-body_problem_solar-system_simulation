import pytest
from entities.api_requests import DateTimeConverter
from entities.json_to_object.JD_Date_Time_Convert import ObjectDateTimeConverter

@pytest.fixture
def inject():
    return DateTimeConverter('2000-01-01')

@pytest.fixture
def Obj(inject):
    return ObjectDateTimeConverter(inject)

def test_ObjectDateTimeConverter_isinstance(Obj):
    expected = True
    result = isinstance(Obj, ObjectDateTimeConverter)

    assert result == expected