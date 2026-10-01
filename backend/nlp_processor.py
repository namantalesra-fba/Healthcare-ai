import re
from typing import List

# Mapping colloquial expressions, synonyms, and variations to canonical model features
SYMPTOM_PATTERNS = {
    "fever": [
        r"\bfever\b",
        r"\btemperature\b",
        r"\bfeeling hot\b",
        r"\brunning a temp\b",
    ],
    "high_fever": [
        r"\bhigh fever\b",
        r"\bvery hot\b",
        r"\bburning up\b",
        r"\bsevere fever\b",
    ],
    "cough": [
        r"\bcough\b",
        r"\bcoughing\b",
        r"\bhack(?:ing)?\b",
        r"\bdry cough\b",
        r"\bwet cough\b",
    ],
    "fatigue": [
        r"\bfatigue\b",
        r"\btired\b",
        r"\btiredness\b",
        r"\bexhausted\b",
        r"\bexhaustion\b",
        r"\bno energy\b",
        r"\blethargic\b",
        r"\bweakness\b",
    ],
    "headache": [
        r"\bheadache\b",
        r"\bhead hurts\b",
        r"\bhead aching\b",
        r"\bpain in (?:my )?head\b",
        r"\bthrobbing head\b",
    ],
    "sore_throat": [
        r"\bsore throat\b",
        r"\bthroat hurts\b",
        r"\bpain in (?:my )?throat\b",
        r"\bscratchy throat\b",
        r"\bthroat pain\b",
    ],
    "runny_nose": [
        r"\brunny nose\b",
        r"\bcold nose\b",
        r"\bstuffy nose\b",
        r"\bblocked nose\b",
        r"\bnose is running\b",
        r"\bcongestion\b",
    ],
    "shortness_of_breath": [
        r"\bshortness of breath\b",
        r"\bdifficulty breathing\b",
        r"\bhard to breathe\b",
        r"\btrouble breathing\b",
        r"\bbreathless\b",
        r"\bcan'?t breathe\b",
    ],
    "chest_pain": [
        r"\bchest pain\b",
        r"\bpain in (?:my )?chest\b",
        r"\bchest hurts\b",
        r"\btightness in (?:my )?chest\b",
        r"\bchest tightness\b",
    ],
    "wheezing": [
        r"\bwheezing\b",
        r"\bwheeze\b",
        r"\bwhistling (?:sound when )?breath(?:ing)?\b",
    ],
    "dizziness": [
        r"\bdizziness\b",
        r"\bdizzy\b",
        r"\bfeeling dizzy\b",
        r"\blightheaded\b",
        r"\bhead spinning\b",
    ],
    "nausea": [
        r"\bnausea\b",
        r"\bnauseous\b",
        r"\bfeel(?:ing)? sick to (?:my )?stomach\b",
        r"\bqueasy\b",
    ],
    "vomiting": [
        r"\bvomiting\b",
        r"\bvomit\b",
        r"\bthrowing up\b",
        r"\bthrew up\b",
        r"\bpuking\b",
    ],
    "skin_rash": [
        r"\bskin rash\b",
        r"\brash\b",
        r"\bred spots\b",
        r"\bred patches\b",
        r"\bskin breakout\b",
        r"\bhives\b",
    ],
    "itching": [
        r"\bitching\b",
        r"\bitchy\b",
        r"\bskin is itchy\b",
        r"\bscratching\b",
        r"\ball over itchy\b",
    ],
    "joint_pain": [
        r"\bjoint pain\b",
        r"\bpain in (?:my )?joints\b",
        r"\baching joints\b",
        r"\bknees hurt\b",
        r"\belbows hurt\b",
    ],
    "muscle_ache": [
        r"\bmuscle ache\b",
        r"\bmuscle aches\b",
        r"\bbody ache\b",
        r"\bbody aches\b",
        r"\bmuscles hurt\b",
        r"\baching body\b",
        r"\bmy body is sore\b",
    ],
    "palpitations": [
        r"\bpalpitations\b",
        r"\bracing heart\b",
        r"\bheart is racing\b",
        r"\bheart pounding\b",
        r"\birregular heartbeat\b",
        r"\bfluttering heart\b",
    ],
    "loss_of_appetite": [
        r"\bloss of appetite\b",
        r"\bno appetite\b",
        r"\bdon'?t feel like eating\b",
        r"\bnot hungry\b",
        r"\blost (?:my )?appetite\b",
    ],
    "chills": [
        r"\bchills\b",
        r"\bshivering\b",
        r"\bshivers\b",
        r"\bfeeling cold\b",
        r"\bcold shakes\b",
    ],
}


def extract_symptoms(text: str) -> List[str]:
    """Cleans raw user text and extracts canonical symptom names

    using rule-based regex matching.
    """
    if not text or not isinstance(text, str):
        return []

    # 1. Normalize input: lowercase and collapse excess whitespace
    normalized_text = re.sub(r"\s+", " ", text.lower().strip())

    detected_symptoms = set()

    # 2. Match patterns against normalized string
    for canonical_symptom, patterns in SYMPTOM_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, normalized_text):
                detected_symptoms.add(canonical_symptom)
                break  # Move to next canonical symptom once matched

    # High fever implies general fever if not explicitly stated
    if "high_fever" in detected_symptoms and "fever" not in detected_symptoms:
        detected_symptoms.add("fever")

    return sorted(list(detected_symptoms))


if __name__ == "__main__":
    test_queries = [
        "Doctor, my head hurts and I have been throwing up since morning.",
        "I am having difficulty breathing and my chest pain is getting worse.",
        "I feel so tired, have a runny nose, and my throat hurts.",
        "My skin is itchy and I noticed a red rash all over my arms.",
        "I have a high fever with chills and severe shivering.",
        "I was feeling dizzy while walking in the park today.",
        "I bought groceries from the supermarket yesterday.",  # Should return empty
    ]

    print("\n--- Testing Local NLP Symptom Extractor ---\n")
    for query in test_queries:
        extracted = extract_symptoms(query)
        print(f"Input   : {query}")
        print(f"Extracted: {extracted}\n")
    print("-------------------------------------------\n")