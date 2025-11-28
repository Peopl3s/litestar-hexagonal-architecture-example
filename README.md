# :star2: Litestar Hexagonal Architecture Project Example

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-000000?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)[![GitHub Stars](https://img.shields.io/github/stars/Peopl3s/litestar-hexagonal-architecture-example?style=for-the-badge&logo=github&logoColor=white&color=000000)](https://github.com/Peopl3s/litestar-hexagonal-architecture-example/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/Peopl3s/litestar-hexagonal-architecture-example?style=for-the-badge&color=000000)](https://github.com/Peopl3s/litestar-hexagonal-architecture-example/commits/main)
[![License](https://img.shields.io/github/license/Peopl3s/litestar-hexagonal-architecture-example?style=for-the-badge&color=000000)](./LICENSE)

![Litestar](https://img.shields.io/badge/Litestar-000000?style=for-the-badge&logo=litestar&logoColor=white)
![FastStream](https://img.shields.io/badge/FastStream-000000?style=for-the-badge&logo=faststream&logoColor=white)
![Dishka](https://img.shields.io/badge/Dishka-000000?style=for-the-badge&logoColor=white)
![Hexagonal Architecture](https://img.shields.io/badge/Hexagonal_Architecture-000000?style=for-the-badge&logoColor=white)
--------


💫 [Litestar Clean Acrhitecture Project Template](https://github.com/Peopl3s/clean-architecture-litestar-project-template)

🔌 [FastAPI Clean Architecture Project Template](https://github.com/Peopl3s/clean-architecture-fastapi-project-template)

---

Hexagonal Architecture, also known as **Ports and Adapters Architecture**, was proposed by Alistair Cockburn as a design approach for building applications centered around a core of business logic that remains independent from external dependencies (such as databases, UIs, external APIs, etc.).

In this architecture, there are **no traditional "layers"** like in layered architectures (e.g., presentation → business → data). Instead, it revolves around an **application core**, surrounded by **ports and adapters**. However, for clarity, we can identify the following **logical components**:

#### 1. **Application Core (Hexagon)**

- Contains **pure business logic** (domain logic).
- **Has no dependencies** on external systems: databases, web frameworks, UIs, etc.
- Interacts with the outside world **exclusively through ports**.

#### 2. **Ports**

- These are **interfaces** defining **how the core communicates with the outside world**.
- There are two types:
    - **Primary (Driving) Ports** — used by **external systems to invoke the core** (e.g., REST APIs, CLI, UI).
    - **Secondary (Driven) Ports** — used by **the core to invoke external systems** (e.g., databases, external services).

#### 3. **Adapters**

- Concrete implementations of ports.
- **Bridge external technologies to the core** via corresponding ports.
- Also divided into:
    - **Primary Adapters** — invoke the core (e.g., Spring controllers, HTTP request handlers).
    - **Secondary Adapters** — are invoked by the core (e.g., repositories, external API clients).

#### Advantages:

- Easy testing (adapters can be replaced with mocks).
- Independence from frameworks and infrastructure.
- Flexibility: UIs, databases, or integration methods can be easily swapped.

#### Example:

- **Core**: Order processing service.
- **Primary Port**: `OrderService` (interface).
- **Primary Adapter**: REST controller calling `OrderService`.
- **Secondary Port**: `OrderRepository` (interface for persisting orders).
- **Secondary Adapter**: PostgreSQL-based implementation of `OrderRepository`.

Thus, in Hexagonal Architecture, traditional **"layers" are replaced by a "core + ports + adapters"** structure, ensuring architectural clarity and flexibility.

```
│
├── app/
│   ├── __init__.py
│   │
│   ├── core/                     # ← Application Core (Hexagon)
│   │   ├── __init__.py
│   │   ├── models.py             # ← Domain models (plain, no ORM/Pydantic)
│   │   └── services.py           # ← Business logic (Use Cases)
│   │
│   ├── ports/                    # ← Ports (interfaces)
│   │   ├── __init__.py
│   │   ├── user_ports.py         # ← IUserRepository, etc.
│   │   └── auth_ports.py
│   │
│   ├── adapters/                 # ← Adapters
│   │   ├── __init__.py
│   │   │
│   │   ├── primary/              # ← Primary (Driving) Adapters
│   │   │   ├── __init__.py
│   │   │   └── api/              # ← Litestar routes
│   │   │       ├── __init__.py
│   │   │       ├── controllers.py
│   │   │       └── dtos.py       # ← DTOs: request/response models (Pydantic)
│   │   │
│   │   └── secondary/            # ← Secondary (Driven) Adapters
│   │       ├── __init__.py
│   │       ├── database/         # ← Repositories, ORM models
│   │       │   ├── __init__.py
│   │       │   ├── models.py     # ← SQLAlchemy models
│   │       │   └── repositories.py  # ← Port implementations
│   │       └── external/         # ← External APIs, file systems, etc.
│   │
│   └── main.py                   # ← Litestar entry point
│   └── config.py                 # ← Project settings
│   └── ioc.py                    # ← DI
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── ...
└── README.md
```

## Stack
* Main framework - Litestar
* Message broker framework - Faststream
* DI - dishka
* Database - SQLAlchemy + alembic
* Validation - Pydantic
* Package manager - uv
* HTTP-requests - httpx
* Retries - stamina
* Deployment - Docker + granian
* Tests - pytest
