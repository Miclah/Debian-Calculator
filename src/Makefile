SRC_DIR := Calculator
TEST_DIR := $(SRC_DIR)/tests
DOC_DIR := ../doc
TEAM_PACK_DIR := ../../$(TEAM_PACK_NAME)
INSTALLER_DIR := ../installer
PYTHON := python3

SRC_FILES := $(wildcard $(SRC_DIR)/*.py)
TEST_SRC_FILES := $(wildcard $(TEST_DIR)/*.py)
MATH_FILES := $(wildcard $(SRC_DIR)/math*.py)
vpath %.sh $(INSTALLER_DIR)

# Default target to install dependencies
.PHONY: all
all: setup

# Install dependencies
.PHONY: setup
setup:
	sudo apt-get -y update
	sudo apt-get install $(PYTHON)-pip
	sudo -H $(PIP) install pyqt5
	sudo -H $(PIP) install $(PYINSTALLER)

# Run the GUI calculator
.PHONY: run
run: $(SRC_FILES)
	$(PYTHON) -m --------- #TODO

# Run unit tests
.PHONY: test
test: $(MATH_FILES) $(TEST_SRC_FILES)
	$(PYTHON) -m unittest discover -s $(TEST_DIR)

# Run code profiler
.PHONY: profile
profile: $(SRC_FILES)
	$(PYTHON) -m ------- #TODO

# Generate documentation with Doxygen
.PHONY: doc
doc: Doxyfile $(SRC_FILES) $(TEST_SRC_FILES)
	cd $(SRC_DIR) && doxygen
	mv $(SRC_DIR)/doc $(DOC_DIR)

# Clean generated files
.PHONY: clean
clean:
	rm -rf $(SRC_DIR)/__pycache__ $(TEST_DIR)/__pycache__ $(DOC_DIR) $(TEAM_PACK_DIR) doxygen_warn_logfile.log
