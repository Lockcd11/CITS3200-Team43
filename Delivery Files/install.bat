@echo off
python -m venv venv
CALL venv\Scripts\activate
pip install neo4j
pip install pybliometrics
pip install pandas
pip install sortedcontainers
pip install flask
pip install flask_wtf
flask run
pause