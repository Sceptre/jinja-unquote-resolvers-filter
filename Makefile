.PHONY: help test auto-style code-style code-lint type-check lint lint-fix clean

.DEFAULT_GOAL := test
PIP="pip"
SRC_CORE="filter"
SRC_TESTS="tests"

define INLINE_AWK
	BEGIN {
		FS = ":.*##"
		cyan = "\033[36m"
		white = "\033[0m"
		printf "\nUsage:\n  make %s<target>%s\n\nTargets:\n", cyan, white
	}
	/^[a-zA-Z_-]+:.*?##/ {
		printf "  %s%-10s%s %s\n", cyan, $$1, white, $$2
	}
endef

export INLINE_AWK

define check_cmds
	$(foreach cmd,$(1),type $(cmd) >/dev/null 2>&1 || (echo "Run '$(PIP) install $(cmd)' first." >&2 ; exit 1);)
endef

help:  ## Display this help
	@awk "$$INLINE_AWK" $(MAKEFILE_LIST)

test: ## Run automated tests
	@pytest -vv -s $(SRC_TESTS)

auto-style:  ## Autopep8 to fix style issues
	$(call check_cmds,autopep8)
	@autopep8 -i -r $(SRC_CORE) $(SRC_TESTS)

code-style:  ## Pycodestyle tests
	$(call check_cmds,pycodestyle)
	@pycodestyle $(SRC_CORE) $(SRC_TESTS)

code-lint:  ## Pylint and Flake8 tests
	$(call check_cmds,pylint flake8)
	@flake8 --ignore=E252 $(SRC_CORE) $(SRC_TESTS)

type-check:  ## Mypy tests
	$(call check_cmds,mypy)
	@mypy $(SRC_CORE) $(SRC_TESTS)

lint: code-style code-lint type-check  ## code-style, code-lint and type-check

lint-fix:  ## Fix linter issues
	@"$(call check_cmds,autopep8)"
	@autopep8 --in-place --aggressive --aggressive -r $(SRC_CORE) $(SRC_TESTS)

clean:  ## Delete pycache files
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '__pycache__' -delete
