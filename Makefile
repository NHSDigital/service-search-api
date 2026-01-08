SHELL=/bin/bash -euo pipefail

all: install publish release smoketest serve

#Installs dependencies using poetry.
install-python:
	$(info ">>>>>>>>>>> INSTALL PYTHON DEPENDENCIES <<<<<<<<<<<<<<")
	python -m venv .venv
	source .venv/bin/activate && poetry install --no-root --with dev

#Installs dependencies using npm.
install-node: 
	$(info ">>>>>>>>>>> INSTALL NODE DEPENDENCIES <<<<<<<<<<<<<<")
	npm install --legacy-peer-deps
	cd sandbox && npm install --legacy-peer-deps

#Configures Git Hooks, which are scipts that run given a specified event.
.git/hooks/pre-commit: 
	$(info ">>>>>>>>>>> GIT PRE-COMMIT HOOKS <<<<<<<<<<<<<<")
	cp scripts/pre-commit .git/hooks/pre-commit

#Condensed Target to run all targets above.
install: install-node install-python .git/hooks/pre-commit

#Run the npm linting script (specified in package.json). Used to check the syntax and formatting of files.
lint: install-python
	$(info ">>>>>>>>>>> LINT <<<<<<<<<<<<<<")
	export OPENAPI_GENERATOR_CLI_SEARCH_URL=DEFAULT
	npm run lint
	poetry run flake8 . 

#Removes build/ + dist/ directories
clean: lint
	$(info ">>>>>>>>>>> CLEAN <<<<<<<<<<<<<<")
	rm -rf build
	rm -rf dist

#Creates the fully expanded OAS spec in json
publish: clean
	$(info ">>>>>>>>>>> PUBLISH <<<<<<<<<<<<<<")
	mkdir -p build
	npm run publish 2> /dev/null
	poetry run scripts/inline_examples.py build/service-search-api.json > build/temp.json
	rm build/service-search-api.json
	mv build/temp.json build/service-search-api.json

#Runs build proxy script
build-proxy: 
	$(info ">>>>>>>>>>> RUN BUILD PROXY SCRIPT <<<<<<<<<<<<<<")
	scripts/build_proxy.sh

#Files to loop over in release
_dist_include="pytest.ini poetry.lock poetry.toml pyproject.toml Makefile build/. tests specification"

copy-examples: 
	$(info ">>>>>>>>>>> COPY EXAMPLES <<<<<<<<<<<<<<")
	cp specification/examples/* sandbox/responses/
	mkdir -p build/examples
	cp sandbox/responses/* build/examples/

#Create /dist/ sub-directory and copy files into directory
release: clean copy-examples publish build-proxy
	$(info ">>>>>>>>>>> RELEASE <<<<<<<<<<<<<<")
	mkdir -p dist
	for f in $(_dist_include); do cp -r $$f dist; done
	mkdir dist/sandbox
	find sandbox -type f -maxdepth 1 ! -name node_modules -exec cp -t dist/sandbox {} +
	cp ecs-proxies-deploy.yml dist/ecs-deploy-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-qa-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-dev-sandbox.yml

#Command to run end-to-end smoktests post-deployment to verify the environment is working
smoketest:
	$(info ">>>>>>>>>>>> SMOKETEST <<<<<<<<<<<<")
	. scripts/get_apigee_token.sh
	poetry run pytest -v --junitxml=smoketest-report.xml --api-name=service-search-api --proxy-name=service-search-api-internal-dev

serve: clean publish
	npm run serve
