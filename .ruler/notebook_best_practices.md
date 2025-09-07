# Notebook Best Practices: Jeremy Howard's nbdev Philosophy

> A comprehensive guide to writing effective Jupyter notebooks following Jeremy Howard's literate programming principles

This document outlines the key principles and practices for creating high-quality Jupyter notebooks based on Jeremy Howard's nbdev methodology and years of experience with notebook-driven development.

## Core Philosophy: Literate Programming

Jeremy Howard advocates for **literate programming** - the idea that code should be written primarily for humans to read, with execution by computers being secondary. Notebooks excel at this because they combine:

- **Code** - The implementation
- **Documentation** - Explanations and context  
- **Examples** - Working demonstrations
- **Tests** - Validation and edge cases

## Essential Principles

### 1. Functions First, Widgets Second

**Always build and test core functions before creating interactive interfaces.**

```python
# ✅ GOOD: Build function first
def calculate_roi(revenue: float, cost: float) -> float:
    """Calculate return on investment as a percentage."""
    return (revenue - cost) / cost * 100

# Test immediately
result = calculate_roi(1200, 1000)
assert result == 20.0
print(f"ROI: {result}%")

# Interactive demo comes last (optional)
from ipywidgets import interact
interact(calculate_roi, revenue=(0, 10000, 100), cost=(0, 5000, 100))
```

```python
# ❌ AVOID: Starting with widgets before building functions
# Don't build functionality inside widget callbacks
```

### 2. Small, Focused Functions

**Each function should do one thing well and be immediately testable.**

```python
# ✅ GOOD: Small, focused function
def extract_domain(url: str) -> str:
    """Extract domain from a URL."""
    from urllib.parse import urlparse
    return urlparse(url).netloc

# Test immediately
test_url = "https://api.example.com/v1/data"
domain = extract_domain(test_url)
assert domain == "api.example.com"
print(f"Domain: {domain}")
```

```python
# ❌ AVOID: Large functions that do multiple things
def process_api_data_and_send_emails_and_log_everything(data):
    # 50+ lines of mixed concerns
    pass
```

### 3. Immediate Testing and Demonstration

**Every function should be followed immediately by working examples and tests.**

**CRITICAL JEREMY HOWARD PATTERN - MUST FOLLOW EXACTLY:**

```
Function Definition (#| export)
    ↓
Mock Tests (clean examples for documentation)
    ↓  
Hidden Real API Test (#| hide - immediate validation)
    ↓
[Next Function...]
```

**❌ NEVER DO THIS (violates nbdev philosophy):**
```
Function 1 definition
Mock tests for Function 1
Function 2 definition  
Mock tests for Function 2
Function 3 definition
Mock tests for Function 3
[GIANT BLOB OF ALL REAL API TESTS AT END] ← WRONG!
```

**✅ ALWAYS DO THIS (Jeremy Howard's way):**
```
Function 1 definition (#| export)
Mock tests for Function 1
Real API test for Function 1 (#| hide)

Function 2 definition (#| export)
Mock tests for Function 2  
Real API test for Function 2 (#| hide)

Function 3 definition (#| export)
Mock tests for Function 3
Real API test for Function 3 (#| hide)
```

```python
#| export
def validate_email(email: str) -> bool:
    """Check if email format is valid."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# Immediate testing with assertions
from fastcore.test import test_eq

test_eq(validate_email("user@example.com"), True)
test_eq(validate_email("invalid-email"), False)
test_eq(validate_email(""), False)

print("✅ Email validation function working correctly")

# Show practical examples
emails = ["john@example.com", "invalid", "test@domain.org"]
for email in emails:
    status = "✅" if validate_email(email) else "❌"
    print(f"{status} {email}")
```

### 4. Progressive Building

**Build complexity gradually, with each step building on the previous.**

```python
# Step 1: Simple function
def make_request(url: str) -> dict:
    """Make a basic HTTP request."""
    import requests
    response = requests.get(url)
    return response.json()

# Test Step 1
test_data = make_request("https://httpbin.org/json")
print("✅ Basic request working")

# Step 2: Add error handling
def make_safe_request(url: str) -> dict:
    """Make HTTP request with error handling."""
    try:
        import requests
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Test Step 2
result = make_safe_request("https://invalid-url.com")
assert "error" in result
print("✅ Error handling working")

# Step 3: Add authentication (builds on previous steps)
def make_authenticated_request(url: str, token: str) -> dict:
    """Make authenticated request using previous function."""
    import requests
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
```

## Notebook Structure Standards

### 1. Title and Metadata

Start every notebook with clear metadata:

```markdown
# API Client Implementation

> A step-by-step implementation of a robust API client

This notebook demonstrates how to build a production-ready API client following best practices for error handling, authentication, and testing.
```

### 2. Imports and Setup

Keep imports clean and organized:

```python
#| default_exp api_client

# Standard library
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

# Third party
import requests
import pandas as pd

# Testing
from fastcore.test import test_eq, test_ne

# Local imports (if any)
from myproject.utils import helper_function
```

### 3. Function Organization

Each major functionality should follow this pattern:

```markdown
## Authentication

Let's start with a simple authentication class:
```

```python
#| export
class APIAuth:
    """Simple API authentication handler."""
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @property
    def headers(self) -> Dict[str, str]:
        """Return authentication headers."""
        return {"Authorization": f"Bearer {self.api_key}"}

# Test immediately
auth = APIAuth("test-key-123")
expected = {"Authorization": "Bearer test-key-123"}
test_eq(auth.headers, expected)
print("✅ Authentication class working")
```

### 4. Export Management

Always include export cell at the end:

```python
#| hide
import nbdev
nbdev.nbdev_export()
```

## Testing Best Practices

### 1. Use fastcore.test Functions

```python
from fastcore.test import test_eq, test_ne, test_close, test_is

# Equality testing
test_eq(calculate_tax(100, 0.1), 10.0)

# Inequality testing  
test_ne(process_data([]), None)

# Float comparison with tolerance
test_close(calculate_pi(), 3.14159, eps=1e-4)

# Identity testing
test_is(get_singleton(), get_singleton())
```

### 2. Test Edge Cases

```python
def safe_divide(a: float, b: float) -> Optional[float]:
    """Safely divide two numbers."""
    if b == 0:
        return None
    return a / b

# Test normal cases
test_eq(safe_divide(10, 2), 5.0)
test_eq(safe_divide(7, 3), 7/3)

# Test edge cases
test_eq(safe_divide(5, 0), None)  # Division by zero
test_eq(safe_divide(0, 5), 0.0)   # Zero dividend
test_eq(safe_divide(-10, 2), -5.0) # Negative numbers

print("✅ All edge cases handled correctly")
```

### 3. Document Error Cases

```python
def parse_config(config_str: str) -> Dict[str, Any]:
    """Parse configuration string to dictionary."""
    import json
    try:
        return json.loads(config_str)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {e}"}

# Test success case
valid_json = '{"key": "value", "number": 42}'
result = parse_config(valid_json)
test_eq(result, {"key": "value", "number": 42})

# Test error case
invalid_json = '{"incomplete": json'
result = parse_config(invalid_json)
assert "error" in result
print("✅ Error handling documented and tested")
```

## Advanced Patterns

### 1. Use show_doc for Class Methods

```python
from nbdev.showdoc import show_doc

class DataProcessor:
    """Process and analyze data efficiently."""
    
    def clean_data(self, data: List[Dict]) -> List[Dict]:
        """Remove invalid entries and normalize data."""
        # Implementation here
        pass
    
    def analyze_trends(self, data: List[Dict]) -> Dict[str, float]:
        """Analyze trends in the cleaned data."""
        # Implementation here  
        pass

# Document methods individually
show_doc(DataProcessor.clean_data)
show_doc(DataProcessor.analyze_trends)
```

### 2. Use Patch for Method Extension

```python
from fastcore.basics import patch

@patch
def to_summary(self: DataProcessor) -> str:
    """Generate a summary report of the processor state."""
    return f"DataProcessor with {len(self.data)} records"

# Test the patched method
processor = DataProcessor()
processor.data = [{"a": 1}, {"b": 2}]
test_eq(processor.to_summary(), "DataProcessor with 2 records")
```

### 3. Rich Display for Objects

```python
class APIResponse:
    def __init__(self, data: dict, status_code: int):
        self.data = data
        self.status_code = status_code
    
    def _repr_markdown_(self) -> str:
        """Rich display in notebooks."""
        return f"""
**API Response**
- Status Code: `{self.status_code}`
- Data Keys: `{list(self.data.keys())}`
- Success: {'✅' if self.status_code == 200 else '❌'}
"""

# When displayed in notebook, shows formatted markdown
response = APIResponse({"users": [1, 2, 3]}, 200)
response  # Rich display automatically shown
```

## Cross-Platform Import Resolution

### 1. Required Path Setup for All Notebooks

For notebooks to work across different environments (Mac Jupyter, Docker, etc.), always include path setup at the beginning of imports:

```python
#| export
from __future__ import annotations

import sys
import os

# Add project root to path so we can import awin_pubkit modules
if '..' not in sys.path:
    sys.path.insert(0, '..')
if '.' not in sys.path:
    sys.path.insert(0, '.')

# Then proceed with regular imports
from typing import Any, Dict, List, Optional
from awin_pubkit.core import AwinClient
```

**Why this is needed:**
- Jupyter notebooks don't automatically include project directory in Python path
- Different platforms (macOS vs Docker) may have different path resolution behavior
- Virtual environments may not be detected consistently by notebook kernels
- This ensures reliable imports regardless of execution environment

**Pattern for all future notebooks:**
1. Always include the path setup code at the top of imports cell
2. Include it in the `#| export` cell so it's available in generated modules
3. Test imports work from the `nbs/` directory before proceeding
4. This pattern works across Mac, Linux, Docker, and other environments

## API Integration and Real Data Testing

### 1. Dual Testing Pattern for API Functions

When building functions that interact with external APIs, use a two-tier testing approach:

```python
# 1. Mock/Unit Tests (exported to docs)
# Test immediately with predictable mock data
class MockClient:
    def request(self, method, path):
        return {"accounts": [{"accountId": 12345, "accountType": "publisher"}]}

mock_client = MockClient()
result = get_publisher_ids(mock_client)
test_eq(len(result), 1)
print("✅ Function logic working correctly")
```

```python
#| hide
# 2. Real API Tests (hidden from docs)
# Validate with actual API integration

try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    api_token = os.getenv('API_TOKEN')
    if api_token:
        real_client = APIClient(api_token)
        real_result = get_publisher_ids(real_client)
        print(f"✅ Found {len(real_result)} real accounts")
        print("✅ Real API integration working")
    else:
        print("ℹ️ Skipping real API test (API_TOKEN not set)")
        
except Exception as e:
    print(f"⚠️ Real API test note: {e}")
```

**Benefits of this pattern**:
- Documentation shows clean, predictable examples
- Hidden tests prove functions work with real APIs
- Graceful degradation when credentials unavailable
- Security best practices (no credentials in published docs)

### 2. API Response Structure Validation

Never assume API response structures. Always validate actual responses:

```python
# ❌ Dangerous assumption
def get_data(client):
    data = client.request("/endpoint")
    if not isinstance(data, list):  # Wrong assumption!
        return []
    return data

# ✅ Proper validation
def get_data(client):
    data = client.request("/endpoint")
    # Validate actual structure
    if isinstance(data, dict) and 'items' in data:
        return data['items']
    elif isinstance(data, list):
        return data
    return []
```

**Best practices**:
- Test with real API responses to understand actual structure
- Handle multiple possible response formats gracefully
- Document the expected API response format in comments
- Update specifications when API structure assumptions are wrong

### 3. Environment Configuration for API Testing

Use `.env` files with `python-dotenv` for secure credential management:

```python
#| hide
# Standard pattern for API testing
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

api_token = os.getenv('API_TOKEN')
if not api_token:
    print("ℹ️ Skipping API tests (API_TOKEN not set in .env)")
    return

# Proceed with real API testing...
```

**Security benefits**:
- Credentials stay out of notebooks and repositories
- Easy to manage different environments (dev/staging/prod)
- Graceful fallback when credentials unavailable
- Consistent credential management across project

## Common Anti-Patterns to Avoid

### ❌ Don't Mix Imports and Logic

```python
# BAD
import pandas as pd
df = pd.read_csv("data.csv")  # Don't mix with imports
import numpy as np
```

```python
# GOOD
import pandas as pd
import numpy as np

# Separate cell for logic
df = pd.read_csv("data.csv")
```

### ❌ Don't Create Massive Functions

```python
# BAD
def do_everything(data):
    # 100+ lines of mixed functionality
    # Data cleaning
    # API calls  
    # Email sending
    # Logging
    # Analysis
    pass
```

```python
# GOOD
def clean_data(data): pass
def call_api(endpoint): pass  
def send_notification(message): pass
def log_activity(action): pass
def analyze_results(results): pass
```

### ❌ Don't Skip Documentation

```python
# BAD
def calc(x, y, z):
    return (x * y) / z if z != 0 else None
```

```python
# GOOD
def calculate_efficiency_ratio(revenue: float, costs: float, time_hours: float) -> Optional[float]:
    """Calculate efficiency ratio as revenue per cost per hour.
    
    Args:
        revenue: Total revenue generated
        costs: Total costs incurred
        time_hours: Time spent in hours
        
    Returns:
        Efficiency ratio or None if time_hours is zero
        
    Example:
        >>> calculate_efficiency_ratio(1000, 500, 10)
        2.0
    """
    if time_hours == 0:
        return None
    return revenue / costs / time_hours
```

## Collaboration Best Practices

### 1. Use nbdev Hooks

```bash
# Install git hooks to clean notebooks
nbdev_install_hooks
```

This automatically:
- Cleans notebook metadata on save
- Resolves merge conflicts at cell level
- Keeps notebooks lightweight and mergeable

### 2. Consistent Cell Organization

```python
# Standard pattern for each major function:

# 1. Function definition with #| export
#| export
def my_function(param: int) -> str:
    """Function description."""
    return str(param * 2)

# 2. Immediate testing
test_eq(my_function(5), "10")
test_eq(my_function(0), "0")

# 3. Usage examples
examples = [1, 2, 3, 4, 5]
results = [my_function(x) for x in examples]
print(f"Results: {results}")

# 4. Edge case testing
test_eq(my_function(-1), "-2")  # Negative input
```

### 3. Clear Section Headers

Use markdown headers to create clear notebook structure:

```markdown
# Main Topic

## Subtopic 1: Basic Implementation

### Helper Functions

### Main Functions  

### Testing

## Subtopic 2: Advanced Features

### Error Handling

### Performance Optimization
```

## Summary

Following Jeremy Howard's nbdev philosophy creates notebooks that are:

- **Educational**: Easy to learn from with clear progression
- **Maintainable**: Small functions with immediate tests
- **Professional**: Production-ready code with comprehensive documentation  
- **Collaborative**: Clean, mergeable notebooks with consistent patterns

The key is treating notebooks as the authoritative source of both code and documentation, where every function is immediately demonstrated and tested in context.

Remember: **Functions First, Widgets Second** - build robust functionality before creating interactive interfaces, and always test immediately after implementation.