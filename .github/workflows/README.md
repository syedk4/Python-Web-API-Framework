# GitHub Actions Workflows

This directory contains automated workflows for the Python Web API Testing Framework.

## 📋 Available Workflows

### 1. **CI/CD Pipeline** (`ci.yml`)

**Triggers:**
- Push to `main`, `feature/testing`, or `develop` branches
- Pull requests to `main` or `develop`
- Manual trigger via GitHub UI

**Jobs:**
- ✅ **Unit Tests** - Runs on Python 3.9, 3.10, 3.11, 3.12
- ✅ **Code Quality** - Flake8 and Pylint checks
- ✅ **Security Scan** - Safety and Bandit security analysis
- ✅ **Build Check** - Verifies application can start

**Artifacts:**
- Test results (7-day retention)
- Security reports (7-day retention)

---

### 2. **Scheduled API Tests** (`scheduled-tests.yml`)

**Triggers:**
- Daily at 2 AM UTC (configurable via cron)
- Manual trigger via GitHub UI

**Jobs:**
- ✅ **API Integration Tests** - Runs real API test cases
- ✅ **Report Generation** - Creates test execution reports

**Artifacts:**
- API test results (30-day retention)
- Test logs (30-day retention)

---

## 🚀 Setup Instructions

### **Step 1: Configure Secrets**

Add the following secrets to your GitHub repository:

1. Go to: **Settings** → **Secrets and variables** → **Actions**
2. Click: **New repository secret**
3. Add these secrets:

| Secret Name | Description | Required |
|------------|-------------|----------|
| `API_BASE_URL` | Base URL for your API | Optional |
| `API_ENDPOINT` | API endpoint path | Optional |
| `API_KEY` | API authentication key | Optional |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI key (for LLM features) | Optional |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | Optional |

---

### **Step 2: Enable Workflows**

1. Go to: **Actions** tab in your repository
2. If workflows are disabled, click **"I understand my workflows, go ahead and enable them"**
3. Workflows will start running automatically on configured triggers

---

### **Step 3: Manual Trigger**

To manually run a workflow:

1. Go to: **Actions** tab
2. Select the workflow (e.g., "CI/CD Pipeline")
3. Click: **"Run workflow"** button
4. Select branch and click **"Run workflow"**

---

## 📊 Viewing Results

### **Workflow Status**

- Green ✅ = All jobs passed
- Red ❌ = One or more jobs failed
- Yellow 🟡 = Jobs in progress

### **Job Logs**

1. Click on a workflow run
2. Click on a specific job (e.g., "Run Unit Tests")
3. View detailed logs for each step

### **Artifacts**

1. Click on a workflow run
2. Scroll to bottom → **Artifacts** section
3. Download artifacts (test results, reports, etc.)

---

## 🛠️ Customization

### **Change Schedule**

Edit `.github/workflows/scheduled-tests.yml`:

```yaml
on:
  schedule:
    # Run daily at 2 AM UTC
    - cron: '0 2 * * *'
```

**Cron format:** `minute hour day month weekday`

**Examples:**
- `0 */6 * * *` - Every 6 hours
- `0 0 * * 1` - Every Monday at midnight
- `0 9 * * 1-5` - Weekdays at 9 AM

### **Add More Python Versions**

Edit `.github/workflows/ci.yml`:

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11', '3.12', '3.13']
```

---

## 🔍 Troubleshooting

### **Workflow Not Running**

- Check if workflows are enabled in repository settings
- Verify branch names match workflow triggers
- Check if repository has GitHub Actions enabled

### **Tests Failing**

- Review job logs for error messages
- Check if all required files are committed
- Verify dependencies in `requirements.txt`

### **Secrets Not Working**

- Ensure secret names match exactly (case-sensitive)
- Secrets are only available in workflows, not pull requests from forks
- Re-add secrets if they were changed

---

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Python Setup Action](https://github.com/actions/setup-python)

