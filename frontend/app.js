// ============================================================
// HEALTHCARE AI
// Complete Frontend Application
//
// Features:
// 1. Voice input
// 2. Local NLP + ML prediction
// 3. Emergency safety layer
// 4. Doctor search
// 5. Available appointment slots
// 6. Appointment booking
// 7. Booking confirmation
// 8. Text-to-speech
// 9. No external AI API
// ============================================================


// ============================================================
// BACKEND CONFIGURATION
// ============================================================

const API_BASE_URL = "http://127.0.0.1:8000";

const PREDICT_URL = `${API_BASE_URL}/predict`;

const DOCTORS_URL = `${API_BASE_URL}/doctors`;


// ============================================================
// DOM ELEMENTS
// ============================================================

// Voice
const micBtn = document.getElementById("micBtn");
const micStatus = document.getElementById("micStatus");

// Input
const symptomInput = document.getElementById("symptomInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const analyzeSpinner = document.getElementById("analyzeSpinner");
const analyzeBtnText = document.getElementById("analyzeBtnText");
const clearBtn = document.getElementById("clearBtn");

// Error
const errorBanner = document.getElementById("errorBanner");

// Results
const resultsSection = document.getElementById("resultsSection");
const resCondition = document.getElementById("resCondition");
const resConfidence = document.getElementById("resConfidence");
const resSpecialist = document.getElementById("resSpecialist");
const resSymptomsList = document.getElementById("resSymptomsList");
const resTopMatches = document.getElementById("resTopMatches");
const resDisclaimer = document.getElementById("resDisclaimer");
const speakBtn = document.getElementById("speakBtn");

// Doctors
const findDoctorsBtn = document.getElementById("findDoctorsBtn");
const doctorsList = document.getElementById("doctorsList");

// Slots
const slotsSection = document.getElementById("slotsSection");
const selectedDoctorName = document.getElementById("selectedDoctorName");
const slotsList = document.getElementById("slotsList");

// Patient
const patientSection = document.getElementById("patientSection");
const patientName = document.getElementById("patientName");
const patientContact = document.getElementById("patientContact");
const bookingSummary = document.getElementById("bookingSummary");
const confirmBookingBtn = document.getElementById("confirmBookingBtn");

// Confirmation
const bookingConfirmation =
    document.getElementById("bookingConfirmation");

// New consultation
const newConsultationBtn =
    document.getElementById("newConsultationBtn");


// ============================================================
// APPLICATION STATE
// ============================================================

let currentPrediction = null;

let currentSymptoms = [];

let selectedDoctor = null;

let selectedSlot = null;

let isRecording = false;

let recognition = null;


// ============================================================
// SPEECH RECOGNITION
// ============================================================

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (SpeechRecognition) {

    recognition = new SpeechRecognition();

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.lang = "en-US";


    recognition.onstart = () => {

        isRecording = true;

        micBtn.classList.add("recording");

        micStatus.textContent =
            "Listening... Speak your symptoms clearly.";

        hideError();
    };


    recognition.onresult = (event) => {

        const transcript =
            event.results[0][0].transcript;

        if (symptomInput.value.trim()) {

            symptomInput.value +=
                " " + transcript;

        } else {

            symptomInput.value =
                transcript;
        }
    };


    recognition.onerror = (event) => {

        console.error(
            "Speech recognition error:",
            event.error
        );

        showError(
            `Microphone error: ${event.error}. You can still type your symptoms manually.`
        );

        stopRecording();
    };


    recognition.onend = () => {

        stopRecording();
    };

} else {

    micStatus.textContent =
        "Voice input is not supported in this browser. Please type your symptoms.";

    micBtn.disabled = true;

    micBtn.style.opacity = "0.5";

    micBtn.style.cursor = "not-allowed";
}


// ============================================================
// STOP RECORDING
// ============================================================

function stopRecording() {

    isRecording = false;

    micBtn.classList.remove("recording");

    micStatus.textContent =
        "Click mic to speak again, or edit the text below.";
}


// ============================================================
// MICROPHONE BUTTON
// ============================================================

micBtn.addEventListener("click", () => {

    if (!recognition) {
        return;
    }

    if (!isRecording) {

        try {

            recognition.start();

        } catch (error) {

            console.warn(
                "Recognition could not start:",
                error
            );
        }

    } else {

        recognition.stop();
    }
});


// ============================================================
// ANALYZE SYMPTOMS
// ============================================================

analyzeBtn.addEventListener(
    "click",
    analyzeSymptoms
);


async function analyzeSymptoms() {

    const text =
        symptomInput.value.trim();


    if (!text) {

        showError(
            "Please speak or type your symptoms before analyzing."
        );

        return;
    }


    hideError();

    setLoading(true);


    try {

        const response =
            await fetch(
                PREDICT_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text: text
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                `Server returned HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        console.log(
            "Healthcare AI response:",
            data
        );


        if (!data.success) {

            throw new Error(
                data.message ||
                "No recognizable symptoms were detected."
            );
        }


        renderResults(data);

    } catch (error) {

        console.error(
            "Prediction error:",
            error
        );


        showError(
            error.message ||
            "Could not connect to Healthcare AI backend."
        );

    } finally {

        setLoading(false);
    }
}


// ============================================================
// RENDER RESULTS
// ============================================================

function renderResults(data) {

    // --------------------------------------------------------
    // SAFETY CHECK
    // --------------------------------------------------------

    if (isEmergencyCase(data)) {

        showEmergencyWarning();

        return;
    }


    const prediction =
        data.prediction || {};


    currentPrediction =
        prediction;


    currentSymptoms =
        data.symptoms || [];


    // --------------------------------------------------------
    // CONDITION
    // --------------------------------------------------------

    const condition =
        prediction.predicted_condition ||
        "Inconclusive";


    // --------------------------------------------------------
    // CONFIDENCE
    // --------------------------------------------------------

    let confidence =
        prediction.confidence;


    if (
        typeof confidence === "number"
    ) {

        confidence =
            (confidence * 100).toFixed(1) + "%";

    } else {

        confidence = "N/A";
    }


    // --------------------------------------------------------
    // SPECIALIST
    // --------------------------------------------------------

    const specialist =
        prediction.recommended_specialist ||
        "General Physician";


    // --------------------------------------------------------
    // UPDATE UI
    // --------------------------------------------------------

    resCondition.textContent =
        condition;


    resConfidence.textContent =
        confidence;


    resSpecialist.textContent =
        specialist;


    resDisclaimer.textContent =
        prediction.disclaimer ||
        "This is an educational screening system, not a medical diagnosis.";


    // --------------------------------------------------------
    // SYMPTOMS
    // --------------------------------------------------------

    renderSymptoms(
        currentSymptoms
    );


    // --------------------------------------------------------
    // TOP MATCHES
    // --------------------------------------------------------

    renderTopMatches(
        prediction.top_matches || []
    );


    // --------------------------------------------------------
    // RESET APPOINTMENT
    // --------------------------------------------------------

    resetAppointmentArea();


    // --------------------------------------------------------
    // SHOW RESULTS
    // --------------------------------------------------------

    resultsSection.classList.remove(
        "hidden"
    );


    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ============================================================
// EMERGENCY SAFETY CHECK
// ============================================================

function isEmergencyCase(data) {

    const symptoms =
        data.symptoms || [];


    const normalizedSymptoms =
        symptoms.map(
            symptom =>
                symptom
                    .toLowerCase()
                    .trim()
        );


    const hasChestPain =
        normalizedSymptoms.includes(
            "chest_pain"
        );


    const hasBreathingDifficulty =
        normalizedSymptoms.includes(
            "shortness_of_breath"
        );


    // Potentially serious symptom combination
    if (
        hasChestPain &&
        hasBreathingDifficulty
    ) {

        return true;
    }


    return false;
}


// ============================================================
// SHOW EMERGENCY WARNING
// ============================================================

function showEmergencyWarning() {

    // Hide normal results
    resultsSection.classList.add(
        "hidden"
    );


    // Hide appointment workflow
    slotsSection.classList.add(
        "hidden"
    );


    patientSection.classList.add(
        "hidden"
    );


    bookingConfirmation.classList.add(
        "hidden"
    );


    // Clear appointment state
    selectedDoctor = null;

    selectedSlot = null;


    // Display warning
    showError(
        "🚨 URGENT MEDICAL WARNING: Chest pain combined with difficulty breathing can be serious. Healthcare AI is an educational screening system and is NOT designed for emergencies. Please seek appropriate emergency medical care immediately."
    );


    // Scroll to warning
    errorBanner.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


// ============================================================
// RENDER SYMPTOMS
// ============================================================

function renderSymptoms(symptoms) {

    resSymptomsList.innerHTML = "";


    if (
        !symptoms ||
        symptoms.length === 0
    ) {

        resSymptomsList.innerHTML =
            `
            <span class="chip-none">
                No recognized symptoms detected.
            </span>
            `;

        return;
    }


    symptoms.forEach(
        (symptom) => {

            const chip =
                document.createElement("span");


            chip.className =
                "chip";


            chip.textContent =
                symptom.replace(
                    /_/g,
                    " "
                );


            resSymptomsList.appendChild(
                chip
            );
        }
    );
}


// ============================================================
// RENDER TOP MATCHES
// ============================================================

function renderTopMatches(matches) {

    resTopMatches.innerHTML = "";


    if (
        !matches ||
        matches.length === 0
    ) {

        const li =
            document.createElement("li");


        li.textContent =
            "No additional candidate matches available.";


        resTopMatches.appendChild(
            li
        );

        return;
    }


    matches.forEach(
        (match) => {

            const li =
                document.createElement("li");


            const name =
                match.condition ||
                "Unknown";


            let probability =
                match.probability;


            if (
                typeof probability === "number"
            ) {

                probability =
                    (probability * 100).toFixed(1) + "%";
            }


            const nameSpan =
                document.createElement("span");


            nameSpan.className =
                "match-name";


            nameSpan.textContent =
                name;


            const percentageSpan =
                document.createElement("span");


            percentageSpan.className =
                "match-pct";


            percentageSpan.textContent =
                probability || "";


            li.appendChild(
                nameSpan
            );


            li.appendChild(
                percentageSpan
            );


            resTopMatches.appendChild(
                li
            );
        }
    );
}


// ============================================================
// FIND DOCTORS
// ============================================================

findDoctorsBtn.addEventListener(
    "click",
    findDoctors
);


async function findDoctors() {

    const specialist =
        resSpecialist.textContent.trim();


    if (!specialist) {

        showError(
            "Please analyze your symptoms first."
        );

        return;
    }


    findDoctorsBtn.disabled = true;

    findDoctorsBtn.textContent =
        "Finding Doctors...";


    hideError();


    try {

        const url =
            `${DOCTORS_URL}?specialization=${encodeURIComponent(
                specialist
            )}`;


        const response =
            await fetch(url);


        if (!response.ok) {

            throw new Error(
                `Doctor search failed: HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        if (!data.success) {

            throw new Error(
                "No doctors were found."
            );
        }


        renderDoctors(
            data.doctors || []
        );

    } catch (error) {

        console.error(
            "Doctor search error:",
            error
        );


        showError(
            error.message ||
            "Unable to load doctors."
        );

    } finally {

        findDoctorsBtn.disabled = false;

        findDoctorsBtn.textContent =
            "👨‍⚕️ Find Available Doctors";
    }
}


// ============================================================
// RENDER DOCTORS
// ============================================================

function renderDoctors(doctors) {

    doctorsList.innerHTML = "";


    slotsSection.classList.add(
        "hidden"
    );


    patientSection.classList.add(
        "hidden"
    );


    bookingConfirmation.classList.add(
        "hidden"
    );


    if (
        !doctors ||
        doctors.length === 0
    ) {

        doctorsList.innerHTML =
            `
            <div class="empty-state">
                No doctors are currently available
                for ${escapeHtml(
                    resSpecialist.textContent
                )}.
            </div>
            `;

        return;
    }


    doctors.forEach(
        (doctor) => {

            const card =
                document.createElement("div");


            card.className =
                "doctor-card";


            // Doctor header
            const top =
                document.createElement("div");


            top.className =
                "doctor-card-top";


            const avatar =
                document.createElement("div");


            avatar.className =
                "doctor-avatar";


            avatar.textContent =
                "👨‍⚕️";


            const title =
                document.createElement("div");


            const doctorName =
                document.createElement("h3");


            doctorName.textContent =
                doctor.name;


            const specialization =
                document.createElement("div");


            specialization.className =
                "doctor-specialization";


            specialization.textContent =
                doctor.specialization;


            title.appendChild(
                doctorName
            );


            title.appendChild(
                specialization
            );


            top.appendChild(
                avatar
            );


            top.appendChild(
                title
            );


            // Doctor information
            const info =
                document.createElement("div");


            info.className =
                "doctor-info";


            const hospital =
                document.createElement("div");


            hospital.textContent =
                `🏥 ${doctor.hospital}`;


            const contact =
                document.createElement("div");


            contact.textContent =
                `📞 ${doctor.contact}`;


            const fee =
                document.createElement("div");


            fee.className =
                "doctor-fee";


            fee.textContent =
                `Consultation Fee: ₹${doctor.fee}`;


            info.appendChild(
                hospital
            );


            info.appendChild(
                contact
            );


            info.appendChild(
                fee
            );


            // View slots
            const button =
                document.createElement("button");


            button.className =
                "primary-button";


            button.textContent =
                "View Available Slots";


            button.addEventListener(
                "click",
                () => {

                    loadDoctorSlots(
                        doctor
                    );
                }
            );


            card.appendChild(
                top
            );


            card.appendChild(
                info
            );


            card.appendChild(
                button
            );


            doctorsList.appendChild(
                card
            );
        }
    );


    doctorsList.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


// ============================================================
// LOAD DOCTOR SLOTS
// ============================================================

async function loadDoctorSlots(doctor) {

    selectedDoctor =
        doctor;


    selectedSlot =
        null;


    selectedDoctorName.textContent =
        doctor.name;


    slotsList.innerHTML =
        "";


    slotsSection.classList.remove(
        "hidden"
    );


    patientSection.classList.add(
        "hidden"
    );


    bookingConfirmation.classList.add(
        "hidden"
    );


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/doctors/${doctor.id}/slots`
            );


        if (!response.ok) {

            throw new Error(
                `Could not load slots: HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        renderSlots(
            data.slots || []
        );

    } catch (error) {

        console.error(
            "Slot loading error:",
            error
        );


        showError(
            error.message ||
            "Unable to load appointment slots."
        );
    }
}


// ============================================================
// RENDER SLOTS
// ============================================================

function renderSlots(slots) {

    slotsList.innerHTML = "";


    if (
        !slots ||
        slots.length === 0
    ) {

        slotsList.innerHTML =
            `
            <div class="empty-state">
                No available appointment slots
                for this doctor.
            </div>
            `;

        return;
    }


    slots.forEach(
        (slot) => {

            const button =
                document.createElement("button");


            button.className =
                "slot-button";


            const date =
                document.createElement("span");


            date.className =
                "slot-date";


            date.textContent =
                formatDate(
                    slot.date
                );


            const time =
                document.createElement("span");


            time.className =
                "slot-time";


            time.textContent =
                `${formatTime(slot.start_time)} - ${formatTime(slot.end_time)}`;


            button.appendChild(
                date
            );


            button.appendChild(
                time
            );


            button.addEventListener(
                "click",
                () => {

                    selectSlot(
                        slot,
                        button
                    );
                }
            );


            slotsList.appendChild(
                button
            );
        }
    );


    slotsSection.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


// ============================================================
// SELECT SLOT
// ============================================================

function selectSlot(slot, button) {

    selectedSlot =
        slot;


    document
        .querySelectorAll(
            ".slot-button"
        )
        .forEach(
            (element) => {

                element.classList.remove(
                    "selected"
                );
            }
        );


    button.classList.add(
        "selected"
    );


    patientSection.classList.remove(
        "hidden"
    );


    updateBookingSummary();


    patientSection.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


// ============================================================
// BOOKING SUMMARY
// ============================================================

function updateBookingSummary() {

    if (
        !selectedDoctor ||
        !selectedSlot
    ) {

        bookingSummary.innerHTML =
            "";

        return;
    }


    bookingSummary.innerHTML =
        `
        <strong>Selected Appointment</strong><br>

        Doctor:
        ${escapeHtml(
            selectedDoctor.name
        )}
        <br>

        Specialization:
        ${escapeHtml(
            selectedDoctor.specialization
        )}
        <br>

        Hospital:
        ${escapeHtml(
            selectedDoctor.hospital
        )}
        <br>

        Date:
        ${escapeHtml(
            formatDate(
                selectedSlot.date
            )
        )}
        <br>

        Time:
        ${escapeHtml(
            formatTime(
                selectedSlot.start_time
            )
        )}
        -
        ${escapeHtml(
            formatTime(
                selectedSlot.end_time
            )
        )}
        <br>

        Consultation Fee:
        ₹${escapeHtml(
            String(
                selectedDoctor.fee
            )
        )}
        `;
}


// ============================================================
// CONFIRM APPOINTMENT
// ============================================================

confirmBookingBtn.addEventListener(
    "click",
    bookAppointment
);


async function bookAppointment() {

    if (
        !selectedDoctor ||
        !selectedSlot
    ) {

        showError(
            "Please select a doctor and appointment slot."
        );

        return;
    }


    const name =
        patientName.value.trim();


    const contact =
        patientContact.value.trim();


    if (!name) {

        showError(
            "Please enter the patient's name."
        );

        patientName.focus();

        return;
    }


    if (!contact) {

        showError(
            "Please enter the patient's contact number."
        );

        patientContact.focus();

        return;
    }


    if (
        contact.length < 10
    ) {

        showError(
            "Please enter a valid contact number."
        );

        patientContact.focus();

        return;
    }


    hideError();


    confirmBookingBtn.disabled =
        true;


    confirmBookingBtn.textContent =
        "Booking Appointment...";


    try {

        const requestBody = {

            slot_id:
                selectedSlot.id,

            doctor_id:
                selectedDoctor.id,

            patient_name:
                name,

            patient_contact:
                contact,

            disease_predicted:
                currentPrediction?.predicted_condition ||
                resCondition.textContent,

            symptoms:
                currentSymptoms.join(", ")
        };


        console.log(
            "Booking request:",
            requestBody
        );


        const response =
            await fetch(
                `${API_BASE_URL}/appointments`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            requestBody
                        )
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Appointment booking failed."
            );
        }


        showBookingConfirmation(
            data
        );

    } catch (error) {

        console.error(
            "Booking error:",
            error
        );


        showError(
            error.message ||
            "Could not book the appointment."
        );

    } finally {

        confirmBookingBtn.disabled =
            false;

        confirmBookingBtn.textContent =
            "✅ Confirm Appointment";
    }
}


// ============================================================
// BOOKING CONFIRMATION
// ============================================================

function showBookingConfirmation(data) {

    const appointment =
        data.appointment || {};


    const doctor =
        appointment.doctor ||
        selectedDoctor;


    const slot =
        appointment.slot ||
        selectedSlot;


    bookingConfirmation.innerHTML =
        "";


    const heading =
        document.createElement("h3");


    heading.textContent =
        "✅ Appointment Confirmed";


    const message =
        document.createElement("p");


    message.innerHTML =
        `
        Appointment ID:
        <strong>
            ${escapeHtml(
                String(
                    appointment.id ||
                    "N/A"
                )
            )}
        </strong>
        <br>

        Patient:
        ${escapeHtml(
            appointment.patient_name ||
            patientName.value
        )}
        <br>

        Doctor:
        ${escapeHtml(
            doctor.name ||
            "Doctor"
        )}
        <br>

        Hospital:
        ${escapeHtml(
            doctor.hospital ||
            ""
        )}
        <br>

        Date:
        ${escapeHtml(
            formatDate(
                slot.date
            )
        )}
        <br>

        Time:
        ${escapeHtml(
            formatTime(
                slot.start_time
            )
        )}
        -
        ${escapeHtml(
            formatTime(
                slot.end_time
            )
        )}
        <br><br>

        ${escapeHtml(
            data.message ||
            "Appointment booked successfully."
        )}
        `;


    bookingConfirmation.appendChild(
        heading
    );


    bookingConfirmation.appendChild(
        message
    );


    bookingConfirmation.classList.remove(
        "hidden"
    );


    patientSection.classList.add(
        "hidden"
    );


    slotsSection.classList.add(
        "hidden"
    );


    selectedSlot = null;


    bookingConfirmation.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


// ============================================================
// TEXT TO SPEECH
// ============================================================

speakBtn.addEventListener(
    "click",
    () => {

        if (
            !(
                "speechSynthesis"
                in window
            )
        ) {

            alert(
                "Speech synthesis is not supported in this browser."
            );

            return;
        }


        window.speechSynthesis.cancel();


        const condition =
            resCondition.textContent;


        const specialist =
            resSpecialist.textContent;


        const confidence =
            resConfidence.textContent;


        const speechText =
            `Healthcare AI screening complete. The possible condition is ${condition}, with a model confidence of ${confidence}. The recommended specialist is ${specialist}.`;


        const utterance =
            new SpeechSynthesisUtterance(
                speechText
            );


        utterance.rate =
            0.95;


        utterance.pitch =
            1.0;


        utterance.lang =
            "en-US";


        window.speechSynthesis.speak(
            utterance
        );
    }
);


// ============================================================
// CLEAR BUTTON
// ============================================================

clearBtn.addEventListener(
    "click",
    resetApplication
);


// ============================================================
// NEW CONSULTATION
// ============================================================

if (newConsultationBtn) {

    newConsultationBtn.addEventListener(
        "click",
        resetApplication
    );
}


// ============================================================
// RESET APPLICATION
// ============================================================

function resetApplication() {

    // Stop recording
    if (
        isRecording &&
        recognition
    ) {

        recognition.stop();
    }


    // Stop text-to-speech
    if (
        "speechSynthesis"
        in window
    ) {

        window.speechSynthesis.cancel();
    }


    // Clear input
    symptomInput.value =
        "";


    // Hide results
    resultsSection.classList.add(
        "hidden"
    );


    // Clear errors
    hideError();


    // Reset state
    currentPrediction =
        null;

    currentSymptoms =
        [];

    selectedDoctor =
        null;

    selectedSlot =
        null;


    // Clear doctors
    doctorsList.innerHTML =
        "";


    // Clear slots
    slotsList.innerHTML =
        "";


    // Hide appointment sections
    slotsSection.classList.add(
        "hidden"
    );

    patientSection.classList.add(
        "hidden"
    );

    bookingConfirmation.classList.add(
        "hidden"
    );


    // Clear patient data
    patientName.value =
        "";

    patientContact.value =
        "";


    bookingSummary.innerHTML =
        "";


    selectedDoctorName.textContent =
        "Select a doctor";


    // Reset microphone
    micStatus.textContent =
        "Click mic to start speaking";


    // Focus input
    symptomInput.focus();
}


// ============================================================
// LOADING STATE
// ============================================================

function setLoading(loading) {

    if (loading) {

        analyzeBtn.disabled =
            true;


        analyzeSpinner.classList.remove(
            "hidden"
        );


        analyzeBtnText.textContent =
            "Analyzing...";

    } else {

        analyzeBtn.disabled =
            false;


        analyzeSpinner.classList.add(
            "hidden"
        );


        analyzeBtnText.textContent =
            "Analyze Symptoms";
    }
}


// ============================================================
// ERROR DISPLAY
// ============================================================

function showError(message) {

    errorBanner.textContent =
        message;


    errorBanner.classList.remove(
        "hidden"
    );


    errorBanner.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


function hideError() {

    errorBanner.classList.add(
        "hidden"
    );


    errorBanner.textContent =
        "";
}


// ============================================================
// DATE FORMATTER
// ============================================================

function formatDate(dateString) {

    if (!dateString) {

        return "Date unavailable";
    }


    const date =
        new Date(
            `${dateString}T00:00:00`
        );


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return dateString;
    }


    return date.toLocaleDateString(
        "en-IN",
        {
            day: "2-digit",
            month: "short",
            year: "numeric"
        }
    );
}


// ============================================================
// TIME FORMATTER
// ============================================================

function formatTime(timeString) {

    if (!timeString) {

        return "Time unavailable";
    }


    const value =
        String(
            timeString
        ).trim();


    // IMPORTANT:
    // Database already contains AM/PM.
    // Therefore do not add AM/PM again.

    if (
        /\b(AM|PM)\b/i.test(value)
    ) {

        return value;
    }


    // Handle HH:MM and HH:MM:SS

    const parts =
        value.split(":");


    if (
        parts.length < 2
    ) {

        return value;
    }


    let hours =
        parseInt(
            parts[0],
            10
        );


    const minutes =
        parts[1];


    if (
        Number.isNaN(hours)
    ) {

        return value;
    }


    const period =
        hours >= 12
            ? "PM"
            : "AM";


    hours =
        hours % 12 || 12;


    return `${hours}:${minutes} ${period}`;
}


// ============================================================
// HTML ESCAPING
// ============================================================

function escapeHtml(value) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        value;


    return div.innerHTML;
}


// ============================================================
// RESET APPOINTMENT AREA
// ============================================================

function resetAppointmentArea() {

    selectedDoctor =
        null;

    selectedSlot =
        null;


    doctorsList.innerHTML =
        "";


    slotsList.innerHTML =
        "";


    slotsSection.classList.add(
        "hidden"
    );


    patientSection.classList.add(
        "hidden"
    );


    bookingConfirmation.classList.add(
        "hidden"
    );


    bookingSummary.innerHTML =
        "";


    selectedDoctorName.textContent =
        "Select a doctor";
}


// ============================================================
// INITIALIZE APPLICATION
// ============================================================

resetAppointmentArea();

console.log(
    "Healthcare AI frontend initialized successfully."
);