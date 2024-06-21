import pytest
from entities.api_requests.NASA.Horizons_Lookup import Lookup


def test_lookup_exception_group() -> None:
    with pytest.raises(expected_exception=ValueError):
        search = Lookup(sstr='earth', group='xxx')


@pytest.mark.parametrize('input, expected',[(('earth', 'pln'), dict()), 
                                            (('moon','sat'), dict()), 
                                            (('Ceres', 'ast'), dict()), 
                                            (('halley', 'com'), dict())])
def test_get_data_output_type(input, expected) -> None:
    sstr, group = input
    search = Lookup(sstr=sstr, group=group)
    result = search.get_data()
    assert type(result) is type(expected)


@pytest.mark.parametrize('input, expected',[(('earth', 'pln'),{'signature', 'count', 'result'}), 
                                            (('xxxxx','pln'), {'signature', 'count'})])
def test_get_data_output_primary_keys(input, expected) -> None:
    sstr, group = input
    search = Lookup(sstr=sstr, group=group)
    result = set(search.get_data().keys())
    assert result == expected

