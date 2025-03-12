import requests

from config.config import TestData


class PostData:
    @staticmethod
    def post_request(endpoint):
        """
        Performs a POST request and handles response effectively.

        Args:
            endpoint (str): The API endpoint (relative path).
            payload (dict): The JSON data to send in the POST request.
            headers (dict): Custom headers (optional).
            timeout (int): Request timeout in seconds (default = 10).

        Returns:
            dict | None: JSON response if successful, otherwise None.
        """
        headers = {
            "Authorization":"Bearer <your-token",
            "Content-Type": "application/json"
        }
        payload = {

        }

        timeout = 10
        url = TestData.API_BASE_URL
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=timeout)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()  # Return JSON response
        except requests.exceptions.RequestException as e:
            print(f"Error during POST request: {e}")
            return None


