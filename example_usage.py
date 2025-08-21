#!/usr/bin/env python3
"""
Example usage of the JSON Comparator tool
"""

from json_comparator import compare_json_strings

# Sample request and response data for demonstration
sample_request = '''{
  "user_id": 123,
  "name": "Alice Johnson", 
  "email": "alice@example.com",
  "age": 28,
  "preferences": {
    "theme": "dark",
    "notifications": true
  },
  "skills": ["Python", "JavaScript", "SQL"]
}'''

# Example with intentional JSON error for testing error highlighting  
sample_request_with_error = '''
{
  "user_id": 123,
  "name": "Alice Johnson",
  "email": "alice@example.com"
  "age": 28,
  "preferences": {
    "theme": "dark",
    "notifications": true
  }
}
'''

sample_response = '''{
  "user_id": 123,
  "name": "Alice Johnson",
  "email": "alice@example.com", 
  "age": 28,
  "account_status": "active",
  "created_at": "2024-01-15T09:30:00Z",
  "last_login": "2024-12-20T14:22:15Z",
  "preferences": {
    "theme": "dark",
    "notifications": true,
    "language": "en"
  },
  "skills": ["Python", "JavaScript", "SQL", "React"],
  "profile": {
    "bio": "Software developer with 5 years experience",
    "location": "San Francisco, CA",
    "avatar_url": "https://example.com/avatars/alice.jpg"
  }
}'''

def run_example():
    """
    Run the example comparison
    """
    print("🚀 Running JSON Comparison Example")
    print("="*50)
    
    print("\n📥 REQUEST JSON:")
    print(sample_request)
    
    print("\n📤 RESPONSE JSON:")
    print(sample_response)
    
    print("\n" + "="*50)
    
    # Generate comparison report
    report = compare_json_strings(sample_request, sample_response)
    print(report)

def run_error_example():
    """
    Demonstrate error highlighting with invalid JSON
    """
    print("\n\n🔴 Testing Error Highlighting")
    print("="*50)
    
    print("\n📥 REQUEST JSON (with error):")
    print(sample_request_with_error)
    
    print("\n📤 RESPONSE JSON:")
    print(sample_response)
    
    print("\n" + "="*50)
    
    try:
        # This will trigger the error highlighting
        report = compare_json_strings(sample_request_with_error, sample_response)
        print(report)
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    run_example()
    run_error_example()