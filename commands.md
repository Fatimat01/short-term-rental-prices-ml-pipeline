- create a boiler plate code for a pipeline step
```sh
cookiecutter cookie-mlflow-step -o src
```

- run individual pipepline step e.g download step or multiple steps separated by comma
```sh
mlflow run . -P steps=download
```

- if there's an error due to incompatibility, run the following to clean the mlflow packages and modify the dependencies version in `conda.yml`, then rerun `mlflow run` command
```sh
for e in $(conda info --envs | grep mlflow | cut -f1 -d" "); 
do conda uninstall --name $e --all -y;
done
```
- Run the eda step
    - this will launch a jupyter notebook
```sh
mlflow run src/eda
```
