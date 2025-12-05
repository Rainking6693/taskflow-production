"""
WSGI configuration for PythonAnywhere deployment.

To deploy on PythonAnywhere:
1. Upload this code to ~/taskflow-backend/
2. Install requirements: pip3 install --user -r requirements.txt
3. Configure web app to use this WSGI file
4. Set environment variables in WSGI configuration
"""

import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/taskflow-backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['SUPABASE_URL'] = 'https://ztrqlzksmychwbmrumbu.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp0cnFsemtzbXljaHdibXJ1bWJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzM0MDU4NjUsImV4cCI6MjA0ODk4MTg2NX0.y6gEd6JT6ybzH5YpWY4H0pI2hN0DqXDPwXnNNEoGzKU'

# Import your Flask app
from app import app as application
