# Drugst.one-Python-package
The python package for the https://drugst.one/ platform.

## Start a new task:
    from drugstone.drugstone import Drugstone

    cf = [
            "CFTR", "TGFB1", "SCNN1B", 
            "DCTN4", "SCNN1A", "SCNN1G",
            "CLCA4", "TNFRSF1A", "FCGR2A", 
            "STX1A"  "ENG"
        ]

    p = {
        "target": "drug",
        "algorithm": "trustrank",
    }

    d = Drugstone()
    t = d.new_task(seeds=cf, params=p)  # -> returns a new Task
    r = t.get_result()                  # -> returns a TaskResult
    r.download_json('download_path')    
    r.to_graph('download_path')

## Start multiple tasks:
There two ways of starting multiple tasks 

### List of algorithms with otherwise same parameter
Starts a task for every algorithm in the list.
The other parameters are the same for every task

    from drugstone.drugstone import Drugstone

    cf = [
            "CFTR", "TGFB1", "SCNN1B", 
            "DCTN4", "SCNN1A", "SCNN1G",
            "CLCA4", "TNFRSF1A", "FCGR2A", 
            "STX1A"  "ENG"
        ]

    p = {
        "target": "drug",
        "algorithm": ["trustrank", "closeness", "degree"],
    }

    d = Drugstone()
    # mind the s in new_tasks
    t = d.new_tasks(seeds=cf, params=p) # -> returns a new Tasks
    r = t.get_result()                  # -> returns a TasksResult
    r.download_json('download_path')    
    # you can get the union or intersection of Tasks
    # this will return a Task (without s)
    # of the union or intersection of the tasks
    u = t.get_union()
    i = t.get_intersection()

### List of independent parameter
Starts a task for every parameter in the list.
The parameters are completely independent. 

    from drugstone.drugstone import Drugstone

    cf = [
            "CFTR", "TGFB1", "SCNN1B", 
            "DCTN4", "SCNN1A", "SCNN1G",
            "CLCA4", "TNFRSF1A", "FCGR2A", 
            "STX1A"  "ENG"
        ]

    p1 = {
        "target": "drug",
        "pdi_dataset": "drugbank",
    }

    p2 = {
        "target": "drug",
        "pdi_dataset": "chembl",
    }

    p3 = {
        "target": "drug",
        "pdi_dataset": "dgidb",
    }

    d = Drugstone()
    t = d.new_tasks(seeds=cf, params=[p1, p2, p3])
    r = t.get_result()                  
    r.download_json('download_path')

## Combine a drug-target search with a drug search:
This will search for drug-targets for the seeds,
and use the targets for a drug-search.

    from drugstone.drugstone import Drugstone

    cf = [
            "CFTR", "TGFB1", "SCNN1B", 
            "DCTN4", "SCNN1A", "SCNN1G",
            "CLCA4", "TNFRSF1A", "FCGR2A", 
            "STX1A"  "ENG"
        ]

    # if the parameters define an algorithm,
    # it will be used for both searches 
    # if there is a target_search or a drug_search
    # it overwrites the algorithm for the according task
    # in this example the 'algorithm' value would
    # be ignored, as it is overwritten for both tasks
    p = {
        "target": "drug",
        "algorithm": "trustrank",
        "target_search": "multisteiner",
        "drug_search": "proximity",
    }

    d = Drugstone()
    t = d.deep_search(seeds=cf, params=p)   # -> returns a new Task
    r = t.get_result()                  
    r.download_json('download_path')

## Import drug or gene data
It is possible to import drug or gene data.
- Visualize your data with TaskResult
- combine or compare your data with drugstone results.


    from drugstone.task.task import Task
    from drugstone.task.drug import Drug
    from drugstone.task.gene import Gene

    d = [Drug(label="xy"),Drug(label="xyz"),Drug(label="uvw")]
    g = [
            Gene(symbol="ab",has_edges_to=["xy", "xyz", "uvw", "abc", "aab"]),
            Gene(symbol="abc",has_edges_to=["xy", "uvw", "aab"]),
            Gene(symbol="aab",has_edges_to=["xy"])
        ]

    imp_task = Task.import_data(drugs=d, genes=g)
    r = imp_task.get_result()
    r.download_json('download_path')
    r.to_graph('download_path')

## create custom Tasks
You can combine tasks in Tasks.

    from drugstone.task.tasks import Tasks

    t_s = [t1, t2, t3] # list of Task objects 
    tasks = Tasks(t_s)
    r = tasks.get_result()
    r.download_json('download_path')

