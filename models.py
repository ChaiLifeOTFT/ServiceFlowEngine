from app import db
from datetime import datetime
from sqlalchemy import Text

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    service_provider_name = db.Column(db.String(100), nullable=False)
    job_address = db.Column(db.String(200), nullable=False)
    reference_number = db.Column(db.String(50), nullable=True)
    service_area_size = db.Column(db.Integer, nullable=False)  # square footage or other unit
    service_type = db.Column(db.String(50), nullable=False)
    total_estimated_minutes = db.Column(db.Integer, nullable=False)
    total_estimated_hours = db.Column(db.Float, nullable=False)
    tasks_json = db.Column(Text, nullable=True)  # JSON string of task details
    status = db.Column(db.String(20), default='estimated')  # estimated, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    job_before_photo = db.Column(db.String(255), nullable=True)
    job_after_photo = db.Column(db.String(255), nullable=True)
    
    # Relationships
    completed_tasks = db.relationship('CompletedTask', backref='job', cascade='all, delete-orphan')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    base_minutes = db.Column(db.Integer, nullable=False)
    minutes_per_unit = db.Column(db.Float, nullable=False)  # minutes per sq ft or other unit
    instructions = db.Column(Text, nullable=False)
    method = db.Column(Text, nullable=False)
    materials = db.Column(Text, nullable=False)  # JSON array of materials
    approved_products = db.Column(Text, nullable=False)  # JSON array of products
    precautions = db.Column(Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class CompletedTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    task_index = db.Column(db.Integer, nullable=False)
    task_name = db.Column(db.String(100), nullable=False)
    estimated_minutes = db.Column(db.Integer, nullable=False)
    actual_minutes = db.Column(db.Integer, nullable=False)
    before_photo = db.Column(db.String(255), nullable=True)
    after_photo = db.Column(db.String(255), nullable=True)
    notes = db.Column(Text, nullable=True)
    exceptions = db.Column(Text, nullable=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
