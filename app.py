import os
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
import uuid
import json
import stripe

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///service_tracker.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# File upload configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize the app with the extension
db.init_app(app)

# Import models and config after app initialization
from models import Job, Task, CompletedTask
from config import ServiceConfig
from task_templates import TaskTemplateManager

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

with app.app_context():
    db.create_all()

# Initialize service configuration and task templates
service_config = ServiceConfig()
task_manager = TaskTemplateManager()

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
YOUR_DOMAIN = os.environ.get('REPLIT_DEV_DOMAIN', 'http://localhost:5000')

@app.route('/')
def index():
    return render_template('index.html', 
                         service_config=service_config.get_config(),
                         service_types=task_manager.get_service_types())

@app.route('/submit_job', methods=['POST'])
def submit_job():
    try:
        # Get form data
        client_name = request.form.get('client_name', '').strip()
        service_provider_name = request.form.get('service_provider_name', '').strip()
        job_address = request.form.get('job_address', '').strip()
        reference_number = request.form.get('reference_number', '').strip()
        service_area_size = int(request.form.get('service_area_size', 0))
        service_type = request.form.get('service_type', '').strip()
        
        # Validation
        if not all([client_name, service_provider_name, job_address, service_area_size, service_type]):
            flash('All required fields must be filled out.', 'error')
            return redirect(url_for('index'))
        
        # Generate tasks based on service type and area size
        tasks_data = task_manager.generate_tasks(service_type, service_area_size)
        
        # Calculate total time
        total_minutes = sum(task['estimated_minutes'] for task in tasks_data)
        total_hours = round(total_minutes / 60, 2)
        
        # Create job record
        job = Job(
            client_name=client_name,
            service_provider_name=service_provider_name,
            job_address=job_address,
            reference_number=reference_number,
            service_area_size=service_area_size,
            service_type=service_type,
            total_estimated_minutes=total_minutes,
            total_estimated_hours=total_hours,
            tasks_json=json.dumps(tasks_data),
            status='estimated'
        )
        
        db.session.add(job)
        db.session.commit()
        
        # Store job ID in session
        session['current_job_id'] = job.id
        
        return redirect(url_for('submitted', job_id=job.id))
        
    except Exception as e:
        logging.error(f"Error submitting job: {e}")
        flash('An error occurred while processing your request.', 'error')
        return redirect(url_for('index'))

@app.route('/submitted/<int:job_id>')
def submitted(job_id):
    job = Job.query.get_or_404(job_id)
    tasks_data = json.loads(job.tasks_json) if job.tasks_json else []
    
    job_data = {
        'client_name': job.client_name,
        'service_provider_name': job.service_provider_name,
        'job_address': job.job_address,
        'reference_number': job.reference_number,
        'service_area_size': job.service_area_size,
        'service_type': job.service_type,
        'total_estimated_minutes': job.total_estimated_minutes,
        'total_estimated_hours': job.total_estimated_hours,
        'tasks': tasks_data
    }
    
    return render_template('submitted.html', 
                         job_data=job_data,
                         service_config=service_config.get_config())

@app.route('/task/<int:job_id>/<int:task_index>')
def task_detail(job_id, task_index):
    job = Job.query.get_or_404(job_id)
    tasks_data = json.loads(job.tasks_json) if job.tasks_json else []
    
    if task_index >= len(tasks_data):
        flash('Task not found.', 'error')
        return redirect(url_for('index'))
    
    task = tasks_data[task_index]
    
    # Get completed tasks to determine progress
    completed_tasks = CompletedTask.query.filter_by(job_id=job_id).all()
    
    progress = {
        'current': task_index + 1,
        'total': len(tasks_data),
        'percentage': ((task_index) / len(tasks_data)) * 100
    }
    
    job_data = {
        'id': job.id,
        'client_name': job.client_name,
        'service_provider_name': job.service_provider_name,
        'job_address': job.job_address,
        'reference_number': job.reference_number,
        'service_area_size': job.service_area_size,
        'service_type': job.service_type
    }
    
    return render_template('task.html', 
                         task=task,
                         task_index=task_index,
                         job_data=job_data,
                         progress=progress,
                         service_config=service_config.get_config())

@app.route('/complete_task/<int:job_id>/<int:task_index>', methods=['POST'])
def complete_task(job_id, task_index):
    try:
        job = Job.query.get_or_404(job_id)
        tasks_data = json.loads(job.tasks_json) if job.tasks_json else []
        
        if task_index >= len(tasks_data):
            flash('Task not found.', 'error')
            return redirect(url_for('index'))
        
        task = tasks_data[task_index]
        
        # Handle file uploads
        before_photo = None
        after_photo = None
        
        if 'task_before_photo' in request.files:
            file = request.files['task_before_photo']
            if file.filename:
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                before_photo = filename
        
        if 'task_after_photo' in request.files:
            file = request.files['task_after_photo']
            if file.filename:
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                after_photo = filename
        
        # Get task timing and notes
        actual_minutes = int(request.form.get('actual_minutes', task['estimated_minutes']))
        notes = request.form.get('task_notes', '')
        exceptions = request.form.get('exceptions', '')
        
        # Create completed task record
        completed_task = CompletedTask(
            job_id=job_id,
            task_index=task_index,
            task_name=task['task'],
            estimated_minutes=task['estimated_minutes'],
            actual_minutes=actual_minutes,
            before_photo=before_photo,
            after_photo=after_photo,
            notes=notes,
            exceptions=exceptions,
            completed_at=datetime.utcnow()
        )
        
        db.session.add(completed_task)
        db.session.commit()
        
        # Check if this is the last task
        if task_index + 1 >= len(tasks_data):
            # Mark job as complete
            job.status = 'completed'
            job.completed_at = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('job_complete', job_id=job_id))
        else:
            # Go to next task
            return redirect(url_for('task_detail', job_id=job_id, task_index=task_index + 1))
            
    except Exception as e:
        logging.error(f"Error completing task: {e}")
        flash('An error occurred while completing the task.', 'error')
        return redirect(url_for('task_detail', job_id=job_id, task_index=task_index))

@app.route('/job_complete/<int:job_id>')
def job_complete(job_id):
    job = Job.query.get_or_404(job_id)
    completed_tasks = CompletedTask.query.filter_by(job_id=job_id).all()
    
    job_data = {
        'client_name': job.client_name,
        'service_provider_name': job.service_provider_name,
        'job_address': job.job_address,
        'reference_number': job.reference_number,
        'service_area_size': job.service_area_size,
        'service_type': job.service_type,
        'total_estimated_minutes': job.total_estimated_minutes,
        'total_estimated_hours': job.total_estimated_hours,
        'completed_tasks': completed_tasks,
        'job_before_photo': getattr(job, 'job_before_photo', None),
        'job_after_photo': getattr(job, 'job_after_photo', None)
    }
    
    return render_template('job_complete.html', 
                         job_data=job_data,
                         service_config=service_config.get_config())

@app.route('/performance')
def performance():
    period = request.args.get('period', 'month')
    
    # Calculate date range
    now = datetime.utcnow()
    if period == 'week':
        start_date = now - timedelta(days=7)
        period_label = "Last 7 Days"
    elif period == 'month':
        start_date = now - timedelta(days=30)
        period_label = "Last 30 Days"
    else:  # all time
        start_date = datetime.min
        period_label = "All Time"
    
    # Get jobs in period
    jobs = Job.query.filter(
        Job.created_at >= start_date,
        Job.status == 'completed'
    ).all()
    
    # Calculate metrics
    total_jobs = len(jobs)
    total_sqft = sum(job.service_area_size for job in jobs)
    
    # Get all completed tasks for these jobs
    job_ids = [job.id for job in jobs]
    completed_tasks = CompletedTask.query.filter(CompletedTask.job_id.in_(job_ids)).all() if job_ids else []
    
    # Calculate averages
    if completed_tasks:
        avg_completion_time = round(sum(task.actual_minutes for task in completed_tasks) / len(completed_tasks))
        total_estimated = sum(task.estimated_minutes for task in completed_tasks)
        total_actual = sum(task.actual_minutes for task in completed_tasks)
        efficiency_rate = round((total_estimated / total_actual * 100)) if total_actual > 0 else 100
    else:
        avg_completion_time = 0
        efficiency_rate = 100
    
    # Calculate cleaner stats
    cleaner_stats = {}
    for job in jobs:
        provider = job.service_provider_name
        if provider not in cleaner_stats:
            cleaner_stats[provider] = {'jobs': 0, 'total_time': 0, 'estimated_time': 0}
        
        cleaner_stats[provider]['jobs'] += 1
        job_tasks = CompletedTask.query.filter_by(job_id=job.id).all()
        cleaner_stats[provider]['total_time'] += sum(task.actual_minutes for task in job_tasks)
        cleaner_stats[provider]['estimated_time'] += sum(task.estimated_minutes for task in job_tasks)
    
    # Format cleaner stats
    formatted_cleaner_stats = []
    for name, stats in cleaner_stats.items():
        avg_time = round(stats['total_time'] / stats['jobs']) if stats['jobs'] > 0 else 0
        efficiency = round(stats['estimated_time'] / stats['total_time'] * 100) if stats['total_time'] > 0 else 100
        efficiency_class = 'good' if efficiency >= 90 else 'warning' if efficiency >= 75 else 'poor'
        
        formatted_cleaner_stats.append({
            'name': name,
            'job_count': stats['jobs'],
            'avg_time': avg_time,
            'efficiency': efficiency,
            'efficiency_class': efficiency_class
        })
    
    # Task breakdown
    task_breakdown = {}
    for task in completed_tasks:
        name = task.task_name
        if name not in task_breakdown:
            task_breakdown[name] = {'count': 0, 'estimated': 0, 'actual': 0}
        
        task_breakdown[name]['count'] += 1
        task_breakdown[name]['estimated'] += task.estimated_minutes
        task_breakdown[name]['actual'] += task.actual_minutes
    
    # Format task breakdown
    formatted_task_breakdown = []
    for name, stats in task_breakdown.items():
        avg_estimated = round(stats['estimated'] / stats['count']) if stats['count'] > 0 else 0
        avg_actual = round(stats['actual'] / stats['count']) if stats['count'] > 0 else 0
        variance = avg_actual - avg_estimated
        performance = round(avg_estimated / avg_actual * 100) if avg_actual > 0 else 100
        
        formatted_task_breakdown.append({
            'name': name,
            'count': stats['count'],
            'avg_estimated': avg_estimated,
            'avg_actual': avg_actual,
            'variance': variance,
            'performance': min(performance, 100)
        })
    
    metrics = {
        'total_jobs': total_jobs,
        'avg_completion_time': avg_completion_time,
        'efficiency_rate': efficiency_rate,
        'total_sqft': total_sqft
    }
    
    return render_template('performance.html',
                         metrics=metrics,
                         cleaner_stats=formatted_cleaner_stats,
                         task_breakdown=formatted_task_breakdown,
                         period=period,
                         period_label=period_label,
                         service_config=service_config.get_config())

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Simple AI chat endpoint - replace with your preferred AI service"""
    if not request.json:
        return jsonify({'error': 'No JSON data provided'}), 400
    user_message = request.json.get('message', '')
    
    # Generic helpful response - integrate with OpenAI, Claude, etc.
    response = {
        'message': f"I understand you're asking about: '{user_message}'. As your service assistant, I'm here to help with task management, time estimation, and workflow optimization. What specific aspect would you like help with?"
    }
    
    return jsonify(response)

@app.route('/pricing')
def pricing():
    """Display pricing page with subscription options"""
    return render_template('pricing.html', service_config=service_config.get_config())

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create Stripe checkout session for subscription"""
    try:
        price_id = request.form.get('price_id')
        if not price_id:
            flash('Please select a subscription plan.', 'error')
            return redirect(url_for('pricing'))
        
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/pricing',
            automatic_tax={'enabled': True},
        )
        
        if checkout_session.url:
            return redirect(checkout_session.url, code=303)
        else:
            flash('Payment processing error. Please try again.', 'error')
            return redirect(url_for('pricing'))
        
    except Exception as e:
        logging.error(f"Stripe error: {e}")
        flash('Payment processing error. Please try again.', 'error')
        return redirect(url_for('pricing'))

@app.route('/success')
def payment_success():
    """Handle successful payment"""
    session_id = request.args.get('session_id')
    if session_id:
        try:
            # Retrieve the session to get customer details
            session_obj = stripe.checkout.Session.retrieve(session_id)
            flash('Payment successful! Welcome to your subscription.', 'success')
        except Exception as e:
            logging.error(f"Error retrieving session: {e}")
            flash('Payment completed but there was an error. Please contact support.', 'warning')
    
    return render_template('success.html', service_config=service_config.get_config())

@app.route('/cancel')
def payment_cancel():
    """Handle cancelled payment"""
    flash('Payment was cancelled.', 'info')
    return redirect(url_for('pricing'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
