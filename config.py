import os
import json

class ServiceConfig:
    """Configuration class for customizing the service application"""
    
    def __init__(self):
        self._config = self._load_default_config()
        self._load_custom_config()
    
    def _load_default_config(self):
        """Load default configuration"""
        return {
            'company_name': '[Company Name]',
            'app_title': 'Professional Service Management',
            'app_subtitle': 'Task-Based Service Workflow & Time Management',
            'logo_path': 'static/img/generic_logo.svg',
            'primary_color': '#0d6efd',
            'service_unit': 'square feet',  # or 'linear feet', 'rooms', 'items', etc.
            'service_unit_abbr': 'sq ft',
            'contact_email': 'info@yourcompany.com',
            'phone_number': '(555) 123-4567',
            'address': '123 Business Street, City, State 12345',
            'ai_assistant_name': 'Service Assistant',
            'ai_assistant_intro': 'I\'m here to help with task management, time estimation, and workflow optimization.',
            'field_labels': {
                'client_name': 'Client Name',
                'service_provider_name': 'Service Provider',
                'job_address': 'Service Address',
                'reference_number': 'Reference/Job Number',
                'service_area_size': 'Service Area Size',
                'service_type': 'Service Type'
            },
            'email_templates': {
                'job_completion_subject': 'Service Job Completed - {client_name}',
                'job_completion_from': 'noreply@yourcompany.com'
            }
        }
    
    def _load_custom_config(self):
        """Load custom configuration from file if it exists"""
        config_file = 'service_config.json'
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    custom_config = json.load(f)
                    self._config.update(custom_config)
            except Exception as e:
                print(f"Error loading custom config: {e}")
    
    def get_config(self):
        """Get the current configuration"""
        return self._config
    
    def update_config(self, updates):
        """Update configuration with new values"""
        self._config.update(updates)
        self._save_custom_config()
    
    def _save_custom_config(self):
        """Save custom configuration to file"""
        try:
            with open('service_config.json', 'w') as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            print(f"Error saving custom config: {e}")
    
    def setup_for_industry(self, industry_type):
        """Quick setup for specific industries"""
        industry_configs = {
            'cleaning': {
                'company_name': 'Elite Cleaning Services',
                'app_title': 'Professional Cleaning Management',
                'app_subtitle': 'Cleaning Task Workflow & Time Management',
                'service_unit': 'square feet',
                'service_unit_abbr': 'sq ft',
                'field_labels': {
                    'service_provider_name': 'Cleaner Name',
                    'service_area_size': 'Square Footage'
                }
            },
            'plumbing': {
                'company_name': 'Professional Plumbing Solutions',
                'app_title': 'Plumbing Service Management',
                'app_subtitle': 'Plumbing Task Workflow & Time Tracking',
                'service_unit': 'service calls',
                'service_unit_abbr': 'calls',
                'field_labels': {
                    'service_provider_name': 'Plumber Name',
                    'service_area_size': 'Number of Fixtures'
                }
            },
            'landscaping': {
                'company_name': 'Premier Landscaping Services',
                'app_title': 'Landscaping Project Management',
                'app_subtitle': 'Landscaping Task Workflow & Time Tracking',
                'service_unit': 'square feet',
                'service_unit_abbr': 'sq ft',
                'field_labels': {
                    'service_provider_name': 'Landscaper Name',
                    'service_area_size': 'Area Size'
                }
            },
            'inspection': {
                'company_name': 'Professional Inspection Services',
                'app_title': 'Home Inspection Management',
                'app_subtitle': 'Inspection Task Workflow & Documentation',
                'service_unit': 'rooms',
                'service_unit_abbr': 'rooms',
                'field_labels': {
                    'service_provider_name': 'Inspector Name',
                    'service_area_size': 'Number of Rooms'
                }
            }
        }
        
        if industry_type in industry_configs:
            self.update_config(industry_configs[industry_type])
