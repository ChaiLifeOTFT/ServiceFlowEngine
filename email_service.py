import os
import sys
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from config import ServiceConfig
import logging

class EmailService:
    """Service for sending email notifications"""
    
    def __init__(self):
        self.config = ServiceConfig()
        self.api_key = os.environ.get('SENDGRID_API_KEY')
        
        if not self.api_key:
            logging.warning('SENDGRID_API_KEY not set - email functionality disabled')
    
    def send_job_completion_email(self, job_data, to_email):
        """Send job completion notification email"""
        if not self.api_key:
            logging.warning('Cannot send email - SENDGRID_API_KEY not configured')
            return False
        
        try:
            config = self.config.get_config()
            
            # Create email content
            subject = config['email_templates']['job_completion_subject'].format(
                client_name=job_data.get('client_name', 'Client')
            )
            
            html_content = self._generate_completion_email_html(job_data)
            
            # Send email
            sg = SendGridAPIClient(self.api_key)
            
            message = Mail(
                from_email=Email(config['email_templates']['job_completion_from']),
                to_emails=To(to_email),
                subject=subject
            )
            
            message.content = Content("text/html", html_content)
            
            sg.send(message)
            return True
            
        except Exception as e:
            logging.error(f"SendGrid error: {e}")
            return False
    
    def _generate_completion_email_html(self, job_data):
        """Generate HTML content for job completion email"""
        config = self.config.get_config()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; }}
                .content {{ margin: 20px 0; }}
                .footer {{ background-color: #e9ecef; padding: 15px; border-radius: 8px; font-size: 12px; }}
                .task-list {{ margin: 15px 0; }}
                .task-item {{ padding: 10px; border-left: 3px solid #007bff; margin: 5px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>{config['company_name']}</h2>
                <h3>Service Job Completion Notice</h3>
            </div>
            
            <div class="content">
                <p>Dear {job_data.get('client_name', 'Valued Client')},</p>
                
                <p>We are pleased to inform you that your service job has been completed successfully.</p>
                
                <h4>Job Details:</h4>
                <ul>
                    <li><strong>Service Address:</strong> {job_data.get('job_address', 'N/A')}</li>
                    <li><strong>Service Type:</strong> {job_data.get('service_type', 'N/A')}</li>
                    <li><strong>Service Provider:</strong> {job_data.get('service_provider_name', 'N/A')}</li>
                    <li><strong>Service Area:</strong> {job_data.get('service_area_size', 'N/A')} {config['service_unit_abbr']}</li>
                    <li><strong>Total Time:</strong> {job_data.get('total_estimated_hours', 'N/A')} hours</li>
                </ul>
                
                <h4>Completed Tasks:</h4>
                <div class="task-list">
        """
        
        # Add task details if available
        if 'completed_tasks' in job_data:
            for task in job_data['completed_tasks']:
                html += f"""
                    <div class="task-item">
                        <strong>{task.task_name}</strong><br>
                        <small>Completed in {task.actual_minutes} minutes</small>
                    </div>
                """
        
        html += f"""
                </div>
                
                <p>Thank you for choosing {config['company_name']} for your service needs. If you have any questions or concerns about the completed work, please don't hesitate to contact us.</p>
            </div>
            
            <div class="footer">
                <p><strong>{config['company_name']}</strong><br>
                {config['address']}<br>
                Phone: {config['phone_number']}<br>
                Email: {config['contact_email']}</p>
            </div>
        </body>
        </html>
        """
        
        return html
