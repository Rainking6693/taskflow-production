from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from supabase import create_client, Client
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ztrqlzksmychwbmrumbu.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp0cnFsemtzbXljaHdibXJ1bWJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzM0MDU4NjUsImV4cCI6MjA0ODk4MTg2NX0.y6gEd6JT6ybzH5YpWY4H0pI2hN0DqXDPwXnNNEoGzKU')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return jsonify({
        'status': 'healthy',
        'app': 'TaskFlow API',
        'version': '1.0.0',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        response = supabase.table('tasks').select('*').order('created_at', desc=True).execute()
        return jsonify(response.data or [])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        title = data.get('title')

        if not title:
            return jsonify({'error': 'Title is required'}), 400

        response = supabase.table('tasks').insert({
            'title': title,
            'completed': False
        }).execute()

        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        updates = {}

        if 'title' in data:
            updates['title'] = data['title']
        if 'completed' in data:
            updates['completed'] = data['completed']

        response = supabase.table('tasks').update(updates).eq('id', task_id).execute()

        return jsonify(response.data[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        supabase.table('tasks').delete().eq('id', task_id).execute()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
