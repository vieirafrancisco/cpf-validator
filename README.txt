# Descrição
Código que simula um sistema distribuido para validação de CPF, utilizando um servidor que gerencia nomes de serviços e seus endereços

# Requisitos:
    - python 3.x
    - virtualenv

# Uso *(OBS: Ordem necessária)*:

Utilizar virtualenv *(recomendado)*:
```bash
virtualenv venv
source venv/bin/activate  # linux
venv\Scripts\activate  # windows
```

Executar:
```bash
python services.py main-server  # inicializar servidor de serviços
python services.py cpf-validator-server  # inicializar servidor para validação de CPF
python client.py [CPF]  # solicitar validação de CPF ao servidor
```
