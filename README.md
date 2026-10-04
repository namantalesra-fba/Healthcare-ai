# 🩺 Healthcare AI

### Voice-Assisted Healthcare Screening & Appointment Scheduling

A local, API-free healthcare assistance prototype that combines **voice input, rule-based NLP, machine learning, specialist recommendation, doctor lookup, and appointment scheduling** into one workflow.

> ⚠️ **Medical Disclaimer:** This is an educational software prototype. It is **not a medical diagnosis system** and must not replace a qualified healthcare professional. Predictions are illustrative screening results based on a synthetic educational dataset.

---

## 📌 Project Overview

Healthcare AI is a web-based application designed to simplify the initial healthcare interaction.

A user can:

1. Enter symptoms using text or voice.
2. Convert voice into text using the browser's Web Speech API.
3. Extract recognized symptoms using rule-based NLP.
4. Detect explicit disease mentions such as hypertension or asthma.
5. Perform a basic safety check for selected red-flag symptoms.
6. Predict a possible condition using a locally trained **Bernoulli Naive Bayes** model.
7. Receive a recommended specialist category.
8. View available doctors.
9. View available appointment slots.
10. Book an appointment.
11. Store appointment and symptom information in a local SQLite database.

### Complete Flow

```text
Voice / Text Input
        ↓
Web Speech API
        ↓
Rule-Based NLP
        ↓
Safety Check
        ↓
Bernoulli Naive Bayes
        ↓
Possible Condition
        ↓
Specialist Mapping
        ↓
Doctor Lookup
        ↓
Available Slots
        ↓
Appointment Booking
        ↓
SQLite Database
```

---

# 🎯 Problem Statement

Healthcare portals can make the initial patient interaction unnecessarily complicated.

Common problems include:

- Complex forms and manual data entry
- Difficulty describing symptoms using medical terminology
- Confusion about which specialist to consult
- Separate symptom-checking and appointment-booking workflows
- Repetitive basic intake tasks

### Our Approach

Healthcare AI combines these steps into one simple workflow:

```text
Patient Symptoms
      ↓
Basic Screening Assistance
      ↓
Specialist Recommendation
      ↓
Doctor Selection
      ↓
Appointment Booking
```

---

# ✨ Key Features

| Feature | Description |
|---|---|
| 🎙️ Voice Input | Browser-based speech-to-text using Web Speech API |
| ⌨️ Text Input | Direct symptom entry |
| 🧠 Rule-Based NLP | Recognizes predefined symptoms and aliases |
| 🤖 ML Prediction | Local Bernoulli Naive Bayes model |
| 🛡️ Safety Check | Checks selected red-flag symptom combinations |
| 👨‍⚕️ Specialist Mapping | Maps possible conditions to specialist categories |
| 🏥 Doctor Lookup | Retrieves doctors from SQLite |
| 📅 Slot Management | Displays available appointment slots |
| ✅ Appointment Booking | Stores confirmed appointments locally |
| 🗄️ SQLite Storage | Stores doctors, slots, appointments and symptom history |
| 🔒 Local ML | Core prediction does not require an external AI API |

---

# 🧠 How It Works

## 1. Voice or Text Input

Example:

```text
I have fever, headache and chills.
```

The user can either type the sentence or speak through the microphone.

## 2. Speech-to-Text

```text
🎙️ Voice
   ↓
Web Speech API
   ↓
"I have fever, headache and chills."
```

## 3. Rule-Based NLP

The local NLP processor identifies recognized symptoms.

```text
"I have fever, headache and chills."
              ↓
fever
headache
chills
```

It can also recognize aliases such as:

```text
high BP     → Hypertension
pimples     → Acne
asthmatic   → Asthma
```

## 4. Safety Check

Before normal ML screening, the application checks selected red-flag symptoms.

Example:

```text
Chest pain + difficulty breathing
              ↓
       Urgent Warning
```

This is only a basic software safeguard and is **not an emergency medical detection system**.

## 5. Machine Learning

Symptoms are converted into binary features:

```text
1 = Present
0 = Absent
```

Example:

```text
fever       = 1
cough       = 0
headache    = 1
vomiting    = 0
chills      = 1
```

These features are passed to the local **Bernoulli Naive Bayes** model.

## 6. Possible Condition

The model returns a ranked prediction.

Example:

```text
Possible Condition:
Malaria

Confidence:
98.80%
```

This is a screening prediction, **not a diagnosis**.

## 7. Specialist Recommendation

Examples:

```text
Asthma
   ↓
Pulmonologist
```

```text
Migraine
   ↓
Neurologist
```

```text
Acne / Eczema
   ↓
Dermatologist
```

## 8. Doctor and Slot Selection

The application retrieves matching doctors and available appointment slots from SQLite.

## 9. Appointment Booking

The user enters patient details, selects a slot, and confirms the appointment.

The selected slot is marked as booked.

---

# 🏗️ System Architecture

```text
                         USER
                          │
                 ┌────────┴────────┐
                 │                 │
               VOICE              TEXT
                 │                 │
                 └────────┬────────┘
                          │
                          ▼
                ┌─────────────────┐
                │  Web Speech API │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Rule-Based NLP  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Safety Check   │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
          Red Flag                Normal
              │                     │
              ▼                     ▼
       Urgent Warning       Bernoulli Naive
                              Bayes Model
                                   │
                                   ▼
                          Possible Condition
                                   │
                                   ▼
                         Specialist Mapping
                                   │
                                   ▼
                              FastAPI
                                   │
                                   ▼
                              SQLite
                                   │
                  ┌────────────────┼────────────────┐
                  │                │                │
               Doctors           Slots        Appointments
```

---

# 🤖 Machine Learning

## Model

### Bernoulli Naive Bayes

The project uses Bernoulli Naive Bayes because the symptom representation is binary:

```text
1 → Symptom Present
0 → Symptom Absent
```

The model learns patterns between symptom presence/absence and condition labels in the training dataset.

### Prediction Flow

```text
User Symptoms
      ↓
Recognized Symptoms
      ↓
Binary Features
      ↓
Bernoulli Naive Bayes
      ↓
Ranked Predictions
      ↓
Possible Condition
```

---

# 📊 Model Evaluation

The current model uses a **500-record synthetic educational dataset**.

| Metric | Value |
|---|---:|
| Total Records | 500 |
| Training Records | 375 |
| Testing Records | 125 |
| Symptom Features | 20 |
| Conditions | 10 |
| Test Accuracy | **96.80%** |

> **Important:** This accuracy is measured on a synthetic educational test dataset. It does not represent clinical accuracy and has not been medically validated.

---

# 🧪 Dataset

The dataset is synthetic and intended for academic demonstration.

### Dataset Size

```text
500 Records
20 Symptom Features
10 Conditions
50 Records per Condition
```

### Supported Conditions

1. Common Cold
2. Flu
3. Migraine
4. Acne
5. Eczema
6. Asthma
7. Bronchitis
8. Hypertension
9. Coronary Artery Disease
10. Malaria

### Symptom Features

```text
fever
cough
fatigue
headache
sore_throat
runny_nose
shortness_of_breath
chest_pain
wheezing
dizziness
nausea
vomiting
skin_rash
itching
joint_pain
muscle_ache
palpitations
loss_of_appetite
high_fever
chills
```

---

# 🩺 Specialist Mapping

| Possible Condition | Specialist |
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

This mapping is part of the educational application workflow and is not a substitute for professional medical referral.

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Voice | Web Speech API |
| Backend | Python, FastAPI, Pydantic |
| Server | Uvicorn |
| NLP | Python Regex / Rule-Based NLP |
| Machine Learning | Bernoulli Naive Bayes |
| Data Processing | Pandas |
| Model Storage | JSON |
| Database | SQLite |
| API Style | REST |
| Development | VS Code |
| Version Control | Git / GitHub |

---

# 📂 Project Structure

```text
Healthcare ai/
│
├── backend/
│   ├── data/
│   │   ├── symptoms_dataset.csv
│   │   └── medivoice.db
│   │
│   ├── models/
│   │   └── disease_classifier.json
│   │
│   ├── database.py
│   ├── seed_data.py
│   ├── nlp_processor.py
│   ├── train_model.py
│   ├── predictor.py
│   └── test_pipeline.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🗄️ Database

The application uses a local SQLite database:

```text
backend/data/medivoice.db
```

## Doctors

```text
id
name
specialization
hospital
contact
fee
```

## Slots

```text
id
doctor_id
date
start_time
end_time
is_booked
```

## Appointments

```text
id
slot_id
doctor_id
patient_name
patient_contact
disease_predicted
symptoms
created_at
```

## Symptom History

```text
id
patient_name
symptoms
disease_predicted
created_at
```

---

# 🔌 API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Application status |
| GET | `/health` | Backend health check |
| POST | `/predict` | Process symptoms and return prediction |
| GET | `/doctors` | Retrieve doctors |
| GET | `/doctors/{doctor_id}/slots` | Retrieve available slots |
| POST | `/appointments` | Create an appointment |

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🚀 Getting Started

## Prerequisites

- Python 3.9+
- Modern web browser
- Chrome or Edge recommended for voice functionality
- Git

## 1. Clone the Repository

```powershell
git clone https://github.com/namantalesra-fba/Healthcare-ai.git
cd Healthcare-ai
```

## 2. Create Virtual Environment

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

If activation is blocked, use the virtual environment Python directly.

## 3. Install Dependencies

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Main dependencies:

```text
fastapi
uvicorn
pandas
pydantic
```

## 4. Initialize the Database

```powershell
.\venv\Scripts\python.exe backend\seed_data.py
```

This creates the local demonstration database, doctors and appointment slots.

## 5. Train the ML Model

```powershell
.\venv\Scripts\python.exe backend\train_model.py
```

This creates:

```text
backend/models/disease_classifier.json
```

The model does not need to be retrained every time the application starts.

Retrain when the dataset or training code changes.

## 6. Start the Backend

```powershell
.\venv\Scripts\python.exe main.py
```

Backend:

```text
http://127.0.0.1:8000
```

## 7. Start the Frontend

Open another terminal:

```powershell
.\venv\Scripts\python.exe -m http.server 5500 --directory frontend
```

Open:

```text
http://127.0.0.1:5500
```

---

# 🧪 Example Usage

### Example 1

Input:

```text
I have runny nose and fever
```

Processing:

```text
Input
 ↓
NLP
 ↓
runny_nose + fever
 ↓
Bernoulli Naive Bayes
 ↓
Possible Condition
 ↓
Specialist
```

### Example 2

Input:

```text
I have headache and vomiting
```

Extracted symptoms:

```text
headache
vomiting
```

The symptoms are then passed to the ML model.

### Example 3

Input:

```text
I have high BP
```

Recognized disease:

```text
Hypertension
```

The system then maps it to the corresponding specialist category.

---

# 🚨 Safety Layer

The application includes a basic safety layer before normal ML screening.

Example:

```text
Chest pain
+
Difficulty breathing
        ↓
Urgent Warning
```

Conceptual flow:

```text
User Input
    ↓
NLP
    ↓
Safety Check
    │
    ├── Red Flag → Urgent Warning
    │
    └── Normal → ML Prediction
```

This layer is only a predefined software safeguard. It does not determine medical emergency severity and does not replace emergency services or professional medical care.

---

# 📱 Complete User Workflow

```text
1. Open Healthcare AI
        ↓
2. Speak or type symptoms
        ↓
3. Analyze symptoms
        ↓
4. NLP extracts recognized symptoms
        ↓
5. Safety check
        ↓
6. ML prediction
        ↓
7. Possible condition displayed
        ↓
8. Specialist recommended
        ↓
9. Doctors displayed
        ↓
10. Available slots displayed
        ↓
11. Patient details entered
        ↓
12. Appointment confirmed
        ↓
13. Appointment stored in SQLite
```

---

# ⚠️ Limitations

### Synthetic Dataset

The current 500-record dataset is synthetic and intended for educational demonstration.

### Limited Conditions

The model currently supports 10 condition classes.

### Rule-Based NLP

The NLP layer recognizes predefined vocabulary and aliases and cannot understand every possible description.

### Model Limitations

Bernoulli Naive Bayes is a lightweight educational model and is not a clinical diagnostic model.

### Voice Recognition

Voice functionality depends on browser support and microphone permissions.

### Local Demonstration Doctors

Doctor and hospital records are demonstration records and are not verified healthcare-provider records.

### No Real Hospital Integration

The application does not connect to hospital systems or real appointment platforms.

### No Production Authentication

The current prototype does not provide production-grade patient authentication or account management.

---

# 🔮 Future Scope

## 1. Larger Validated Dataset

Use larger, carefully validated datasets from reliable medical sources.

## 2. More Conditions

Expand supported conditions and symptoms.

## 3. Better NLP

Improve natural-language understanding and symptom normalization.

## 4. Multilingual Voice

Add Hindi and other Indian-language voice support.

## 5. Explainable Predictions

Show which recognized symptoms influenced the screening result.

## 6. Verified Doctors

Integrate verified healthcare providers.

## 7. Secure Authentication

Add secure user accounts and appropriate patient-data protection.

## 8. Real Appointment Integration

Connect with legitimate healthcare scheduling systems.

## 9. Notifications

Add appointment reminders and confirmations.

## 10. Improved Local AI

Explore more capable local AI models while maintaining privacy and reducing dependence on external APIs.

---

# 📈 Project Highlights

| Metric | Value |
|---|---:|
| Educational Records | **500** |
| Symptom Features | **20** |
| Supported Conditions | **10** |
| ML Algorithm | **Bernoulli Naive Bayes** |
| Training Records | **375** |
| Testing Records | **125** |
| Test Accuracy | **96.80%** |
| External AI APIs | **0** |
| Database | **SQLite** |

---

# 👥 Project Team

## Project Exhibition Group 239

| # | Name | Registration No. | Contribution |
|---:|---|---|---|
| 1 | Naman Talesra | 25BAI11621 | Backend & ML Integration |
| 2 | Dhirtiman Das | 25BAI11413 | NLP & Symptom Processing |
| 3 | Abhinav Gupta | 25BAI10929 | Machine Learning & Prediction |
| 4 | Anurag Dubey | 23BAI11240 | Voice Interface & Frontend |
| 5 | Abhimanyu | 25BAI10964 | Database & Application Integration |

---

# 🎓 Academic Information

**Project:** Healthcare AI

**Course:** Project Exhibition – I

**Course Code:** DSN2098

**Project Exhibition Group:** 239

**Supervisor:** Dr. Abdul Rehman

**Reviewer 1:** Dr. D Lakshmi

**Reviewer 2:** Chayan Paul

---

# 🔒 Privacy & Data

The core machine-learning prediction pipeline runs locally.

The application does not require:

- OpenAI API
- Gemini API
- ChatGPT API
- External AI inference APIs

The local SQLite database stores demonstration doctors, appointment slots, appointments and symptom history.

The database file is excluded from Git version control through `.gitignore`.

---

# 🛡️ Medical Disclaimer

Healthcare AI is an educational software project.

Its predictions are generated from a synthetic demonstration dataset and **must not be treated as medical advice, diagnosis, or treatment recommendations**.

The application does not replace:

- Doctors
- Hospitals
- Emergency services
- Professional medical consultation

For serious or emergency medical concerns, seek immediate professional medical assistance.

---

# 🤝 Contributing

For educational development:

```powershell
git checkout -b feature/your-feature
```

Make changes:

```powershell
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 📜 License

This project is intended primarily for educational and academic demonstration.

Add an appropriate open-source license if the team decides to distribute the project publicly.

---

<div align="center">

# 🩺 Healthcare AI

### Voice → NLP → Safety → Machine Learning → Specialist → Doctor → Appointment

**Local • API-Free • AI-Assisted • Educational Prototype**

<br>

**Project Exhibition – I | Group 239**

</div>
