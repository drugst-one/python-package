# Drugstone
This is the python package for the drugst.one platform.

This package offers tools for drug-repurposing and 
is a programmatic approach to the functionality of the web portal.
For more information visit: https://drugst.one/

[![Downloads](https://pepy.tech/badge/requests/month)](https://pepy.tech/project/drugstone)
[![Supported Versions](https://img.shields.io/pypi/pyversions/drugstone.svg)](https://pypi.org/project/drugstone)


## Installation
Drugstone depends on a few packages to work. 
You can use pip to install them.
```console
pip install urllib3 requests pandas pyvis upsetplot
```
Then you can install drugstone.
```console
pip install drugstone
```
Finally, it should be possible to import drugstone to your python script.
````python
import drugstone
````
You can use 
```python
import drugstone as ds
```
to access the complete drugstone API with the `ds.` notation.

Drugstone officially supports Python 3.6+.


## Supported features
Drugstone offers a toolbox for drug repurposing applications.
- Search for drugs, interacting with a list of genes
- Search for drug-targets, for a list of genes
- Visualize data in common formats like JSON or CSV
- create interaction graphs for drug- and gene-interactions


## Start a new task
With Drugstone it is easy and convenient to search for drugs or drug-targets,
starting with a list of genes.
```python
from drugstone import new_task

genes = [
    "CFTR", "TGFB1", "SCNN1B", 
    "DCTN4", "SCNN1A", "SCNN1G",
    "CLCA4", "TNFRSF1A", "FCGR2A"
]

parameters = {
    "target": "drug",
    "algorithm": "trustrank"
}

# new_task() returns a Task object.
# You can find the classes further below.
task = new_task(genes, parameters)
# get_result() returns a TaskResult object.
r = task.get_result()
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
from drugstone import new_tasks

genes = [
    "CFTR", "TGFB1", "SCNN1B", 
    "DCTN4", "SCNN1A", "SCNN1G",
    "CLCA4", "TNFRSF1A", "FCGR2A"
]

parameters = {
    "target": "drug",
    "algorithms": ["trustrank", "closeness", "degree"]
}

# Mind the 's' in new_tasks.
tasks = new_tasks(genes, parameters)    # returns a Tasks object
r = tasks.get_result()                  # returns a TasksResult object
r.download_json()
````

### Independent parameters
`new_tasks()` accepts a list of parameter dictionaries.
For every dictionary a task will be started.
````python
from drugstone import new_tasks

genes = [
    "CFTR", "TGFB1", "SCNN1B", 
    "DCTN4", "SCNN1A", "SCNN1G",
    "CLCA4", "TNFRSF1A", "FCGR2A"
]

p1 = {
    "target": "drug",
    "pdi_dataset": "drugbank"
}

p2 = {
    "target": "drug",
    "pdi_dataset": "chembl"
}

p3 = {
    "target": "drug",
    "pdi_dataset": "dgidb"
}

tasks = new_tasks(genes, [p1, p2, p3])  # returns a Tasks object
r = tasks.get_result()                  # returns a TasksResult object
r.download_json()
````

### Union and intersection of tasks
You can get the union or intersection of tasks.
That returns a TaskResult with the according result.
````python
from drugstone import new_tasks

genes = [
    "CFTR", "TGFB1", "SCNN1B", 
    "DCTN4", "SCNN1A", "SCNN1G",
    "CLCA4", "TNFRSF1A", "FCGR2A"
]

parameters = {
    "target": "drug",
    "algorithms": ["trustrank", "closeness", "degree"]
}

tasks = new_tasks(genes, parameters)    # returns a Tasks object

u = tasks.get_union()                   # returns a TaskResult object
u.download_json()

i = tasks.get_intersection()
i.download_json()
````


## Combine a drug-target search with a drug search
This will perform a drug-target search for the seed genes 
and then use the drug-target search results and the seed genes
to perform a drug-search.
Finally, a Task with the drug-search results will be returned. 
````python
from drugstone import deep_search

genes = [
    "CFTR", "TGFB1", "SCNN1B", 
    "DCTN4", "SCNN1A", "SCNN1G",
    "CLCA4", "TNFRSF1A", "FCGR2A"
]

parameters = {
    "algorithm": "trustrank"
}

task = deep_search(genes, parameters)   # returns a Task object
r = task.get_result()                   # returns a TaskResult object
r.download_json()
````
When the parameters dictionary contains an algorithm,
it will be used for both, drug-target- and drug-search.
You can overwrite the algorithm for the according search, 
by defining `"target_search"` or `"drug_search"` in the parameters.
````python
parameters = {
    "algorithm": "trustrank",
    "target_search": "multisteiner",
    "drug_search": "proximity"
}
````
In this example, the *algorithm* value would be ignored, 
as it is overwritten in both cases.


## Static tasks
You can import your own data into drugstone.
That can be useful for e.g.
- visualizing the data with TaskResult or
- combining or comparing the data with drugstone results.
```python
from drugstone import static_task, Drug, Gene

drugs = [
    Drug(label="xy"),
    Drug(label="xyz"),
    Drug(label="uvw")
]

genes = [
    Gene(symbol="ab", has_edges_to=["xy", "xyz", "uvw", "abc", "aab"]),
    Gene(symbol="abc", has_edges_to=["xy", "uvw", "aab"]),
    Gene(symbol="aab", has_edges_to=["xy"])
]

s_task = static_task(drugs, genes)
r = s_task.get_result()
r.download_graph()
```

You can also create Tasks objects with a list of Task objects.
````python
from drugstone import static_tasks, new_task

tasks = []

for _ in range(5):
    t = new_task(["BRCA1"], {})
    tasks.append(t)

s_tasks = static_tasks(tasks)
r = s_tasks.get_result()
r.download_json()
````


## class Task
Represents a task.

`get_result() -> TaskResult` \
Returns a TaskResult for the result of the task.

`get_info() -> dict:` \
Returns a dict with information about the task.

`get_parameters() -> dict:` \
Returns a dict with the parameters of the task.


## class TaskResult
Represents the results of a task.

`get_genes() -> dict:` \
Returns a dict with the genes.

`get_drugs() -> dict:` \
Returns a dict with the drugs.

`to_dict() -> dict:` \
Returns a dict with the result.

`to_pandas_dataframe() -> DataFrame:` \
Returns a pandas DataFrame of the result.

`download_json(path: str, name: str) -> None:` \
Downloads a json file with the result.

`download_genes_csv(path: str, name: str) -> None:` \
Downloads a csv file with the genes of the result.

`download_drugs_csv(path: str, name: str) -> None:` \
Downloads a csv file with the drugs of the result.

`download_edges_csv(path: str, name: str) -> None:` \
Downloads a csv file with the edges of the result.

`download_graph(path: str, name: str) -> None:` \
Downloads a html file with a graph of the nodes.


## class Tasks
Wraps a list of Task objects.

`get_result() -> TasksResult:` \
Returns a TasksResult for the list of tasks.

`get_union() -> TaskResult:` \
Returns a TaskResult with the union of the tasks.

`get_intersection() -> TaskResult:` \
Returns a TaskResult with the intersection of the tasks.


## class TasksResult
Represents the results of a list of Task objects.

`get_tasks_list() -> List[Task]:` \
Returns the list of tasks.

`to_dict() -> dict:` \
Returns a dict with the results of the tasks.

`download_json(path: str, name: str) -> None:` \
Downloads a json file with the results.

`create_upset_plot() -> None:` \
Opens a new window with an upset plot of the results.



Copyright: 2022 - Institute for Computational Systems Biology 
by Prof. Dr. Jan Baumbach \
Author: Ugur Turhan