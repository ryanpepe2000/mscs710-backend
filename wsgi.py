"""
Launches the Matrix Backend. To do so execute the following command within the root
directory of this project:

$ python3 wsgi.py

@date 3.16.21
@author Christian Saltarelli
"""
from matrix_backend import init_app

app = init_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
