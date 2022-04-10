"""
Launches the Matrix Server. To do so execute the following command within the root
directory of this project:

$ python3 run.py

@date 3.16.22
@author Christian Saltarelli
"""
from app import init_app

app = init_app()

# Example Command: docker run -p 5000:5000 -e FLASK_ENV='development' matrix_app_dev
if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run()