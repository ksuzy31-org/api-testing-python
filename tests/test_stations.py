from asserter import assert_true, assert_equal
from session import Endpoints, HTTPSession, RequestTypes, StatusCodes
from test_utils import decorate_test, Constants, DataModel, RequestParams

# Additional imports for mocking and building fake responses
from unittest.mock import patch
from requests import RequestException
import json

ENDPOINT = Endpoints.STATIONS

params = {RequestParams.lat_min_key: RequestParams.lat_min_value,
          RequestParams.lat_max_key: RequestParams.lat_max_value,
          RequestParams.long_min_key: RequestParams.long_min_value,
          RequestParams.long_max_key: RequestParams.long_max_value}


def _build_station_payload():
    return json.dumps([
        {
            Constants.id: DataModel.id_value,
            Constants.latitude: DataModel.latitude_value,
            Constants.longitude: DataModel.longitude_value,
            Constants.name: DataModel.name_value,
            Constants.city: DataModel.city_value,
            Constants.country: DataModel.country_value,
            Constants.provider: DataModel.provider_value,
            Constants.evses: [
                {
                    Constants.id: DataModel.evses_id,
                    Constants.eves_group_name: DataModel.eves_group_name,
                    Constants.eves_connectors: [
                        {Constants.type: DataModel.evses_connector_type, Constants.max_kw: DataModel.evses_connector_max_kw}
                    ],
                },
                {
                    Constants.id: DataModel.evses_id + 1,
                    Constants.eves_group_name: DataModel.eves_group_name,
                    Constants.eves_connectors: [
                        {Constants.type: DataModel.evses_connector_type, Constants.max_kw: DataModel.evses_connector_max_kw}
                    ],
                }
            ]
        }
    ])


class TestStations:

    @staticmethod
    @decorate_test
    def test_station_api_status_code():
        class Resp:
            status_code = 200
            text = _build_station_payload()
        with patch('session.requests.get', return_value=Resp()):
            status_code, _ = HTTPSession.send_request(RequestTypes.GET, ENDPOINT, dict(params))
            assert_equal(status_code, StatusCodes.STATUS_200, f'Status code of {ENDPOINT} enpoint')

    @staticmethod
    @decorate_test
    def test_station_api_returned_list_length():
        class Resp:
            status_code = 200
            text = _build_station_payload()
        with patch('session.requests.get', return_value=Resp()):
            _, station_data = HTTPSession.send_request(RequestTypes.GET, ENDPOINT, dict(params))
            assert_equal(len(station_data), DataModel.station_data_length,
                         'Number of stations returned by data response:')

    @staticmethod
    @decorate_test
    def test_data_model():
        class Resp:
            status_code = 200
            text = _build_station_payload()
        with patch('session.requests.get', return_value=Resp()):
            _, station_data = HTTPSession.send_request(RequestTypes.GET, ENDPOINT, dict(params))
            assert_equal(type(station_data), list, 'The initial level of data type where')
            assert_true(any([isinstance(a, dict) for a in station_data]),
                        'Station data contains dictionary data type')

            assert_true(all(isinstance(a.get(Constants.id, None), int) for a in station_data),
                        'All Station data entities have "id" attribute of int type')
            station_id = station_data[0][Constants.id]
            assert_equal(station_id, DataModel.id_value, 'Station data have "id" entity where')

            station_latitude = station_data[0][Constants.latitude]
            assert_true((isinstance(station_latitude, float)),
                        'Station data have "Latitude" entity attribute of float type')
            assert_equal(station_latitude, DataModel.latitude_value, 'Station data have "Latitude" entity where')

            station_longitude = station_data[0][Constants.longitude]
            assert_true((isinstance(station_longitude, float)),
                        'Station data have "Longitude" entity attribute of float type')
            assert_equal(station_longitude, DataModel.longitude_value, 'Station data have "Longitude" entity where')

            station_name = station_data[0][Constants.name]
            assert_equal(station_name, DataModel.name_value, 'Station data have "name" entity where')

            station_city = station_data[0][Constants.city]
            assert_true(isinstance(station_city, str), 'Station data have "city" entity attribute of String type')
            assert_equal(station_city, DataModel.city_value, 'Station data have "city" entity where')

            station_country = station_data[0][Constants.country]
            assert_true(isinstance(station_country, str), 'Station data have "country" entity attribute of String type')
            assert_equal(station_country, DataModel.country_value, 'Station data have "country" entity where')

            station_provider = station_data[0][Constants.provider]
            assert_true(isinstance(station_provider, str), 'Station data have "provider" entity attribute of String type')
            assert_equal(station_provider, DataModel.provider_value, 'Station data have "provider" entity where')

            assert_equal(len(station_data[0][Constants.evses]), DataModel.evses_length,
                         'Number of eves returned by station data response:')

            evses_id = station_data[0][Constants.evses][0][Constants.id]
            assert_true(isinstance(evses_id, int), 'Eves Id have "provider" entity attribute of int type')
            assert_equal(evses_id, DataModel.evses_id, 'Eves Id have "provider" entity where')

            evses_group_name = station_data[0][Constants.evses][0][Constants.eves_group_name]
            assert_true(isinstance(evses_group_name, str),
                        'Eves Group Name have "provider" entity attribute of String type')
            assert_equal(evses_group_name, DataModel.eves_group_name,
                         'Eves Group Name have "provider" entity where')

            evses_connector_type = station_data[0][Constants.evses][0][Constants.eves_connectors][0][Constants.type]
            assert_true(isinstance(evses_connector_type, str),
                        'Eves connector type have "provider" entity attribute of String type')
            assert_equal(evses_connector_type, DataModel.evses_connector_type,
                         'Eves connector type have "provider" entity where')

            evses_connector_max_kw = station_data[0][Constants.evses][0][Constants.eves_connectors][0][Constants.max_kw]
            assert_true(isinstance(evses_connector_max_kw, int),
                        'Eves connector maxKw have "provider" entity attribute of int type')
            assert_equal(evses_connector_max_kw, DataModel.evses_connector_max_kw,
                         'Eves connector maxKw have "provider" entity where')

    # New tests using mocks to avoid external HTTP calls and file I/O
    @staticmethod
    @decorate_test
    def test_send_request_calls_logger_when_logging_enabled():
        class Resp:
            status_code = 200
            text = _build_station_payload()
        with patch('session.Logger.log_request') as mock_log, patch('session.requests.get', return_value=Resp()) as mock_get:
            local_params = dict(params)  # ensure original params are not mutated
            status_code, data = HTTPSession.send_request(RequestTypes.GET, ENDPOINT, local_params)
            assert_equal(status_code, StatusCodes.STATUS_200, 'Status code should be 200 when logging enabled')
            assert_true(isinstance(data, list), 'Response payload should parse into a list')
            assert_true(mock_log.called is True, 'Logger.log_request should be called when do_logging is True')
            # Ensure GET was called with endpoint and params
            called_args, called_kwargs = mock_get.call_args
            assert_equal(called_args[0], ENDPOINT, 'GET called with endpoint')
            assert_equal(called_args[1], local_params, 'GET called with params')

    @staticmethod
    @decorate_test
    def test_send_request_does_not_call_logger_when_logging_disabled():
        class Resp:
            status_code = 200
            text = _build_station_payload()
        with patch('session.Logger.log_request') as mock_log, patch('session.requests.get', return_value=Resp()):
            local_params = dict(params)
            local_params['do_logging'] = False
            status_code, _ = HTTPSession.send_request(RequestTypes.GET, ENDPOINT, local_params)
            assert_equal(status_code, StatusCodes.STATUS_200, 'Status code should be 200 when logging disabled')
            # When do_logging is False, Logger.log_request must not be called
            assert_true(mock_log.called is False, 'Logger.log_request should not be called when do_logging is False')
            # Ensure the 'do_logging' key was removed from the params passed to logger (via pop)
            assert_true('do_logging' not in local_params, 'do_logging flag should be popped from params')

    @staticmethod
    @decorate_test
    def test_send_request_handles_request_exception_and_returns_none():
        with patch('session.requests.get', side_effect=RequestException('boom')):
            result = HTTPSession.send_request(RequestTypes.GET, ENDPOINT, dict(params))
            # On exception, function returns None (no tuple)
            assert_true(result is None, 'send_request should return None on RequestException')

    @staticmethod
    @decorate_test
    def test_params_are_not_modified_when_do_logging_key_absent():
        class Resp:
            status_code = 200
            text = _build_station_payload()
        with patch('session.requests.get', return_value=Resp()):
            local_params = dict(params)
            _ = HTTPSession.send_request(RequestTypes.GET, ENDPOINT, local_params)
            # Since do_logging key was absent, pop should not remove anything
            assert_equal(local_params, params, 'Params should remain unchanged when do_logging key is absent')

    @staticmethod
    @decorate_test
    def test_response_body_is_parsed_as_list():
        class Resp:
            status_code = 200
            text = _build_station_payload()
        with patch('session.requests.get', return_value=Resp()):
            _, station_data = HTTPSession.send_request(RequestTypes.GET, ENDPOINT, dict(params))
            assert_true(isinstance(station_data, list), 'Parsed response should be a list of stations')
            assert_true(any(isinstance(item, dict) for item in station_data), 'Station list should contain dicts')
