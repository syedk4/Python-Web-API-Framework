# 🤖 Phase 2: LLM Integration Guide

## Overview

**Phase 2** adds AI-powered requirement parsing and scenario generation using Large Language Models (LLMs). This enhances the rule-based approach from Phase 1 with intelligent natural language understanding.

## ✨ New Features

### **Hybrid Approach**
- **LLM First**: Attempts AI-powered parsing when enabled
- **Rule-Based Fallback**: Automatically falls back to regex/keyword matching if LLM unavailable
- **Best of Both**: Merges LLM results with rule-based extraction for comprehensive coverage

### **Supported LLM Providers**
- ✅ **OpenAI** (GPT-4, GPT-3.5)
- ✅ **Anthropic** (Claude 3 Sonnet, Claude 3 Opus)

### **Cost Control**
- Token usage tracking
- Cost estimation per request
- Configurable cost limits
- Real-time cost display in UI

## 🚀 Setup Instructions

### **Step 1: Install Dependencies**

```bash
pip install -r requirements.txt
```

This installs:
- `openai==1.12.0` - OpenAI API client
- `anthropic==0.18.1` - Anthropic API client

### **Step 2: Configure LLM Settings**

Edit your `config.env` file and add:

```env
# Enable LLM features
LLM_ENABLED=true

# Choose provider: openai or anthropic
LLM_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_MAX_TOKENS=2000

# OR Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
ANTHROPIC_MAX_TOKENS=2000

# LLM Settings
LLM_TEMPERATURE=0.3
LLM_MAX_COST_PER_REQUEST=0.10
```

### **Step 3: Get API Keys**

#### **Option 1: OpenAI**
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy and paste into `OPENAI_API_KEY`

#### **Option 2: Anthropic**
1. Go to https://console.anthropic.com/
2. Create an API key
3. Copy and paste into `ANTHROPIC_API_KEY`

### **Step 4: Restart Application**

```bash
python app.py
```

## 📊 How It Works

### **Parsing Flow**

```
User Requirements
       ↓
   LLM Enabled?
       ↓
    YES → Try LLM Parsing
       ↓
   Success? → Merge with Rule-Based
       ↓
    NO → Use Rule-Based Only
       ↓
   Final Parsed Result
```

### **Example: LLM vs Rule-Based**

**Input:**
```
As a user, I want to create an account with my email and a secure password.
The system should validate the email format and ensure the password is strong.
```

**Rule-Based Output:**
- Entity: user
- Operations: [create]
- Fields: [email, password]
- Validations: [email format]

**LLM-Enhanced Output:**
- Entity: user account
- Operations: [create, validate]
- Fields: [
    {name: "email", type: "email", required: true},
    {name: "password", type: "password", required: true, validation: "strong"}
  ]
- Validations: [
    {field: "email", rule: "format", pattern: "email"},
    {field: "password", rule: "strength", requirements: ["uppercase", "lowercase", "number", "special"]}
  ]

## 💰 Cost Estimation

### **Approximate Pricing (as of 2024)**

| Provider | Model | Cost per 1K tokens |
|----------|-------|-------------------|
| OpenAI | GPT-4 Turbo | $0.01 |
| OpenAI | GPT-3.5 Turbo | $0.0015 |
| Anthropic | Claude 3 Opus | $0.015 |
| Anthropic | Claude 3 Sonnet | $0.003 |

### **Typical Usage**
- Average requirement: ~500 tokens
- Average response: ~800 tokens
- **Total per generation**: ~1,300 tokens
- **Cost per generation**: $0.01 - $0.02 (depending on model)

## 🎛️ Configuration Options

### **LLM_ENABLED**
- `true`: Enable LLM features
- `false`: Use only rule-based parsing (Phase 1)

### **LLM_PROVIDER**
- `openai`: Use OpenAI GPT models
- `anthropic`: Use Anthropic Claude models

### **LLM_TEMPERATURE**
- Range: 0.0 - 1.0
- Lower = more deterministic
- Higher = more creative
- **Recommended**: 0.3 for API testing (consistency is important)

### **LLM_MAX_COST_PER_REQUEST**
- Safety limit in USD
- Prevents runaway costs
- **Recommended**: $0.10

## 🔧 Troubleshooting

### **"LLM Not Available" Message**

**Possible causes:**
1. `LLM_ENABLED=false` in config
2. API key not configured
3. Invalid API key
4. Network connectivity issues

**Solution:**
- Check `config.env` settings
- Verify API key is valid
- Test API key with provider's dashboard

### **High Costs**

**Solutions:**
- Use GPT-3.5 instead of GPT-4
- Use Claude Sonnet instead of Opus
- Reduce `MAX_TOKENS` setting
- Lower `MAX_COST_PER_REQUEST` limit

### **Slow Response**

**Solutions:**
- LLM calls take 2-5 seconds (normal)
- Use rule-based mode for faster results
- Consider caching common requirements (future enhancement)

## 📈 Benefits of Phase 2

### **Better Understanding**
- Handles complex, nuanced requirements
- Understands context and intent
- Extracts implicit information

### **More Accurate**
- Better field type detection
- More comprehensive validation rules
- Smarter business rule extraction

### **Flexible Input**
- Works with various writing styles
- Handles incomplete requirements
- Adapts to different formats

## 🔄 Fallback Behavior

**LLM will automatically fallback to rule-based if:**
- API key is invalid
- Network error occurs
- LLM response is malformed
- Cost limit is exceeded
- Provider is unavailable

**You'll always get results** - either from LLM or rule-based parsing!

## 🎯 Best Practices

1. **Start with Rule-Based**: Test without LLM first
2. **Enable LLM Gradually**: Try on complex requirements
3. **Monitor Costs**: Check usage regularly
4. **Use Appropriate Model**: GPT-3.5 for simple, GPT-4 for complex
5. **Set Cost Limits**: Protect against unexpected charges

## 📝 Next Steps

- ✅ Phase 1: Rule-based parsing (Complete)
- ✅ Phase 2: LLM integration (Complete)
- 🔜 Phase 3: Scenario enhancement with LLM
- 🔜 Phase 4: Test data generation with LLM
- 🔜 Phase 5: Intelligent test execution suggestions

