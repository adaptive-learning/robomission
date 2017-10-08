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


.PHONY: server
server:
	#python manage.py run_liveserver
	python backend/manage.py runserver


.PHONY: shell
shell:
	python backend/manage.py shell_plus


.PHONY: notebook
notebook:
	python backend/manage.py shell_plus --notebook


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
	python backend/manage.py migrate --noinput


.PHONY: flush
flush:
	python backend/manage.py flush --noinput


.PHONY: admin
admin:
	python backend/manage.py create_admin


.PHONY: tasks
tasks:
	python backend/manage.py build_tasks


.PHONY: data
data:
	python backend/manage.py load_data


.PHONY: export
export:
	python manage.py export_data


.PHONY: frontend
frontend:
	cd frontend && npm run build
