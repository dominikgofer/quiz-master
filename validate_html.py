#!/usr/bin/env python3
"""
HTML5 Validator for Django Templates
Renders Django pages and validates them against W3C HTML5 standard
"""

import os
import sys
import django
import requests
from django.test import Client
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_platform.settings')
django.setup()


def validate_html(html_content):
    """Send HTML to W3C validator API and return results"""
    validator_url = 'https://validator.w3.org/nu/?out=json'
    
    try:
        response = requests.post(
            validator_url,
            data=html_content.encode('utf-8'),
            headers={
                'Content-Type': 'text/html; charset=utf-8',
                'User-Agent': 'Mozilla/5.0 (HTML5 Validator Script)'
            },
            timeout=30
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}


def print_validation_results(url, results):
    """Print validation results in a readable format"""
    print(f"\n{'='*80}")
    print(f"Validating: {Fore.CYAN}{url}{Style.RESET_ALL}")
    print(f"{'='*80}")
    
    if 'error' in results:
        print(f"{Fore.RED}✗ Error connecting to validator: {results['error']}{Style.RESET_ALL}")
        return False
    
    messages = results.get('messages', [])
    
    if not messages:
        print(f"{Fore.GREEN}✓ No validation errors or warnings!{Style.RESET_ALL}")
        return True
    
    errors = [m for m in messages if m['type'] == 'error']
    warnings = [m for m in messages if m['type'] == 'info']
    
    print(f"\nErrors: {Fore.RED}{len(errors)}{Style.RESET_ALL}")
    print(f"Warnings: {Fore.YELLOW}{len(warnings)}{Style.RESET_ALL}\n")
    
    # Print errors
    for msg in errors:
        line = msg.get('lastLine', '?')
        col = msg.get('lastColumn', '?')
        message = msg.get('message', '')
        extract = msg.get('extract', '')
        
        print(f"{Fore.RED}ERROR{Style.RESET_ALL} [Line {line}:{col}]")
        print(f"  {message}")
        if extract:
            print(f"  Context: {Fore.LIGHTBLACK_EX}{extract.strip()}{Style.RESET_ALL}")
        print()
    
    # Print warnings
    for msg in warnings:
        line = msg.get('lastLine', '?')
        col = msg.get('lastColumn', '?')
        message = msg.get('message', '')
        
        print(f"{Fore.YELLOW}WARNING{Style.RESET_ALL} [Line {line}:{col}]")
        print(f"  {message}")
        print()
    
    return len(errors) == 0


def validate_page(url, client=None):
    """Render a Django page and validate it"""
    if client is None:
        client = Client()
    
    try:
        response = client.get(url)
        
        if response.status_code != 200:
            print(f"{Fore.RED}✗ Failed to fetch {url} (Status: {response.status_code}){Style.RESET_ALL}")
            return False
        
        html_content = response.content.decode('utf-8')
        results = validate_html(html_content)
        return print_validation_results(url, results)
        
    except Exception as e:
        print(f"{Fore.RED}✗ Error rendering {url}: {str(e)}{Style.RESET_ALL}")
        return False


def main():
    """Main validation function"""
    # List of URLs to validate
    urls_to_validate = [
        '/',
        '/login/',
        '/register/',
        # Add more URLs as needed
        # '/quizzes/',
        # '/dashboard/',
    ]
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        urls_to_validate = sys.argv[1:]
    
    print(f"{Fore.CYAN}Starting HTML5 Validation{Style.RESET_ALL}")
    print(f"Validating {len(urls_to_validate)} page(s)...\n")
    
    client = Client()
    results = []
    
    for url in urls_to_validate:
        is_valid = validate_page(url, client)
        results.append((url, is_valid))
    
    # Summary
    print(f"\n{'='*80}")
    print(f"{Fore.CYAN}VALIDATION SUMMARY{Style.RESET_ALL}")
    print(f"{'='*80}")
    
    passed = sum(1 for _, valid in results if valid)
    failed = len(results) - passed
    
    for url, valid in results:
        status = f"{Fore.GREEN}✓ PASS{Style.RESET_ALL}" if valid else f"{Fore.RED}✗ FAIL{Style.RESET_ALL}"
        print(f"{status} {url}")
    
    print(f"\nTotal: {len(results)} | Passed: {Fore.GREEN}{passed}{Style.RESET_ALL} | Failed: {Fore.RED}{failed}{Style.RESET_ALL}")
    
    # Exit with error code if any validation failed
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
