# client.py
import requests
import time

class StatusClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_status(self, max_wait_time=60):
        """
        Polls the status endpoint until the job is completed or an error occurs.
        Returns the final status: 'completed', 'error', or 'timeout' if the max_wait_time is exceeded.
        """
        total_wait_time = 0
        delay = 1  # Start with a 1-second delay
        max_delay = 15  # Maximum delay between polls

        while total_wait_time < max_wait_time:
            try:
                response = requests.get(f"{self.base_url}/status")
                response.raise_for_status()
                result = response.json().get("result", "pending")

                if result in ["completed", "error"]:
                    return result  # Job is no longer pending
                else:
                    print(f"Status is pending. Waiting for {delay} seconds before next check.")
            except requests.RequestException as e:
                print(f"An error occurred: {e}")
                return "error"

            time.sleep(delay)
            total_wait_time += delay
            delay = min(delay * 2, max_delay)  # Exponential backoff

        return "timeout"

if __name__ == "__main__":
    # Example usage
    client = StatusClient(base_url="http://0.0.0.0:8000")
    status = client.get_status(max_wait_time=60)
    print(f"Final job status: {status}")
