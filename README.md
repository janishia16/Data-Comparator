# JSON Request/Response Comparator

A Python tool to compare JSON request and response bodies in an easy-to-read table format. Perfect for API testing, data validation, and debugging.

## Features

- ✅ **Side-by-side comparison** of request and response JSON data
- ✅ **Nested JSON support** with dot-notation field paths
- ✅ **Visual indicators** for matches and differences
- ✅ **Detailed summary** with statistics
- ✅ **Missing field detection** 
- ✅ **Clean table output** using tabulate

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Method 1: Interactive Command Line

Run the script directly for interactive input:

```bash
python json_comparator.py
```

Then paste your request JSON, press Enter twice, paste your response JSON, and press Enter twice to see the comparison.

### Method 2: As a Python Module

```python
from json_comparator import compare_json_strings

request_json = '{"user_id": 123, "name": "John"}'
response_json = '{"user_id": 123, "name": "John Doe"}'

report = compare_json_strings(request_json, response_json)
print(report)
```

### Method 3: Run Example

See a demonstration with sample data:

```bash
python example_usage.py
```

## Example Output

```
🔍 JSON REQUEST vs RESPONSE COMPARISON REPORT
============================================================

┌─────────────────────────┬─────────────────────────┬─────────────────────────┬─────────────┐
│ Field Path              │ Request Value           │ Response Value          │ Status      │
├─────────────────────────┼─────────────────────────┼─────────────────────────┼─────────────┤
│ user_id                 │ 12345                   │ 12345                   │ ✅ MATCH    │
│ email                   │ john.doe@example.com    │ john.doe@example.com    │ ✅ MATCH    │
│ name                    │ John Doe                │ John Doe                │ ✅ MATCH    │
│ preferences.theme       │ dark                    │ light                   │ ❌ DIFFERENT│
│ address.country         │ ❌ MISSING              │ USA                     │ ❌ DIFFERENT│
│ created_at              │ ❌ MISSING              │ 2024-01-15T10:30:00Z    │ ❌ DIFFERENT│
└─────────────────────────┴─────────────────────────┴─────────────────────────┴─────────────┘

📊 SUMMARY:
============================================================
Total Fields Compared: 8
✅ Matching Fields: 5 (62.5%)
❌ Different/Missing Fields: 3 (37.5%)
```

## How It Works

1. **JSON Parsing**: Safely parses both JSON inputs with error handling
2. **Flattening**: Converts nested JSON structures to dot-notation paths (e.g., `address.street`)
3. **Comparison**: Compares values field by field
4. **Visualization**: Displays results in a clean table with status indicators
5. **Summary**: Provides statistics and lists of differences/matches

## Field Path Examples

- Simple field: `user_id`
- Nested object: `address.street`
- Array element: `tags[0]`
- Nested array: `orders[0].items[1].name`

## Error Handling

- Invalid JSON format detection
- Missing field identification
- Graceful handling of different data types
- Clear error messages with helpful context