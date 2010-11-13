FILES = UmatiChooserView.py UmatiMainView.py

all: $(FILES)

%.py: %.ui
	pyuic4 $< -o $@

clean:
	rm $(FILES) *.pyc