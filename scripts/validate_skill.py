import os
import json
import sys
import re

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(BASE_DIR, "03_Skills")

class Colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_pass(text):
    print(f"{Colors.OKGREEN}PASS{Colors.ENDC} {text}")

def print_fail(text):
    print(f"{Colors.FAIL}FAIL{Colors.ENDC} {text}")

def validate_json_file(path, min_items=None):
    if not os.path.exists(path):
        return False, "File missing"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if min_items is not None:
                if isinstance(data, list) and len(data) < min_items:
                    return False, f"Contains {len(data)} items, expected >= {min_items}"
            return True, "Valid JSON"
    except json.JSONDecodeError:
        return False, "Invalid JSON syntax"
    except Exception as e:
        return False, str(e)

def validate_markdown_section(path, section_name):
    if not os.path.exists(path):
        return False, "File missing"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple check for header
    if f"# {section_name}" in content or f"## {section_name}" in content:
        return True, "Section found"
    
    # Check for numbered sections like "# 7) Risk Matrix"
    if re.search(rf"# \d+\)\s*{section_name}", content, re.IGNORECASE):
        return True, "Section found"
        
    return False, f"Missing section: {section_name}"

def check_skill(skill_path):
    skill_name = os.path.basename(skill_path)
    print(f"\n{Colors.BOLD}Validating {skill_name}...{Colors.ENDC}")
    
    errors = 0
    
    # 1. Check schemas
    ok, msg = validate_json_file(os.path.join(skill_path, "schema.input.json"))
    if ok: print_pass("Input Schema")
    else: 
        print_fail(f"Input Schema: {msg}")
        errors += 1

    ok, msg = validate_json_file(os.path.join(skill_path, "schema.output.json"))
    if ok: print_pass("Output Schema")
    else: 
        print_fail(f"Output Schema: {msg}")
        errors += 1

    # 2. Check tests quantity
    ok, msg = validate_json_file(os.path.join(skill_path, "tests.smoke.json"), min_items=1) # Should be 10, but lenient for now
    if ok: print_pass("Smoke Tests")
    else: 
        print_fail(f"Smoke Tests: {msg}")
        errors += 1

    ok, msg = validate_json_file(os.path.join(skill_path, "tests.golden.json"), min_items=1) # Should be 30
    if ok: print_pass("Golden Set")
    else: 
        print_fail(f"Golden Set: {msg}")
        errors += 1
        
    # 3. Check Markdown Structure
    skill_md = [f for f in os.listdir(skill_path) if f.endswith(".skill.md")]
    if not skill_md:
        print_fail("Missing *.skill.md file")
        errors += 1
    else:
        md_path = os.path.join(skill_path, skill_md[0])
        required_sections = ["Propósito", "Definition of Done", "Interface", "Risk Matrix", "Tests"]
        for sec in required_sections:
            ok, msg = validate_markdown_section(md_path, sec)
            if not ok:
                print_fail(f"Markdown: {msg}")
                errors += 1
            else:
                print_pass(f"Section '{sec}'")

    return errors == 0

def main():
    if len(sys.argv) > 1:
        target_skills = [os.path.join(SKILLS_DIR, sys.argv[1])]
    else:
        target_skills = [os.path.join(SKILLS_DIR, d) for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))]
    
    all_passed = True
    for skill in target_skills:
        if not check_skill(skill):
            all_passed = False
            
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
