# CVision - AI-Powered Resume Analyzer

An intelligent ATS-powered resume analyzer built with **Django**, **spaCy NLP**, **Celery**, and **Redis**.  
CVision helps users understand how well their resumes match job descriptions by generating an **ATS Score**, highlighting **matched & missing keywords**, and offering **improvement suggestions** — all in real-time.


## 🚀 Features

- 🔐 **JWT Authentication** – Secure user login & registration with token-based access.  
- 📄 **Resume & JD Upload** – Accepts `.pdf`, `.docx`, or `.txt` formats.  
- ⚙️ **Asynchronous Processing** – Resume analysis runs in the background using **Celery + Redis**.  
- 🧩 **NLP Analysis** – Extracts skills, keywords, and computes ATS score via **spaCy**.  
- 🕓 **Analysis History** – View past results anytime.  
- 🔔 **Real-Time Notifications** – UI alerts when analysis completes.  
- 🌐 **Responsive UI** – Built with **Django Templates (Jinja2)** and **Bootstrap**.  

---

## 🧰 Tech Stack

| Category | Tools / Frameworks |
|-----------|--------------------|
| **Backend** | Django, Django REST Framework |
| **Auth** | JWT (SimpleJWT) |
| **NLP Engine** | spaCy |
| **Async Tasks** | Celery, Redis |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) |
| **Frontend** | HTML, CSS, Bootstrap, Jinja2 |
| **Deployment** | Render / Railway / AWS |

---

## ⚙️ Setup Instructions

### 🧩 Clone the Repository
```bash
git clone https://github.com/yourusername/cvision-ai-resume-analyzer.git
cd resume_analyzer
```
### 🛠️ Create Virtual Environment & Install Dependencies

``` bash
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```


### ⚙️ Configure Environment Variables
Create a .env file in the root directory and add the following:
```bash
SECRET_KEY=your_django_secret_key
DEBUG=True
REDIS_URL=redis://localhost:6379
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
CELERY_ACCEPT_CONTENT=['json']
CELERY_TASK_SERIALIZER=json
CELERY_RESULT_SERIALIZER=json
CELERY_TIMEZONE=UTC
```

### ⚙️ 🗃️ Apply Migrations & Load spaCy Model

```bash
python manage.py makemigrations
python manage.py migrate
python -m spacy download en_core_web_sm
```

### 🚀 Start Redis & Celery
```bash
Start Redis (via Docker or local install):

docker run -d -p 6379:6379 redis
```
Start Celery Worker:
```bash
celery -A resume_analysis worker -l info
```
### 💻 Run the Django Server
```bash
python manage.py runserver
```

Now visit 👉 http://127.0.0.1:8000

### 🔗 API Endpoints

| **Method** | **Endpoint** | **Description** |
|-------------|--------------|-----------------|
| `POST` | `/api/register/` | Register new user |
| `POST` | `/api/login/` | Obtain JWT tokens |
| `POST` | `/api/analyze_resume/` | Upload resume & JD for analysis |
| `GET` | `api/analyses_history` | View analysis history |
| `GET` | `api/analyses_detail/<uuid:id>/` | Fetch specific analysis result |

### ⚙️ How It Works

- 🔐 **User Authentication:** User logs in and receives a secure JWT token.  
- 📄 **Resume Upload:** User uploads their resume and job description for analysis.  
- ⚙️ **Asynchronous Processing:** Celery processes the input asynchronously in the background.  
- 🧩 **NLP Analysis:** spaCy NLP engine extracts skills, keywords, and calculates the ATS score.  
- 📊 **Results Dashboard:** Displays score, matched & missing keywords, and improvement suggestions.  
- 🕓 **History Access:** User can revisit and review all past analyses anytime.






