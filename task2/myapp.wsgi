import sys
import os

# Path to my project directory
project_dir = r"C:\Users\Kev\PycharmProjects\ai-web\task2\week2"
sys.path.insert(0, project_dir)  # Add the project directory to the Python path

# Set the Flask application's entry point
from myapp2 import app as application  # Replace 'myapp2' with your Python file's name (without the .py)
