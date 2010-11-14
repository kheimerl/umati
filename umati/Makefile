FILES = UmatiChooserView.py UmatiMainView.py UmatiMathTaskView.py UmatiVendView.py

all: $(FILES)

%.py: %.ui
	pyuic4 $< -o $@

clean:
	rm $(FILES) *.pyc *~