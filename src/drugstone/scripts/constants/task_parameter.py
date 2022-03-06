"""
drugstone.scripts.constants.task_parameter

This module implements the class TaskParameter.

:copyright: 2022 Institute for Computational Systems Biology by Prof. Dr. Jan Baumbach
:author: Ugur Turhan
"""


class TaskParameter:

    # Available general parameters.
    IDENTIFIER = "identifier"
    ALGORITHM = "algorithm"
    PPI = "ppi_dataset"
    PDI = "pdi_dataset"
    TARGET = "target"
    MAX_DEG = "max_deg"
    INCLUDE_INDIRECT_DRUGS = "include_indirect_drugs"
    HUB_PENALTY = "hub_penalty"
    RESULT_SIZE = "result_size"
    INCLUDE_NON_APPROVED_DRUGS = "include_non_approved_drugs"
    FILTER_PATHS = "filter_paths"

    # Available parameter for the trustrank algorithm.
    class Trustrank:
        DAMPING_FACTOR = "damping_factor"

    # Available parameter for the multi steiner algorithm.
    class MultiSteiner:
        NUM_TREES = "num_trees"
        TOLERANCE = "tolerance"
    
    # Available parameter for the keypathwayminer algorithm.
    class KeyPathwayMiner:
        K = "k"

    # Available options for the 'identifier' parameter.
    class IdentifierValues:
        IDENTIFIER_VALUES = ["symbol", "uniprot", "ensg"]
        SYMBOL = "symbol"
        UNIPROT = "uniprot"
        ENSG = "ensg"

    # Available options for the 'algorithm' parameter.
    class AlgorithmValues:
        DRUG_TARGET_SEARCH_VALUES = [
            "multisteiner", "keypathwayminer", "trustrank",
            "closeness", "degree", "betweenness"
        ]
        DRUG_SEARCH_VALUES = ["trustrank", "closeness", "degree", "proximity"]
        ALGORITHM_VALUES = DRUG_TARGET_SEARCH_VALUES + DRUG_SEARCH_VALUES
        MULTISTEINER = "multisteiner"
        KEYPATHWAYMINER = "keypathwayminer"
        TRUSTRANK = "trustrank"
        CLOSENESS = "closeness"
        DEGREE = "degree"
        PROXIMITY = "proximity"
        BETWEENNESS = "betweenness"
    
    # Available options for the 'ppi' parameter.
    class PpiValues:
        PPI_VALUES = ["STRING", "BioGRID", "APID"]
        STRING = "STRING"
        BIOGRID = "BioGRID"
        APID = "APID"
    
    # Available options for the 'pdi' parameter.
    class PdiValues:
        PDI_VALUES = ["drugbank", "chembl", "dgidb"]
        DRUGBANK = "drugbank"
        CHEMBL = "chembl"
        DGIDB = "dgidb"
    
    # Available options for the 'target' parameter.
    class TargetValues:
        TARGET_VALUES = ["drug", "drug-target"]
        DRUG = "drug"
        DRUG_TARGET = "drug-target"
