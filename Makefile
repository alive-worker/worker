.PHONY: install seed run test docker docker-shell clean

install:
	pip install -r requirements.txt

seed:
	python -m scripts.seed

run:
	uvicorn app.main:app --reload

test:
	pytest -q

docker:
	docker build -t notebox .

docker-shell:
	docker run --rm -it notebox bash

clean:
	rm -f notebox.db notebox.db-journal
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
