# Phase 3 - Azure OpenAI Setup Guide

## 🎯 Current Status

✅ **Phase 3 Implementation:** Complete  
✅ **Azure OpenAI Detection:** Working  
✅ **Azure Endpoint Configuration:** Set  
❌ **Deployment Name:** Needs to be configured

---

## 🔧 What You Need to Do

### Step 1: Find Your Deployment Name

1. Go to **Azure Portal** (https://portal.azure.com)
2. Navigate to your **Azure OpenAI resource** (`payroll-open-ai`)
3. Click on **"Model deployments"** or **"Deployments"**
4. Look for the deployment name (examples: `gpt-4`, `gpt-35-turbo`, `my-deployment`, etc.)

### Step 2: Update config.env

Open `config.env` and update line 26:

```env
OPENAI_MODEL=your-deployment-name-here
```

Replace `gpt-4o-mini` with your actual deployment name from Azure Portal.

---

## 📋 Current Configuration

```env
AZURE_OPENAI_ENDPOINT=https://payroll-open-ai.cognitiveservices.azure.com
AZURE_OPENAI_API_VERSION=2024-02-15-preview
OPENAI_API_KEY=DIYGp4ugd1hjaHzfLetC... (84 characters)
OPENAI_MODEL=gpt-4o-mini  ← CHANGE THIS TO YOUR DEPLOYMENT NAME
```

---

## 🧪 Testing After Configuration

Once you update the deployment name, run:

```bash
py test_phase3.py
```

You should see:
- ✅ LLM Available: True
- ✅ LLM Generated X scenarios (instead of "Rule-based generation")
- ✅ Different number of scenarios between LLM ON and LLM OFF

---

## 🎉 What Phase 3 Will Do

When properly configured, Phase 3 will:

1. **Generate unique, context-aware test scenarios** using AI
2. **Create 10-15+ comprehensive test cases** (vs 9 rule-based)
3. **Include detailed test data and assertions**
4. **Adapt to your specific requirements** instead of using templates

---

## 🆘 Common Deployment Names

- `gpt-4`
- `gpt-4-turbo`
- `gpt-35-turbo`
- `gpt-4o`
- `gpt-4o-mini`
- Custom names you created

---

## 📞 Need Help?

If you're unsure about the deployment name, you can:
1. Check Azure Portal → OpenAI Resource → Model deployments
2. Run: `az cognitiveservices account deployment list --name payroll-open-ai --resource-group <your-rg>`
3. Contact your Azure administrator

---

**Once configured, Phase 3 will make LLM ON/OFF produce significantly different test scenarios!**

