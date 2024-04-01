JCC = javac

default = build

build:
	@echo "Building..."
	$(JCC) -d ./ -cp ./src ./src/rpal20.java

clean:
	@echo "Cleaning..."
	del .\*.class