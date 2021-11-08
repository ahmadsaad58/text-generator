.DEFAULT_GOAL := format
MAKEFLAGS += --no-builtin-rules
SHELL         := bash

ifeq ($(shell uname -s), Darwin)
	BLACK         := black
	PYLINT        := pylint
	PYTHON        := python3
else ifeq ($(shell uname -p), unknown)
	BLACK         := black
	PYLINT        := pylint
	PYTHON        := python
else
	BLACK         := black
	PYLINT        := pylint3
	PYTHON        := python3
endif

MFILES := `ls Model/*.py`
DFILES := `ls Model/Data/*.py`

format:
	@for name in $(MFILES); do $(BLACK) $$name; done
	@for name in $(DFILES); do $(BLACK) $$name; done

lint:
	@for name in $(MFILES); do $(PYLINT) $$name; done
	@for name in $(DFILES); do $(PYLINT) $$name; done


# output versions of all tools
versions:
	@echo  'shell uname -p'
	@echo $(shell uname -p)
	@echo
	@echo  'shell uname -s'
	@echo $(shell uname -s)
	@echo
	@echo "% which $(BLACK)"
	@which $(BLACK)
	@echo
	@echo "% $(BLACK) --version"
	@$(BLACK) --version
	@echo
	@echo "% which $(PYLINT)"
	@which $(PYLINT)
	@echo
	@echo "% $(PYLINT) --version"
	@$(PYLINT) --version
	@echo
	@echo "% which $(PYTHON)"
	@which $(PYTHON)
	@echo
	@echo "% $(PYTHON) --version"
	@$(PYTHON) --version
