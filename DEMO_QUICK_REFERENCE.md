# Demo Video - Quick Reference Card

## 🎬 **Recording Checklist**

### **Before Recording:**
- [ ] Application is running (http://localhost:5000)
- [ ] Browser is open and ready
- [ ] Screen recording software is set up
- [ ] Microphone is tested
- [ ] Close unnecessary applications/tabs
- [ ] Set browser zoom to 100%
- [ ] Clear browser notifications
- [ ] Prepare user story text (copy to clipboard)
- [ ] Review script once

---

## 📋 **Demo Flow (12-15 minutes)**

### **1. Introduction (1-2 min)**
- Introduce yourself and the framework
- Mention key features
- Show dashboard

### **2. Configuration (2 min)**
- Show configuration page
- Explain settings (don't fill them out, just show)
- Mention AI integration

### **3. Scenario Generation (3-4 min)** ⭐ **MAIN FEATURE**
- Navigate to Scenario Generator
- Explain LLM toggle
- Paste user story
- Click Generate
- Show generated scenarios
- Highlight different test categories
- Download CSV

### **4. Test Execution (3-4 min)**
- Navigate to Test Runner
- Select CSV file
- Start tests
- Show real-time progress
- Explain pass/fail results
- View summary

### **5. Reports (2-3 min)**
- Open HTML report
- Show summary section
- Show detailed results
- Explain how to use reports

### **6. Conclusion (1 min)**
- Summarize benefits
- Call to action
- Thank viewers

---

## 💬 **Key Talking Points**

### **Opening Hook:**
> "This framework saves QA teams hours by automatically generating comprehensive API test scenarios using AI."

### **Main Value Propositions:**
1. **Speed**: "Generate 15+ test scenarios in 10 seconds"
2. **Coverage**: "AI creates tests you might not think of"
3. **Accuracy**: "Automated execution eliminates human error"
4. **Professional**: "Comprehensive HTML reports for stakeholders"

### **Technical Highlights:**
- "Powered by Azure OpenAI / GPT-4"
- "Supports multiple authentication methods"
- "Real-time test execution with WebSocket updates"
- "CSV and JSON export formats"

---

## 📝 **User Story to Use (Copy This)**

```
API URL: http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction/PDFViewer
API Key: 0c4b24cf-0211-4dcb-8f2f-280ab556ca78

Create a POST endpoint that accepts the following fields:
- environment (string, required)
- customerNumber (string, required)
- shipTo (string, required)
- invoiceNumber (string, required)
- orderNumber (string, required)
- languageCheck (string, required)

Returns 200 on success, 400 for validation errors, 500 for server errors.
```

---

## 🎯 **What to Emphasize**

### **During Scenario Generation:**
✅ "Notice how the AI automatically understood the URL structure"
✅ "It created 15 different test scenarios covering all aspects"
✅ "Functional, validation, security, and edge cases - all automated"
✅ "This would take hours to create manually"

### **During Test Execution:**
✅ "Real-time progress tracking"
✅ "Each test is making actual HTTP requests"
✅ "Pass and fail results are expected - we're testing error handling too"
✅ "All results are logged for debugging"

### **During Report Review:**
✅ "Professional HTML report ready to share"
✅ "Color-coded for easy reading"
✅ "All request and response details included"
✅ "Perfect for documentation and compliance"

---

## ⚠️ **Common Mistakes to Avoid**

❌ Don't rush through the scenario generation - it's the star feature!
❌ Don't skip explaining why some tests fail (validation tests)
❌ Don't forget to mention AI/LLM integration
❌ Don't use technical jargon without explanation
❌ Don't go too fast - pause to let viewers absorb information

---

## 🎤 **Voice & Tone Tips**

✅ **Enthusiastic but professional**
✅ **Clear and confident**
✅ **Pause after important points**
✅ **Smile while talking (it shows in your voice!)**
✅ **Use "we" and "let's" to engage viewers**

### **Example Phrases:**
- "Let me show you..."
- "Notice how..."
- "This is really powerful because..."
- "In just a few seconds..."
- "The AI automatically..."

---

## 🎬 **Recording Tips**

### **Video Quality:**
- Record in 1080p (1920x1080)
- Use full screen browser (F11)
- Hide bookmarks bar
- Close unnecessary tabs

### **Audio Quality:**
- Use a good microphone
- Record in a quiet room
- Speak clearly and at moderate pace
- Leave 2 seconds of silence at start/end for editing

### **Screen Recording:**
- Use OBS Studio, Camtasia, or similar
- Record at 30 FPS minimum
- Highlight mouse cursor
- Use zoom/highlight for important areas

---

## ⏱️ **Timing Guide**

| Section | Duration | Key Action |
|---------|----------|------------|
| Intro | 1-2 min | Show dashboard, explain features |
| Config | 2 min | Show settings page |
| **Scenario Gen** | **3-4 min** | **Generate scenarios (MAIN)** |
| Test Execution | 3-4 min | Run tests, show progress |
| Reports | 2-3 min | Show HTML report |
| Conclusion | 1 min | Summarize, call to action |

**Total: 12-15 minutes**

---

## 📊 **Expected Results to Show**

### **Scenario Generation:**
- **~15 scenarios** generated
- **5 categories**: Functional, Validation, Business Logic, Edge Case, Security
- **3 priorities**: P0, P1, P2
- **Correct base_url**: `http://aazeus-fnprwb01.ashleyfurniture.com/WebAPI/InvoiceExtraction`
- **Correct endpoint**: `/PDFViewer`

### **Test Execution:**
- **Total**: 15 tests
- **Passed**: ~8 tests
- **Failed**: ~7 tests (expected - validation tests)
- **Pass Rate**: ~50-60%

---

## 🎯 **Call to Action (End of Video)**

> "If you found this helpful, please:
> - ⭐ Star the repository on GitHub
> - 📝 Try it with your own APIs
> - 💬 Share your feedback
> - 🔔 Subscribe for more testing tutorials
>
> Thank you for watching, and happy testing!"

---

## 🚀 **Bonus: Alternative Demo Scenarios**

If you want to record multiple versions or show variety:

### **Scenario 2: User Registration API**
```
Create a POST endpoint for user registration with email, password, and username.
Email must be valid format.
Password must be at least 8 characters.
Username must be unique.
Returns 201 on success, 400 for validation errors.
```

### **Scenario 3: E-commerce Product API**
```
Create a GET endpoint to retrieve product details.
Accepts productId as parameter.
Returns 200 with product data on success.
Returns 404 if product not found.
```

---

## ✅ **Final Checklist Before Publishing**

- [ ] Video is clear and smooth
- [ ] Audio is clear (no background noise)
- [ ] All features demonstrated work correctly
- [ ] Timing is appropriate (not too fast/slow)
- [ ] Added intro/outro screens
- [ ] Added captions/subtitles (optional but recommended)
- [ ] Exported in high quality (1080p, H.264)
- [ ] Tested video playback
- [ ] Prepared video description and tags

---

**Good luck with your recording! 🎬**

