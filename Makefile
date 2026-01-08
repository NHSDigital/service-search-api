SHELL := /bin/bash -euo pipefail

VENV_DIR := .venv
ACTIVATE := source $(VENV_DIR)/bin/activate

all: install publish release smoketest serve

# ---------- Python Dependencies ----------
install-python:
	$(info ">>>>>>>>>>> INSTALL PYTHON DEPENDENCIES <<<<<<<<<<<<<<")
	# Create virtual environment if missing
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	# Upgrade pip and install poetry in venv
	$(ACTIVATE) && pip install --upgrade pip
	$(ACTIVATE) && pip install poetry
	# Install project dependencies via poetry
	$(ACTIVATE) && poetry install --no-root --with dev

# ---------- Node Dependencies ----------
install-node:
	$(info ">>>>>>>>>>> INSTALL NODE DEPENDENCIES <<<<<<<<<<<<<<")
	npm install --legacy-peer-deps
	cd sandbox && npm install --legacy-peer-deps

# ---------- Git Hooks ----------
.git/hooks/pre-commit:
	$(info ">>>>>>>>>>> GIT PRE-COMMIT HOOKS <<<<<<<<<<<<<<")
	cp scripts/pre-commit .git/hooks/pre-commit

# ---------- Combined Install ----------
install: install-node install-python .git/hooks/pre-commit

# ---------- Lint ----------
lint: install-python
	$(info ">>>>>>>>>>> LINT <<<<<<<<<<<<<<")
	$(ACTIVATE) && export OPENAPI_GENERATOR_CLI_SEARCH_URL=DEFAULT
	$(ACTIVATE) && npm run lint
	$(ACTIVATE) && poetry run flake8 .

# ---------- Clean ----------
clean: lint
	$(info ">>>>>>>>>>> CLEAN <<<<<<<<<<<<<<")
	rm -rf build
	rm -rf dist

# ---------- Publish ----------
publish: clean
	$(info ">>>>>>>>>>> PUBLISH <<<<<<<<<<<<<<")
	mkdir -p build
	$(ACTIVATE) && npm run publish 2> /dev/null
	$(ACTIVATE) && poetry run scripts/inline_examples.py build/service-search-api.json > build/temp.json
	rm build/service-search-api.json
	mv build/temp.json build/service-search-api.json

# ---------- Build Proxy ----------
build-proxy:
	$(info ">>>>>>>>>>> RUN BUILD PROXY SCRIPT <<<<<<<<<<<<<<")
	scripts/build_proxy.sh

# ---------- Copy Examples ----------
_dist_include := pytest.ini poetry.lock poetry.toml pyproject.toml Makefile build/. tests specification
copy-examples:
	$(info ">>>>>>>>>>> COPY EXAMPLES <<<<<<<<<<<<<<")
	cp specification/examples/* sandbox/responses/
	mkdir -p build/examples
	cp sandbox/responses/* build/examples/

# ---------- Release ----------
release: clean copy-examples publish build-proxy
	$(info ">>>>>>>>>>> RELEASE <<<<<<<<<<<<<<")
	mkdir -p dist
	for f in $(_dist_include); do cp -r $$f dist; done
	mkdir dist/sandbox
	find sandbox -type f -maxdepth 1 ! -name node_modules -exec cp -t dist/sandbox {} +
	cp ecs-proxies-deploy.yml dist/ecs-deploy-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-qa-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-dev-sandbox.yml

# ---------- Smoketest ----------
smoketest:
	$(info ">>>>>>>>>>>> SMOKETEST <<<<<<<<<<<<")
	$(ACTIVATE) && . scripts/get_apigee_token.sh
	$(ACTIVATE) && poetry run pytest -v --junitxml=smoketest-report.xml \
		--api-name=service-search-api --proxy-name=service-search-api-internal-dev

# ---------- Serve ----------
serve: clean publish
	$(info ">>>>>>>>>>> SERVE <<<<<<<<<<<<<<")
	$(ACTIVATE) && npm run serve
