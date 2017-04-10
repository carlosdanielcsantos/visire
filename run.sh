docker build -t vsr:latest .
docker run -d -p 5000:5000 vsr
python -mwebbrowser http://0.0.0.0:5000
