\# 🩺 Healthcare AI



\### Local AI-Powered Healthcare Screening \& Appointment System



Healthcare AI is a local, API-free healthcare screening and appointment booking system that combines \*\*voice input, NLP-based symptom extraction, machine learning prediction, specialist recommendation, and SQLite-based appointment management\*\* into one workflow.



> ⚠️ \*\*Disclaimer:\*\* This project is an educational demonstration and is not a medical diagnosis or a replacement for professional medical care.



\---



\## 📌 Problem Statement



Many healthcare applications depend on external AI APIs or complex cloud infrastructure.



This project demonstrates how a lightweight healthcare assistant can be built using \*\*local technologies\*\* without relying on paid AI APIs.



The system allows a user to:



1\. Describe symptoms using voice or text.

2\. Extract recognizable symptoms using local NLP.

3\. Predict possible conditions using a locally trained ML model.

4\. Recommend a relevant medical specialist.

5\. Search locally stored doctors.

6\. View available appointment slots.

7\. Book an appointment using a local SQLite database.



\---



\## ✨ Key Features



\### 🎙️ Voice Input

Uses the browser's \*\*Web Speech API\*\* to convert spoken symptoms into text.



\### 🧠 Local NLP

A rule-based NLP processor identifies recognized symptoms from natural-language descriptions.



Example:



```text

"I have a headache and I have been vomiting since morning."

```



becomes:



```text

headache

vomiting

```



\### 🤖 Machine Learning Prediction

A \*\*Multinomial Naive Bayes\*\* classifier trained on a local symptom dataset generates possible condition matches.



\### 👨‍⚕️ Specialist Recommendation

The predicted condition is mapped to an appropriate specialist category.



\### 🗄️ Local SQLite Database

The database stores:



\- Doctors

\- Appointment slots

\- Appointments

\- Symptom history



\### 📅 Appointment Booking

Users can:



\- Select a doctor

\- View available slots

\- Enter patient details

\- Book an appointment

\- Receive an appointment confirmation



\### 🚨 Safety Layer

The frontend includes an emergency check for combinations such as:



```text

Chest pain + difficulty breathing

```



The system stops the normal screening flow and displays an urgent medical warning.



\---



\# 🏗️ System Workflow



```text

&#x20;       🎙️ Voice / 📝 Text

&#x20;               │

&#x20;               ▼

&#x20;      Web Speech API

&#x20;               │

&#x20;               ▼

&#x20;      Local NLP Processor

&#x20;               │

&#x20;               ▼

&#x20;      Symptom Extraction

&#x20;               │

&#x20;               ▼

&#x20;         Safety Check

&#x20;               │

&#x20;               ▼

&#x20;      Machine Learning Model

&#x20;      Multinomial Naive Bayes

&#x20;               │

&#x20;               ▼

&#x20;      Possible Condition

&#x20;               │

&#x20;               ▼

&#x20;     Specialist Recommendation

&#x20;               │

&#x20;               ▼

&#x20;         SQLite Database

&#x20;               │

&#x20;               ▼

&#x20;       Doctor Selection

&#x20;               │

&#x20;               ▼

&#x20;      Available Appointment

&#x20;            Slots

&#x20;               │

&#x20;               ▼

&#x20;      Patient Information

&#x20;               │

&#x20;               ▼

&#x20;      Appointment Booking

```



\---



\# 🧩 System Architecture



The application consists of three major layers.



\## 1. Frontend



Technologies:



\- HTML

\- CSS

\- JavaScript

\- Web Speech API



Responsibilities:



\- User interface

\- Voice input

\- Symptom input

\- Display prediction results

\- Doctor selection

\- Slot selection

\- Appointment form

\- Booking confirmation



\---



\## 2. Backend



Technologies:



\- Python

\- FastAPI

\- Pydantic



The backend provides REST API endpoints for:



```text

GET  /

GET  /health

POST /predict

GET  /doctors

GET  /doctors/{doctor\_id}/slots

POST /appointments

```



\---



\## 3. Data \& Machine Learning Layer



Technologies:



\- Pandas

\- Scikit-Learn

\- Joblib

\- SQLite



The ML model uses the symptom dataset to generate condition predictions.



The SQLite database manages doctors, appointment slots and bookings.



\---



\# 🤖 Machine Learning



The project uses:



```text

Multinomial Naive Bayes

```



The model is trained using binary symptom features.



Example features include:



```text

fever

cough

fatigue

headache

sore\_throat

runny\_nose

shortness\_of\_breath

chest\_pain

wheezing

dizziness

nausea

vomiting

skin\_rash

itching

joint\_pain

muscle\_ache

palpitations

loss\_of\_appetite

high\_fever

chills

```



The training script performs a manual \*\*75/25 train-test split\*\*.



The current demonstration dataset contains:



```text

39 rows

20 symptom features

10 condition classes

```



The model artifacts are stored using Joblib.



\---



\# 🧠 NLP Processing



The project does not use an external AI API for symptom extraction.



Instead, the local NLP processor uses predefined patterns and regular expressions.



For example:



```text

"my head hurts"

```



can be mapped to:



```text

headache

```



Similarly:



```text

"throwing up"

```



can be mapped to:



```text

vomiting

```



This keeps the system:



\- Local

\- Fast

\- API-free

\- Easy to demonstrate

\- Easy to understand



\---



\# 🏥 Specialist Mapping



The system maps predicted conditions to specialist categories.



Examples:



| Condition | Specialist |

|---|---|

| Common Cold | General Physician |

| Flu | General Physician |

| Malaria | General Physician |

| Acne | Dermatologist |

| Eczema | Dermatologist |

| Asthma | Pulmonologist |

| Bronchitis | Pulmonologist |

| Hypertension | Cardiologist |

| Coronary Artery Disease | Cardiologist |

| Migraine | Neurologist |



\---



\# 🗄️ Database



The project uses SQLite.



Database tables include:



```text

doctors

slots

appointments

symptom\_history

```



\### Doctors



Stores:



\- Doctor name

\- Specialization

\- Hospital

\- Contact

\- Consultation fee



\### Slots



Stores:



\- Doctor

\- Date

\- Start time

\- End time

\- Booking status



\### Appointments



Stores:



\- Patient name

\- Contact

\- Doctor

\- Slot

\- Predicted condition

\- Symptoms

\- Creation timestamp



\---



\# 📂 Project Structure



```text

Healthcare-AI/

│

├── backend/

│   │

│   ├── data/

│   │   └── symptoms\_dataset.csv

│   │

│   ├── models/

│   │   ├── disease\_classifier.joblib

│   │   └── mlb.joblib

│   │

│   ├── database.py

│   ├── nlp\_processor.py

│   ├── predictor.py

│   ├── seed\_data.py

│   ├── test\_pipeline.py

│   └── train\_model.py

│

├── frontend/

│   ├── app.js

│   ├── index.html

│   └── style.css

│

├── main.py

├── .gitignore

└── README.md

```



\---



\# ⚙️ Installation



\## 1. Clone the repository



```bash

git clone https://github.com/YOUR\_USERNAME/Healthcare-AI.git

```



Move into the project:



```bash

cd Healthcare-AI

```



\---



\## 2. Create a virtual environment



Windows:



```powershell

python -m venv venv

```



Activate it:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\---



\## 3. Install dependencies



Install the required packages:



```powershell

pip install fastapi uvicorn pandas scikit-learn joblib pydantic

```



\---



\# 🗄️ Initialize the Database



Run:



```powershell

python backend/seed\_data.py

```



This creates the local SQLite database and seeds doctors and appointment slots.



\---



\# 🤖 Train the Model



Run:



```powershell

python backend/train\_model.py

```



This generates:



```text

backend/models/disease\_classifier.joblib

backend/models/mlb.joblib

```



\---



\# 🚀 Run the Backend



From the project root:



```powershell

python -m uvicorn main:app --reload

```



Backend:



```text

http://127.0.0.1:8000

```



API documentation:



```text

http://127.0.0.1:8000/docs

```



\---



\# 🌐 Run the Frontend



Open another terminal:



```powershell

python -m http.server 5500 --directory frontend

```



Then open:



```text

http://127.0.0.1:5500

```



\---



\# 🧪 Example Demo



Enter:



```text

I have a headache, nausea and I have been vomiting since morning.

```



The system:



```text

1\. Extracts symptoms

&#x20;      ↓

2\. Identifies:

&#x20;  headache

&#x20;  nausea

&#x20;  vomiting

&#x20;      ↓

3\. Runs ML prediction

&#x20;      ↓

4\. Displays possible condition

&#x20;      ↓

5\. Recommends a specialist

&#x20;      ↓

6\. Displays doctors

&#x20;      ↓

7\. Displays appointment slots

&#x20;      ↓

8\. Books appointment

```



\---



\# 🚨 Safety Demonstration



The application contains an emergency safety layer.



For example:



```text

I have chest pain and difficulty breathing.

```



The normal screening flow is stopped and an urgent warning is displayed.



This demonstrates that emergency symptom combinations are handled separately rather than being treated as an ordinary prediction request.



\---



\# 🛠️ Technology Stack



| Layer | Technology |

|---|---|

| Frontend | HTML, CSS, JavaScript |

| Voice | Web Speech API |

| Backend | Python, FastAPI |

| NLP | Python Regex / Rule-based NLP |

| ML | Scikit-Learn |

| Model | Multinomial Naive Bayes |

| Data Processing | Pandas |

| Model Storage | Joblib |

| Database | SQLite |

| API | REST |

| Version Control | Git / GitHub |



\---



\# 🔐 Privacy \& API-Free Design



The core processing pipeline does not require:



\- OpenAI API

\- Gemini API

\- Cloud AI APIs

\- Paid AI services



The ML model and NLP processing run locally.



The appointment database is also local.



This makes the project suitable for offline classroom demonstrations after dependencies have been installed.



\---



\# 🔮 Future Scope



Possible future improvements include:



\- Larger and medically validated datasets

\- More advanced NLP

\- Transformer-based symptom understanding

\- Multilingual voice input

\- Authentication

\- Doctor dashboard

\- Patient dashboard

\- Appointment cancellation

\- Medical record management

\- Cloud deployment

\- Mobile application

\- More advanced emergency detection

\- Explainable ML predictions



\---



\# ⚠️ Disclaimer



Healthcare AI is an educational software project.



Its predictions are generated from a small demonstration dataset and should \*\*not\*\* be considered medical advice, diagnosis, treatment recommendations, or a substitute for qualified healthcare professionals.



For real medical concerns, consult an appropriately qualified healthcare professional.



\---



\# 👨‍💻 Project



\*\*Healthcare AI\*\*



A college project demonstrating the integration of:



```text

Voice Recognition

&#x20;       +

NLP

&#x20;       +

Machine Learning

&#x20;       +

FastAPI

&#x20;       +

SQLite

&#x20;       +

Appointment Management

```



Built as a local, API-free AI healthcare demonstration.

```



