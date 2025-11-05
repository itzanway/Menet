from typing import List, Dict, Tuple

# Red flags that indicate urgent evaluation
RED_FLAGS = {
    "chest_pain": "Chest pain or pressure, especially with sweating or fainting — seek emergency care (call emergency services).",
    "shortness_of_breath": "Severe shortness of breath or difficulty breathing — seek emergency care immediately.",
    "loss_of_consciousness": "Loss of consciousness or fainting — emergency care required.",
    "sudden_weakness": "Sudden weakness or numbness on one side of the body — possible stroke; go to ER.",
    "severe_bleeding": "Severe bleeding that won't stop — urgent care or ER."
}

# Map symptom keywords to friendly names and risk tiers
SYMPTOM_MAP = {
    "fever": {"label": "Fever", "tier": "common"},
    "cough": {"label": "Cough", "tier": "common"},
    "sore throat": {"label": "Sore throat", "tier": "common"},
    "headache": {"label": "Headache", "tier": "common"},
    "nausea": {"label": "Nausea", "tier": "common"},
    "vomiting": {"label": "Vomiting", "tier": "concerning"},
    "shortness of breath": {"label": "Shortness of breath", "tier": "red"},
    "chest pain": {"label": "Chest pain", "tier": "red"},
    "dizziness": {"label": "Dizziness", "tier": "concerning"},
    "loss of taste": {"label": "Loss of taste/smell", "tier": "common"},
    "bleeding": {"label": "Bleeding", "tier": "red"},
    "confusion": {"label": "Confusion", "tier": "red"},
    "rash": {"label": "Rash", "tier": "common"}
}

def normalize_symptom_text(text: str) -> str:
    return text.lower().strip()

def analyze_symptoms(symptoms: List[str]) -> Dict:
    """
    Input: list of symptom strings (free text or keywords)
    Output: dict with detected symptoms, any red flags, suggested action
    """
    detected = []
    red_flags_found = []
    tiers = {"red": 0, "concerning": 0, "common": 0}

    for s in symptoms:
        ns = normalize_symptom_text(s)
        matched = None
        # exact match first
        if ns in SYMPTOM_MAP:
            matched = SYMPTOM_MAP[ns]
        else:
            # partial match search
            for key in SYMPTOM_MAP:
                if key in ns:
                    matched = SYMPTOM_MAP[key]
                    break
        if matched:
            detected.append(matched["label"])
            tiers[matched["tier"]] += 1
            # check red flags
            if matched["tier"] == "red":
                # map to specific red flag message if available
                for rf in RED_FLAGS:
                    if rf.replace("_", " ") in ns or matched["label"].lower() in RED_FLAGS[rf].lower():
                        red_flags_found.append(RED_FLAGS[rf])
                # if none matched, append generic
                if not red_flags_found:
                    red_flags_found.append(f"{matched['label']} is concerning — seek urgent medical attention.")
        else:
            detected.append(s)  # unknown pass-through

    # Decide suggested action
    if red_flags_found:
        action = {
            "level": "urgent",
            "message": " / ".join(red_flags_found)
        }
    elif tiers["concerning"] > 0:
        action = {
            "level": "see_provider",
            "message": "Symptoms are concerning — schedule a visit with a healthcare provider soon."
        }
    else:
        action = {
            "level": "self_care",
            "message": "Symptoms appear mild — consider self-care (rest, hydration). If symptoms worsen, see a provider."
        }

    return {
        "detected_symptoms": detected,
        "red_flags": red_flags_found,
        "counts": tiers,
        "action": action
    }

if __name__ == "__main__":
    # quick demo
    demo = ["High fever", "chest pain", "headache"]
    print(analyze_symptoms(demo))
