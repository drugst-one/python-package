

def merge_results(first: dict, second: dict) -> dict:

    first_drugs = first["drugs"] if "drugs" in first else {}
    second_drugs = second["drugs"] if "drugs" in second else {}

    first_genes = first["genes"] if "genes" in first else {}
    second_genes = second["genes"] if "genes" in second else {}

    for drug, details in second_drugs.items():
        if drug in first_drugs:
            first_drugs[drug] = {**first_drugs[drug], **second_drugs[drug]}
        else:
            first_drugs[drug] = details

    for gene, details in second_genes.items():
        if gene in first_genes:
            for k, v in details.items():
                if k in first_genes[gene]:
                    if isinstance(v, list):
                        new_v = [*first_genes[gene][k], *v]
                        first_genes[gene][k] = new_v
                else:
                    first_genes[gene][k] = v
        else:
            first_genes[gene] = details

    return {"drugs": first_drugs, "genes": first_genes}
