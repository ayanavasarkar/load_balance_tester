import argparse, time
import requests, math, threading
import numpy as np
from tqdm import tqdm

class LoadTester:
    def __init__(self, kwargs):
        """Initialize the LoadTester object.

        Args:
            kwargs (dict): A dictionary containing the following key-value pairs:
                - url (str): The URL to test.
                - qps (float): Requests per second.
                - timeout (float, optional): Timeout for each request in seconds (default is 5.0).
                - max_requests (int, optional): Maximum number of requests to make (default is 10).
                - method (str, optional): HTTP method to use, either "GET" or "POST" (default is "GET").
                - headers (dict, optional): Custom headers for the request (default is None).
                - payload (dict or str, optional): Request payload (default is None).
                - logging (bool, optional): Whether logging is enabled (default is True).
                - percentiles (list of float, optional): List of percentiles for latency reporting (default is None).

        Raises:
            KeyError: If any required key is missing in kwargs.
        """
        
        print("Starting Load Tester")
        self.url = kwargs['url']
        self.qps = kwargs['qps']
        self.timeout = kwargs['timeout']
        self.headers = kwargs['headers']
        self.payload = kwargs['payload']
        self.errors = 0
        self.latencies = []
        self.max_requests = kwargs['max_requests']
        self.request_count = 0  # Counter for requests made
        self.method = kwargs['method'].upper()
        
        # Create the Log_file if log enabled
        self.log_enabled = kwargs['logging']
        # Check for Logging; Default is TRUE
        if self.log_enabled:
            self.log_file = "load_test_log"+str(time.time())+".txt"
        
        self.percentiles = kwargs['percentiles'] if kwargs['percentiles'] else []
        self.reponses = kwargs['response_thres'] if kwargs['response_thres'] else []

    def request(self) -> None:
        """Send a HTTP request and record latency and errors.
        Sends a HTTP request to the specified URL using the configured method, headers, and payload.
        Records the latency of the request and tracks any errors encountered.
        """
        start_time = time.time()
        
        try:
            # Get a Response based on Timeout using a custom HTTP Method
            response = requests.request(self.method, self.url, 
                                        headers=self.headers, data=self.payload, 
                                        timeout=self.timeout)
            latency = time.time() - start_time
            self.latencies.append(latency)
            if response.status_code != 200:
                self.errors += 1
        except Exception as e:
            print("Error:", e)
            latency = time.time() - start_time
            self.errors += 1

        self.request_count += 1  # Increment request count

        if self.log_enabled:
            self.log_request(start_time, latency, response.status_code)
        
    def run(self) -> None:
        """
        Run the Benchmarking Test
        """
        # Define the Progress Bar
        progress_bar = tqdm(total=self.max_requests, desc="Testing")
        
        # Run each for a request till the Maximum Request Capacity
        while self.request_count < self.max_requests:
            threading.Thread(target=self.request).start()
            time.sleep(1 / self.qps)
            progress_bar.update(1)
        progress_bar.close()

    def log_request(self, start_time, latency, status_code) -> None:
        """
        Log the Results from each request
        """
        with open(self.log_file, 'a') as f:
            f.write(f"Timestamp: {start_time}, Latency: {latency} seconds, Status Code: {status_code}\n")

    def report(self) -> None:
        """
        Report the Results of the Testing for Benchmarking.
        """
        print("Total Requests:", len(self.latencies))
        print("Total Errors:", self.errors)
        self.log_report()

    def log_report(self) -> None:
        """
        Log the Report in a Text File.
        Log metrics like:
            Total Requests, TOtal Errors, Average, Max and Minimum Latencies
            Amplitude and the Standard Deviations.
        """
        with open(self.log_file, 'a') as f:
            f.write("____________________________________________________________")
            f.write("___________________ FINAL REPORT ___________________________")
            f.write("____________________________________________________________")
            f.write(f"TOTAL REQUESTS: {len(self.latencies)}\n")
            f.write(f"TOTAL ERRORS: {self.errors}\n")

            f.write(f"\n")
            f.write(f"Detailed Stats: \n")

            if self.latencies:
                avg_latency = sum(self.latencies) / len(self.latencies)
                std_dev = math.sqrt(sum((x - avg_latency) ** 2 for x in self.latencies) / len(self.latencies))
                
                f.write(f"Average Latency: {avg_latency} seconds\n")
                f.write(f"Maximum Latency (Slowest): {max(self.latencies)} seconds\n")
                f.write(f"Minimum Latency (Fastest): {min(self.latencies)} seconds\n")
                f.write(f"Amplitude Latency (Difference between Fastest and Slowest): {max(self.latencies)- min(self.latencies)} seconds\n")
                f.write(f"Standard Deviation: {std_dev} seconds\n")

                if self.percentiles:
                    for p in self.percentiles:
                        print(f"{p}-th Percentile Latency:", np.percentile(self.latencies, p))
                        f.write(f"{p}-th Percentile Latency: {np.percentile(self.latencies, p)}\n")
                
                if self.reponses:
                    response_time_counts = self.calculate_response_time_percentiles(thresholds=self.reponses)
                    f.write(f"Response Time Thresholds (Percentage of response times above the threshold): {response_time_counts}\n")

            else:
                f.write(f"Average Latency: No Requests made for Latency Computation")
                print("No requests made.")

    def calculate_response_time_percentiles(self, thresholds) -> dict:
        """Calculate the percentage of requests meeting specified response time thresholds.

        Args:
            thresholds (list of float): List of response time thresholds in seconds.

        Returns:
            dict: A dictionary containing the percentage of requests meeting each threshold.
                Keys are the thresholds and values are the corresponding percentages.
        """
        response_time_counts = {}
        total_requests = len(self.latencies)

        for threshold in thresholds:
            count = sum(latency >= threshold for latency in self.latencies)
            percentage = (count / total_requests) * 100
            response_time_counts[threshold] = str(percentage) + "%"

        return response_time_counts


def main():
    parser = argparse.ArgumentParser(description="HTTP Load Tester")
    parser.add_argument("--url", default="https://lu.ma/6jrcq4ow", help="URL to test")
    parser.add_argument("--qps", type=float, default=1, help="Requests per second")
    parser.add_argument("--timeout", type=float, default=5.0, help="Requests per second")
    parser.add_argument("--max_requests", type=int, default=10, help="Maximum Number of Requests")
    parser.add_argument("--method", default="GET", choices=["GET", "POST", "PUT", "DELETE"], help="HTTP method to use")
    parser.add_argument("--headers", nargs='*', help="Custom headers as key-value pairs separated by space")
    parser.add_argument("--payload", help="Request payload")
    parser.add_argument("--logging", default=False, help="Logging Enabled/Disabled")
    parser.add_argument("--percentiles", nargs='+', default=[90], type=list, 
                        help="Percentiles for latency reporting as a list of percentile values, e.g., [10, 90]")
    parser.add_argument("--response_thres", nargs='+', default=[0.25, 0.5], type=list, 
                        help="Response time Thresholds as a list of time in seconds; e.g, [0.5, 0.25]")
    args = parser.parse_args()

    args = dict(args._get_kwargs())
    
    load_tester = LoadTester(kwargs=args)
    load_tester.run()
    load_tester.report()

if __name__ == "__main__":
    main()


# Custom HTTP methods: Allowing users to specify HTTP methods other than GET.
# Headers and Payloads: Support for custom headers and request payloads.
# Concurrency control: Allowing users to specify the number of concurrent requests.
# Timeouts: Setting a timeout for each request.
# Logging: Logging request/response details.
# Output formats: Supporting different formats for the report, such as JSON or CSV.
# Custom reporting: More detailed reporting options, like percentiles for latency.
# Response Time Thresholds: Introduce the ability to define response time thresholds and
# report on the percentage of requests that meet or exceed these thresholds.
# Timeout per Request: Currently, there's a global timeout for requests. 
# You could add an option to specify a timeout for each individual request.