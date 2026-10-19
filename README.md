versão do python no projeto `3.12.13`

## criando a virtualenv:

Garantinho que o shell esteja na versão adequada do python `pyenv shell 3.12.13`

```sh
pyenv virtualenv [python_version] <environment_name>
pyenv virtualenv armarinho-fernandes
pyenv activate armarinho-fernandes
```

## Referencias

https://realpython.com/intro-to-pyenv/

## Tarefas

### Relacionadas a solicitação de relatório

[] Poder escolher o tipo de solicitação (Loja|CD) por env
[] Escolher qual empresa solicitar o relatório
[] Gerar relatório de solicitação

### Relacionadas a extração de relatório

[] Acionar automação por webhook;
[] Poder escolher o tipo de solicitação (Loja|CD) no momento da execução;
[] Extrair apenas o ultimo relatório gerado de acordo com um atributo "ultimo_relatorio = sim" então só ira extrair o ultimo relatório das lojas e pode escolher o tipo de solicitação

**Feature adicional**
[] Criar conciliação dos relatórios já extraidos por tipo (Loja|CD)
[] Gerar insights referente a conciliação