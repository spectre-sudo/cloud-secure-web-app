# Cloud-Based Secure Web Application Architecture

## Overview

This project implements a secure cloud-native DevSecOps web application deployed on AWS infrastructure.

## Architecture Components

### Client Layer

Users access the application through a web browser over HTTP/HTTPS.

### Nginx Reverse Proxy

Nginx acts as a reverse proxy server handling incoming traffic and forwarding requests to the Flask application container.

### Flask Application

The application is developed using Python Flask and provides:

* User registration and login
* Role-based access control
* CRUD task management
* Session authentication
* Security protections

### Docker Container

The Flask application is containerized using Docker to ensure portability and consistent deployment across environments.

### AWS EC2

The Dockerized application is deployed on an Ubuntu EC2 instance hosted inside a custom AWS VPC.

### AWS Networking

The infrastructure includes:

* Custom VPC
* Public and private subnets
* Route tables
* Internet Gateway
* NAT Gateway
* Security Groups

### AWS S3

Amazon S3 is configured for secure cloud storage and backup purposes.

### AWS CloudWatch

CloudWatch is used for:

* Infrastructure monitoring
* CPU metrics
* Alert generation
* Operational visibility

### CI/CD Pipeline

GitHub Actions provides automated CI/CD workflow execution on code push events.

## Security Features

The project implements multiple security controls:

* bcrypt password hashing
* Role-based access control
* SQL injection protection using SQLAlchemy ORM
* XSS mitigation through Jinja2 escaping
* Security headers
* Docker isolation
* AWS Security Groups
* SSH-based administration

## Deployment Flow

1. Developer pushes code to GitHub
2. GitHub Actions pipeline executes
3. Docker container is built
4. Application deployed on AWS EC2
5. Nginx routes traffic to Flask container
6. CloudWatch monitors infrastructure metrics
