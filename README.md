<h1 align="center">
<img src="https://drugst.one/assets/logo_black.png" width="300">
</h1><br>

This is the python package for the drugst.one platform. It offers tools for network-based drug repurposing and 
is a programmatic interface to Drugst.one.

- **Website:** https://drugst.one/
- **Source code:** https://github.com/drugst-one/python-package
- **Bug reports:** https://github.com/drugst-one/python-package/issues


## Installation
<!-- Drugstone depends on a few packages to work.  -->
<!-- You can use pip to install them. -->
<!-- ```console
pip install urllib3 requests pandas pyvis upsetplot
``` -->
Install drugstone.
```console
pip install drugstone
```
Import drugstone in python 
````python
import drugstone
````

Drugstone officially supports Python 3.6+.


## Supported features
Drugstone offers a toolbox for drug repurposing applications.
- Search for drugs, interacting with a list of genes
- Search for drug targets, for a list of genes
- Visualize data in common formats like JSON or CSV
- create interaction graphs for drug and gene interactions


## Available Datasets

Protein-protein interactions (ppi_dataset):

``` NeDRex, BioGRID, IID, IntAct, STRING, APID```

Protein-drug interactions (pdi_dataset): 

```NeDRex, DrugBank, Drug Central, ChEMBL, DGIdb```

Please note that some of the datasets require you to accept their terms and conditions before usage. ```DrugBank``` can only be used if the license has been agreed to and since ```NeDRex``` includes ```DrugBank``` data, only a part of ```NeDRex``` is available without agreeing to our license.

The terms and conditions can be read by calling 

```drugstone.print_license()```

and can be accepted after reading with 

```drugstone.accept_license()```. 


## Available backends

In the the main Drugst.One database is updated automatically weekly. This is the database used by default (https://api.drugst.one/). For more stable results, change the api endpoint to our stable API (https://api.stable.drugst.one/) using the function below. The Drugst.One stable version is updated yearly (on the first of January).

```python
drugstone.set_api('https://api.stable.drugst.one/')
```


## Start a new task
With Drugstone it is easy and convenient to search for drugs or drug-targets,
starting with a list of genes.
```python
genes = [
    "CFTR", "TGFB1", "SCNN1B", 
    "DCTN4", "SCNN1A", "SCNN1G",
    "CLCA4", "TNFRSF1A", "FCGR2A"
]

parameters = {
    "target": "drug",
    "algorithm": "trustrank"
}

task = drugstone.new_task(genes, parameters)

r = task.get_result()

genes = r.get_genes()
drugs = r.get_drugs()

# save directly to files
r.download_json()
r.download_graph()
```


## Start multiple tasks
You can start multiple tasks at once, either with 
completely independent parameters or 
with same parameters and different algorithms.

### Multiple algorithms
By defining an *algorithms* value in the parameters dictionary, 
you can pass a list of algorithm values.
For every algorithm, a task will be started, with 
otherwise same parameter values.
````python
genes = [
    "CFTR", "TGFB1", "SCNN1B", 
    "DCTN4", "SCNN1A", "SCNN1G",
    "CLCA4", "TNFRSF1A", "FCGR2A"
]

parameters = {
    "target": "drug",
    "algorithms": ["trustrank", "closeness", "degree"]
}

tasks = drugstone.new_tasks(genes, parameters)   
r = task.to_dict()                
r.download_json()
````

### Independent parameters
`new_tasks()` accepts a list of parameter dictionaries.
For every dictionary a task will be started.
````python
genes = [
    "CFTR", "TGFB1", "SCNN1B", 
    "DCTN4", "SCNN1A", "SCNN1G",
    "CLCA4", "TNFRSF1A", "FCGR2A"
]

p1 = {
    "target": "drug",
    "ppiDataset": 'nedrex',
    "pdiDataset": "drugcentral"
}

p2 = {
    "target": "drug",
    "ppiDataset": 'IID',
    "pdiDataset": "chembl"
}

p3 = {
    "target": "drug",
    "ppiDataset": 'apid',
    "pdiDataset": "dgidb"
}

tasks = drugstone.new_tasks(genes, [p1, p2, p3]) 
r = tasks.get_result() 
r.to_dict()                 
r.download_json()  
# only with Python 3.6                 
r.create_upset_plot()                 
````

### Union and intersection of tasks
You can get the union or intersection of tasks.
That returns a TaskResult with the according result.
````python
genes = [
    "CFTR", "TGFB1", "SCNN1B", 
    "DCTN4", "SCNN1A", "SCNN1G",
    "CLCA4", "TNFRSF1A", "FCGR2A"
]

parameters = {
    "target": "drug",
    "algorithms": ["trustrank", "closeness", "degree"]
}

tasks = drugstone.new_tasks(genes, parameters)    

u = tasks.get_union()                  
u.download_json()

i = tasks.get_intersection()
i.download_json()
````

### Use your own network
You can add custom nodes and edges to the network, which may be considered for the drug-target or the drug search. Also, it is possible to ONLY consider your provided PPI-network and exclude PPI-edges provdided by Drugst.One.
Please note that this is an experimental feature and is still being tested.
```python
import drugstone

seeds = [
    "CFTR", "TGFB1"
]

parameters = {
    "target": "drug",
    "algorithm": "trustrank",
    "pdiDataset": 'nedrex',     # drug nodes and edges will still be taken from Drugst.One
    "custom_edges": [   # add here your edges for you custom PPI
        {"from": "CFTR", "to": "SCNN1G"},
        {"from": "CFTR", "to": "SCNN1B"},
        {"from": "TGFB1", "to": "DCTN4"},
        {"from": "SCNN1B", "to": "SCNN1A"},
        {"from": "SCNN1B", "to": "CLCA4"},
        {"from": "TNFRSF1A", "to": "FCGR2A"}
    ],
    "exclude_drugstone_ppi_edges": True, # this parameter removes all Drugst.One PPI edges (only if edges in 'custom_edges' are provided)
    "identifier": "symbol",
    "include_indirect_drugs": True,
    "network_nodes": ["CFTR", "TGFB1", "SCNN1B",    # add here your nodes for you custom PPI
                      "DCTN4", "SCNN1A", "SCNN1G",
                      "CLCA4", "TNFRSF1A", "FCGR2A"]
}
task = drugstone.new_task(seeds, parameters)
r = task.get_result()
genes = r.get_genes()
drugs = r.get_drugs()
```


## Combine a drug-target search with a drug search
This will perform a drug-target search for the seed genes 
and then use the drug-target search results and the seed genes
to perform a drug-search.
Finally, a Task with the drug-search results will be returned. 
````python
genes = [
    "CFTR", "TGFB1", "SCNN1B", 
    "DCTN4", "SCNN1A", "SCNN1G",
    "CLCA4", "TNFRSF1A", "FCGR2A"
]

parameters = {
    "algorithm": "trustrank"
}

task = drugstone.deep_search(genes, parameters)  
r = tasks.get_result() 
r.to_dict()                 
r.download_json()
# only with Python 3.6                 
r.create_upset_plot()  
````

## Available Parameters

````
parameters = {
    "identifier": "symbol", #("entrez" | "uniprot" | "ensg" will be supported in future versions)
    "algorithm": "adjacentDrugs", "trustrank" | "multisteiner" | "keypathwayminer" | "closeness" | "degree" | "proximity" | "betweenness",
    "ppiDataset": "NeDRex",
    "pdiDataset": "NeDRex",
    "resultSize": 20,
    "target": "drug" | "drug-target",
    "includeIndirectDrugs": True | False,
    "includeNonApprovedDrugs": True | False,
    "maxDeg": sys.maxsize, # filter out nodes with high degrees
    "hubPenalty": 0.0, # penalize hub nodes
    "filterPaths": True | False, # include only shortest connections in the result

    "damping_factor": 0.85, # only in trustrank

    "num_trees": 5, # only in multisteiner
    "tolerance": 10, # only in multisteiner

    "k": 5, # only in keypathwayminer
} 
````

For more information about the algorithms, please refer to <a href="https://drugst.one/doc#implementation_algorithms">https://drugst.one/doc#implementation_algorithms</a>.

For more information abouyt the available dataset types, please refer to <a href="https://drugst.one/doc#implementation_datasources">https://drugst.one/doc#implementation_datasources</a>.

## class Task
Represents a task.

`get_result() -> TaskResult` \
Returns a TaskResult for the result of the task.

`get_info() -> dict` \
Returns a dict with information about the task.

`get_parameters() -> dict` \
Returns a dict with the parameters of the task.


## class TaskResult
Represents the results of a task.

`get_genes() -> dict` \
Returns a dict with the genes.

`get_drugs() -> dict` \
Returns a dict with the drugs.

`to_dict() -> dict` \
Returns a dict with the result.

`to_pandas_dataframe() -> DataFrame` \
Returns a pandas DataFrame of the result.

`download_json(path: str, name: str) -> None` \
Downloads a json file with the result.

`download_genes_csv(path: str, name: str) -> None` \
Downloads a csv file with the genes of the result.

`download_drugs_csv(path: str, name: str) -> None` \
Downloads a csv file with the drugs of the result.

`download_edges_csv(path: str, name: str) -> None` \
Downloads a csv file with the edges of the result.

`download_graph(path: str, name: str) -> None` \
Downloads a html file with a graph of the nodes.


## class Tasks
Wraps a list of Task objects.

`get_result() -> TasksResult` \
Returns a TasksResult for the list of tasks.

`get_union() -> TaskResult` \
Returns a TaskResult with the union of the tasks.

`get_intersection() -> TaskResult` \
Returns a TaskResult with the intersection of the tasks.


## class TasksResult
Represents the results of a list of Task objects.

`get_tasks_list() -> List[Task]` \
Returns the list of tasks.

`to_dict() -> dict` \
Returns a dict with the results of the tasks.

`download_json(path: str, name: str) -> None` \
Downloads a json file with the results.

`create_upset_plot() -> None` \
Opens a new window with an upset plot of the results.


## Miscellaneous

### map nodes to Drugst.One proteins
This will fetch all available information for the given nodes from the Drugst.One database as a list of dictionaries. Each node contains a key 'drugstoneType', where the value is 'protein' if the given node can be mapped to a protein. If a node can not be mapped, the 'drugstoneType' will be 'other'. <br>
Be aware of the parameter dictionary with the key 'identifier', available options are one of 'symbol' (HUGO symbol), 'uniprot' (Uniprot AC), 'ensg' or 'ensembl' (Ensembl Gene ID), 'entrez' or 'ncbigene' (Entrez ID), depending on your input.
```python
import drugstone

nodes = [
    "CFTR", "TGFB1", "SCNN1B", "justatest"
]

parameters = {'identifier': 'symbol'}

drugstone_nodes = drugstone.map_nodes(nodes, parameters)
```

### build network
This will fetch all available edges for a given list of proteins. Returned will be a list of node entities. Each of these nodes contains the key 'hasEdgesTo' with a list of all node ids this node has an edge to.<br>
Be aware of the parameter dictionary with the key 'identifier', available options are one of 'symbol' (HUGO symbol), 'uniprot' (Uniprot AC), 'ensg' or 'ensembl' (Ensembl Gene ID), 'entrez' or 'ncbigene' (Entrez ID), depending on your input.
```python
import drugstone

# optional
drugstone.print_license()
drugstone.accept_license()

genes = [
    "CFTR","TGFB1","TNFRSF1A","FCGR2A","ENG","DCTN4","CLCA4","STX1A","SCNN1G","SCNN1A","SCNN1B", "justatest"
]

parameters = {'identifier': 'symbol', 'ppiDataset': 'IID'}

network = drugstone.build_network(genes, parameters)
```


Copyright: 2024 - Institute for Computational Systems Biology 
by Prof. Dr. Jan Baumbach.