# 📋 Data Comparator - Multi-Format Analysis Tool

A comprehensive tool to compare **JSON, XML, CSV, and YAML** data side-by-side with detailed analysis and formatting. Perfect for API testing, data validation, debugging, and configuration management.

## 🚀 Features

### 🌐 **Web Interface**
- ✅ **Multi-format support**: JSON, XML, CSV, YAML
- ✅ **Live format detection** and parsing
- ✅ **Side-by-side comparison** with detailed analysis
- ✅ **Smart beautify/formatting** for all data types
- ✅ **Copy & Clear functions** for easy data management
- ✅ **Line numbers** with syntax error highlighting
- ✅ **Responsive design** with modern UI
- ✅ **Real-time comparison** with visual indicators

### 🐍 **Python Module**
- ✅ **Command-line interface** for quick comparisons
- ✅ **Programmable API** for automation
- ✅ **Detailed reporting** with statistics
- ✅ **Clean table output** using tabulate
- ✅ **Error handling** with helpful messages

### 📊 **Advanced Comparison**
- ✅ **Deep nested structure** analysis
- ✅ **Array/list element** individual comparison
- ✅ **Multi-row CSV** handling
- ✅ **YAML array** element-by-element analysis
- ✅ **Missing field detection** across formats
- ✅ **Data type normalization** (string vs number matching)

## 🏗️ Installation

1. **Clone or download** this repository
2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### 🌐 Web Interface (Recommended)

1. **Start the web server**:
```bash
python3 -m http.server 8000
```

2. **Open your browser** and go to:
```
http://localhost:8000
```

3. **Paste your data** in the two text areas and click **"Compare Data"**

**Supported formats:**
- **JSON**: `{"user": "Alice", "age": 28}`
- **XML**: `<user><name>Alice</name><age>28</age></user>`
- **YAML**: `user: Alice\nage: 28`
- **CSV**: `name,age\nAlice,28`

### 🐍 Python Command Line

#### Interactive Mode:
```bash
python json_comparator.py
```

#### Run Example:
```bash
python example_usage.py
```

#### As a Module:
```python
from json_comparator import compare_json_strings

request_json = '''
{
  "user_id": 123,
  "name": "Alice Johnson", 
  "email": "alice@example.com",
  "skills": ["Python", "JavaScript"]
}
'''

response_json = '''
{
  "user_id": 123,
  "name": "Alice Johnson",
  "email": "alice@example.com", 
  "account_status": "active",
  "skills": ["Python", "JavaScript", "React"]
}
'''

report = compare_json_strings(request_json, response_json)
print(report)
```

## 📋 Example Output

```
🔍 JSON REQUEST vs RESPONSE COMPARISON REPORT
============================================================

+---------------------------+-------------------------------------------------------+-----------------------
| Field Path                | Request Value                                         | Response Value        
+===========================+=======================================================+=======================
| user_id                   | 123                                                   | 123                   
| name                      | Alice Johnson                                         | Alice Johnson         
| email                     | alice@example.com                                     | alice@example.com     
| account_status            | ❌ MISSING                                             | active                
| skills[0]                 | Python                                                | Python                
| skills[1]                 | JavaScript                                            | JavaScript            
| skills[2]                 | ❌ MISSING                                             | React                 
+---------------------------+-------------------------------------------------------+-----------------------

📊 SUMMARY:
============================================================
Total Fields Compared: 7
✅ Matching Fields: 5 (71.4%)
❌ Different/Missing Fields: 2 (28.6%)

✅ MATCHING FIELDS:
• user_id
• name  
• email
• skills[0]
• skills[1]

⚠️ FIELDS WITH DIFFERENCES:
• account_status
• skills[2]
```

## 🌟 Format-Specific Features

### 📄 **JSON**
- Deep nested object comparison
- Array element-by-element analysis
- Flexible parsing (handles malformed JSON)

### 📰 **XML**
- Element and attribute comparison
- Namespace handling
- Text content extraction

### 📊 **CSV**
- Header-based field mapping
- Multi-row data comparison
- Quoted field support

### 📝 **YAML**  
- Array and object comparison
- Multi-document support
- Complex data structure handling

## 🔧 Web Interface Features

### 🎨 **Beautify Functions**
- **JSON**: Pretty-print with indentation
- **XML**: Clean formatting with proper nesting
- **YAML**: Standard YAML formatting
- **CSV**: Clean spacing and alignment

### 📋 **Utility Functions**
- **Copy**: Copy data to clipboard (multiple fallback methods)
- **Clear**: Clear text areas
- **Format Detection**: Auto-detect data format
- **Error Highlighting**: Visual syntax error indication

### 📱 **Responsive Design**
- Mobile-friendly interface
- Keyboard shortcuts (`Ctrl/Cmd + Enter` to compare)
- Accessible design with clear visual indicators

## 🏗️ Technical Architecture

### 🎯 **Format Detection**
```javascript
// Smart detection logic
if (text.startsWith('<')) → XML
else if (hasYAMLPatterns) → YAML  
else if (hasCommaStructure) → CSV
else → JSON (default)
```

### 🗂️ **Data Flattening**
```
Nested Structure → Flat Paths
{
  user: {
    name: "Alice",
    skills: ["Python", "JS"]
  }
} 
↓
{
  "user.name": "Alice",
  "user.skills[0]": "Python", 
  "user.skills[1]": "JS"
}
```

### 🔍 **Comparison Logic**
1. Parse both data sources
2. Flatten nested structures  
3. Compare field by field
4. Generate detailed report with statistics

## 📁 Project Structure

```
ReqRes/
├── 📄 index.html           # Web interface (main application)
├── 🐍 json_comparator.py   # Python comparison engine
├── 🐍 example_usage.py     # Demo with sample data
├── 📋 requirements.txt     # Python dependencies
└── 📖 README.md           # This file
```

## 🎯 Use Cases

- **🔧 API Testing**: Compare request/response data
- **📊 Data Migration**: Validate data transformations
- **🐛 Debugging**: Identify data discrepancies  
- **⚙️ Configuration Management**: Compare config files
- **📋 Data Validation**: Ensure data integrity
- **🔄 Format Conversion**: Validate cross-format data

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Add tests for new formats or features
4. Submit a pull request

## 📜 License

This project is open source. Feel free to use, modify, and distribute.

---

**🚀 Ready to compare your data?** Start with the web interface at `http://localhost:8000` or try the Python examples!
