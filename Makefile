setup:
	pip install -r requirements.txt

start:
	python3 main.py

test:
	python3 -m unittest discover