"""
Python-API-Testing-Framework - Flask Application
Main web application with routes for configuration, test execution, and results
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from pathlib import Path
from datetime import datetime

from core.config_manager import ConfigManager
from core.data_parser import DataParser
from core.test_executor import TestExecutor
from core.report_generator import ReportGenerator

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'python-api-testing-framework-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize core components
config_manager = ConfigManager()
data_parser = DataParser()
report_generator = ReportGenerator()

# Global test executor (for managing running tests)
current_executor = None


@app.route('/')
def index():
    """Dashboard/Home page"""
    config = config_manager.load_config()
    test_files = data_parser.get_test_files()

    # Get recent test results
    recent_results = get_recent_results(limit=5)

    return render_template('index.html',
                           config=config,
                           test_files=test_files,
                           recent_results=recent_results)


@app.route('/configure', methods=['GET', 'POST'])
def configure():
    """Configuration management page"""
    if request.method == 'POST':
        # Save configuration
        config_data = {
            'API_BASE_URL': request.form.get('api_base_url', ''),
            'API_ENDPOINT': request.form.get('api_endpoint', ''),
            'METHOD': request.form.get('method', 'POST'),
            'API_KEY': request.form.get('api_key', ''),
            'CORRELATION_ID': request.form.get('correlation_id', 'test'),
            'TIMEOUT': request.form.get('timeout', '30'),
            'MAX_RESPONSE_TIME': request.form.get('max_response_time', '5000')
        }

        success = config_manager.save_config(config_data)

        if success:
            return jsonify({'success': True, 'message': 'Configuration saved successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to save configuration'}), 500

    # GET request - show configuration form
    config = config_manager.load_config()
    return render_template('configure.html', config=config)


@app.route('/test-runner')
def test_runner():
    """Test execution page"""
    test_files = data_parser.get_test_files()
    config = config_manager.load_config()
    return render_template('test_runner.html', test_files=test_files, config=config)


@app.route('/results')
def results():
    """Test results viewing page"""
    # Get all test result files
    results_list = get_all_results()
    return render_template('results.html', results=results_list)


@app.route('/api/test-files')
def api_test_files():
    """API endpoint to get list of test files"""
    test_files = data_parser.get_test_files()
    return jsonify(test_files)


@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """API endpoint for configuration"""
    if request.method == 'POST':
        config_data = request.json
        success = config_manager.save_config(config_data)
        return jsonify({'success': success})
    else:
        config = config_manager.load_config()
        # Mask sensitive values
        masked_config = config.copy()
        if 'API_KEY' in masked_config and masked_config['API_KEY']:
            masked_config['API_KEY'] = '****'
        return jsonify(masked_config)


@app.route('/api/upload-test-file', methods=['POST'])
def upload_test_file():
    """Upload a test data file"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join('Test_Data', filename)
        file.save(filepath)
        return jsonify({'success': True, 'message': f'File {filename} uploaded successfully'})

    return jsonify({'success': False, 'message': 'Invalid file type'}), 400


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['csv', 'json']


@app.route('/api/download-test-file/<filename>')
def download_test_file(filename):
    """Download a test data file from Test_Data directory"""
    try:
        # Secure the filename to prevent directory traversal
        filename = secure_filename(filename)
        filepath = os.path.join('Test_Data', filename)

        # Check if file exists
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'message': 'File not found'}), 404

        # Check if it's an allowed file type
        if not allowed_file(filename):
            return jsonify({'success': False, 'message': 'Invalid file type'}), 400

        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/download-sample/<filename>')
def download_sample_file(filename):
    """Download a sample test data file"""
    try:
        # Map of allowed sample files
        allowed_samples = {
            'csv-legacy': 'test-data-sample.csv',
            'csv-dynamic': 'InvoiceExtraction-TestCases-sample.csv',
            'json': 'test-data-sample.json'
        }

        # Get the actual filename
        actual_filename = allowed_samples.get(filename)
        if not actual_filename:
            return jsonify({'success': False, 'message': 'Invalid sample file'}), 400

        filepath = os.path.join('Test_Data', actual_filename)

        # Check if file exists
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'message': 'Sample file not found'}), 404

        return send_file(filepath, as_attachment=True, download_name=actual_filename)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@socketio.on('start_tests')
def handle_start_tests(data):
    """WebSocket handler for starting tests"""
    global current_executor

    try:
        # Get test file and configuration
        test_file = data.get('test_file')
        language = data.get('language', 'EN-US')

        # Load configuration
        config = config_manager.load_config()

        # Parse test data
        test_data_list = data_parser.parse_file(f"Test_Data/{test_file}")

        # Replace template variables and update language in test data
        for test_data in test_data_list:
            body = test_data.get('body')

            # Handle both dict and list body formats
            if isinstance(body, dict):
                # Replace template variables
                if 'environment' in body and body['environment'] == '{{environment}}':
                    body['environment'] = 'AFI'
                if 'languageCheck' in body:
                    body['languageCheck'] = language

            elif isinstance(body, list):
                # Body is a list (from dynamic CSV format)
                for item in body:
                    if isinstance(item, dict):
                        # Replace template variables
                        if 'environment' in item and item['environment'] == '{{environment}}':
                            item['environment'] = 'AFI'
                        if 'languageCheck' in item:
                            item['languageCheck'] = language

        # Create executor
        current_executor = TestExecutor(config)

        # Progress callback
        def progress_callback(progress):
            socketio.emit('test_progress', progress)

        # Execute tests
        results = current_executor.execute_tests(
            test_data_list, progress_callback)

        # Generate report
        summary = current_executor.get_summary()
        html_report = report_generator.generate_html_report(
            current_executor.get_results(),
            summary
        )
        report_path = report_generator.save_report(html_report)

        # Debug: Print summary to console
        print(
            f"DEBUG: Test Summary - Total: {summary['total']}, Passed: {summary['passed']}, Failed: {summary['failed']}, Pass Rate: {summary['pass_rate']}%")

        # Send completion event
        socketio.emit('tests_complete', {
            'summary': summary,
            'results': current_executor.get_results(),
            'report_path': report_path
        })

    except Exception as e:
        socketio.emit('test_error', {'error': str(e)})


@socketio.on('stop_tests')
def handle_stop_tests():
    """WebSocket handler for stopping tests"""
    global current_executor
    if current_executor:
        current_executor.stop()
        socketio.emit('tests_stopped', {'message': 'Tests stopped by user'})


def get_recent_results(limit=5):
    """Get recent test results"""
    results_dir = Path('test-results')
    if not results_dir.exists():
        return []

    # Get all result directories
    result_dirs = []
    for date_dir in results_dir.iterdir():
        if date_dir.is_dir():
            for run_dir in date_dir.iterdir():
                if run_dir.is_dir():
                    result_dirs.append(run_dir)

    # Sort by modification time
    result_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    # Get recent results
    recent = []
    for result_dir in result_dirs[:limit]:
        # Look for HTML report
        html_files = list(result_dir.glob('*.html'))
        if html_files:
            recent.append({
                'path': str(result_dir),
                'date': result_dir.parent.name,
                'time': result_dir.name.replace('run_', '').replace('-', ':'),
                'report': str(html_files[0])
            })

    return recent


def get_all_results():
    """Get all test results"""
    results_dir = Path('test-results')
    if not results_dir.exists():
        return []

    all_results = []
    for date_dir in results_dir.iterdir():
        if date_dir.is_dir():
            for run_dir in date_dir.iterdir():
                if run_dir.is_dir():
                    html_files = list(run_dir.glob('*.html'))
                    pdf_files = list(run_dir.glob('*.pdf'))

                    all_results.append({
                        'path': str(run_dir),
                        'date': date_dir.name,
                        'time': run_dir.name.replace('run_', '').replace('-', ':'),
                        'report': str(html_files[0]) if html_files else None,
                        'pdf_count': len(pdf_files)
                    })

    # Sort by date and time (newest first)
    all_results.sort(key=lambda x: (x['date'], x['time']), reverse=True)
    return all_results


@app.route('/download/<path:filename>')
def download_file(filename):
    """Download a file (PDF or HTML report)"""
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('Test_Data', exist_ok=True)
    os.makedirs('test-results', exist_ok=True)

    print("=" * 80)
    print("Python-API-Testing-Framework - Starting Application")
    print("=" * 80)
    print()
    print("Server running at: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print()

    # Run with SocketIO
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
