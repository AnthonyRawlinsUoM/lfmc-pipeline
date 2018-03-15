all: build

build:
	@npm install
	@docker build --tag=anthonyrawlinsuom/lfmc-pipeline .

install:
	@docker push anthonyrawlinsuom/lfmc-pipeline

clean:
	@docker rmi anthonyrawlinsuom/lfmc-pipeline