import os
import json
import re
import datetime
import argparse
import sys

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "02_Templates")
SKILLS_DIR = os.path.join(BASE_DIR, "03_Skills")

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}")

def print_success(text):
    print(f"{Colors.OKGREEN}✔ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✘ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")

class SkillManager:
    def get_next_skill_id(self):
        existing_skills = [d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))]
        max_id = -1
        for skill in existing_skills:
            match = re.match(r"SK(\d+)_", skill)
            if match:
                skill_id = int(match.group(1))
                if skill_id > max_id:
                    max_id = skill_id
        return max_id + 1

    def create_skill_directory(self, skill_id, skill_slug):
        sid_str = f"SK{skill_id:02d}"
        dir_name = f"{sid_str}_{skill_slug}"
        full_path = os.path.join(SKILLS_DIR, dir_name)
        
        if os.path.exists(full_path):
            print_error(f"Directory {dir_name} already exists.")
            sys.exit(1)
            
        os.makedirs(full_path)
        print_success(f"Created directory: {dir_name}")
        return full_path, sid_str

class TemplateEngine:
    def __init__(self, templates_dir):
        self.templates_dir = templates_dir

    def render(self, template_name, context):
        template_path = os.path.join(self.templates_dir, template_name)
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple replacement for now
        for key, value in context.items():
            content = content.replace(f"<{key}>", str(value))
            # Also handle variations if needed, or Jinja2 if we want to add dependency
            
        return content

    def copy_file(self, template_name, target_path, context=None):
        if context:
            content = self.render(template_name, context)
        else:
            with open(os.path.join(self.templates_dir, template_name), 'r', encoding='utf-8') as f:
                content = f.read()
        
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print_success(f"Generated: {os.path.basename(target_path)}")

class IntakeWizard:
    def ask(self, question, default=None, required=True):
        prompt = f"{Colors.OKCYAN}{question}{Colors.ENDC}"
        if default:
            prompt += f" [{default}]"
        prompt += ": "
        
        while True:
            value = input(prompt).strip()
            if not value and default:
                return default
            if not value and required:
                print_error("This field is required.")
                continue
            return value

    def run(self):
        print_header("Skill Factory Intake Wizard")
        print_info("Defining a new AI Skill based on Production Standards.")
        
        data = {}
        data['name'] = self.ask("Skill Slug (snake_case)", required=True).lower().replace(" ", "_")
        data['title'] = self.ask("Skill Title (Verb + Object)", required=True)
        data['owner'] = self.ask("Owner (Email/Team)", default="AI Team")
        data['domain'] = self.ask("Domain", default="general")
        data['description'] = self.ask("Short Description (Purpose)", required=True)
        
        # Operational Envelope defaults
        data['max_tokens'] = self.ask("Max Tokens", default="1000")
        data['timeout'] = self.ask("Timeout (seconds)", default="10")
        
        return data

def main():
    parser = argparse.ArgumentParser(description="Skill Factory CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    # Command: create
    create_parser = subparsers.add_parser("create", help="Create a new skill from templates")
    
    args = parser.parse_args()
    
    if args.command == "create":
        wizard = IntakeWizard()
        context = wizard.run()
        
        manager = SkillManager()
        next_id = manager.get_next_skill_id()
        skill_dir, skill_id_str = manager.create_skill_directory(next_id, context['name'])
        
        # Update context with dynamic values
        context['skill_id'] = skill_id_str
        context['date'] = datetime.date.today().isoformat()
        
        engine = TemplateEngine(TEMPLATES_DIR)
        
        # Files to generate
        files_map = {
            "skill.template.md": f"{skill_id_str}_{context['name'].upper()}.skill.md",
            "risk_matrix.template.md": "risk_matrix.md",
            "schema.input.template.json": "schema.input.json",
            "schema.output.template.json": "schema.output.json",
            "tests.smoke.template.json": "tests.smoke.json",
            "tests.golden.template.json": "tests.golden.json"
        }
        
        # Special handling for skill.md to inject more context
        # We need to map context keys to template placeholders
        # skill.template.md uses: <snake_case>, <Verbo + Objeto>, <email o team> etc.
        template_context = {
            "snake_case": f"{skill_id_str.lower()}_{context['name']}",
            "Verbo + Objeto": context['title'],
            "email o team": context['owner'],
            "tourism|insurance|ecommerce|...": context['domain'],
            "tool_name": "none", # Default
            "schema_name": "none" # Default
        }

        print_header("Generating Files")
        for template, target in files_map.items():
            target_path = os.path.join(skill_dir, target)
            engine.copy_file(template, target_path, template_context)
            
        print_header("Next Steps")
        print(f"1. Go to: {skill_dir}")
        print(f"2. Edit {skill_id_str}_{context['name'].upper()}.skill.md to refine logic.")
        print("3. Define schemas in schema.input.json and schema.output.json")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
