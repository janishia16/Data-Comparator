#!/usr/bin/env python3
"""
JSON Request/Response Comparator

A tool to compare JSON request and response bodies in a table format
for easy data validation and verification.
"""

import json
import sys
from typing import Dict, Any, List, Tuple
from tabulate import tabulate
from collections import OrderedDict

# For colored output
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)  # Initialize colorama
    COLOR_SUPPORT = True
except ImportError:
    COLOR_SUPPORT = False


class JSONComparator:
    def __init__(self):
        self.differences = []
        self.matches = []
        self.all_fields = set()
    
    def colorize_status(self, status: str) -> str:
        """Apply color formatting to status messages"""
        if not COLOR_SUPPORT:
            return status
        
        if "✅ MATCH" in status:
            return f"{Fore.GREEN}{status}{Style.RESET_ALL}"
        elif "🔄 DIFFERENT VALUES" in status:
            return f"{Fore.YELLOW}{Back.BLACK}{status}{Style.RESET_ALL}"
        elif "❌ MISSING" in status:
            return f"{Fore.RED}{Back.BLACK}{status}{Style.RESET_ALL}"
        else:
            return status
    
    def flatten_json(self, data: Dict[Any, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """
        Flatten nested JSON structure into dot-notation keys
        """
        items = []
        if isinstance(data, dict):
            for k, v in data.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, (dict, list)):
                    items.extend(self.flatten_json(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
        elif isinstance(data, list):
            for i, v in enumerate(data):
                new_key = f"{parent_key}{sep}[{i}]" if parent_key else f"[{i}]"
                if isinstance(v, (dict, list)):
                    items.extend(self.flatten_json(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
        return dict(items)
    
    def get_leaf_name(self, field_path: str) -> str:
        """
        Extract the leaf component name from a field path with immediate parent context
        Examples:
        - "TxnDate" -> "TxnDate"
        - "Invoice.TxnDate" -> "Invoice.TxnDate"
        - "Customer.Invoice.TxnDate" -> "Invoice.TxnDate" (skip first parent)
        - "Customer.Address.Street" -> "Address.Street"
        - "items[0].name" -> "name"
        - "tags[0]" -> "tags_item"
        """
        # Handle array items specially
        import re
        if re.search(r'\[\d+\]$', field_path):
            # This is an array item, get the array name
            clean_path = re.sub(r'\[\d+\]$', '', field_path)
            if '.' in clean_path:
                array_name = clean_path.split('.')[-1]
            else:
                array_name = clean_path
            return f"{array_name}_item" if array_name else "array_item"
        
        # Remove array indices from middle of path
        clean_path = re.sub(r'\[\d+\]', '', field_path)
        
        # Get field name with immediate parent (skip first parent)
        if '.' in clean_path:
            parts = clean_path.split('.')
            if len(parts) >= 3:
                # Skip first parent, return immediate parent + field name
                return '.'.join(parts[-2:])
            elif len(parts) == 2:
                # Return parent + field name
                return '.'.join(parts)
            else:
                return parts[0]
        return clean_path
    
    def parse_json_with_line_info(self, json_string: str, label: str = "JSON"):
        """Parse JSON and provide detailed error information with line numbers"""
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            # Get line and column information
            line_num = e.lineno if hasattr(e, 'lineno') else 1
            col_num = e.colno if hasattr(e, 'colno') else 1
            
            # Get the problematic line
            lines = json_string.split('\n')
            error_line = lines[line_num - 1] if line_num <= len(lines) else ""
            
            # Create visual pointer to error location
            pointer = ' ' * (col_num - 1) + '^'
            
            # Create colored error message
            if COLOR_SUPPORT:
                error_msg = f"""
{Fore.RED}❌ {label} PARSING ERROR:{Style.RESET_ALL}
{Fore.YELLOW}Line {line_num}, Column {col_num}:{Style.RESET_ALL} {e.msg}

{Fore.CYAN}Error Location:{Style.RESET_ALL}
{line_num:3d} | {error_line}
    | {Fore.RED}{pointer}{Style.RESET_ALL}

{Fore.YELLOW}Original Error:{Style.RESET_ALL} {str(e)}
"""
            else:
                error_msg = f"""
❌ {label} PARSING ERROR:
Line {line_num}, Column {col_num}: {e.msg}

Error Location:
{line_num:3d} | {error_line}
    | {pointer}

Original Error: {str(e)}
"""
            
            raise ValueError(error_msg)

    def compare_json(self, request_json: str, response_json: str) -> List[List[str]]:
        """
        Compare two JSON strings and return comparison data for table display
        Compares only leaf field names, ignoring parent hierarchy
        """
        try:
            # Parse JSON strings with detailed error reporting
            request_data = self.parse_json_with_line_info(request_json, "REQUEST")
            response_data = self.parse_json_with_line_info(response_json, "RESPONSE")
            
            # Flatten both JSON structures
            flat_request = self.flatten_json(request_data)
            flat_response = self.flatten_json(response_data)
            
            # Group fields by their leaf names
            request_by_leaf = {}
            response_by_leaf = {}
            
            for full_path, value in flat_request.items():
                leaf_name = self.get_leaf_name(full_path)
                if leaf_name not in request_by_leaf:
                    request_by_leaf[leaf_name] = []
                request_by_leaf[leaf_name].append((full_path, value))
            
            for full_path, value in flat_response.items():
                leaf_name = self.get_leaf_name(full_path)
                if leaf_name not in response_by_leaf:
                    response_by_leaf[leaf_name] = []
                response_by_leaf[leaf_name].append((full_path, value))
            
            # Get all unique leaf names
            all_leaf_names = set(request_by_leaf.keys()) | set(response_by_leaf.keys())
            
            # Prepare table data
            table_data = []
            
            for leaf_name in sorted(all_leaf_names):
                req_items = request_by_leaf.get(leaf_name, [])
                resp_items = response_by_leaf.get(leaf_name, [])
                
                if not req_items:
                    # Field only exists in response
                    for resp_path, resp_value in resp_items:
                        status = "❌ MISSING IN REQUEST"
                        self.differences.append(leaf_name)
                        table_data.append([
                            leaf_name,
                            "❌ MISSING",
                            str(resp_value)[:50] + "..." if len(str(resp_value)) > 50 else str(resp_value),
                            self.colorize_status(status)
                        ])
                elif not resp_items:
                    # Field only exists in request
                    for req_path, req_value in req_items:
                        status = "❌ MISSING IN RESPONSE"
                        self.differences.append(leaf_name)
                        table_data.append([
                            leaf_name,
                            str(req_value)[:50] + "..." if len(str(req_value)) > 50 else str(req_value),
                            "❌ MISSING",
                            self.colorize_status(status)
                        ])
                else:
                    # Compare values (take the first occurrence from each side)
                    req_value = req_items[0][1]
                    resp_value = resp_items[0][1]
                    
                    # Show all paths where this field exists
                    req_paths = [item[0] for item in req_items]
                    resp_paths = [item[0] for item in resp_items]
                    
                    if req_value == resp_value:
                        status = "✅ MATCH"
                        self.matches.append(leaf_name)
                    else:
                        status = "🔄 DIFFERENT VALUES"
                        self.differences.append(leaf_name)
                    
                    # Create display text showing paths if multiple
                    req_display = str(req_value)[:50] + "..." if len(str(req_value)) > 50 else str(req_value)
                    resp_display = str(resp_value)[:50] + "..." if len(str(resp_value)) > 50 else str(resp_value)
                    
                    if len(req_paths) > 1:
                        req_display += f" (found in: {', '.join(req_paths)})"
                    if len(resp_paths) > 1:
                        resp_display += f" (found in: {', '.join(resp_paths)})"
                    
                    table_data.append([
                        leaf_name,
                        req_display,
                        resp_display,
                        self.colorize_status(status)
                    ])
            
            return table_data
            
        except ValueError as e:
            # Re-raise ValueError (from parse_json_with_line_info) as-is
            raise e
        except Exception as e:
            raise ValueError(f"Unexpected error during comparison: {e}")
    
    def generate_report(self, request_json: str, response_json: str) -> str:
        """
        Generate a comprehensive comparison report
        """
        self.differences = []
        self.matches = []
        
        table_data = self.compare_json(request_json, response_json)
        
        # Create the comparison table
        headers = ["Field Path", "Request Value", "Response Value", "Status"]
        table = tabulate(table_data, headers=headers, tablefmt="grid", stralign="left")
        
        # Generate summary
        total_fields = len(table_data)
        matches_count = len(self.matches)
        differences_count = len(self.differences)
        
        report = f"""
🔍 JSON REQUEST vs RESPONSE COMPARISON REPORT
{'='*60}

{table}

📊 SUMMARY:
{'='*60}
Total Fields Compared: {total_fields}
✅ Matching Fields: {matches_count} ({matches_count/total_fields*100:.1f}%)
❌ Different/Missing Fields: {differences_count} ({differences_count/total_fields*100:.1f}%)

"""
        
        if self.differences:
            report += f"""
⚠️  FIELDS WITH DIFFERENCES:
{'-'*30}
"""
            for diff in self.differences:
                report += f"• {diff}\n"
        
        if self.matches:
            report += f"""
✅ MATCHING FIELDS:
{'-'*20}
"""
            for match in self.matches:
                report += f"• {match}\n"
        
        return report


def main():
    """
    Main function for command line usage
    """
    print("🔍 JSON Request/Response Comparator")
    print("="*40)
    
    # Get JSON inputs
    print("\n📥 Please enter your REQUEST JSON:")
    print("(Paste your JSON and press Enter twice to finish)")
    
    request_lines = []
    while True:
        try:
            line = input()
            if line.strip() == "" and request_lines:
                break
            request_lines.append(line)
        except EOFError:
            break
    
    request_json = '\n'.join(request_lines)
    
    print("\n📤 Please enter your RESPONSE JSON:")
    print("(Paste your JSON and press Enter twice to finish)")
    
    response_lines = []
    while True:
        try:
            line = input()
            if line.strip() == "" and response_lines:
                break
            response_lines.append(line)
        except EOFError:
            break
    
    response_json = '\n'.join(response_lines)
    
    # Perform comparison
    try:
        comparator = JSONComparator()
        report = comparator.generate_report(request_json, response_json)
        print(report)
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def compare_json_strings(request_json: str, response_json: str) -> str:
    """
    Utility function to compare JSON strings and return formatted report
    """
    comparator = JSONComparator()
    return comparator.generate_report(request_json, response_json)


if __name__ == "__main__":
    main()