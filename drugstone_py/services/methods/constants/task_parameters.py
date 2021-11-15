class TaskParameters:

    IDENTIFIER = [
        "symbol", 
        "uniprot", 
        "ensg"
    ]

    ALGORITHM = [
        "multisteiner", 
        "keypathwayminer", 
        "trustrank", 
        "closeness", 
        "degree", 
        "proximity", 
        "betweenness"
    ]

    PPI = [
        "STRING", 
        "BioGRID", 
        "APID"
    ]

    PDI = [
        "drugbank", 
        "chembl", 
        "dgidb"
    ]

    TARGET = [
        "drug", 
        "drug-target"
    ]