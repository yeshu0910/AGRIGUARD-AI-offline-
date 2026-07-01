"""
Parses model labels in PlantVillage format: Crop___disease_name
Handles sub-varieties (e.g., Pepper bell) and multi-word disease names.
"""


def parse_label(label: str) -> tuple[str, str]:
    parts = label.split("___", 1)
    crop_part = parts[0].rstrip("_").replace("_", " ")
    rest = parts[1] if len(parts) > 1 else ""

    if crop_part == "Pepper":
        crop_part = "Pepper bell"

    disease = rest.replace("_", " ").strip()
    disease = " ".join(disease.split())

    return crop_part, disease if disease else "healthy"
