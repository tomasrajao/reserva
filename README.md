## Sistema de Gerenciamento de Reservas de Salas de Reunião

Sistema de gerenciamento de reservas de salas de reunião, que permite usuários cadastrarem salas de reunião, verificar a disponibilidade das salas em horários específicos, reservar salas e cancelar reservas.

O sistema é feito em FastAPI, utiliza PostgreSQL como banco de dados, possui cobertura de testes e está disponível em container Docker. 

### Configurações

#### Clone do repositório
Executar no terminal uma das opções:

Via HTTP:

```
https://github.com/tomasrajao/reserva.git
```
Via SSH:

```
git@github.com:tomasrajao/reserva.git
```
Via Github CLI:

```
gh repo clone tomasrajao/reserva
```
##
#### Criar imagem Docker e inicializar container
```
docker build -t 'reserva' .
docker compose up --build
```
##
#### Definir arquivo de variáveis de ambiente (.env)
```
echo 'SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL="postgresql+psycopg://app_user:app_password@localhost:5432/app_db"' >> .env
```

##
### Documentação

#### Documentação das APIs disponível em:
##### -  <http://localhost:8000/docs>

##

### Endpoints

Para utilizar das funcionalidades da API, o primeiro passo é criar um usuário, com nome, email e senha.

#### Criar usuário (POST /users)
Exemplo:
- Body
```json
{
  "user_name": "João",
  "email": "joao.costa@empresa.com.br",
  "password": "@joaocosta2828"
}
```

- Retorno (201)
```json
{
  "id": 1,
  "user_name": "João",
  "email": "joao.costa@empresa.com.br"
}
```
##
#### Login de usuário (POST /auth/token)

 - Body
```json
{
  "username": "joao.costa@empresa.com.br",
  "password": "@joaocosta2828"
}
```

- Retorno (200)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZUB0ZXN0LmNvbSIsImV4cCI6MTY5MDI1ODE1M30.Nx0P_ornVwJBH_LLLVrlJoh6RmJeQr7YJmlGY04",
  "token_type": "bearer"
}
```
##
#### Cadastrar sala de reunião (POST /rooms)
Exemplo:
- Body
```json
{
  "name": "Sala A",
  "capacity": 10,
  "location": "Andar 1"
}
```
- Retorno (201)
```json
{
  "name": "Sala C",
  "capacity": 12,
  "location": "Andar 1",
  "id": 3
}
```
##
#### Listar salas de reunião (GET /rooms)
- Params (opcional)
```json
{
  "offset": 0,
  "limit": 100
}
```
- Retorno (200)
```json
{
  "rooms": [
    {
      "name": "Sala A",
      "capacity": 10,
      "location": "Andar 1",
      "id": 1
    },
    {
      "name": "Sala B",
      "capacity": 15,
      "location": "Andar 2",
      "id": 2
    }
  ]
}
```
##
#### Consultar disponibilidade das salas (GET /rooms/{id}/availability)
- Params

```json
{
    "start_time": "2025-02-10T10:00:00",
    "end_time": "2025-02-10T12:00:00"
}
```
- Exemplo de retorno (200)
```json
{
    "message": "Sala A is available from 2025-02-10 10:00:00 to 2025-02-10 12:00:00."
}
```
##
#### Reservar uma sala (POST /reservations)
- Header
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZUB0ZXN0LmNvbSIsImV4cCI6MTY5MDI1ODE1M30.Nx0P_ornVwJBH_LLLVrlJoh6RmJeQr7YJmlGY04",
}
```
- Body
```json
{
  "start_time": "2025-02-11T10:00:00",
  "end_time": "2025-02-11T12:00:00",
  "room_id": 1
}
```
- Retorno (201)
```json
{
  "start_time": "2025-02-11T10:00:00",
  "end_time": "2025-02-11T12:00:00",
  "room_id": 1,
  "id": 1,
  "room": {
    "name": "Sala A",
    "capacity": 10,
    "location": "Andar 1"
  },
  "user": {
    "user_name": "João"
  }
}
```
##
#### Cancelar reserva (DELETE /reservations/{id})
Informar ID correspondente à reserva na URL
- Header
```json
{
  "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZUB0ZXN0LmNvbSIsImV4cCI6MTY5MDI1ODE1M30.Nx0P_ornVwJBH_LLLVrlJoh6RmJeQr7YJmlGY04",
}
```
 - Retorno (204)
##
#### Listar reservas de uma sala (GET /rooms/{id}/reservations)
Informar ID correspondente à sala na URL
- Params (opcional)
```json
{
  "date": "2025-02-11"
}
```
 - Retorno (200)
 ```json
 {
  "reservations": [
    {
        "start_time": "2025-02-13T12:00:00:000000",
        "end_time": "2025-02-13T13:00:00:000000",
        "room_id": 1,
        "id": 1,
        "room": {
            "name": "Sala A",
            "capacity": 10,
            "location": "Andar 1"
        },
        "user": {
        "user_name": "João"
        }
    },
    {
        "start_time": "2025-02-13T16:00:00:000000",
        "end_time": "2025-02-13T18:00:00:000000",
        "room_id": 1,
        "id": 2,
        "room": {
            "name": "Sala A",
            "capacity": 10,
            "location": "Andar 1"
        },
        "user": {
        "user_name": "João"
        }
    }
  ]
 ```
