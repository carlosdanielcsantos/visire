This is the Video Silence Remover project.

Video Silence Remover is a webapp written in Python-Flask that let you remove silence or low volume segments from videos.

You can run the app in two ways:

1. Through Docker:

   - Install Docker
   - Run the executable run.sh
   - Docker will build and run the appropriate container
   - If you have python installed, the webapp will be automatically launched in your default browser. Otherwise, open your browser and go to http://0.0.0.0:5000.

2. Directly in your machine
   
   - Install python and pip
   - (Optional) Create a virtualenv
   - Install dependencies: pip install -r requirements.txt
   - Install ffmpeg
   - Run webserver with app: python app.py
   - Open app: python -mwebbrowser http://0.0.0.0:5000

