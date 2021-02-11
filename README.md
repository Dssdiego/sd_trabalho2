# Trabalho 2 - Sistemas Distribuídos

## Informações Úteis

Foi utilizado o **Python 3.9.1** para este projeto, portanto o comando para rodar os scripts pode ser

```
python ...
```

ou 

```
python3 ...
```

dependendo de como ele está instalado em sua máquina

## Instalação

Para rodar os scripts, é necessária que a biblioteca **pyzmq** esteja instalada.

Para isso basta rodar

```
pip install -r requirements.txt
```

ou simplesmente

```
pip install pyzmq
```

## Executando o Projeto

### Iniciando o Middleware

```
python middleware.py
```

### Iniciando um Dispositivo

```
python dispositivo.py
```

### Iniciando um Cliente

```
python cliente.py
```

## Arquitetura

<img src="https://github.com/Dssdiego/sd_trabalho2/blob/main/arquitetura.jpg">

## Observações

Para fins de simplicidade, o cliente faz as requisições automaticamente em um determinado espaço de tempo, em sequência, a saber:

- Verifica a lista de dispositivos conectados no middleware
- Liga algum dispositivo aleatório da rede
- Desliga algum dispositivo aleatório da rede
