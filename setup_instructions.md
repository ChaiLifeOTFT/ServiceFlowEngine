# Service Workflow Template - Setup Instructions

This is a generic service workflow management system that can be customized for any task-based service industry including cleaning, plumbing, landscaping, home inspection, and more.

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install flask flask-sqlalchemy werkzeug sendgrid reportlab
   ```

2. **Set Environment Variables**
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   export DATABASE_URL="sqlite:///service_tracker.db"  # or your database URL
   export SENDGRID_API_KEY="your-sendgrid-key"  # optional for email notifications
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

4. **Access the Application**
   - Open your browser to `http://localhost:5000`
   - Start creating service job estimates and tracking tasks

## Customization Guide

### 1. Basic Company Branding

Create a `service_config.json` file in the root directory to customize your branding:

```json
{
  "company_name": "Your Service Company",
  "app_title": "Your Service Management System",
  "app_subtitle": "Professional Service Workflow & Time Management",
  "contact_email": "info@yourcompany.com",
  "phone_number": "(555) 123-4567",
  "address": "123 Your Street, City, State 12345"
}
