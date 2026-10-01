\# Cloud Data Redundancy Removal System



A cloud-based web application for managing user data and reducing redundant records through duplicate email validation and centralized database management.



The application is built using Flask and SQLite and deployed on an AWS EC2 instance using Gunicorn and Nginx.



\---



\## 🚀 Project Overview



The Cloud Data Redundancy Removal System is designed to maintain unique user records by validating email addresses before storing new data.



The application provides a simple web interface where users can:



\- Add new records

\- Validate duplicate email addresses

\- View stored records

\- Track total unique records

\- Delete existing records

\- Manage data through a centralized SQLite database



\---



\## 🎯 Problem Statement



Duplicate data can increase storage usage, reduce data quality and make database management more difficult.



This project provides a simple solution that validates user information before inserting records into the database and prevents duplicate email entries.



\---



\## ✨ Features



\- Duplicate email detection

\- Unique record management

\- Add new user records

\- Delete existing records

\- Total unique record counter

\- SQLite database integration

\- Flask web application

\- AWS EC2 deployment

\- Gunicorn WSGI server

\- Nginx reverse proxy

\- Linux server environment

\- Systemd service for application management



\---



\## 🏗️ Technology Stack



\### Application



\- Python

\- Flask

\- SQLite

\- HTML

\- CSS



\### Cloud \& Infrastructure



\- Amazon EC2

\- Amazon Linux 2023

\- Nginx

\- Gunicorn

\- systemd



\### Development \& Version Control



\- Git

\- GitHub

\- Windows PowerShell

\- Linux Terminal



\---



\## ☁️ AWS Deployment Architecture



```text

&#x20;                   Internet

&#x20;                      |

&#x20;                      v

&#x20;             Public EC2 IP Address

&#x20;                      |

&#x20;                      v

&#x20;                 AWS EC2

&#x20;             Amazon Linux 2023

&#x20;                      |

&#x20;                      v

&#x20;                   Nginx

&#x20;               Reverse Proxy

&#x20;                      |

&#x20;                      v

&#x20;                 Gunicorn

&#x20;                      |

&#x20;                      v

&#x20;                Flask App

&#x20;                      |

&#x20;                      v

&#x20;                SQLite Database

&#x20;                   data.db

---

## 📸 Application Screenshot

The following screenshot shows the deployed Cloud Data Redundancy Removal System running on AWS EC2.

![Cloud Data Redundancy Removal System](screenshots/cloud-data-redundancy-system.png)

---

### Architecture Diagram

The following diagram represents the deployed AWS infrastructure and application request flow.

![AWS Architecture Diagram](screenshots/aws-architecture-diagram.png)

---

## ⚙️ Infrastructure & Deployment Details

### Amazon EC2

The Flask application is deployed on an Amazon EC2 instance running Amazon Linux 2023.

### Security Group

The EC2 Security Group controls inbound network traffic to the instance.

- HTTP — TCP port 80 — allows web application access
- SSH — TCP port 22 — restricted to the administrator's public IP address

### Nginx

Nginx is configured as a reverse proxy and listens for HTTP requests on port 80.

Incoming requests are forwarded to the Gunicorn application server using:

`http://127.0.0.1:5000`

### Gunicorn

Gunicorn acts as the WSGI application server and runs the Flask application on port 5000.

### Systemd

A dedicated `codealpha.service` systemd service manages the Flask/Gunicorn application.

The service is enabled to start automatically with the server.

### Database

SQLite is used as the application's database for storing user records and preventing duplicate email entries.

---

## 🔄 Deployment Flow

1. User sends an HTTP request to the EC2 public IP.
2. AWS Security Group allows HTTP traffic on port 80.
3. Nginx receives the request.
4. Nginx forwards the request to Gunicorn at `127.0.0.1:5000`.
5. Gunicorn serves the Flask application.
6. Flask processes the request and interacts with the SQLite database.
7. The response is returned to the user through Nginx.

