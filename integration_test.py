import multiprocessing
import subprocess
import time
import os
from client import StatusClient

def start_server():
    # Start the server using subprocess with optional configurable environment variables
    env = os.environ.copy()
    # Use the provided environment variables if they exist
    if "TOTAL_DELAY_SECONDS" in env:
        env["TOTAL_DELAY_SECONDS"] = env["TOTAL_DELAY_SECONDS"]
    if "ERROR_CHANCE" in env:
        env["ERROR_CHANCE"] = env["ERROR_CHANCE"]
    if "RESET_INTERVAL_SECONDS" in env:
        env["RESET_INTERVAL_SECONDS"] = env["RESET_INTERVAL_SECONDS"]
    subprocess.run(["python", "server.py"], env=env)

if __name__ == "__main__":
    try:
        # Optionally set configurable variables for the server
        # Uncomment and set values as needed, or leave commented to use defaults
        # os.environ["TOTAL_DELAY_SECONDS"] = "20"
        # os.environ["ERROR_CHANCE"] = "0.2"
        # os.environ["RESET_INTERVAL_SECONDS"] = "15"

        # Start the server in a separate process
        server_process = multiprocessing.Process(target=start_server)
        server_process.start()

        # Allow the server to initialize
        time.sleep(2)

        client = StatusClient(base_url="http://localhost:8000")
        while True:
            status = client.get_status(max_wait_time=60)
            print(f"Integration Test - Final job status: {status}")
            time.sleep(5)  # Wait before checking again
    except KeyboardInterrupt:
        print("Stopping integration test...")
    finally:
        # Terminate the server process
        server_process.terminate()
        server_process.join()
        print("Server process terminated.")

        print("Integration test completed.")
        exit(0)





