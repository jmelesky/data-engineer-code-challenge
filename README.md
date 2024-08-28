# Working Families Data Engineer Technical Challenge 
Code for the Working Families Data Engineer code challenge. 

## Task 1A

See changes and comments inline in [`ingest_mobilize_python.py`](ingest_mobilize_python.py)

## Task 1B

This has been tested against python 3.11, and uses nothing outside the python standard library. Running should be as simple as:

```
python3 ./process_data.py
```

It reads from `data/attendances.json` (relative to CWD) and writes to `attendances.csv`, `events.csv`, `timeslots.csv`, and `persons.csv`, also within `data/`.

See code for comments and discussion, as well as [task2](docs/task2.md).

## Tasks 2 & 3

Located in `docs/`: [task2](docs/task2.md) and [task3](docs/task3.md).


