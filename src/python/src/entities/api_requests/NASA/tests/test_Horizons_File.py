import pytest
from entities.api_requests.NASA.Horizons_File import HorizonsFile

@pytest.mark.parametrize('input, expected', [((399, True, True, '500@0', '2000-01-01', '2020-01-01', '123', 'km-d'), True),
                                             ((399, True, True, '500@0', '2000-01-01', '2020-01-01', '1m', 'km-d'), True),
                                             ((399, True, True, '500@0', '2000-01-01', '2020-01-01', '1d', 'km-d'), True),
                                             ((399, True, True, '500@0', '2000-01-01', '2020-01-01', '1h', 'km-d'), True),
                                             ((399, True, True, '500@0', '2000-01-01', '2020-01-01', '1mo', 'km-d'), True),
                                             ((399, True, True, '500@0', '2000-01-01', '2020-01-01', '1y', 'km-d'), True),
                                             ((399, True, True, '500@0', '2000-01-01', '2020-01-01', '1 y', 'km-d'), True)])
def test_horazonsfile_step_size_is_valid(input, expected):
    command, obj_data, make_ephem, center, start_time, stop_time, step_size, out_units = input
    report = HorizonsFile(command=command, obj_data=obj_data,
                        make_ephem=make_ephem, center=center,
                        start_time=start_time, stop_time=stop_time,
                        step_size=step_size, out_units=out_units)
    result = isinstance(report, HorizonsFile)
    assert result == expected

@pytest.mark.parametrize('input, expected', [((399, True, True, '500@0', '2000-01-01', '2020-01-01', '123x', 'km-d'), ValueError),
                                             ((399, True, True, '500@0', '2000-01-01', '2020-01-01', 'xxx', 'km-d'), ValueError)])
def test_horizonsfile_step_size_exception(input, expected):
    with pytest.raises(expected):
        command, obj_data, make_ephem, center, start_time, stop_time, step_size, out_units = input
        report = HorizonsFile(command=command, obj_data=obj_data,
                          make_ephem=make_ephem, center=center,
                          start_time=start_time, stop_time=stop_time,
                          step_size=step_size, out_units=out_units)

@pytest.mark.parametrize('input, expected', [((399, True, True, '500@0', '2000-01-01', '2020-01-01', '1y', 'xx-x'), ValueError),
                                             ((399, True, True, '500@0', '2000-01-01', '2020-01-01', '1y', 'xxx'), ValueError)])
def test_horizonsfile_out_units_exception(input, expected):
    with pytest.raises(expected):
        command, obj_data, make_ephem, center, start_time, stop_time, step_size, out_units = input
        report = HorizonsFile(command=command, obj_data=obj_data,
                          make_ephem=make_ephem, center=center,
                          start_time=start_time, stop_time=stop_time,
                          step_size=step_size, out_units=out_units)


@pytest.mark.parametrize('input, expected', [((399, True, True, '500@0', 2451544.5, 2455197.5, '1y', 'km-d'), str()),
                                             ((499, False, False, '500@0', '2010-01-01', '2023-01-01', '1y', 'au-d'), str())])
def test_horizonsfile_get_data_output_type(input, expected):
    command, obj_data, make_ephem, center, start_time, stop_time, step_size, out_units = input

    report = HorizonsFile(command=command, obj_data=obj_data,
                          make_ephem=make_ephem, center=center,
                          start_time=start_time, stop_time=stop_time,
                          step_size=step_size, out_units=out_units)
    
    result = report.get_report()
    print(result)
    assert type(result) is type(expected)
