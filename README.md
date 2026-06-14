# ⚡ Ariana Backend PoC: Async Processing & Caching System

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20.svg?logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.x-green.svg?logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-In__Memory-red.svg?logo=redis&logoColor=white)

## 📖 Overview
This repository is a **Proof of Concept (PoC)** engineered to demonstrate high-performance asynchronous task management and distributed caching within a Django environment. 

The core objective is to resolve severe database bottlenecks during heavy computational or I/O-bound tasks (such as financial report generation). By decoupling the request-response cycle, the web server remains fully non-blocking, maximizing throughput and scalability.

## 🏗️ Architectural Pattern
1. **Client Request:** User triggers a request for a heavy financial report.
2. **Cache Lookup (Optimistic):** Django first interrogates **Redis Cache**. If data exists, it returns a response in sub-milliseconds.
3. **Task Offloading:** If a cache miss occurs, Django offloads the processing task to the **Redis Message Broker** via Celery `delay()` and immediately returns a `202 Accepted` status.
4. **Background Execution:** A standalone **Celery Worker** consumes the task from the queue, executes the 10-second processing logic, and persists the final result back into Redis Cache.

## ✨ Key Technical Features
* **Asynchronous Task Queue:** Managed via Celery to ensure user interactions are never blocked by heavy server-side processes.
* **Dual-Purpose Redis Infrastructure:** Leveraged simultaneously as a high-speed message broker (Queue) and an in-memory database engine (Caching).
* **Cross-Platform Thread Pooling:** Configured with specific Windows execution-pool strategies (`-P threads`) to guarantee stability outside native Linux environments.
* **Enterprise Directory Structure:** Clean isolation of business logic (`reports` app) from core configuration settings.

## 🛠️ Tech Stack
* **Framework:** Django 5.x / Django ORM
* **Task Manager:** Celery 5.x
* **In-Memory Store:** Redis 5.0+ (Local/Windows-compatible architecture)
* **Language:** Python 3.11+

## 🚀 Local Setup & Installation

### Prerequisites
Ensure you have a local Redis server running on port `6379`. 

### Installation Steps
1. **Clone the repository:**
```bash
git clone [https://github.com/Abolfazlparadox/Ariana_PoC.git](https://github.com/Abolfazlparadox/Ariana_PoC.git)
cd Ariana_PoC

```

2. **Initialize and Activate Virtual Environment:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

```


3. **Install Dependencies:**
```powershell
pip install -r requirements.txt

```


4. **Run Database Migrations:**
```powershell
python manage.py migrate

```



## 💻 Running the Application

To test the complete asynchronous cycle, execute the following components in **two separate terminal instances**:

### Terminal 1: Launch Celery Worker

```powershell
celery -A core.celery worker --loglevel=info -P threads

```

### Terminal 2: Start Django Web Server

```powershell
python manage.py runserver

```

### Verification Endpoint

Open your browser or Postman and trigger:
`http://127.0.0.1:8000/reports/financial/?id=10`

* **1st Trigger (Cache Miss):** Immediate JSON response confirming the task has been queued. Server thread is released instantly.
* **2nd Trigger (Cache Hit - After 10s):** Blazing fast delivery of the populated report data directly from Redis memory.

## 🔍 Deep-Dive: Troubleshooting & Compatibility Lessons

During development on Windows environments, a protocol mismatch arose where modern Python `redis` clients attempted to utilize the **RESP3** protocol (`HELLO 3` command) which is unsupported by legacy Windows Redis binaries (v5.0).

**Resolution:** This architectural bottleneck was seamlessly mitigated by downgrading the transport layer client to `redis==4.5.5` inside the `requirements.txt`, ensuring complete backward compatibility, rock-solid stability, and preventing runtime `ResponseError` exceptions without modifying core business logic.

## ✉️ Contact & Developer Profile

**Abolfazl Mohammadshahi** - Software Engineer

* [LinkedIn](https://www.linkedin.com/in/abolfazl-mohammadshahi-12b87b324)
* [GitHub](https://github.com/Abolfazlparadox)
* Email: abolfazlmohammadshahi78@gmail.com
