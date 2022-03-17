"""
Launches the Matrix Backend.

@date 3.16.21
@author Christian Saltarelli
"""

from matrix_backend import init_app

app = init_app()

if __name__ == "__main__":
    app.run()
