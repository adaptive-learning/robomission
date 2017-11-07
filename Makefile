.PHONY: help
help:
	@echo "See Makefile for available targets."


.PHONY: install
install: dependencies logs db frontend


.PHONY: dependencies
dependencies: backend-dependencies frontend-dependencies


.PHONY: backend-dependencies
backend-dependencies:
	@echo "== Install Python dependencies. =="
	pip install -r requirements.txt


.PHONY: frontend-dependencies
frontend-dependencies:
	@echo "== Install frontend dependencies. =="
	cd frontend && npm install


.PHONY: server
server:
	python backend/manage.py runserver


.PHONY: liveserver
liveserver:
	# Run both Django and Webpack servers simultaneously:
	python backend/manage.py run_liveserver


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
	cd backend; pytest


.PHONY: test-frontend
test-frontend:
	@echo "===== Frontend tests ====="
	@echo "TBA"


.PHONY: test-load
test-load:
	# assumes that server is already running at http://127.0.0.1:8000
	locust -f backend/learn/tests/locustfile.py --host=http://127.0.0.1:8000
	# test setting at: http://127.0.0.1:8089/


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


.PHONY: storybook
storybook:
	cd frontend; npm run storybook


.PHONY: db
db: migrate tasks data


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


.PHONY: logs
logs:
	mkdir -p logs
	touch logs/robomission.log
