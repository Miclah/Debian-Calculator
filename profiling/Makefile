.PHONY: all clean

all: stddev

stddev: stddev.py math_lib.py extended_math_lib.py
	@python stddev.py < data.txt

clean:
	rm -f *.pyc
