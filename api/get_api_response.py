import requests
from requests.exceptions import RequestException, Timeout, HTTPError
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

    @staticmethod
    def execute_get_request(url, headers=None, params=None, timeout=10, retries=3):
        """
        Executes a GET request and verifies its success.

        Args:
            url (str): The API endpoint URL.
            headers (dict): Optional request headers.
            params (dict): Optional query parameters.
            timeout (int): Request timeout in seconds (default 10).
            retries (int): Number of retry attempts for failed requests.

        Returns:
            dict: JSON response data if successful.

        Raises:
            AssertionError: If the request fails after retries.
        """
        for attempt in range(1, retries + 1):
            try:
                response = requests.get(url, headers=headers, params=params, timeout=timeout)
                response.raise_for_status()  # Raises HTTPError for 4xx/5xx status codes

                print(f"✅ GET request successful on attempt {attempt}: {response.status_code}")
                return response.json()

            except (Timeout, HTTPError) as e:
                print(f"⚠️ Attempt {attempt} failed: {e}")

            except RequestException as e:
                print(f"❌ Request error on attempt {attempt}: {e}")
                break  # Exit loop for network-related issues

        raise AssertionError(f"❌ GET request failed after {retries} attempts for URL: {url}")