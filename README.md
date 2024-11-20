# take-home-HG
Response to assessment
# Video Translation System Simulation: Server and Client Library

This project provides a simulation of a video translation backend server and a client library to interact with it.

---

## Features

- **Server:**
  - Implements a `/status` endpoint simulating a job that transitions between states: `pending`, `completed`, or `error`.
  - Configurable delay for job completion.
  - Configurable error probability.
  - Auto-reset mechanism to restart the job after a set interval, simulating a continuous server.

- **Client Library:**
  - Polls the server using exponential backoff to reduce unnecessary requests while maintaining responsiveness.
  - Handles errors gracefully and returns the job status (`completed`, `error`, or `timeout`). A timeout is essential to prevent the client from waiting indefinitely if the server fails to return a final status due to delays, errors, or network issues. It ensures the application remains responsive, avoids wasting resources on excessive polling, 

---

## How to Use

### Prerequisites

Install the necessary Python libraries:
Optionally use an isolated environment with conda

```bash
conda create -n new-env python=3.11
conda activate new-env
# install the necessary packages
pip install fastapi uvicorn requests
```

## Server 
Example usage:
```bash 
TOTAL_DELAY_SECONDS=20 ERROR_CHANCE=0.2 RESET_INTERVAL_SECONDS=15 python server.py
```


#### Configurable Variables

You can set the following environment variables to control the server behavior:

| Variable                 | Default Value | Description                                                                  |
|--------------------------|---------------|------------------------------------------------------------------------------|
| `TOTAL_DELAY_SECONDS`    | `30`          | Total delay in seconds before the job transitions to `completed` or `error`. |
| `ERROR_CHANCE`           | `0.1`         | Probability of the job ending in an error (e.g., `0.1` = 10%).               |
| `RESET_INTERVAL_SECONDS` | `20`          | Time in seconds before the job resets to `pending` after completion/error. Waiting for status of a new job  |

## Client
The client library (StatusClient) provides a simple way to interact with the server. The library takes in one parameter. 

```bash
python client.py
```

or 

```python
client = StatusClient(base_url="http://localhost:8000")
status = client.get_status(max_wait_time=60)
print(f"Job status: {status}")
```



| Parameter       | Default Value | Description                                                      |
|-----------------|---------------|------------------------------------------------------------------|
| `max_wait_time` | `60`          | Maximum time (in seconds) the client will wait for the job status before a timeout error|

## Integration_test

To run the integration test with custom server configuration, you can set the configurable variables directly in the `integration_test.py` file or as part of the script execution.

To terminate the integration test:

1- Press Ctrl+C once to stop the integration test loop.  
2- Press Ctrl+C again to terminate the server process.


example: 

```bash
TOTAL_DELAY_SECONDS=20 ERROR_CHANCE=0.2 RESET_INTERVAL_SECONDS=15 python integration_test.py
```
