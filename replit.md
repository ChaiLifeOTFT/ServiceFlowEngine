# Overview

This is a professional service workflow management system designed for task-based service industries. The application provides comprehensive job estimation, task tracking, time management, and performance analytics capabilities. It operates as a generic template that can be customized for various service industries including cleaning, plumbing, landscaping, home inspection, and maintenance services.

The system handles the complete service workflow from initial job estimation through task execution to completion documentation, with features like photo documentation, time tracking, performance metrics, and email notifications.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Application Framework
- **Flask-based Web Application**: Built with Python Flask providing server-side rendering and RESTful API endpoints
- **SQLAlchemy ORM**: Database abstraction layer with declarative models for job, task, and completion tracking
- **Responsive Web Interface**: Bootstrap-powered responsive design optimized for mobile field use with touch-friendly controls

## Database Design
- **Job Management**: Central Job model tracking client information, service details, estimated times, and completion status
- **Task Templates**: Template-based task system with configurable task definitions including time estimates, instructions, materials, and safety precautions
- **Completion Tracking**: CompletedTask model for recording actual vs estimated times, photos, notes, and exceptions
- **Performance Analytics**: Historical data collection for efficiency analysis and team performance metrics

## Configuration Management
- **Dynamic Branding**: ServiceConfig class enables white-label customization through JSON configuration files
- **Industry Adaptation**: Configurable field labels, service units, and terminology to adapt to different service industries
- **Template Management**: TaskTemplateManager provides industry-specific task libraries with detailed instructions

## File Upload System
- **Photo Documentation**: Before/after photo capture and storage for task documentation
- **Secure File Handling**: UUID-based file naming with size and type validation
- **Mobile Optimization**: Camera-friendly upload interface optimized for field use

## Performance Tracking
- **Real-time Analytics**: Time efficiency tracking comparing estimated vs actual task completion times
- **Historical Metrics**: Trend analysis across different time periods (weekly, monthly, all-time)
- **Team Performance**: Individual and aggregate performance metrics with visual dashboards

## Workflow Engine
- **Sequential Task Processing**: Guided step-by-step task execution with progress tracking
- **Timer Integration**: Built-in timing system for accurate task duration measurement
- **Status Management**: Job lifecycle tracking from estimation through completion

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web application framework for routing, templating, and request handling
- **Flask-SQLAlchemy**: Database ORM providing model definitions and query capabilities
- **Werkzeug**: WSGI utilities for file uploads, security helpers, and middleware support

## Frontend Libraries
- **Bootstrap 5**: Responsive CSS framework with dark theme support
- **Font Awesome**: Icon library for UI elements and visual indicators
- **Chart.js**: JavaScript charting library for performance analytics visualization

## Email Service Integration
- **SendGrid**: Email delivery service for job completion notifications and client communications
- **Optional Configuration**: Email functionality gracefully degrades if API keys are not configured

## Document Generation
- **ReportLab**: PDF generation library for creating professional service reports and documentation
- **QR Code Generation**: QR code creation for job tracking and mobile access

## File Storage
- **Local File System**: Static file storage for uploaded photos and generated documents
- **Configurable Upload Directory**: Centralized file management with size and type restrictions

## Database Support
- **SQLite**: Default embedded database for development and small deployments
- **PostgreSQL Compatible**: Architecture supports PostgreSQL for production deployments
- **Environment-based Configuration**: Database selection through environment variables