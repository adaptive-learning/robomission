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


# Double $$ is needed for expression expansion in Makefile.
INVESTIGATION_NTB="backend/monitoring/notebooks/investigation_$$(date +'%Y_%m_%d').ipynb"

.PHONY: investigation
investigation:
	git checkout monitoring 2>/dev/null || git checkout -b monitoring
	cp --no-clobber backend/monitoring/notebooks/investigation_template.ipynb ${INVESTIGATION_NTB}
	python backend/manage.py shell_plus --notebook
	xdg-open http://localhost:8888/notebooks/${INVESTIGATION_NTB}


.PHONY: export_monitoring_notebook
export_monitoring_notebook:
	python backend/manage.py export_monitoring_notebook


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
db: migrate domain


.PHONY: migrate
migrate:
	python backend/manage.py migrate --noinput


.PHONY: flush
flush:
	python backend/manage.py flush --noinput


.PHONY: reset_db
reset_db:
	python backend/manage.py reset_db
	python backend/manage.py migrate
	python backend/manage.py load_domain
	python backend/manage.py create_admin
	python backend/manage.py create_social_apps


.PHONY: admin
admin:
	python backend/manage.py create_admin


.PHONY: domain
domain:
	python backend/manage.py load_domain


.PHONY: export
export:
	python backend/manage.py export_data


.PHONY: metrics
metrics:
	python backend/manage.py compute_metrics


.PHONY: frontend
frontend:
	cd frontend && npm run build


.PHONY: logs
logs:
	mkdir -p logs


.PHONY: schedule_jobs
schedule_jobs:
	python backend/manage.py crontab add


.PHONY: socialapps
socialapps:
	python backend/manage.py create_social_apps


.PHONY: jupyter_components
jupyter_components:
	cd frontend && npm run jupyter-build
	python setup.py develop


.PHONY: upload_package
upload_package:
	python setup.py sdist
	twine upload dist/*
