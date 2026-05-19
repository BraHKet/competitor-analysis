install:
	pip install -r requirements.txt

test:
	python -m pytest -q

run:
	python main.py

lint:
	python -m compileall src tests