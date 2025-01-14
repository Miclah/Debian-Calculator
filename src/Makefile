GUI=gui.py
MATH_TEST=UT_math_lib.py
MATH_LIB=math_lib.py
EXT_MATH_LIB=extended_math_lib.py
PROFILER=stddev.py
TEAM=xpetra32_xdanyl00_xmilis00_xbabia01

# Default target to install dependencies
.PHONY: all
all: setup

# Install dependencies
.PHONY: setup
setup:
	sudo apt-get -y update
	sudo apt install python3
	sudo apt-get install python3-pyqt5
	pip install pyinstaller

# Run the GUI calculator
.PHONY: run
run: $(SRC_FILES)
	python3 $(GUI)

# Run unit tests
.PHONY: test
test: $(MATH_TEST)
	python3 $(MATH_TEST)

# Run code profiler
.PHONY: profile
profile: $(PROFILER)
	python3 $(PROFILER) < ../profiling/1000

# Generate documentation with Doxygen
.PHONY: doc
doc: Doxyfile $(MATH_LIB) $(EXT_MATH_LIB) $(MATH_TEST)
	doxygen

# Clean generated files
.PHONY: clean
clean:
	rm -rf __pycache__ documentation
	rm -f doxy_error.log

# Installer for calculator
installer: setup $(GUI) $(MATH_LIB) $(EXT_MATH_LIB) dependencies.txt
	chmod +x py_script.sh
	bash py_script.sh

# Installer for deviation
installer2: setup $(PROFILER) $(MATH_LIB) $(EXT_MATH_LIB) dependencies.txt
	chmod +x py_script2.sh
	bash py_script2.sh

pack: doc installer installer2  clean
	mkdir -p ../../$(TEAM)/repo && mkdir -p ../../$(TEAM)/installer

	cp -r ../ ../../$(TEAM)/repo
	cp -r ../installer/calculator_installer.deb ../../$(TEAM)/installer
	cp -r ../installer/deviation_installer.deb ../../$(TEAM)/installer
	cp -r ../doc ../../$(TEAM)

	rm -rf ../../$(TEAM)/repo/doc
	rm -rf ../doc

	cd ../../ && zip -r $(TEAM).zip $(TEAM)/
