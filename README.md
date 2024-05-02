# HTTP Load Tester

HTTP Load Tester is a Python tool for load testing and benchmarking HTTP endpoints. It provides various features to simulate concurrent requests, measure response times, and report errors.

## Features

- Simulate concurrent HTTP requests at a specified rate (QPS)
- Support for various HTTP methods: GET, POST, PUT, DELETE
- Customizable request headers and payloads
- Reporting of latencies and error rates
- Support for response time thresholds
- Logging of request details to a text file
- Docker containerization for easy deployment

## How to Use

1. **Clone the Repository:**
git clone https://github.com/yourusername/http-load-tester.git
cd http-load-tester

2. **Install Dependencies:**
pip install -r requirements.txt

3. **Run the Load Tester:**
Example Usage:

python load_tester.py http://example.com --qps 10 --method GET
Replace `http://example.com` with the URL you want to test. Adjust other parameters such as QPS and method as needed.

## How to Build the Docker Image

1. **Build the Docker Image:**
docker build -t http-load-tester .

2. **Run the Load Tester Inside Docker:**
docker run http-load-tester http://example.com --qps 10 --method GET

Replace `http://example.com` with the URL you want to test. Adjust other parameters as needed.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with any improvements or bug fixes.