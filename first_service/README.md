# Local run
1. python3 -m venv .env
2. source .env/bin/activate
3. pip3 install -r requirements.txt

# Docker run
1. docker build --tag first-service-docker .
2. docker run -d -p 5000:5000 first-service-docker