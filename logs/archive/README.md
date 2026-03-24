# Log Archive Directory

This directory contains rotated log files.

## Naming Convention

Archived logs follow this pattern:
```
<log_name>.log.<date>
```

Examples:
- `app.log.2026-03-22`
- `test_execution.log.2026-03-21`
- `llm_service.log.2026-03-20`

## Retention Policy

| Log File | Retention Period |
|----------|------------------|
| app.log | 30 days |
| test_execution.log | 60 days |
| scenario_generation.log | 30 days |
| llm_service.log | 90 days |
| llm_cost_tracking.log | 1 year |
| api_requests.log | 14 days |
| api_responses.log | 7 days |
| error.log | 90 days |
| security.log | 1 year |
| audit.log | 1 year |
| performance.log | 30 days |

## Automatic Cleanup

Archived logs older than their retention period should be automatically deleted.

## Manual Cleanup

To manually clean up old archives:

```bash
# Windows PowerShell
Get-ChildItem -Path logs\archive -Recurse | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item

# Linux/Mac
find logs/archive -type f -mtime +30 -delete
```

## Compression

For long-term storage, consider compressing old archives:

```bash
# Windows (using 7-Zip or similar)
7z a logs\archive\archive-2026-03.zip logs\archive\*.2026-03-*

# Linux/Mac
tar -czf logs/archive/archive-2026-03.tar.gz logs/archive/*.2026-03-*
```

