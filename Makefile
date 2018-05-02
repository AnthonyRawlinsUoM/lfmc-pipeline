all: build install pull

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