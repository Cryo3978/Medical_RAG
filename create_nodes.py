import csv
import json

semantic_groups = {
    "AnatomicalEntity": [],
    "ChemicalDrug": [],
    "MedicalCondition": [],
    "GeneOrSequence": [],
    "PhysiologicalProcess": [],
    "ClinicalPhenomenon": [],
    "MedicalDevice": [],
    "MedicalProcedure": [],
    "Organization": [],
    "MedicalConcept": [],
    "BehavioralActivity": [],
    "PopulationGroup": [],
    "LivingEntity": [],
    "BiologicalSubstance": [],
    "SpaceTimeConcept": []
}

sty_to_group = {
    # AnatomicalEntity
    'Anatomical Structure': 'AnatomicalEntity',
    'Body Part, Organ, or Organ Component': 'AnatomicalEntity',
    'Tissue': 'AnatomicalEntity',
    'Cell': 'AnatomicalEntity',
    'Cell Component': 'AnatomicalEntity',
    'Fully Formed Anatomical Structure': 'AnatomicalEntity',
    'Embryonic Structure': 'AnatomicalEntity',
    'Body System': 'AnatomicalEntity',
    'Body Location or Region': 'AnatomicalEntity',
    'Body Space or Junction': 'AnatomicalEntity',

    # ChemicalDrug
    'Pharmacologic Substance': 'ChemicalDrug',
    'Organic Chemical': 'ChemicalDrug',
    'Inorganic Chemical': 'ChemicalDrug',
    'Antibiotic': 'ChemicalDrug',
    'Clinical Drug': 'ChemicalDrug',
    'Vitamin': 'ChemicalDrug',
    'Hormone': 'ChemicalDrug',
    'Amino Acid, Peptide, or Protein': 'ChemicalDrug',
    'Nucleic Acid, Nucleoside, or Nucleotide': 'ChemicalDrug',
    'Amino Acid Sequence': 'ChemicalDrug',
    'Nucleotide Sequence': 'ChemicalDrug',
    'Molecular Sequence': 'GeneOrSequence',
    'Biologically Active Substance': 'BiologicalSubstance',
    'Chemical Viewed Structurally': 'BiologicalSubstance',
    'Chemical Viewed Functionally': 'BiologicalSubstance',
    'Element, Ion, or Isotope': 'BiologicalSubstance',
    'Substance': 'BiologicalSubstance',

    # MedicalCondition
    'Disease or Syndrome': 'MedicalCondition',
    'Neoplastic Process': 'MedicalCondition',
    'Pathologic Function': 'MedicalCondition',
    'Injury or Poisoning': 'MedicalCondition',
    'Congenital Abnormality': 'MedicalCondition',
    'Acquired Abnormality': 'MedicalCondition',
    'Experimental Model of Disease': 'MedicalCondition',
    'Sign or Symptom': 'MedicalCondition',
    'Anatomical Abnormality': 'MedicalCondition',
    'Mental or Behavioral Dysfunction': 'MedicalCondition',

    # GeneOrSequence
    'Gene or Genome': 'GeneOrSequence',
    'Genetic Function': 'GeneOrSequence',

    # PhysiologicalProcess
    'Cell Function': 'PhysiologicalProcess',
    'Organ or Tissue Function': 'PhysiologicalProcess',
    'Physiologic Function': 'PhysiologicalProcess',
    'Molecular Function': 'PhysiologicalProcess',
    'Biologic Function': 'PhysiologicalProcess',
    'Organism Function': 'PhysiologicalProcess',

    # ClinicalPhenomenon
    'Natural Phenomenon or Process': 'ClinicalPhenomenon',
    'Human-caused Phenomenon or Process': 'ClinicalPhenomenon',
    'Phenomenon or Process': 'ClinicalPhenomenon',
    'Environmental Effect of Humans': 'ClinicalPhenomenon',
    'Event': 'ClinicalPhenomenon',

    # MedicalDevice
    'Medical Device': 'MedicalDevice',
    'Research Device': 'MedicalDevice',
    'Drug Delivery Device': 'MedicalDevice',
    'Biomedical or Dental Material': 'MedicalDevice',

    # MedicalProcedure
    'Therapeutic or Preventive Procedure': 'MedicalProcedure',
    'Diagnostic Procedure': 'MedicalProcedure',
    'Laboratory Procedure': 'MedicalProcedure',
    'Laboratory or Test Result': 'MedicalProcedure',
    'Molecular Biology Research Technique': 'MedicalProcedure',

    # Organization
    'Organization': 'Organization',
    'Professional Society': 'Organization',
    'Health Care Related Organization': 'Organization',
    'Self-help or Relief Organization': 'Organization',

    # MedicalConcept
    'Conceptual Entity': 'MedicalConcept',
    'Idea or Concept': 'MedicalConcept',
    'Functional Concept': 'MedicalConcept',
    'Qualitative Concept': 'MedicalConcept',
    'Classification': 'MedicalConcept',
    'Intellectual Product': 'MedicalConcept',
    'Regulation or Law': 'MedicalConcept',
    'Quantitative Concept': 'MedicalConcept',

    # BehavioralActivity
    'Activity': 'BehavioralActivity',
    'Behavior': 'BehavioralActivity',
    'Social Behavior': 'BehavioralActivity',
    'Individual Behavior': 'BehavioralActivity',
    'Occupational Activity': 'BehavioralActivity',
    'Daily or Recreational Activity': 'BehavioralActivity',
    'Educational Activity': 'BehavioralActivity',
    'Research Activity': 'BehavioralActivity',
    'Machine Activity': 'BehavioralActivity',
    'Professional or Occupational Group': 'BehavioralActivity',

    # PopulationGroup
    'Population Group': 'PopulationGroup',
    'Patient or Disabled Group': 'PopulationGroup',
    'Family Group': 'PopulationGroup',
    'Age Group': 'PopulationGroup',
    'Group': 'PopulationGroup',
    'Group Attribute': 'PopulationGroup',

    # LivingEntity
    'Human': 'LivingEntity',
    'Organism': 'LivingEntity',
    'Animal': 'LivingEntity',
    'Vertebrate': 'LivingEntity',
    'Mammal': 'LivingEntity',
    'Bird': 'LivingEntity',
    'Fish': 'LivingEntity',
    'Reptile': 'LivingEntity',
    'Amphibian': 'LivingEntity',
    'Bacterium': 'LivingEntity',
    'Virus': 'LivingEntity',
    'Fungus': 'LivingEntity',
    'Archaeon': 'LivingEntity',
    'Eukaryote': 'LivingEntity',
    'Plant': 'LivingEntity',
    'Organism Attribute': 'LivingEntity',
    'Human-caused Phenomenon or Process': 'ClinicalPhenomenon',

    # SpaceTimeConcept
    'Spatial Concept': 'SpaceTimeConcept',
    'Temporal Concept': 'SpaceTimeConcept',
    'Geographic Area': 'SpaceTimeConcept',
    'Body Location or Region': 'SpaceTimeConcept',
    
    "Food": "BiologicalSubstance",
    "Body Substance": "AnatomicalEntity",
    "Clinical Attribute": "MedicalConcept",
    "Biomedical Occupation or Discipline": "BehavioralActivity",
    "Finding": "MedicalCondition",
    "Receptor": "GeneOrSequence",
    "Language": "MedicalConcept",
    "Indicator, Reagent, or Diagnostic Aid": "MedicalDevice",
    "Manufactured Object": "MedicalDevice",
    "Mental Process": "PhysiologicalProcess",
    "Enzyme": "GeneOrSequence",
    "Immunologic Factor": "GeneOrSequence",
    "Cell or Molecular Dysfunction": "MedicalCondition",
    "Occupation or Discipline": "BehavioralActivity",
    "Entity": "MedicalConcept",
    "Physical Object": "MedicalDevice",
    "Chemical": "BiologicalSubstance",
    "Health Care Activity": "BehavioralActivity",
    "Carbohydrate Sequence": "GeneOrSequence",
    "Governmental or Regulatory Activity": "MedicalConcept",
    "Hazardous or Poisonous Substance": "BiologicalSubstance"
}


def parse_mrconso(path):
    cui_dict = {}
    with open(path, "r", encoding="utf-8",errors="ignore") as f:
        for line in f:
            parts = line.strip().split("|")
            cui, lat, ts, pref, sab, code, name = parts[0], parts[1], parts[2], parts[6], parts[11], parts[13], parts[14]
            if lat=='ENG'and pref=='Y':
                if cui not in cui_dict:
                    cui_dict[cui] = {
                        "name": name,
                        "sab": sab,
                        "code": code,
                        "other names":[]
                    }
                else:
                    cui_dict[cui]['other names'].append(name)
    return cui_dict

def parse_mrsty(path):
    missing_cats=set()
    cui_types = {}
    with open(path, "r", encoding="utf-8",errors="ignore") as f:
        for line in f:
            parts = line.strip().split("|")
            cui = parts[0]
            tui = parts[1]
            label = parts[3]
            if label in sty_to_group:
                category=sty_to_group[label]
            else:
                missing_cats.add(label)
                
            cui_types.setdefault(cui, []).append({"tui": tui, "label": label, "category": category })
    if missing_cats:
        print(f"cannotfind:{missing_cats}")
    else:
        print(f"all the rows have been successfully cated")
    return cui_types

def build_csv(mrconso_path, mrsty_path, output_csv_path):
    cui_data = parse_mrconso(mrconso_path)
    sty_data = parse_mrsty(mrsty_path)

    with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            ":ID", "name", "synonyms", "sab", "sab_code", "tui", "category:LABEL"
        ])
        writer.writeheader()

        for cui, data in cui_data.items():
            types = sty_data.get(cui, [])
            synonyms = [data['name']] + data["other names"]
            synonyms = synonyms[:10]  # Limit total to 20 to avoid huge strings
            writer.writerow({
                ":ID": cui,
                "name": data["name"],
                "synonyms": json.dumps(synonyms, ensure_ascii=False),
                "sab_code": data["code"],
                "sab": data["sab"],
                "tui": json.dumps([t["tui"] for t in types]),
                "category:LABEL": types[0]["category"] if types else ""
            })

    print(f"CSV saved to: {output_csv_path}")


# sample
build_csv("MRCONSO.RRF", "MRSTY.RRF", "umls_nodes.csv")
