import pytest
import requests

from Data.data_for_test import data_for_reversed_strings
from Util.Logger import getLogger

from Util.Read_INI_File import read_config_ini


@pytest.mark.usefixtures("setup")
class Test_application:
    tmp_input_string = None

    @staticmethod
    def build_url():
        url = "http://" + read_config_ini()['Server']['host'] + ":" + read_config_ini()['Port']['Port']
        return url

    # Test reverse API with valid input
    @pytest.mark.parametrize("data", data_for_reversed_strings())
    def test_reverse_valid_input(self, data):
        log = getLogger()
        url = self.build_url()
        input_string = data["input_string"]
        expected_result = data["expected_result"]

        response = requests.get(url + "/reverse", params={"in": input_string})
        data_response = response.json()
        log.info("Response status code:" + str(response.status_code))

        assert response.status_code == 200
        assert data_response["result"] == expected_result
        # pytest.global_var = data["input_string"]
        Test_application.tmp_input_string = data["input_string"]

    # Test restore API with valid input
    def test_restore_valid_input(self):
        log = getLogger()
        url = self.build_url()
        expected_result = Test_application.tmp_input_string

        response = requests.get(url + "/restore")
        data_response = response.json()
        log.info("Response status code:" + str(response.status_code))

        assert response.status_code == 200
        assert data_response["Source"] == expected_result

    # Test reverse with empty input
    def test_reverse_empty_input(self):
        log = getLogger()
        url = self.build_url()

        response = requests.get(url + "/reverse")
        data_response = response.json()
        log.info("Response status code:" + str(response.status_code))

        assert response.status_code == 200
        assert data_response["result"] == ""

    # Test restore with empty input
    def test_restore_empty_input(self):
        log = getLogger()
        url = self.build_url()

        response = requests.get(url + "/restore")
        data_response = response.json()
        log.info("Response status code:" + str(response.status_code))

        assert response.status_code == 200
        assert data_response["Source"] == ""

    # Test API with invalid input
    def test_restore_invalid_input(self):
        log = getLogger()
        url = self.build_url()
        response = requests.get(url)
        log.info("Response status code:" + str(response.status_code))
        assert response.status_code == 404
