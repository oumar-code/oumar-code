"""
Microbiology Skills Catalogue
=============================
Skills and knowledge from ND Science Laboratory Technology + HND Applied Science (Microbiology).
Integrated with the skill tracking system for AI-powered education platforms.

Academic Background
-------------------
- ND Science Laboratory Technology (Years 1-2)
- HND Applied Science - Microbiology Specialization (Years 3-4)
- SIWES Industrial Training: Zamfara State Waterboard (3-6 months ND + 1 year HND)
- Final Project: Prevalence of Schistosoma haematobium in Tudun Wada, Talata Mafara, Zamfara State

Usage
-----
    from fashion.microbiology_skills import MICROBIOLOGY_SKILLS, get_microbiology_catalogue

    # Get full catalogue
    catalogue = get_microbiology_catalogue()
    
    # Search by level
    beginner_skills = get_skills_by_level("Beginner")
    
    # Search by subdomain
    medical_micro = get_skills_by_subdomain("medical")
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Microbiology Skills Catalogue
# ---------------------------------------------------------------------------

MICROBIOLOGY_SKILLS: dict[str, dict] = {
    # ========================================================================
    # FOUNDATION SKILLS (ND SLT Core)
    # ========================================================================
    
    # ── General Biology ──────────────────────────────────────────────────
    "cellular-biology": {
        "name": "Cellular Biology",
        "level": "Beginner",
        "subdomain": "foundation",
        "mastery_sessions": 3,
        "description": "Cell structure, organelles, cell membrane, nucleus, cell division (mitosis/meiosis)",
        "badge": "🔬 Cell Scholar",
        "topics": ["prokaryotic cells", "eukaryotic cells", "cell organelles", "cell division"],
        "ai_relevance": "Foundation for understanding microbial cells and AI-driven cellular analysis"
    },
    
    "general-biology-principles": {
        "name": "General Biology Principles",
        "level": "Beginner",
        "subdomain": "foundation",
        "mastery_sessions": 2,
        "description": "Taxonomy, evolution, genetics basics, ecology",
        "badge": "🌿 Biology Basics",
        "topics": ["taxonomy", "evolution", "genetic inheritance", "ecological principles"],
        "ai_relevance": "Taxonomic classification can be automated with ML models"
    },
    
    # ── General Chemistry ────────────────────────────────────────────────
    "general-chemistry": {
        "name": "General Chemistry",
        "level": "Beginner",
        "subdomain": "foundation",
        "mastery_sessions": 3,
        "description": "Atomic structure, bonding, chemical equations, stoichiometry, periodic table",
        "badge": "⚗️ Chemistry Catalyst",
        "topics": ["atomic structure", "chemical bonding", "redox reactions", "stoichiometry"],
        "ai_relevance": "Chemical modeling and molecular dynamics simulation"
    },
    
    "organic-chemistry-intro": {
        "name": "Introductory Organic Chemistry",
        "level": "Beginner",
        "subdomain": "foundation",
        "mastery_sessions": 2,
        "description": "Organic compounds, functional groups, nomenclature",
        "badge": "🧪 Organic Pioneer",
        "topics": ["hydrocarbons", "functional groups", "nomenclature", "reactions"],
        "ai_relevance": "Predicting organic compound properties with AI"
    },
    
    # ── General Physics ──────────────────────────────────────────────────
    "general-physics": {
        "name": "General Physics",
        "level": "Beginner",
        "subdomain": "foundation",
        "mastery_sessions": 2,
        "description": "Mechanics, thermodynamics, optics, waves",
        "badge": "⚡ Physics Fundamentals",
        "topics": ["kinematics", "forces", "energy", "thermodynamics", "light"],
        "ai_relevance": "Physics-based simulation and modeling of microbial processes"
    },
    
    # ── Mathematics & Statistics ─────────────────────────────────────────
    "mathematics-fundamentals": {
        "name": "Mathematics Fundamentals",
        "level": "Beginner",
        "subdomain": "foundation",
        "mastery_sessions": 2,
        "description": "Algebra, calculus, differential equations",
        "badge": "🧮 Math Maestro",
        "topics": ["algebra", "calculus", "differential equations"],
        "ai_relevance": "Mathematical modeling of microbial growth kinetics"
    },
    
    "statistics-for-science": {
        "name": "Statistics for Science",
        "level": "Beginner",
        "subdomain": "foundation",
        "mastery_sessions": 3,
        "description": "Descriptive statistics, distributions, hypothesis testing, data analysis",
        "badge": "📊 Stats Scientist",
        "topics": ["descriptive stats", "probability", "hypothesis testing", "regression"],
        "ai_relevance": "Essential for ML model validation and scientific data analysis"
    },
    
    # ── Basic Laboratory Techniques ──────────────────────────────────────
    "basic-lab-techniques": {
        "name": "Basic Laboratory Techniques",
        "level": "Beginner",
        "subdomain": "foundation",
        "mastery_sessions": 4,
        "description": "Aseptic technique, sterilization, pipetting, dilution series, sample preparation",
        "badge": "🔬 Lab Technician",
        "topics": ["autoclaving", "pipetting", "dilutions", "buffer preparation", "safety protocols"],
        "ai_relevance": "Critical for training AI systems on lab procedure automation"
    },
    
    "microscopy-basics": {
        "name": "Microscopy Basics",
        "level": "Beginner",
        "subdomain": "foundation",
        "mastery_sessions": 3,
        "description": "Compound microscope operation, magnification, resolution, focusing",
        "badge": "🔎 Microscopy Novice",
        "topics": ["microscope operation", "slide preparation", "magnification", "depth of field"],
        "ai_relevance": "Image analysis and automated microscopy with computer vision"
    },
    
    # ── General Microbiology (ND Core) ───────────────────────────────────
    "microbial-diversity": {
        "name": "Microbial Diversity",
        "level": "Beginner",
        "subdomain": "general-microbiology",
        "mastery_sessions": 3,
        "description": "Bacteria, archaea, fungi, viruses, protozoa - classification and characteristics",
        "badge": "🧬 Microbial Explorer",
        "topics": ["bacterial morphology", "fungal types", "viral structure", "protozoal forms"],
        "ai_relevance": "Taxonomic classification with deep learning models"
    },
    
    "microbial-staining": {
        "name": "Microbial Staining Techniques",
        "level": "Beginner",
        "subdomain": "general-microbiology",
        "mastery_sessions": 3,
        "description": "Gram staining, acid-fast staining, spore staining, flagella staining",
        "badge": "🎨 Staining Specialist",
        "topics": ["gram staining", "acid-fast staining", "spore stains", "negative staining"],
        "ai_relevance": "Image recognition of stained microbial preparations"
    },
    
    "microbial-cultivation": {
        "name": "Microbial Cultivation",
        "level": "Beginner",
        "subdomain": "general-microbiology",
        "mastery_sessions": 3,
        "description": "Culture media preparation, culturing techniques, colony morphology",
        "badge": "🌱 Culture Cultivator",
        "topics": ["growth media", "colony identification", "culture maintenance"],
        "ai_relevance": "Predictive modeling of microbial growth in fermentation systems"
    },
    
    "introductory-biochemistry": {
        "name": "Introductory Biochemistry",
        "level": "Beginner",
        "subdomain": "general-microbiology",
        "mastery_sessions": 2,
        "description": "Proteins, carbohydrates, lipids, nucleic acids, metabolic pathways",
        "badge": "🧬 Biochemistry Basics",
        "topics": ["amino acids", "proteins", "carbohydrate metabolism", "nucleic acids"],
        "ai_relevance": "Bioinformatics and protein structure prediction"
    },
    
    "english-communication": {
        "name": "Scientific Communication (English)",
        "level": "Beginner",
        "subdomain": "foundation",
        "mastery_sessions": 2,
        "description": "Technical writing, lab reports, scientific notation, presentation",
        "badge": "📝 Science Writer",
        "topics": ["lab reports", "scientific writing", "data presentation"],
        "ai_relevance": "NLP models for automated lab report generation and analysis"
    },
    
    # ========================================================================
    # INTERMEDIATE SKILLS (HND Applied Science - Microbiology)
    # ========================================================================
    
    # ── Advanced Microbiology ────────────────────────────────────────────
    "advanced-microbiology": {
        "name": "Advanced General Microbiology",
        "level": "Intermediate",
        "subdomain": "advanced-microbiology",
        "mastery_sessions": 4,
        "description": "Microbial ecology, biofilms, quorum sensing, microbial interactions",
        "badge": "🌍 Micro Ecologist",
        "topics": ["biofilms", "quorum sensing", "microbial communities", "interactions"],
        "ai_relevance": "Modeling complex microbial ecosystems with AI"
    },
    
    "microbial-physiology": {
        "name": "Microbial Physiology & Metabolism",
        "level": "Intermediate",
        "subdomain": "advanced-microbiology",
        "mastery_sessions": 4,
        "description": "Bacterial metabolism, aerobic/anaerobic respiration, fermentation, energy production",
        "badge": "⚡ Metabolism Master",
        "topics": ["glycolysis", "krebs cycle", "electron transport", "fermentation", "photosynthesis"],
        "ai_relevance": "Metabolic modeling and pathway prediction with ML"
    },
    
    "microbial-genetics": {
        "name": "Microbial Genetics & Molecular Biology",
        "level": "Intermediate",
        "subdomain": "advanced-microbiology",
        "mastery_sessions": 5,
        "description": "DNA/RNA structure, replication, transcription, translation, mutations, plasmids, genetic engineering",
        "badge": "🧬 Genetic Engineer",
        "topics": ["DNA/RNA", "replication", "transcription", "translation", "mutations", "plasmids"],
        "ai_relevance": "Genomic analysis, sequence prediction, gene annotation with bioinformatics"
    },
    
    # ── Diagnostic Microbiology ──────────────────────────────────────────
    "medical-microbiology": {
        "name": "Medical Microbiology & Parasitology",
        "level": "Intermediate",
        "subdomain": "medical",
        "mastery_sessions": 4,
        "description": "Pathogenic bacteria, viruses, fungi, parasites; disease mechanisms; identification",
        "badge": "🏥 Clinical Microbiologist",
        "topics": ["pathogens", "pathogenesis", "disease identification", "antibiotic resistance"],
        "ai_relevance": "Disease prediction and diagnosis with clinical decision support AI"
    },
    
    "parasitology": {
        "name": "Parasitology",
        "level": "Intermediate",
        "subdomain": "medical",
        "mastery_sessions": 3,
        "description": "Parasitic diseases, parasitic organisms, life cycles, epidemiology",
        "badge": "🦠 Parasite Expert",
        "topics": ["helminths", "protozoan parasites", "life cycles", "epidemiology"],
        "ai_relevance": "Disease epidemiology prediction and surveillance"
    },
    
    "immunology": {
        "name": "Immunology",
        "level": "Intermediate",
        "subdomain": "medical",
        "mastery_sessions": 4,
        "description": "Immune system, innate/adaptive immunity, antibodies, antigens, immune response",
        "badge": "🛡️ Immunity Architect",
        "topics": ["innate immunity", "adaptive immunity", "antibodies", "vaccines", "immunoassays"],
        "ai_relevance": "Vaccine design and immune prediction with machine learning"
    },
    
    "virology": {
        "name": "Virology",
        "level": "Intermediate",
        "subdomain": "medical",
        "mastery_sessions": 3,
        "description": "Viral structure, replication, classification, viral diseases, antiviral strategies",
        "badge": "🦠 Virologist",
        "topics": ["viral structure", "replication", "classification", "pathogenesis", "epidemiology"],
        "ai_relevance": "Viral genome analysis and mutation prediction"
    },
    
    # ── Environmental Microbiology ───────────────────────────────────────
    "environmental-microbiology": {
        "name": "Environmental Microbiology",
        "level": "Intermediate",
        "subdomain": "environmental",
        "mastery_sessions": 4,
        "description": "Water quality testing, soil microorganisms, bioremediation, biogeochemical cycles",
        "badge": "🌍 Eco Microbiologist",
        "topics": ["water testing", "soil ecology", "bioremediation", "nutrient cycles"],
        "ai_relevance": "Environmental monitoring and predictive water quality models"
    },
    
    "water-microbiology": {
        "name": "Water Microbiology",
        "level": "Intermediate",
        "subdomain": "environmental",
        "mastery_sessions": 3,
        "description": "Waterborne pathogens, water testing protocols, purification, sanitation",
        "badge": "💧 Water Scientist",
        "topics": ["pathogen detection", "indicator organisms", "water treatment", "quality standards"],
        "ai_relevance": "AI-driven water quality prediction (relevant to Zamfara State Waterboard experience)"
    },
    
    # ── Food & Dairy Microbiology ────────────────────────────────────────
    "food-microbiology": {
        "name": "Food & Dairy Microbiology",
        "level": "Intermediate",
        "subdomain": "food",
        "mastery_sessions": 4,
        "description": "Spoilage organisms, foodborne pathogens, fermentation, preservation, quality control",
        "badge": "🍽️ Food Safety Expert",
        "topics": ["spoilage microbes", "foodborne pathogens", "fermentation", "preservation"],
        "ai_relevance": "Food safety prediction and shelf-life modeling with AI"
    },
    
    "dairy-microbiology": {
        "name": "Dairy Microbiology",
        "level": "Intermediate",
        "subdomain": "food",
        "mastery_sessions": 3,
        "description": "Lactobacillus, yogurt production, cheese fermentation, milk quality testing",
        "badge": "🥛 Dairy Microbiologist",
        "topics": ["lactic acid bacteria", "yogurt/cheese production", "milk pathogen testing"],
        "ai_relevance": "Fermentation process optimization with ML"
    },
    
    # ── Industrial Microbiology ──────────────────────────────────────────
    "industrial-microbiology": {
        "name": "Industrial Microbiology & Biotechnology",
        "level": "Intermediate",
        "subdomain": "industrial",
        "mastery_sessions": 5,
        "description": "Fermentation, bioreactors, antibiotic production, enzyme production, recombinant DNA",
        "badge": "🏭 Biotech Engineer",
        "topics": ["fermentation", "bioreactors", "antibiotic production", "enzyme engineering"],
        "ai_relevance": "AI-optimized fermentation control and bioprocess design"
    },
    
    "fermentation-science": {
        "name": "Fermentation & Bioprocess Engineering",
        "level": "Intermediate",
        "subdomain": "industrial",
        "mastery_sessions": 4,
        "description": "Fermentation kinetics, bioreactor design, scale-up, downstream processing",
        "badge": "⚙️ Fermentation Master",
        "topics": ["batch fermentation", "fed-batch", "continuous culture", "downstream processing"],
        "ai_relevance": "Predictive fermentation modeling and real-time bioprocess optimization"
    },
    
    # ── Mycology ─────────────────────────────────────────────────────────
    "mycology": {
        "name": "Mycology",
        "level": "Intermediate",
        "subdomain": "medical",
        "mastery_sessions": 3,
        "description": "Fungal classification, fungal diseases, identification, cultivation",
        "badge": "🍄 Mycologist",
        "topics": ["fungal morphology", "ascomycetes", "basidiomycetes", "mycotic diseases"],
        "ai_relevance": "Fungal species identification with image recognition"
    },
    
    # ── Biochemistry of Microorganisms ───────────────────────────────────
    "biochemistry-microbes": {
        "name": "Biochemistry of Microorganisms",
        "level": "Intermediate",
        "subdomain": "advanced-microbiology",
        "mastery_sessions": 3,
        "description": "Microbial enzymes, secondary metabolism, biosynthetic pathways",
        "badge": "🧪 Microbial Biochemist",
        "topics": ["enzyme biochemistry", "secondary metabolites", "biosynthetic pathways"],
        "ai_relevance": "Enzyme engineering and metabolite prediction"
    },
    
    # ── Quality Control & Assurance ──────────────────────────────────────
    "quality-control": {
        "name": "Quality Control & Quality Assurance",
        "level": "Intermediate",
        "subdomain": "industrial",
        "mastery_sessions": 4,
        "description": "Sterility testing, potency testing, contamination detection, validation",
        "badge": "✅ QA Specialist",
        "topics": ["sterility testing", "contamination detection", "validation", "GMP"],
        "ai_relevance": "Automated defect detection and quality prediction"
    },
    
    # ========================================================================
    # ADVANCED SKILLS (HND Project & Specialization)
    # ========================================================================
    
    # ── Research Methods ─────────────────────────────────────────────────
    "research-methods": {
        "name": "Research Methods & Laboratory Techniques",
        "level": "Advanced",
        "subdomain": "research",
        "mastery_sessions": 5,
        "description": "Experimental design, data collection, scientific methodology, lab protocols",
        "badge": "🔬 Research Scientist",
        "topics": ["experimental design", "controls", "replication", "documentation"],
        "ai_relevance": "Automated experimental design and hypothesis generation"
    },
    
    "instrumental-analysis": {
        "name": "Instrumental Methods of Analysis",
        "level": "Advanced",
        "subdomain": "research",
        "mastery_sessions": 4,
        "description": "HPLC, GC, spectrophotometry, mass spectrometry, chromatography",
        "badge": "🔧 Instrument Master",
        "topics": ["HPLC", "GC", "spectrophotometry", "mass spectrometry"],
        "ai_relevance": "Automated instrument control and data interpretation with AI"
    },
    
    "biostatistics": {
        "name": "Biostatistics",
        "level": "Advanced",
        "subdomain": "research",
        "mastery_sessions": 4,
        "description": "Study design, statistical inference, survival analysis, epidemiological statistics",
        "badge": "📊 Biostat Expert",
        "topics": ["study design", "hypothesis testing", "survival analysis", "regression"],
        "ai_relevance": "Statistical learning and predictive modeling"
    },
    
    # ── Final Year Project ───────────────────────────────────────────────
    "parasitology-epidemiology": {
        "name": "Parasitology & Epidemiology - Schistosomiasis Research",
        "level": "Advanced",
        "subdomain": "research",
        "mastery_sessions": 6,
        "description": "Schistosoma haematobium prevalence, epidemiological surveys, community-based research, data analysis",
        "badge": "🏆 Epidemiologist",
        "topics": ["prevalence surveys", "epidemiological methods", "community health", "data analysis"],
        "ai_relevance": "Disease surveillance and prediction models (PRIMARY RESEARCH FOCUS)"
    },
    
    # ── Collaborative & Emerging Areas ───────────────────────────────────
    "ai-powered-diagnostics": {
        "name": "AI-Powered Diagnostic Microbiology",
        "level": "Advanced",
        "subdomain": "ai-emerging",
        "mastery_sessions": 4,
        "description": "Machine learning for pathogen identification, automated microscopy, diagnostic algorithms",
        "badge": "🤖 AI Diagnostician",
        "topics": ["image recognition", "ML classifiers", "diagnostic algorithms", "expert systems"],
        "ai_relevance": "PRIMARY FOCUS: Bridging microbiology with AI/ML for next-gen diagnostics"
    },
    
    "machine-learning-microbiology": {
        "name": "Machine Learning for Microbiology",
        "level": "Advanced",
        "subdomain": "ai-emerging",
        "mastery_sessions": 5,
        "description": "Genomic analysis, biomarker discovery, predictive modeling, deep learning applications",
        "badge": "🧠 ML Microbiologist",
        "topics": ["genomic ML", "biomarker discovery", "neural networks", "time-series forecasting"],
        "ai_relevance": "PRIMARY FOCUS: AI integration for microbial research and innovation"
    },
    
    "bioinformatics": {
        "name": "Bioinformatics",
        "level": "Advanced",
        "subdomain": "ai-emerging",
        "mastery_sessions": 4,
        "description": "Sequence analysis, phylogenomics, protein structure prediction, database mining",
        "badge": "🧬 Bioinformatician",
        "topics": ["sequence alignment", "phylogenetics", "structure prediction", "databases"],
        "ai_relevance": "Genomic data analysis and evolutionary insights"
    },
    
    # ========================================================================
    # MASTER SKILLS (Innovation & Advanced Applications)
    # ========================================================================
    
    "advanced-biotech": {
        "name": "Advanced Biotechnology Innovation",
        "level": "Master",
        "subdomain": "innovation",
        "mastery_sessions": 6,
        "description": "Synthetic biology, CRISPR, gene therapy, cell culture engineering",
        "badge": "🚀 Biotech Innovator",
        "topics": ["synthetic biology", "CRISPR", "gene therapy", "cell engineering"],
        "ai_relevance": "AI-guided genetic design and optimization"
    },
    
    "precision-medicine": {
        "name": "Precision Medicine with AI",
        "level": "Master",
        "subdomain": "innovation",
        "mastery_sessions": 5,
        "description": "Personalized diagnostics, targeted treatment, genomic medicine, clinical AI",
        "badge": "💊 Precision Medicine Expert",
        "topics": ["genomic medicine", "personalized diagnosis", "treatment optimization"],
        "ai_relevance": "Patient-specific predictions and treatment selection"
    },
    
    "global-health-ai": {
        "name": "Global Health & AI for Disease Surveillance",
        "level": "Master",
        "subdomain": "innovation",
        "mastery_sessions": 5,
        "description": "Epidemic forecasting, real-time surveillance, AI-driven outbreak detection",
        "badge": "🌍 Global Health Leader",
        "topics": ["disease surveillance", "epidemic modeling", "outbreak detection", "wastewater genomics"],
        "ai_relevance": "PRIMARY FOCUS: Using AI for African health challenges (water quality, disease monitoring)"
    },
    
    "entrepreneurship-biotech": {
        "name": "Biotech Entrepreneurship",
        "level": "Master",
        "subdomain": "innovation",
        "mastery_sessions": 4,
        "description": "Startup strategy, product development, regulatory pathway, commercialization",
        "badge": "💼 BioTech Entrepreneur",
        "topics": ["business planning", "IP strategy", "regulatory affairs", "fundraising"],
        "ai_relevance": "Market analysis and strategic planning with AI"
    },
}

LEVEL_ORDER = ["Beginner", "Intermediate", "Advanced", "Master"]

LEVEL_THRESHOLDS = {
    "Beginner": 5,       # 5 beginner skills to unlock Intermediate
    "Intermediate": 6,   # 6 intermediate skills to unlock Advanced
    "Advanced": 4,       # 4 advanced skills to unlock Master
}

SUBDOMAIN_MAP = {
    "foundation": "Foundation Sciences (Biology, Chemistry, Physics, Math)",
    "general-microbiology": "General Microbiology (ND Core)",
    "advanced-microbiology": "Advanced Microbiology",
    "medical": "Medical & Diagnostic Microbiology",
    "environmental": "Environmental Microbiology (Water Quality Expertise)",
    "food": "Food & Dairy Microbiology",
    "industrial": "Industrial Microbiology & Biotechnology",
    "research": "Research Methods & Data Analysis",
    "ai-emerging": "AI-Powered Microbiology (EMERGING FOCUS)",
    "innovation": "Innovation & Advanced Applications",
}


# ---------------------------------------------------------------------------
# Utility Functions for Vector Database Integration
# ---------------------------------------------------------------------------

def get_microbiology_catalogue() -> dict[str, dict]:
    """Return the complete microbiology skills catalogue."""
    return MICROBIOLOGY_SKILLS.copy()


def get_skills_by_level(level: str) -> dict[str, dict]:
    """Get all skills for a specific level (Beginner, Intermediate, Advanced, Master)."""
    return {
        tag: info for tag, info in MICROBIOLOGY_SKILLS.items()
        if info.get("level") == level
    }


def get_skills_by_subdomain(subdomain: str) -> dict[str, dict]:
    """Get all skills in a specific subdomain."""
    return {
        tag: info for tag, info in MICROBIOLOGY_SKILLS.items()
        if info.get("subdomain") == subdomain
    }


def get_vector_representation(skill_tag: str) -> dict[str, Any]:
    """
    Generate vector-friendly representation of a skill for embedding in vector DB.
    
    Returns
    -------
    dict with skill metadata flattened for embedding
    """
    skill = MICROBIOLOGY_SKILLS.get(skill_tag, {})
    if not skill:
        return {}
    
    return {
        "skill_id": skill_tag,
        "skill_name": skill.get("name"),
        "level": skill.get("level"),
        "subdomain": skill.get("subdomain"),
        "description": skill.get("description"),
        "topics": " | ".join(skill.get("topics", [])),
        "ai_relevance": skill.get("ai_relevance"),
        "badge": skill.get("badge"),
        "mastery_sessions": skill.get("mastery_sessions"),
        "combined_text": f"{skill.get('name')} - {skill.get('description')} - {skill.get('ai_relevance')}",
    }


def export_for_vector_db(format_type: str = "jsonl") -> str:
    """
    Export all microbiology skills in vector-DB-friendly formats.
    
    Parameters
    ----------
    format_type : str
        "jsonl" (default) for line-delimited JSON, "json" for array
    
    Returns
    -------
    str
        Serialized data ready for vector database import
    """
    records = [
        get_vector_representation(tag)
        for tag in MICROBIOLOGY_SKILLS.keys()
    ]
    
    if format_type == "jsonl":
        return "\n".join(json.dumps(record) for record in records)
    elif format_type == "json":
        return json.dumps(records, indent=2)
    else:
        raise ValueError(f"Unsupported format: {format_type}")


def get_skills_summary() -> dict[str, Any]:
    """
    Generate a summary of all microbiology skills by level and subdomain.
    """
    summary = {
        "total_skills": len(MICROBIOLOGY_SKILLS),
        "by_level": {},
        "by_subdomain": {},
        "ai_focus_areas": [],
    }
    
    for level in LEVEL_ORDER:
        skills = get_skills_by_level(level)
        summary["by_level"][level] = len(skills)
    
    for subdomain in set(s.get("subdomain") for s in MICROBIOLOGY_SKILLS.values()):
        skills = get_skills_by_subdomain(subdomain)
        summary["by_subdomain"][subdomain] = {
            "count": len(skills),
            "description": SUBDOMAIN_MAP.get(subdomain, subdomain),
        }
    
    # Identify AI-focus areas
    ai_focus = [
        tag for tag, info in MICROBIOLOGY_SKILLS.items()
        if "ai" in info.get("ai_relevance", "").lower() or "PRIMARY FOCUS" in info.get("ai_relevance", "")
    ]
    summary["ai_focus_areas"] = ai_focus
    summary["ai_focus_count"] = len(ai_focus)
    
    return summary


# ---------------------------------------------------------------------------
# Quick Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 80)
    print("MICROBIOLOGY SKILLS CATALOGUE")
    print("=" * 80)
    
    summary = get_skills_summary()
    print(f"\nTotal Skills: {summary['total_skills']}")
    print(f"AI Focus Areas: {summary['ai_focus_count']}")
    
    print("\n--- Skills by Level ---")
    for level, count in summary["by_level"].items():
        print(f"  {level}: {count} skills")
    
    print("\n--- Skills by Subdomain ---")
    for subdomain, info in summary["by_subdomain"].items():
        print(f"  {subdomain}: {info['count']} skills")
    
    print("\n--- AI Focus Areas ---")
    for tag in summary["ai_focus_areas"][:5]:
        skill = MICROBIOLOGY_SKILLS[tag]
        print(f"  • {skill['name']} ({skill['level']})")
    
    print("\n--- Vector DB Export (first 2 records) ---")
    export = export_for_vector_db("json")
    records = json.loads(export)
    for record in records[:2]:
        print(json.dumps(record, indent=2))
