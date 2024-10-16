# Автоматизаци пайплана ML при помощи Airflow и Mlflow

## VENV
- python -m venv myyvenv
- Порядок действий для первичной установки без postgresql (SQLite)

## Mlflow
- pip install mlflow
- mkdir mlflow 
- cd mlflow
- export MLFLOW_REGISTRY_URI=mlflow
- Запуск сервера: mlflow server --host localhost --port 5001 --backend-store-uri sqlite:///${MLFLOW_REGISTRY_URI}/mlflow.db --default-artifact-root ${MLFLOW_REGISTRY_URI}
- Полезная инфа: https://www.mlflow.org/docs/latest/tracking.html#tracking-ui

## Airflow
- mkdir airflow
- cd airflow
- source .../myvenv/bin/activate
- airflow pip install apache-airflow
- export AIRFLOW_HOME=.
- airflow db init

Config
- dags_folder = ../dags
- load_examples = False
- [webserver] rbac = True
- airflow users create --username admin --firstname yourname --lastname yourlastname --role Admin --email youremail@example.com
- airflow webserver -p 8080


airflow scheduler

- cd ../airflow
- source ../myvenv/bin/activate
- export AIRFLOW_HOME=../airflow
- airflow scheduler
