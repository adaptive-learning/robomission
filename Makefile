.PHONY: help
help:
	@echo "See Makefile for available targets."


.PHONY: install
install: dependencies db frontend


.PHONY: dependencies
dependencies: backend-dependencies frontend-dependencies


.PHONY: backend-dependencies
backend-dependencies:
	@echo "== Install Python dependencies. =="
	pip install -r requirements.txt


.PHONY: frontend-dependencies
frontend-dependencies:
	@echo "== Install frontend dependencies. =="
	cd frontend && npm update

.PHONY: start
start:
	python manage.py run_liveserver


.PHONY: test
test: test-backend test-frontend


.PHONY: test-backend
test-backend:
	@echo "===== Backend tests ====="
	pytest


.PHONY: test-frontend
test-frontend:
	@echo "===== Frontend tests ====="
	@echo "TBA"


.PHONY: lint
lint: lint-backend lint-frontend


.PHONY: lint-backend
lint-backend:
	@echo "===== Backend linting ====="
	pylint --ignore=migrations backend


.PHONY: lint-frontend
lint-frontend:
	@echo "===== Frontend linting ====="
	@echo "TBA"


.PHONY: db
db: migrate data


.PHONY: migrate
migrate:
	python manage.py migrate --noinput


.PHONY: flush
flush:
	python manage.py flush --noinput


.PHONY: admin
admin:
	python manage.py create_admin


.PHONY: data
data:
	python manage.py load_static_data


.PHONY: export
export:
	python manage.py export_data


.PHONY: frontend
frontend:
	cd frontend && npm run build
