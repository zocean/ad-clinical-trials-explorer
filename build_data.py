#!/usr/bin/env python3
"""
Build script to aggregate all clinical trial JSON files into a single data file.
This makes it efficient for the website to load all trials at once.
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def main():
    data_dir = Path(__file__).parent / "data"
    gene_data_dir = Path(__file__).parent.parent / "json_output_drug"
    output_file = Path(__file__).parent / "trials_data.js"
    
    trials = []
    drug_counts = defaultdict(int)
    category_counts = defaultdict(int)
    agent_type_counts = defaultdict(int)
    gene_counts = defaultdict(int)
    
    # Create a map of NCT IDs to gene data
    gene_data_map = {}
    if gene_data_dir.exists():
        print(f"Loading gene data from {gene_data_dir}...")
        for json_file in sorted(gene_data_dir.glob("*.json")):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    gene_data = json.load(f)
                    nct_id = gene_data.get("nct_id")
                    if nct_id:
                        gene_data_map[nct_id] = {
                            "gene_symbol": gene_data.get("gene_symbol", []),
                            "explanation_target_gene": gene_data.get("explanation_target_gene", []),
                            "confidence_level": gene_data.get("confidence_level", "")
                        }
                        # Count genes
                        for gene in gene_data.get("gene_symbol", []):
                            if gene:
                                gene_counts[gene] += 1
            except Exception as e:
                print(f"Error loading gene data from {json_file}: {e}")
        print(f"Loaded gene data for {len(gene_data_map)} trials")
    
    # Walk through all subdirectories
    for trial_dir in sorted(data_dir.iterdir()):
        if trial_dir.is_dir():
            # Find JSON files in this directory
            json_files = list(trial_dir.glob("*.json"))
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        trial = json.load(f)
                    
                    nct_id = trial.get("nct_id", "")
                    
                    # Normalize target category (handle case variations)
                    raw_category = trial.get("target_category", "N/A") or "N/A"
                    category_map = {
                        "cognitive enhancer": "Cognitive Enhancer",
                        "Cognitive enhancer": "Cognitive Enhancer",
                        "disease-targeted small molecule": "Disease-Targeted Small Molecule",
                        "Disease-targeted small molecule": "Disease-Targeted Small Molecule",
                        "disease-targeted biologic": "Disease-Targeted Biologic",
                        "Disease-targeted biologic": "Disease-Targeted Biologic",
                        "neuropsychiatric symptom improvement": "Neuropsychiatric Symptom Improvement",
                        "Neuropsychiatric symptom improvement": "Neuropsychiatric Symptom Improvement",
                    }
                    normalized_category = category_map.get(raw_category, raw_category)
                    
                    # Get gene data if available
                    gene_data = gene_data_map.get(nct_id, {})
                    
                    # Clean up the trial data
                    cleaned_trial = {
                        "nct_id": nct_id,
                        "title": trial.get("title", ""),
                        "status": trial.get("status", ""),
                        "last_update_time": trial.get("last_update_time", ""),
                        "description_brief": trial.get("description_brief", ""),
                        "phase": trial.get("phase", []),
                        "study_type": trial.get("study_type", ""),
                        "target_category": normalized_category,
                        "drug": trial.get("drug", []),
                        "agent_type": trial.get("agent_type", "N/A"),
                        "explanation_target": trial.get("explanation_target", []),
                        "explanation_agent": trial.get("explanation_agent", []),
                        "gene_symbol": gene_data.get("gene_symbol", []),
                        "explanation_target_gene": gene_data.get("explanation_target_gene", []),
                        "confidence_level": gene_data.get("confidence_level", ""),
                    }
                    
                    trials.append(cleaned_trial)
                    
                    # Count drugs
                    for drug in cleaned_trial["drug"]:
                        if drug:
                            drug_counts[drug] += 1
                    
                    # Count categories
                    cat = cleaned_trial["target_category"]
                    if cat:
                        category_counts[cat] += 1
                    
                    # Count agent types
                    agent = cleaned_trial["agent_type"]
                    if agent:
                        agent_type_counts[agent] += 1
                        
                except Exception as e:
                    print(f"Error processing {json_file}: {e}")
    
    # Calculate total unique drugs before filtering
    total_unique_drugs = len(drug_counts)
    
    # Sort drug counts for word cloud (top 25)
    top_drugs = sorted(drug_counts.items(), key=lambda x: -x[1])[:25]
    
    # Sort gene counts for word cloud (top 50)
    top_genes = sorted(gene_counts.items(), key=lambda x: -x[1])[:50]
    
    # Create the output data structure
    output_data = {
        "trials": trials,
        "drug_counts": dict(top_drugs),
        "gene_counts": dict(top_genes),
        "category_counts": dict(category_counts),
        "agent_type_counts": dict(agent_type_counts),
        "total_trials": len(trials),
        "total_unique_drugs": total_unique_drugs
    }
    
    # Write as JavaScript file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("// Auto-generated clinical trials data\n")
        f.write(f"const TRIALS_DATA = {json.dumps(output_data, indent=2, ensure_ascii=False)};\n")
    
    print(f"Successfully processed {len(trials)} trials")
    print(f"Output written to {output_file}")
    print(f"\nCategory distribution:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    print(f"\nTop 10 drugs:")
    for drug, count in top_drugs[:10]:
        print(f"  {drug}: {count}")
    print(f"\nTop 10 genes:")
    for gene, count in top_genes[:10]:
        print(f"  {gene}: {count}")

if __name__ == "__main__":
    main()

