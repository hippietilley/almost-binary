.PHONY: requirements
requirements:
	pip install --upgrade pip
	pip install --upgrade pip-tools
	pip-compile -rU --resolver=backtracking --no-emit-index-url requirements.in
	pip-compile -rU --resolver=backtracking --no-emit-index-url requirements_dev.in

.PHONY: install_requirements
install_requirements:
	pip install --upgrade pip
	pip install --upgrade pip-tools
	pip install -r requirements.txt
	pip install -r requirements_dev.txt

