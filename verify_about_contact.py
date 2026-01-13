#!/usr/bin/env python3
"""
Verification script for About Us and Contact Us pages
"""

import os
import sys

def check_files():
    """Check if required files exist"""
    print("=" * 60)
    print("ABOUT US & CONTACT US PAGES VERIFICATION")
    print("=" * 60)
    
    checks = {
        'templates/about.html': 'About Us template',
        'templates/contact.html': 'Contact Us template',
    }
    
    all_passed = True
    
    print("\n1. FILE EXISTENCE CHECKS")
    print("-" * 60)
    for file_path, description in checks.items():
        if os.path.exists(file_path):
            print(f"✓ {description}: EXISTS")
        else:
            print(f"✗ {description}: MISSING")
            all_passed = False
    
    return all_passed

def check_routes():
    """Check if routes exist in app.py"""
    print("\n2. ROUTE CHECKS")
    print("-" * 60)
    
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        routes = {
            '@app.route(\'/about\')': 'About Us route',
            'def about()': 'About function',
            '@app.route(\'/contact\')': 'Contact Us route',
            'def contact()': 'Contact function',
        }
        
        all_passed = True
        for route, description in routes.items():
            if route in content:
                print(f"✓ {description}: EXISTS")
            else:
                print(f"✗ {description}: MISSING")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"✗ Error reading app.py: {e}")
        return False

def check_css():
    """Check if CSS styles exist"""
    print("\n3. CSS STYLES CHECKS")
    print("-" * 60)
    
    try:
        with open('static/css/style.css', 'r') as f:
            content = f.read()
        
        styles = [
            '.about-section',
            '.contact-section',
            '.values-grid',
            '.contact-form',
            '.social-links',
            '.faq-section',
        ]
        
        all_passed = True
        for style in styles:
            if style in content:
                print(f"✓ {style}: EXISTS")
            else:
                print(f"✗ {style}: MISSING")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"✗ Error reading style.css: {e}")
        return False

def check_footer_links():
    """Check if footer has About and Contact links"""
    print("\n4. FOOTER NAVIGATION CHECKS")
    print("-" * 60)
    
    try:
        with open('templates/base.html', 'r') as f:
            content = f.read()
        
        links = {
            '{{ url_for(\'about\') }}': 'About Us link',
            '{{ url_for(\'contact\') }}': 'Contact Us link',
        }
        
        all_passed = True
        for link, description in links.items():
            if link in content:
                print(f"✓ {description}: EXISTS")
            else:
                print(f"✗ {description}: MISSING")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"✗ Error reading base.html: {e}")
        return False

def main():
    """Main verification function"""
    results = []
    
    results.append(check_files())
    results.append(check_routes())
    results.append(check_css())
    results.append(check_footer_links())
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if all(results):
        print("✓ All checks passed! About Us and Contact Us pages are ready.")
        print("\nYou can now access:")
        print("  • About Us page: http://localhost:5000/about")
        print("  • Contact Us page: http://localhost:5000/contact")
        return 0
    else:
        print("✗ Some checks failed. Please review the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
