.PHONY: build test

name := acbook-env
pwd := $(shell pwd)

build:
	@docker build -t ${name} -f docker/Dockerfile .

test:
	@docker run --rm -it -v $(pwd):/workspace ${name} \
		pytest -lvs test/test_cli.py::TestCli::test_report_outcomes 

sh:
	@docker run --rm -it -v $(pwd):/workspace ${name} bash
