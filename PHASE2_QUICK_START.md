# 🚀 Phase 2: Quick Start Guide

## Get AI-Powered Scenario Generation in 5 Minutes!

---

## ⚡ Quick Setup

### **1. Install Dependencies** (30 seconds)

```bash
pip install openai anthropic
```

Or use the full requirements:
```bash
pip install -r requirements.txt
```

---

### **2. Get an API Key** (2 minutes)

#### **Option A: OpenAI (Recommended for beginners)**

1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

#### **Option B: Anthropic Claude**

1. Go to: https://console.anthropic.com/
2. Sign up or log in
3. Create an API key
4. Copy the key (starts with `sk-ant-...`)

---

### **3. Configure** (1 minute)

Edit `config.env` and add these lines:

**For OpenAI:**
```env
LLM_ENABLED=true
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

**For Anthropic:**
```env
LLM_ENABLED=true
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

---

### **4. Run** (30 seconds)

```bash
python app.py
```

---

### **5. Test** (1 minute)

1. Open: http://localhost:5000
2. Go to: **Scenario Generator**
3. Look for: **"Use AI-Powered Parsing"** toggle
4. Status should show: **"Available"** (green badge)
5. Try generating scenarios!

---

## ✅ Verification

### **Check LLM Status**

You should see:
- ✅ Green badge: "Available"
- ✅ Text: "AI parsing enabled using OPENAI" (or ANTHROPIC)
- ✅ Toggle switch is enabled
- ✅ Cost tracker shows: "$0.0000"

### **If You See Issues:**

| Issue | Solution |
|-------|----------|
| "Disabled" (gray badge) | Set `LLM_ENABLED=true` in config.env |
| "Not Configured" (yellow) | Add valid API key to config.env |
| Toggle is disabled | Check API key is valid |
| No cost display | LLM not configured properly |

---

## 🎯 First Test

Try this requirement:

```
As a user, I want to register an account with my email and password.

The system should:
- Validate email format
- Ensure password is at least 8 characters
- Check if email already exists
- Return 201 on success
- Return 400 for validation errors

API: POST /api/users
Base URL: https://api.example.com
```

**With LLM enabled**, you'll get:
- ✅ Better field detection
- ✅ More validation rules
- ✅ Smarter test scenarios
- ✅ Implicit requirements extracted

---

## 💰 Cost Expectations

### **First 10 Generations**
- **OpenAI GPT-3.5**: ~$0.02 total
- **OpenAI GPT-4**: ~$0.13 total
- **Claude Sonnet**: ~$0.04 total
- **Claude Opus**: ~$0.20 total

### **Recommendation**
Start with **GPT-3.5** or **Claude Sonnet** for best cost/performance ratio.

---

## 🔄 Switching Between Modes

### **Use LLM (AI-Powered)**
- ✅ Toggle ON
- Best for: Complex requirements
- Speed: 2-5 seconds
- Cost: ~$0.002-0.02 per generation

### **Use Rule-Based (Phase 1)**
- ❌ Toggle OFF
- Best for: Simple requirements
- Speed: Instant
- Cost: Free

---

## 🛠️ Troubleshooting

### **"Module not found: openai"**
```bash
pip install openai
```

### **"Module not found: anthropic"**
```bash
pip install anthropic
```

### **"Invalid API key"**
- Check key is copied correctly
- No extra spaces
- Starts with `sk-` (OpenAI) or `sk-ant-` (Anthropic)

### **"LLM not available"**
- Restart the application after config changes
- Check `LLM_ENABLED=true`
- Verify API key is valid

---

## 📚 Learn More

- **Full Guide**: See `PHASE2_LLM_GUIDE.md`
- **Implementation Details**: See `PHASE2_IMPLEMENTATION_SUMMARY.md`
- **User Guide**: See `SCENARIO_GENERATOR_GUIDE.md`

---

## 🎉 You're Ready!

Phase 2 is now active! You can:
- ✅ Generate smarter test scenarios
- ✅ Handle complex requirements
- ✅ Toggle between AI and rule-based
- ✅ Track costs in real-time

**Happy Testing!** 🚀

