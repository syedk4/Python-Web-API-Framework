# 📝 Logs Directory

This directory contains all application log files for the Python-Web-API-Framework.

## 📁 Log Files

| File | Purpose | Retention |
|------|---------|-----------|
| `app.log` | Main application events | 30 days |
| `test_execution.log` | Test runner activity | 60 days |
| `scenario_generation.log` | Scenario generator operations | 30 days |
| `llm_service.log` | LLM API calls (Phase 2) | 90 days |
| `llm_cost_tracking.log` | LLM cost audit (CSV) | 1 year |
| `api_requests.log` | Outgoing API calls | 14 days |
| `api_responses.log` | API response details | 7 days |
| `data_parser.log` | CSV/JSON parsing | 30 days |
| `file_operations.log` | File I/O operations | 30 days |
| `report_generation.log` | Report creation | 30 days |
| `security.log` | Security events | 1 year |
| `audit.log` | Compliance audit trail | 1 year |
| `performance.log` | Performance metrics | 30 days |
| `error.log` | Consolidated errors | 90 days |

## 🎯 Quick Reference

### **Debugging Test Failures**
```
1. test_execution.log → Test results
2. api_requests.log → Request details
3. api_responses.log → Response details
4. error.log → Any errors
```

### **Monitoring LLM Costs**
```
1. llm_service.log → Real-time costs
2. llm_cost_tracking.log → Detailed CSV breakdown
```

### **Performance Issues**
```
1. performance.log → Slow operations
2. api_requests.log → Slow API calls
3. test_execution.log → Test duration
```

### **Security Audit**
```
1. security.log → Security events
2. audit.log → Compliance trail
3. error.log → Critical errors
```

## 🔍 Common Commands

### View Recent Errors
```powershell
# Windows
Get-Content error.log -Tail 50

# Linux/Mac
tail -n 50 error.log
```

### Search Logs
```powershell
# Windows
Select-String -Path app.log -Pattern "ERROR"

# Linux/Mac
grep "ERROR" app.log
```

### Monitor Real-Time
```powershell
# Windows
Get-Content app.log -Wait -Tail 10

# Linux/Mac
tail -f app.log
```

### Analyze LLM Costs
```powershell
# Import CSV
Import-Csv llm_cost_tracking.log | Measure-Object -Property cost -Sum
```

## 📦 Archive

Old logs are automatically rotated to `archive/` directory.

See `archive/README.md` for retention policies and cleanup instructions.

## 📚 Full Documentation

For complete logging documentation, see: `../LOGGING_GUIDE.md`

## 🔒 Security Note

**Never commit log files to version control!**

Log files are excluded in `.gitignore` to prevent:
- Exposing sensitive data
- Bloating repository size
- Security vulnerabilities

## ⚠️ Important

- Log files may contain sensitive information
- Regularly review and clean old logs
- Monitor disk space usage
- Protect log files with appropriate permissions

---

**Created:** 2026-03-23  
**Status:** ✅ Ready for use

