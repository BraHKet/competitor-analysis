install:
	pip install -r requirements.txt

test:
	python -m pytest -q

run:
	python main.py

typecheck:
	mypy src --strict

run-custom:
	python main.py --input $(INPUT)