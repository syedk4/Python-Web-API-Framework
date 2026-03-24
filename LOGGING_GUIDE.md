# 📝 Logging System Guide

## Overview

The Python-Web-API-Framework includes a comprehensive logging system to track application behavior, debug issues, monitor performance, and maintain audit trails.

---

## 📁 Log Files Structure

```
logs/
├── app.log                    # Main application events
├── test_execution.log         # Test runner activity
├── scenario_generation.log    # Scenario generator operations
├── llm_service.log           # LLM API calls (Phase 2)
├── llm_cost_tracking.log     # LLM cost audit trail (CSV format)
├── api_requests.log          # Outgoing API calls
├── api_responses.log         # API response details
├── data_parser.log           # CSV/JSON parsing
├── file_operations.log       # File I/O operations
├── report_generation.log     # Report creation
├── security.log              # Security events
├── audit.log                 # Compliance audit trail
├── performance.log           # Performance metrics
├── error.log                 # Consolidated errors
└── archive/                  # Rotated log files
    └── README.md
```

---

## 📊 Log Files Reference

### **1. app.log** - Main Application Log

**Purpose:** General application events, startup, shutdown, errors

**What is logged:**
- ✅ Application startup/shutdown
- ✅ Configuration loading
- ✅ Route access (API endpoints)
- ✅ Unhandled exceptions
- ✅ Flask server events
- ✅ SocketIO connections/disconnections

**Rotation:** Daily or 10MB  
**Retention:** 30 days  
**Log Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL

---

### **2. test_execution.log** - Test Runner Activity

**Purpose:** Track all test executions and results

**What is logged:**
- ✅ Test suite started/completed
- ✅ Individual test execution (pass/fail)
- ✅ Test data file loaded
- ✅ API requests made during tests
- ✅ Response times
- ✅ Assertion failures
- ✅ Test execution errors

**Rotation:** Daily or 20MB  
**Retention:** 60 days  
**Log Levels:** INFO, WARNING, ERROR

---

### **3. scenario_generation.log** - Scenario Generator

**Purpose:** Track scenario generation process

**What is logged:**
- ✅ Requirements parsing attempts
- ✅ Rule-based parsing results
- ✅ LLM parsing attempts (Phase 2)
- ✅ Scenario generation success/failure
- ✅ Number of scenarios generated
- ✅ File save operations
- ✅ Parsing errors or warnings

**Rotation:** Daily or 5MB  
**Retention:** 30 days  
**Log Levels:** DEBUG, INFO, WARNING, ERROR

---

### **4. llm_service.log** - LLM API Calls (Phase 2)

**Purpose:** Track all LLM interactions and costs

**What is logged:**
- ✅ LLM service initialization
- ✅ Provider selection (OpenAI/Anthropic)
- ✅ API key validation status
- ✅ Each LLM API call (timestamp, provider, model)
- ✅ Token usage (input/output tokens)
- ✅ Cost per request
- ✅ Cumulative cost tracking
- ✅ API errors/rate limits
- ✅ Fallback to rule-based parsing
- ✅ Response parsing errors

**Rotation:** Daily or 10MB  
**Retention:** 90 days (for billing audit)  
**Log Levels:** DEBUG, INFO, WARNING, ERROR

**Example entries:**
```
2024-03-23 10:15:23 INFO - LLM Service initialized: provider=openai, model=gpt-3.5-turbo
2024-03-23 10:15:45 INFO - LLM API call: tokens=1250, cost=$0.0019, duration=2.3s
2024-03-23 10:16:12 WARNING - LLM API error: Rate limit exceeded, falling back to rule-based
2024-03-23 10:17:00 INFO - Total LLM cost today: $0.0456
```

---

### **5. llm_cost_tracking.log** - Cost Audit Trail (Phase 2)

**Purpose:** Dedicated cost tracking for billing/auditing

**Format:** CSV for easy analysis

**What is logged:**
- ✅ Daily cost summaries
- ✅ Per-request cost breakdown
- ✅ Token usage statistics
- ✅ Cost limit warnings
- ✅ Provider comparison metrics

**Rotation:** Monthly  
**Retention:** 1 year (audit requirement)  
**Log Levels:** INFO, WARNING

**CSV Format:**
```csv
timestamp,provider,model,input_tokens,output_tokens,total_tokens,cost,request_type,duration_seconds
2024-03-23 10:15:45,openai,gpt-3.5-turbo,450,800,1250,0.0019,parse_requirements,2.3
```

---

### **6. api_requests.log** - Outgoing API Calls

**Purpose:** Track all API calls made during testing

**What is logged:**
- ✅ Request URL, method, headers
- ✅ Request body (sanitized - no sensitive data)
- ✅ Response status code
- ✅ Response time
- ✅ Response size
- ✅ Connection errors
- ✅ Timeout errors
- ✅ SSL/TLS errors

**Rotation:** Daily or 50MB  
**Retention:** 14 days  
**Log Levels:** DEBUG, INFO, WARNING, ERROR

---

### **7. api_responses.log** - API Response Details

**Purpose:** Detailed response logging for debugging

**What is logged:**
- ✅ Response headers
- ✅ Response body (truncated if large)
- ✅ Validation results
- ✅ Assertion outcomes

**Rotation:** Daily or 50MB
**Retention:** 7 days
**Log Levels:** DEBUG, INFO

---

### **8. data_parser.log** - Data Parsing

**Purpose:** Track CSV/JSON parsing operations

**What is logged:**
- ✅ File loading attempts
- ✅ Parsing errors (malformed CSV/JSON)
- ✅ Data validation issues
- ✅ Number of records parsed
- ✅ Schema validation results

**Rotation:** Daily or 5MB
**Retention:** 30 days
**Log Levels:** DEBUG, INFO, WARNING, ERROR

---

### **9. file_operations.log** - File I/O

**Purpose:** Track all file read/write operations

**What is logged:**
- ✅ File uploads
- ✅ Test data file saves
- ✅ Report generation
- ✅ Configuration file reads
- ✅ File permission errors
- ✅ Disk space warnings

**Rotation:** Daily or 5MB
**Retention:** 30 days
**Log Levels:** INFO, WARNING, ERROR

---

### **10. report_generation.log** - Report Creation

**Purpose:** Track report generation process

**What is logged:**
- ✅ Report generation started/completed
- ✅ Report type (HTML/PDF/JSON)
- ✅ Data aggregation steps
- ✅ Chart/graph generation
- ✅ File save location
- ✅ Generation errors

**Rotation:** Daily or 5MB
**Retention:** 30 days
**Log Levels:** INFO, WARNING, ERROR

---

### **11. security.log** - Security Events

**Purpose:** Track security-related events

**What is logged:**
- ✅ API key validation attempts
- ✅ Configuration changes
- ✅ Unauthorized access attempts
- ✅ File upload validation
- ✅ Input sanitization warnings
- ✅ CORS violations

**Rotation:** Weekly
**Retention:** 1 year
**Log Levels:** WARNING, ERROR, CRITICAL

**⚠️ SECURITY NOTE:** Never log actual API keys, passwords, or tokens. Only log validation status and masked identifiers.

---

### **12. audit.log** - Audit Trail

**Purpose:** Compliance and tracking

**What is logged:**
- ✅ User actions (if multi-user in future)
- ✅ Configuration changes
- ✅ Test data modifications
- ✅ Report access
- ✅ LLM API usage (for billing)

**Rotation:** Monthly
**Retention:** 1 year
**Log Levels:** INFO

---

### **13. performance.log** - Performance Metrics

**Purpose:** Track application performance

**What is logged:**
- ✅ Request processing times
- ✅ Database query times (if applicable)
- ✅ Memory usage warnings
- ✅ Slow API responses (>5s)
- ✅ Resource bottlenecks

**Rotation:** Daily or 10MB
**Retention:** 30 days
**Log Levels:** INFO, WARNING

---

### **14. error.log** - Consolidated Errors

**Purpose:** All errors in one place for quick debugging

**What is logged:**
- ✅ All ERROR and CRITICAL level messages from all modules
- ✅ Stack traces
- ✅ Exception details
- ✅ Context information

**Rotation:** Daily or 10MB
**Retention:** 90 days
**Log Levels:** ERROR, CRITICAL

---

## 🎯 Log Levels Explained

| Level | When to Use | Example |
|-------|-------------|---------|
| **DEBUG** | Detailed diagnostic information | "Parsing field: email" |
| **INFO** | General informational messages | "Test suite started" |
| **WARNING** | Warning messages, app continues | "API response slow (3.5s)" |
| **ERROR** | Error occurred, feature failed | "Failed to parse CSV file" |
| **CRITICAL** | Critical error, app may crash | "Database connection lost" |

---

## 📋 Log Rotation Strategy

| Log File | Rotation Trigger | Max Files | Total Size |
|----------|------------------|-----------|------------|
| app.log | Daily or 10MB | 30 | ~300MB |
| test_execution.log | Daily or 20MB | 60 | ~1.2GB |
| scenario_generation.log | Daily or 5MB | 30 | ~150MB |
| llm_service.log | Daily or 10MB | 90 | ~900MB |
| llm_cost_tracking.log | Monthly | 12 | ~60MB |
| api_requests.log | Daily or 50MB | 14 | ~700MB |
| api_responses.log | Daily or 50MB | 7 | ~350MB |
| error.log | Daily or 10MB | 90 | ~900MB |
| security.log | Weekly | 52 | ~260MB |
| audit.log | Monthly | 12 | ~60MB |

---

## 🔍 How to Use Logs

### **Debugging Test Failures**
1. Check `test_execution.log` for test results
2. Check `api_requests.log` for request details
3. Check `api_responses.log` for response details
4. Check `error.log` for any errors

### **Monitoring LLM Costs**
1. Check `llm_service.log` for real-time costs
2. Check `llm_cost_tracking.log` for detailed breakdown
3. Import CSV into Excel/Google Sheets for analysis

### **Investigating Performance Issues**
1. Check `performance.log` for slow operations
2. Check `api_requests.log` for slow API calls
3. Check `test_execution.log` for test duration

### **Security Audit**
1. Check `security.log` for security events
2. Check `audit.log` for compliance trail
3. Check `error.log` for critical errors

---

## 🛠️ Log Analysis Tools

### **View Recent Errors**
```powershell
# Windows PowerShell
Get-Content logs\error.log -Tail 50

# Linux/Mac
tail -n 50 logs/error.log
```

### **Search for Specific Text**
```powershell
# Windows PowerShell
Select-String -Path logs\app.log -Pattern "ERROR"

# Linux/Mac
grep "ERROR" logs/app.log
```

### **Analyze LLM Costs**
```powershell
# Import CSV into Excel or use PowerShell
Import-Csv logs\llm_cost_tracking.log | Measure-Object -Property cost -Sum
```

### **Monitor Real-Time Logs**
```powershell
# Windows PowerShell
Get-Content logs\app.log -Wait -Tail 10

# Linux/Mac
tail -f logs/app.log
```

---

## 🔒 Security Best Practices

### **DO NOT Log:**
- ❌ API keys or passwords
- ❌ Full authentication tokens
- ❌ Sensitive user data (PII)
- ❌ Credit card information
- ❌ Complete request bodies with sensitive data

### **DO Log (Sanitized):**
- ✅ API key status (valid/invalid) - not the key itself
- ✅ Token type (Bearer/API Key) - not the token
- ✅ Masked sensitive fields (email: `u***@example.com`)
- ✅ Request metadata (URL, method, status)

---

## 📦 Archive Management

### **Automatic Archiving**
Logs are automatically rotated to `logs/archive/` when they exceed size or time limits.

### **Manual Archive**
```powershell
# Move old logs to archive
Move-Item logs\*.log.* logs\archive\
```

### **Cleanup Old Archives**
```powershell
# Delete archives older than 90 days
Get-ChildItem logs\archive -Recurse | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-90)} | Remove-Item
```

---

## 📈 Benefits

| Benefit | Description |
|---------|-------------|
| **Debugging** | Quickly identify issues with detailed logs |
| **Cost Control** | Track LLM costs in real-time |
| **Performance** | Monitor slow operations |
| **Security** | Audit trail for security events |
| **Compliance** | Meet audit requirements |
| **Analytics** | Understand usage patterns |
| **Troubleshooting** | Reproduce and fix bugs |

---

## 🚀 Next Steps

To implement logging in your code:

1. **Import logging module** (when implemented)
2. **Get logger instance** for your module
3. **Log events** at appropriate levels
4. **Monitor logs** regularly

**Note:** The logging infrastructure is ready. The next phase will integrate logging into the application code.

---

## 📚 Related Documentation

- `PHASE2_LLM_GUIDE.md` - LLM features and cost tracking
- `SCENARIO_GENERATOR_GUIDE.md` - Scenario generator usage
- `PROJECT_OVERVIEW_DEMO.md` - Project overview

---

**Created:** 2026-03-23
**Version:** 1.0
**Status:** ✅ Log files created and ready for use

