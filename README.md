# Reynolds Number Calculator

## 1. Proposta

Este projeto trata-se de uma calculadora que tem o objetivo de retornar para o usuário os valores do Número de Reynolds e do regime de escoamento do fluido, recebendo como entradas Viscosidade Cinemática `(Kinematic Viscosity (St))`, Diâmetro da Tubulação `(Pipe Diameter (m))`, Vazão Volumétrica do Fluído `(Volumetric Flow Rate (m3/s))`

## 2. Ferramentas/Tecnologias Utilizadas

- Python
- Django
- Django Rest Framework
- RabbitMQ
- MailHog
- PostgreSQL
- Celery
- Flower
- React
- Docker
- Docker Compose
- Git
- Ubuntu Server 20.04

## 3. Como Executar o projeto Localmente

Para executar esse projeto, é necessário ter o Docker + Docker Compose instalados na máquina. Instruções aqui: https://docs.docker.com/engine/install/

Também é recomendado ter o make instalado na máquina para a execução do comando do arquivo Makefile. Para instalar no ubuntu e derivados, siga o seguinte passo:

```
sudo apt update
sudo apt install make
```

Agora vamos executar o sistema localmente:

```
- Clone o respositório
https://github.com/edcarlos-neves/automation-team-store-challenger

- Entre na pasta reynolds-number-calculator
cd automation-team-store-challenger

- Execute o comando do Docker
make docker_build

- Crie o primeiro usuário
make docker_create_admin_user

- Vá em localhost:8000 onde você vai encontrar a interface web
```

## 4. Endpoints da API

### 4.1. Análises

#### Obter todas as análises (Retorna todas as análises)

```
GET api/analysis/
Headers:
	Authorization: Bearer + Token
Retorna:
[
   {
      "id":124,
      "reynolds_number":12732.395447351628,
      "reynolds_number_regime":"turbulent",
      "viscosity":1.0,
      "diameter":2.0,
      "flow":2.0,
      "creator":1
   },
   {
      "id":122,
      "reynolds_number":128.3939036707727,
      "reynolds_number_regime":"laminar",
      "viscosity":85.0,
      "diameter":7.0,
      "flow":6.0,
      "creator":1
   }
]
```

#### Obter uma análise específica

```
GET api/analysis/{analysis_id}
Headers:
	Authorization: Bearer + Token
Retorna:
{
   "id":119,
   "reynolds_number":6701.260761764015,
   "reynolds_number_regime":"turbulent",
   "viscosity":19.0,
   "diameter":0.1,
   "flow":1.0,
   "creator":1
}
```

#### Atualizar uma análise específica

```
PUT api/analysis/{analysis_id}
Headers:
	Authorization: Bearer + Token
Body:
{
   "viscosity":19,
   "diameter":0.1,
   "flow":0.01
}
Retorna:
{
   "id":119,
   "reynolds_number":6701.260761764015,
   "reynolds_number_regime":"turbulent",
   "viscosity":19.0,
   "diameter":0.1,
   "flow":1.0,
   "creator":1
}
```

#### Deletar uma análise específica

```
DELETE api/analysis/{analysis_id}
Headers:
	Authorization: Bearer + Token
Retorna:
[]
```

#### Criar uma nova análise

```
POST api/analysis/
Headers:
	Authorization: Bearer + Token
Body:
{
   "viscosity":19,
   "diameter":0.1,
   "flow":0.01
}
Retorna:
{
   "id":119,
   "reynolds_number":6701.260761764015,
   "reynolds_number_regime":"turbulent",
   "viscosity":19.0,
   "diameter":0.1,
   "flow":1.0,
   "creator":1
}
```

### 4.2. Autenticação

Todas as chamadas da API precisam serem autenticadas. Para obter o token de autenticação, vá no seguinte endpoint:

```
POST /api/token/
Body:
{
   "username":  "username",
   "password":  "password"
}
Retorna:
{
   "refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyMzExMzQzNSwianRpIjoiY2FlY2I1YmQ2MDUyNDRiZDg1ZmZiMTcwNjU2MjYxMGMiLCJ1c2VyX2lkIjoxfQ.-RIqQr_Gbw0Z0g5VVJkIfR6E_CNnUNo-MqwaNuiq0DM",
   "access":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjIzNjMxODM1LCJqdGkiOiIwZmFkMTdhZDk1OWI0NjM2OWU0MjliODQyZWVlYzNhOSIsInVzZXJfaWQiOjF9.xBVNXv5MVfPTQKahCvcxQAdHqo3Y9lbUkSTMXgikYrc"
}
```

Obs.: No header, você precisa passar `access` como `token` (Authorization: Bearer + Token `(access)`)

## 5. Funcionalidades

### 5.1 - Envio de email a cada análise criada

Para cada análise criada, um email é enviado. Este envio é assíncrono usando (Celery + RabbitMQ + Flower). O envio do email é simulado usando o MailHog.

- Para acessar ao MailHog: vá em http://localhost:8025/
- Para acessar o flower, vá em http://localhost:5555/dashboard

### 5.2 Front-end em React para testes

O sistema tem um front-end feito em react para que os testes possam ser feitos.

- Para acessar o front-end, vá em http://localhost:8000/
- Para logar no sistema utilize o usuário que você criou no passo 3

### 5.3 Download de todas as análises em CSV pelo painel do admin

É possível fazer uma seleção de análise e fazer o download destas pelo painel do admin

- Para logar painel do admin vá em http://localhost:8000/admin/
- Para ver a análises, vá em http://localhost:8000/admin/analysis/analysis/
- Selecione as análises
- Em actions, selecione Export to CSV, clique em go e escolha o local onde quer baixar

### 5.4 Documentação

- Para acessar a documentação, vá em http://localhost:8000/docs/

## 6. Sistema para testes

- Para facilitar os testes, o sistema está disponível em: http://143.198.119.27:8000/ (basta usar cada endpoint)
- Para logar no sistema, utilize as seguintes credenciais:

```
  "username": "admin",
  "password": "admin@3123"
```

- Para acessar ao MailHog: vá em http://143.198.119.27:8025/
- Para acessar o flower, vá em http://143.198.119.27:5555/dashboard

## 7. Execução dos testes

Para executar os testes, dê o seguinte comando: `make docker_test`
