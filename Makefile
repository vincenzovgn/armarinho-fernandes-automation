VERSION ?= 1.0

shell:
	pyenv shell 3.12.13

set-virtualenv:
	pyenv virtualenv 3.12.13 armarinho-fernandes

virtualenv-local:
	pyenv local armarinho-fernandes

activate:
	pyenv activate armarinho-fernandes

# para passar a versão como argumento no comando use a variavel VERSION, exemplo `make build VERSION=1.1` - isso vai sobrescrever o padrão
build:
	docker build -f Dockerfile . -t armarinho:${VERSION} --build-arg ENV=local

run:
	docker run --rm armarinho:${VERSION}
	