"""
Local recommendation engine for crop disease diagnosis.
Fully offline — uses a curated knowledge base keyed by (crop, disease).
Returns severity, chemical treatment, organic treatment, and prevention tips.
"""

KNOWLEDGE_BASE: dict[tuple[str, str], dict] = {}


def _seed_knowledge():
    if KNOWLEDGE_BASE:
        return

    crop_map = {
        ("Tomato", "Bacterial spot"): {
            "severity": "Medium",
            "affected_area": "Leaves and fruit",
            "chemical": "Copper-based bactericide (e.g., Kocide 2000, 2g/L water)",
            "organic": "Neem oil spray (5ml/L water) every 7 days",
            "prevention": [
                "Use disease-free seeds and transplants",
                "Avoid working with wet plants",
                "Rotate crops to non-host plants for 2 years",
                "Apply mulch to prevent soil splash",
            ],
        },
        ("Tomato", "Early blight"): {
            "severity": "Medium",
            "affected_area": "Lower leaves",
            "chemical": "Mancozeb fungicide (2g/L water) every 7-10 days",
            "organic": "Copper soap spray or Bordeaux mixture (10g copper sulfate + 10g lime per L)",
            "prevention": [
                "Remove infected leaves immediately",
                "Avoid overhead watering",
                "Improve air circulation between plants",
                "Mulch around plants to reduce soil splash",
            ],
        },
        ("Tomato", "Late blight"): {
            "severity": "High",
            "affected_area": "Entire plant including fruit",
            "chemical": "Chlorothalonil (2ml/L water) or metalaxyl-based fungicide",
            "organic": "Remove and destroy all infected plants immediately",
            "prevention": [
                "Destroy all infected plants immediately",
                "Avoid planting in same area for 3 seasons",
                "Ensure proper drainage in the field",
                "Use resistant varieties where possible",
            ],
        },
        ("Tomato", "Leaf Mold"): {
            "severity": "Medium",
            "affected_area": "Lower and middle leaves",
            "chemical": "Mancozeb or copper fungicide (2g/L water)",
            "organic": "Baking soda solution (1 tsp per liter) weekly",
            "prevention": [
                "Improve greenhouse ventilation",
                "Reduce humidity below 85%",
                "Avoid overhead watering",
                "Space plants wider for air circulation",
            ],
        },
        ("Tomato", "Septoria leaf spot"): {
            "severity": "Medium",
            "affected_area": "Lower leaves, stems",
            "chemical": "Chlorothalonil or mancozeb (2g/L water) every 7-10 days",
            "organic": "Copper fungicide or sulfur spray",
            "prevention": [
                "Remove infected leaves at first sign",
                "Avoid overhead irrigation",
                "Crop rotation for at least 2 years",
                "Remove plant debris after harvest",
            ],
        },
        ("Tomato", "Spider mites Two spotted spider mite"): {
            "severity": "Medium",
            "affected_area": "Underside of leaves",
            "chemical": "Abamectin or bifenthrin-based miticide",
            "organic": "Neem oil spray (5ml/L) or insecticidal soap",
            "prevention": [
                "Keep plants well-watered to reduce stress",
                "Introduce predatory mites (Phytoseiulus persimilis)",
                "Avoid broad-spectrum pesticides that kill natural enemies",
                "Remove heavily infested leaves",
            ],
        },
        ("Tomato", "Target Spot"): {
            "severity": "Medium",
            "affected_area": "Leaves, stems, fruit",
            "chemical": "Azoxystrobin or chlorothalonil fungicide",
            "organic": "Copper fungicide spray weekly",
            "prevention": [
                "Use disease-free seeds",
                "Practice crop rotation (2-3 years)",
                "Improve air circulation",
                "Avoid overhead watering",
            ],
        },
        ("Tomato", "Tomato YellowLeaf Curl Virus"): {
            "severity": "High",
            "affected_area": "Entire plant — leaves curl upward and yellow",
            "chemical": "No chemical cure; control whitefly vectors with imidacloprid",
            "organic": "Reflective mulch to repel whiteflies; neem oil spray",
            "prevention": [
                "Control whitefly populations aggressively",
                "Use virus-resistant tomato varieties",
                "Remove and destroy infected plants",
                "Install fine mesh screens in nurseries",
            ],
        },
        ("Tomato", "Tomato mosaic virus"): {
            "severity": "High",
            "affected_area": "Leaves, fruit, entire plant",
            "chemical": "No chemical cure; disinfect tools with 10% bleach solution",
            "organic": "Remove and destroy infected plants; wash hands before handling",
            "prevention": [
                "Use virus-free seeds",
                "Disinfect gardening tools and hands regularly",
                "Rotate out of solanaceous crops for 2 years",
                "Control aphid and thrip vectors",
            ],
        },
        ("Tomato", "healthy"): {
            "severity": "None",
            "affected_area": "None",
            "chemical": "None required",
            "organic": "Continue balanced organic care routine",
            "prevention": [
                "Continue current care practices",
                "Monitor plants weekly for early signs",
                "Maintain proper watering (1-2 inches per week)",
                "Fertilize with balanced organic compost monthly",
            ],
        },
        ("Potato", "Early blight"): {
            "severity": "Medium",
            "affected_area": "Lower leaves",
            "chemical": "Mancozeb or chlorothalonil (2g/L water) every 7 days",
            "organic": "Copper fungicide spray or Bordeaux mixture",
            "prevention": [
                "Remove infected foliage promptly",
                "Hill soil around stems to reduce tuber exposure",
                "Avoid overhead irrigation",
                "Rotate crops (non-solanaceous) for 3 years",
            ],
        },
        ("Potato", "Late blight"): {
            "severity": "High",
            "affected_area": "Entire plant and tubers",
            "chemical": "Metalaxyl + mancozeb (2.5g/L water) or cymoxanil",
            "organic": "Remove and destroy all infected plants and tubers immediately",
            "prevention": [
                "Destroy all infected plants immediately",
                "Use certified disease-free seed potatoes",
                "Apply preventive copper sprays before rain",
                "Avoid planting in same field for 3-4 years",
            ],
        },
        ("Potato", "healthy"): {
            "severity": "None",
            "affected_area": "None",
            "chemical": "None required",
            "organic": "Continue regular organic care",
            "prevention": [
                "Continue current care practices",
                "Monitor for early signs of blight weekly",
                "Maintain proper hilling and drainage",
                "Rotate crops every season",
            ],
        },
        ("Pepper bell", "Bacterial spot"): {
            "severity": "Medium",
            "affected_area": "Leaves, stems, fruit",
            "chemical": "Copper-based bactericide (2g/L water) weekly",
            "organic": "Neem oil spray (5ml/L) or Bacillus subtilis-based biofungicide",
            "prevention": [
                "Use disease-free seeds (hot water treat at 50°C for 25 min)",
                "Avoid overhead watering",
                "Rotate with non-host crops for 2 years",
                "Remove infected plant debris",
            ],
        },
        ("Pepper bell", "healthy"): {
            "severity": "None",
            "affected_area": "None",
            "chemical": "None required",
            "organic": "Continue regular organic care routine",
            "prevention": [
                "Continue current care practices",
                "Monitor for bacterial spot and aphids weekly",
                "Maintain consistent watering (1-1.5 inches per week)",
                "Apply compost mulch around plants",
            ],
        },
    }

    extra_crops: dict[tuple[str, str], dict] = {
        ("Apple", "Apple scab"): {
            "severity": "Medium",
            "affected_area": "Leaves and fruit",
            "chemical": "Mancozeb or captan fungicide (2g/L water) at pink bud stage",
            "organic": "Sulfur spray or Bordeaux mixture before infection period",
            "prevention": [
                "Remove fallen leaves in autumn to reduce inoculum",
                "Prune for good air circulation",
                "Apply preventive fungicides during wet springs",
                "Plant resistant varieties when possible",
            ],
        },
        ("Apple", "Black rot"): {
            "severity": "Medium",
            "affected_area": "Fruit, leaves, and branches",
            "chemical": "Thiophanate-methyl or captan fungicide",
            "organic": "Remove and destroy infected fruit and cankers",
            "prevention": [
                "Prune out cankered branches in dry weather",
                "Remove mummified fruit from trees",
                "Avoid wounding trees during cultivation",
                "Apply copper sprays during dormancy",
            ],
        },
        ("Apple", "Cedar apple rust"): {
            "severity": "Low",
            "affected_area": "Leaves and fruit",
            "chemical": "Myclobutanil or mancozeb every 7-10 days during spring",
            "organic": "Remove nearby cedar/juniper hosts if possible",
            "prevention": [
                "Remove cedar trees within 1 km of orchard",
                "Plant resistant apple varieties",
                "Apply preventive fungicides from pink bud to petal fall",
                "Monitor for orange spots on leaves in spring",
            ],
        },
        ("Apple", "healthy"): {
            "severity": "None",
            "affected_area": "None",
            "chemical": "None required",
            "organic": "Continue balanced organic orchard care",
            "prevention": [
                "Continue current care practices",
                "Prune annually for structure and airflow",
                "Apply dormant oil in late winter",
                "Monitor weekly for pests and diseases",
            ],
        },
        ("Cucumber", "Downy mildew"): {
            "severity": "High",
            "affected_area": "Leaves — angular yellow lesions on upper surface",
            "chemical": "Chlorothalonil or mancozeb (2g/L) at first sign; metalaxyl-based fungicides",
            "organic": "Copper fungicide spray; apply Bacillus subtilis biofungicide",
            "prevention": [
                "Use resistant varieties where available",
                "Avoid overhead irrigation; water at soil level",
                "Ensure proper plant spacing for air circulation",
                "Rotate out of cucurbit crops for 2 years",
            ],
        },
        ("Cucumber", "Powdery mildew"): {
            "severity": "Medium",
            "affected_area": "Upper leaf surfaces — white powdery coating",
            "chemical": "Sulfur-based fungicide (3g/L) or myclobutanil every 7-14 days",
            "organic": "Baking soda solution (1 tsp/L water with few drops of soap) weekly",
            "prevention": [
                "Plant in full sun with good air flow",
                "Avoid high nitrogen fertilizers",
                "Use resistant varieties",
                "Apply neem oil weekly as preventive",
            ],
        },
        ("Cucumber", "healthy"): {
            "severity": "None",
            "affected_area": "None",
            "chemical": "None required",
            "organic": "Continue regular organic care routine",
            "prevention": [
                "Continue current care practices",
                "Water at base to keep leaves dry",
                "Apply compost tea monthly",
                "Monitor for cucurbit pests weekly",
            ],
        },
        ("Pumpkin", "Downy mildew"): {
            "severity": "High",
            "affected_area": "Leaves — yellow angular lesions",
            "chemical": "Chlorothalonil or mancozeb (2g/L) at first sign; metalaxyl + mancozeb",
            "organic": "Copper fungicide spray; neem oil (5ml/L) as preventive",
            "prevention": [
                "Use resistant pumpkin varieties",
                "Avoid overhead watering in the evening",
                "Space plants 3-4 feet apart for airflow",
                "Rotate with non-cucurbit crops for 2-3 years",
            ],
        },
        ("Pumpkin", "Powdery mildew"): {
            "severity": "Medium",
            "affected_area": "Leaves — white powdery coating",
            "chemical": "Sulfur-based fungicide (3g/L) or trifloxystrobin every 7-14 days",
            "organic": "Milk spray (1 part milk to 9 parts water) weekly; neem oil",
            "prevention": [
                "Plant in full sun with adequate spacing",
                "Avoid excessive nitrogen fertilizer",
                "Remove and destroy infected leaves immediately",
                "Apply sulfur dust preventively in humid conditions",
            ],
        },
        ("Pumpkin", "healthy"): {
            "severity": "None",
            "affected_area": "None",
            "chemical": "None required",
            "organic": "Continue regular organic care routine",
            "prevention": [
                "Continue current care practices",
                "Water at soil level to keep foliage dry",
                "Apply balanced organic fertilizer monthly",
                "Monitor for vine borers and cucumber beetles",
            ],
        },
        ("Rice", "Blast"): {
            "severity": "High",
            "affected_area": "Leaves, nodes, panicles — diamond-shaped lesions",
            "chemical": "Tricyclazole (0.6g/L) or carbendazim at booting stage",
            "organic": "Use silicon-rich amendments (rice hull ash) to strengthen cell walls",
            "prevention": [
                "Plant resistant varieties",
                "Avoid excessive nitrogen fertilization",
                "Maintain proper water management",
                "Remove crop debris after harvest",
            ],
        },
        ("Rice", "Brown spot"): {
            "severity": "Medium",
            "affected_area": "Leaves and grains",
            "chemical": "Mancozeb or edifenphos at booting stage",
            "organic": "Apply neem cake as soil amendment; spray neem oil",
            "prevention": [
                "Use certified disease-free seeds",
                "Maintain balanced soil nutrition (avoid zinc deficiency)",
                "Practice crop rotation",
                "Remove weed hosts from field margins",
            ],
        },
        ("Rice", "Tungro"): {
            "severity": "High",
            "affected_area": "Entire plant — stunting, yellow-orange discoloration",
            "chemical": "No chemical cure; control leafhopper vectors with imidacloprid",
            "organic": "Reflective mulch to repel leafhoppers; neem oil spray",
            "prevention": [
                "Plant resistant or tolerant varieties",
                "Control leafhopper populations early",
                "Stagger planting dates to reduce vector buildup",
                "Remove infected plants and weeds",
            ],
        },
        ("Rice", "healthy"): {
            "severity": "None",
            "affected_area": "None",
            "chemical": "None required",
            "organic": "Continue regular organic care routine",
            "prevention": [
                "Continue current care practices",
                "Maintain proper water depth",
                "Apply compost or green manure before planting",
                "Monitor for pests and diseases weekly",
            ],
        },
        ("Wheat", "Brown rust"): {
            "severity": "Medium",
            "affected_area": "Leaves — orange-brown pustules",
            "chemical": "Propiconazole or tebuconazole (1ml/L) at first sign",
            "organic": "Sulfur spray; apply neem oil weekly",
            "prevention": [
                "Plant resistant varieties",
                "Avoid early planting in rust-prone areas",
                "Reduce plant density for airflow",
                "Remove volunteer wheat plants",
            ],
        },
        ("Wheat", "Septoria"): {
            "severity": "Medium",
            "affected_area": "Leaves — irregular gray-brown lesions with dark spots",
            "chemical": "Azoxystrobin or chlorothalonil fungicide at flag leaf stage",
            "organic": "Copper fungicide spray; practice strict crop rotation",
            "prevention": [
                "Use certified disease-free seed",
                "Rotate with non-cereal crops for 2 years",
                "Plow under crop residue after harvest",
                "Avoid dense planting",
            ],
        },
        ("Wheat", "Yellow rust"): {
            "severity": "High",
            "affected_area": "Leaves — yellow-orange pustules in stripes",
            "chemical": "Tebuconazole or propiconazole (1ml/L) at first sign",
            "organic": "Sulfur-based fungicide; remove volunteer wheat",
            "prevention": [
                "Plant yellow rust-resistant varieties",
                "Avoid excessive nitrogen fertilizer",
                "Monitor regularly during cool wet springs",
                "Apply preventive fungicide at stem elongation if history of rust",
            ],
        },
        ("Wheat", "healthy"): {
            "severity": "None",
            "affected_area": "None",
            "chemical": "None required",
            "organic": "Continue regular organic care routine",
            "prevention": [
                "Continue current care practices",
                "Use certified seed each season",
                "Balance nitrogen fertilization to prevent lodging",
                "Monitor weekly for pests and diseases",
            ],
        },
    }

    KNOWLEDGE_BASE.update(crop_map)
    KNOWLEDGE_BASE.update(extra_crops)


def get_recommendation(crop: str, disease: str) -> dict:
    _seed_knowledge()
    disease_lower = disease.lower()

    direct_key = (crop, disease)
    if direct_key in KNOWLEDGE_BASE:
        return dict(KNOWLEDGE_BASE[direct_key])

    for (c, d), rec in KNOWLEDGE_BASE.items():
        if c.lower() == crop.lower() and d.lower() == disease_lower:
            return dict(rec)

    for (c, d), rec in KNOWLEDGE_BASE.items():
        if c.lower() == crop.lower():
            disease_words = set(d.lower().replace("/", " ").split())
            query_words = set(disease_lower.replace("/", " ").split())
            if disease_words & query_words:
                return dict(rec)

    return {
        "severity": "Medium",
        "affected_area": "Could not be determined automatically",
        "chemical": "Consult a local agricultural extension officer",
        "organic": "Consider neem oil spray as a general bio-pesticide",
        "prevention": [
            "Consult a local agricultural extension officer",
            "Isolate affected plants to prevent spread",
            "Monitor crop daily for changes",
            "Remove and dispose of affected plant parts",
        ],
    }


def build_report(crop: str, disease: str) -> dict:
    rec = get_recommendation(crop, disease)
    return {
        "severity": rec["severity"],
        "affected_area": rec["affected_area"],
        "chemical_treatment": rec["chemical"],
        "organic_treatment": rec["organic"],
        "prevention": rec["prevention"],
        "recommendation": [
            f"[Chemical] {rec['chemical']}",
            f"[Organic] {rec['organic']}",
            *rec["prevention"],
        ],
    }
