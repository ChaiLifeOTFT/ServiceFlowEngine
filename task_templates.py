import json

class TaskTemplateManager:
    """Manages task templates for different service types"""
    
    def __init__(self):
        self.templates = self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default task templates for various service types"""
        return {
            'cleaning': {
                'name': 'Professional Cleaning',
                'tasks': [
                    {
                        'task': 'Initial Assessment & Setup',
                        'base_minutes': 15,
                        'minutes_per_sqft': 0.01,
                        'instructions': 'Assess the area, set up equipment and materials, and plan the work sequence.',
                        'method': 'Visual inspection and equipment preparation',
                        'materials': ['Equipment', 'Cleaning supplies', 'Safety gear'],
                        'approved_products': ['Multi-surface cleaner', 'Microfiber cloths', 'Vacuum cleaner'],
                        'precautions': 'Ensure proper ventilation and wear appropriate safety equipment.'
                    },
                    {
                        'task': 'Surface Cleaning',
                        'base_minutes': 30,
                        'minutes_per_sqft': 0.05,
                        'instructions': 'Clean all surfaces according to material specifications.',
                        'method': 'Systematic cleaning from top to bottom',
                        'materials': ['Cleaning cloths', 'Appropriate cleaners', 'Scrub brushes'],
                        'approved_products': ['All-purpose cleaner', 'Disinfectant', 'Polish'],
                        'precautions': 'Test cleaners on inconspicuous areas first. Avoid cross-contamination.'
                    },
                    {
                        'task': 'Floor Care',
                        'base_minutes': 20,
                        'minutes_per_sqft': 0.03,
                        'instructions': 'Clean and maintain floor surfaces according to type.',
                        'method': 'Sweep, mop, or vacuum as appropriate for floor type',
                        'materials': ['Mops', 'Floor cleaner', 'Vacuum'],
                        'approved_products': ['Floor-specific cleaners', 'Neutral pH cleaners'],
                        'precautions': 'Use appropriate cleaning method for floor material.'
                    },
                    {
                        'task': 'Final Inspection & Documentation',
                        'base_minutes': 10,
                        'minutes_per_sqft': 0.005,
                        'instructions': 'Conduct final quality check and document completion.',
                        'method': 'Systematic inspection and photo documentation',
                        'materials': ['Camera/phone', 'Checklist'],
                        'approved_products': ['N/A'],
                        'precautions': 'Ensure all areas meet quality standards before completion.'
                    }
                ]
            },
            'plumbing': {
                'name': 'Plumbing Service',
                'tasks': [
                    {
                        'task': 'Initial Diagnosis',
                        'base_minutes': 30,
                        'minutes_per_sqft': 0,
                        'instructions': 'Assess plumbing issue and determine required repairs.',
                        'method': 'Visual inspection and diagnostic testing',
                        'materials': ['Diagnostic tools', 'Flashlight', 'Measuring tools'],
                        'approved_products': ['Leak detection fluid', 'Pressure gauges'],
                        'precautions': 'Turn off water supply if necessary. Check for gas leaks in gas lines.'
                    },
                    {
                        'task': 'Repair Execution',
                        'base_minutes': 60,
                        'minutes_per_sqft': 0,
                        'instructions': 'Execute required repairs according to plumbing codes.',
                        'method': 'Professional repair techniques following local codes',
                        'materials': ['Pipes', 'Fittings', 'Tools', 'Sealants'],
                        'approved_products': ['Approved pipe materials', 'Thread sealant', 'Flux'],
                        'precautions': 'Follow all safety protocols. Ensure proper ventilation when soldering.'
                    },
                    {
                        'task': 'Testing & Verification',
                        'base_minutes': 20,
                        'minutes_per_sqft': 0,
                        'instructions': 'Test repairs for proper function and code compliance.',
                        'method': 'Pressure testing and functional verification',
                        'materials': ['Testing equipment', 'Pressure gauge'],
                        'approved_products': ['Test plugs', 'Pressure testing equipment'],
                        'precautions': 'Ensure all connections are secure before pressurizing.'
                    },
                    {
                        'task': 'Cleanup & Documentation',
                        'base_minutes': 15,
                        'minutes_per_sqft': 0,
                        'instructions': 'Clean work area and document completed work.',
                        'method': 'Area restoration and photo documentation',
                        'materials': ['Cleaning supplies', 'Camera'],
                        'approved_products': ['General cleaners'],
                        'precautions': 'Dispose of materials properly according to local regulations.'
                    }
                ]
            },
            'landscaping': {
                'name': 'Landscaping Service',
                'tasks': [
                    {
                        'task': 'Site Preparation',
                        'base_minutes': 45,
                        'minutes_per_sqft': 0.02,
                        'instructions': 'Prepare the landscaping area for work.',
                        'method': 'Clear debris, mark utilities, set up work area',
                        'materials': ['Hand tools', 'Marking paint', 'Tarps'],
                        'approved_products': ['Utility marking paint', 'Site protection materials'],
                        'precautions': 'Call utility locating service before digging. Check for overhead hazards.'
                    },
                    {
                        'task': 'Planting/Installation',
                        'base_minutes': 90,
                        'minutes_per_sqft': 0.08,
                        'instructions': 'Install plants, hardscaping, or other landscape features.',
                        'method': 'Follow landscape design and proper planting techniques',
                        'materials': ['Plants', 'Soil amendments', 'Tools', 'Hardscape materials'],
                        'approved_products': ['Quality nursery stock', 'Approved soil amendments'],
                        'precautions': 'Plant at proper depth. Ensure adequate spacing. Handle plants carefully.'
                    },
                    {
                        'task': 'Irrigation Setup',
                        'base_minutes': 60,
                        'minutes_per_sqft': 0.03,
                        'instructions': 'Install or adjust irrigation systems as needed.',
                        'method': 'Professional irrigation installation and testing',
                        'materials': ['Irrigation components', 'Tools', 'Fittings'],
                        'approved_products': ['Quality irrigation components', 'PVC fittings'],
                        'precautions': 'Test all zones before backfilling. Check for proper coverage.'
                    },
                    {
                        'task': 'Final Grading & Cleanup',
                        'base_minutes': 30,
                        'minutes_per_sqft': 0.01,
                        'instructions': 'Final site grading, cleanup, and client walkthrough.',
                        'method': 'Proper grading for drainage and aesthetic cleanup',
                        'materials': ['Grading tools', 'Cleanup equipment'],
                        'approved_products': ['Topsoil', 'Mulch', 'Seed'],
                        'precautions': 'Ensure proper drainage away from structures.'
                    }
                ]
            },
            'inspection': {
                'name': 'Home Inspection',
                'tasks': [
                    {
                        'task': 'Exterior Inspection',
                        'base_minutes': 60,
                        'minutes_per_sqft': 0,
                        'instructions': 'Comprehensive inspection of exterior components.',
                        'method': 'Systematic visual inspection with documentation',
                        'materials': ['Ladder', 'Camera', 'Measuring tools', 'Checklist'],
                        'approved_products': ['Inspection forms', 'Digital camera'],
                        'precautions': 'Use proper ladder safety. Check for hazardous materials.'
                    },
                    {
                        'task': 'Interior Systems Inspection',
                        'base_minutes': 120,
                        'minutes_per_sqft': 0,
                        'instructions': 'Inspect electrical, plumbing, and HVAC systems.',
                        'method': 'Professional system evaluation with testing equipment',
                        'materials': ['Testing equipment', 'Electrical tester', 'Thermometer'],
                        'approved_products': ['GFCI tester', 'Circuit analyzer', 'Gas detector'],
                        'precautions': 'Do not remove electrical panels. Test GFCI outlets carefully.'
                    },
                    {
                        'task': 'Structural Assessment',
                        'base_minutes': 45,
                        'minutes_per_sqft': 0,
                        'instructions': 'Evaluate structural integrity and foundation.',
                        'method': 'Visual assessment of structural components',
                        'materials': ['Flashlight', 'Moisture meter', 'Level'],
                        'approved_products': ['Moisture detection equipment'],
                        'precautions': 'Do not enter unsafe areas. Note but do not test structural elements.'
                    },
                    {
                        'task': 'Report Compilation',
                        'base_minutes': 90,
                        'minutes_per_sqft': 0,
                        'instructions': 'Compile comprehensive inspection report with photos.',
                        'method': 'Professional report writing with photo documentation',
                        'materials': ['Computer', 'Report template', 'Photo editing software'],
                        'approved_products': ['Inspection software', 'Report templates'],
                        'precautions': 'Ensure all findings are documented accurately.'
                    }
                ]
            }
        }
    
    def get_service_types(self):
        """Get available service types"""
        return [(key, value['name']) for key, value in self.templates.items()]
    
    def generate_tasks(self, service_type, area_size):
        """Generate tasks for a specific service type and area size"""
        if service_type not in self.templates:
            raise ValueError(f"Unknown service type: {service_type}")
        
        template = self.templates[service_type]
        tasks = []
        
        for task_template in template['tasks']:
            # Calculate estimated time based on base time + area-based time
            base_minutes = task_template['base_minutes']
            area_minutes = task_template['minutes_per_sqft'] * area_size
            total_minutes = round(base_minutes + area_minutes)
            
            task = {
                'task': task_template['task'],
                'estimated_minutes': total_minutes,
                'estimated_hours': round(total_minutes / 60, 2),
                'instructions': task_template['instructions'],
                'method': task_template['method'],
                'materials': task_template['materials'],
                'approved_products': task_template['approved_products'],
                'precautions': task_template['precautions']
            }
            
            tasks.append(task)
        
        return tasks
    
    def add_custom_service_type(self, service_type, name, tasks):
        """Add a custom service type with tasks"""
        self.templates[service_type] = {
            'name': name,
            'tasks': tasks
        }
    
    def get_task_template(self, service_type, task_name):
        """Get a specific task template"""
        if service_type in self.templates:
            for task in self.templates[service_type]['tasks']:
                if task['task'] == task_name:
                    return task
        return None
