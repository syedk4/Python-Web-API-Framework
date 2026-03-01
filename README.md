# HTTPie-Python-Web

A web-based API testing framework built with Flask, providing an intuitive interface for running, managing, and analyzing API tests.

## 🌟 Features

- **Web-Based Configuration Manager** - Easy API configuration through web interface
- **Test File Management** - Upload, list, and manage CSV/JSON test files
- **Real-Time Test Execution** - Live progress updates via WebSocket
- **Interactive Dashboard** - View test files, configuration status, and recent results
- **Comprehensive Reports** - Beautiful HTML reports with detailed test results
- **Multi-Language Support** - Test APIs in multiple languages (EN-US, FR-CA, ES-MX)
- **PDF Generation Support** - Automatic PDF file handling and storage
- **Responsive UI** - Bootstrap 5 responsive design works on all devices

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the project directory
cd C:\Users\slatheef\Documents\HTTPie\HTTPie-Python-Web

# Create virtual environment
py -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Edit `config.env` file with your API settings:

```env
API_BASE_URL=http://your-api-server.com/api
API_ENDPOINT=/your-endpoint
API_KEY=your-api-key-here
CORRELATION_ID=test
TIMEOUT=30
MAX_RESPONSE_TIME=5000
```

### 3. Run the Application

```bash
py app.py
```

The application will start at: **http://localhost:5000**

## 📁 Project Structure

```
HTTPie-Python-Web/
├── app.py                      # Main Flask application
├── config.env                  # API configuration
├── requirements.txt            # Python dependencies
├── core/                       # Core modules
│   ├── __init__.py
│   ├── config_manager.py       # Configuration management
│   ├── data_parser.py          # Test data parsing (CSV/JSON)
│   ├── test_executor.py        # Test execution engine
│   └── report_generator.py     # HTML report generation
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Dashboard
│   ├── configure.html         # Configuration page
│   ├── test_runner.html       # Test execution page
│   └── results.html           # Results viewing page
├── static/                     # Static files
│   ├── css/
│   │   └── main.css           # Custom styles
│   └── js/
│       └── main.js            # JavaScript utilities
├── Test_Data/                  # Test data files (CSV/JSON)
├── test-results/              # Test results and reports
└── uploads/                   # Uploaded test files
```

## 🎯 Usage Guide

### Dashboard

The dashboard provides an overview of:
- Available test files
- API configuration status
- Recent test runs
- Quick access to all features

### Configure API

1. Navigate to **Configure** page
2. Enter your API details:
   - API Base URL
   - API Endpoint
   - API Key
   - Correlation ID
   - Timeout settings
3. Click **Save Configuration**

### Run Tests

1. Navigate to **Run Tests** page
2. Select a test file from the dropdown
3. Choose language (EN-US, FR-CA, or ES-MX)
4. Click **Start Tests**
5. Monitor real-time progress
6. View results and download report when complete

### View Results

1. Navigate to **Results** page
2. Browse all test runs
3. Click **View Report** to see detailed results
4. Use search to filter results

## 📝 Test Data Format

### CSV Format (Dynamic)

```csv
test_name,method,base_url,endpoint,body,headers,expected_status,description
Test 1,POST,http://api.example.com,/endpoint,{"key":"value"},Content-Type:application/json,200,Sample test
```

### CSV Format (Legacy)

```csv
testDescription,customerNumber,invoiceNumber,orderNumber,shipTo
Test Invoice,1234567,40756307,C746966,01
```

### JSON Format

```json
[
  {
    "test_name": "Test 1",
    "method": "POST",
    "base_url": "http://api.example.com",
    "endpoint": "/endpoint",
    "body": {"key": "value"},
    "headers": "Content-Type:application/json",
    "expected_status": "200"
  }
]
```

## 🔧 Advanced Configuration

### Environment Variables

All configuration can be set in `config.env`:

- `API_BASE_URL` - Base URL of your API
- `API_ENDPOINT` - Specific endpoint to test
- `API_KEY` - Authentication key
- `CORRELATION_ID` - Request tracking ID
- `TIMEOUT` - Request timeout in seconds
- `MAX_RESPONSE_TIME` - Maximum acceptable response time in milliseconds

### Custom Port

To run on a different port, modify `app.py`:

```python
socketio.run(app, debug=True, host='0.0.0.0', port=8080)
```

## 📊 Reports

Test reports include:
- Summary statistics (total, passed, failed, pass rate)
- Detailed test results table
- Response times and sizes
- Status codes (actual vs expected)
- Timestamps for each test

Reports are saved in: `test-results/YYYY-MM-DD/run_HH-MM-SS/`

## 🛠️ Troubleshooting

### Port Already in Use

```bash
# Change port in app.py or kill the process using port 5000
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### Module Not Found

```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Configuration Not Loading

- Check `config.env` file exists in project root
- Verify file format (KEY=VALUE, no quotes)
- Restart the application after changes

## 📄 License

This project is part of the HTTPie-Python testing framework.

## 🤝 Support

For issues or questions, please contact the development team.

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-01
