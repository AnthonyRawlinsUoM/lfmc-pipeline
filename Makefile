all: build install pull

stack:
	@docker build --tag=128.250.160.167:5000/lfmc-pipeline .
	@docker push 128.250.160.167:5000/lfmc-pipeline

build:
	@npm install --no-optional
	@docker build --tag=anthonyrawlinsuom/lfmc-pipeline .

install:
	@docker push anthonyrawlinsuom/lfmc-pipeline
	
pull:
	@docker pull anthonyrawlinsuom/lfmc-pipeline
	
release:
	./release.sh

clean:
	@docker rmi --force anthonyrawlinsuom/lfmc-pipeline