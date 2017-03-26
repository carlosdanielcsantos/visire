docker build -t video-silence-remover:latest .
docker run -d -p 5000:5000 video-silence-remover
python -mwebbrowser http://0.0.0.0:5000
