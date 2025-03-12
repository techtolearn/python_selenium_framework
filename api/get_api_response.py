import requests

from config.config import TestData


class GetApiData:
    def get_data(self, end_point,container, key):
        try:
            response = requests.get(TestData.BASE_URL +end_point)
            assert response.status_code == 200

            data = response.json() # convert response to json

            response_section = data.get(container, [])
            if isinstance(response_section, list):
                for item in response_section:
                    if key in item:
                        return item[key]
            elif isinstance(response_section, dict):
                return response_section.get(key)

            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data : {e}")
            return None