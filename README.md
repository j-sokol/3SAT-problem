# 3SAT Problem (aka Boolean satisfiability problem)

Implementation of 3-SAT problem using genetic algorithm.

If you want to see some statistics of how algorithm runs, head to `report/` directory to see jupyter notebooks and latex reports (sadly it's only in czech language).
# How to run

Repository contains testing knapsack data and referential solution data for comparison.

No libraries are needed, only default Python 3.7 instalation.

## Creating virtual environment

```
python3 -m venv __venv__
. ./__venv__/bin/activate
pip install numpy
./run_all.sh
```
or if you want to see genetic algorithm statistics:
```
./run_genetic.sh
```


