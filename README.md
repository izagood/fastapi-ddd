# FastAPI Domain-Driven Design (DDD) Example

> FastAPI + SQLAlchemy(Async) + DDD 레이어드 아키텍처 예제 프로젝트

![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0%2B-red?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/tests-112%20passed-brightgreen)
![Ruff](https://img.shields.io/badge/code%20style-ruff-000000?logo=ruff&logoColor=white)

---

## 프로젝트 소개

Domain-Driven Design(DDD) 패턴을 FastAPI와 SQLAlchemy(async)에 적용한 **학습 목적의 예제 프로젝트**입니다.

Member(회원) 도메인을 중심으로 Entity, Value Object, Domain Event, Repository, Unit of Work, Domain Service 등 DDD의 주요 전술적 패턴을 구현합니다.

---

## 기술 스택

| 분류 | 기술 |
|------|------|
| **웹 프레임워크** | FastAPI 0.115+ |
| **ORM** | SQLAlchemy 2.0+ (async) |
| **검증** | Pydantic v2, Pydantic Settings |
| **마이그레이션** | Alembic |
| **비밀번호** | bcrypt |
| **DB** | PostgreSQL + asyncpg (운영) / SQLite + aiosqlite (개발·테스트) |
| **서버** | Uvicorn, Gunicorn |
| **패키지 관리** | uv |
| **린트·포맷** | Ruff |
| **테스트** | pytest, pytest-asyncio, pytest-cov, httpx |
| **로깅** | Loguru |

---

## 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│              (REST Routers, Request/Response)                │
└──────────────────────────┬──────────────────────────────────┘
                           │ depends on
┌──────────────────────────▼──────────────────────────────────┐
│                    Application Layer                         │
│         (MemberService, DTO, AbstractUnitOfWork)            │
└──────────────────────────┬──────────────────────────────────┘
                           │ depends on
┌──────────────────────────▼──────────────────────────────────┐
│                      Domain Layer                            │
│    (Member Entity, Value Objects, Events, Repository ABC,   │
│     MemberDomainService, Exceptions)                        │
└──────────────────────────▲──────────────────────────────────┘
                           │ implements (Dependency Inversion)
┌──────────────────────────┴──────────────────────────────────┐
│                  Infrastructure Layer                         │
│     (SQLAlchemy Repository, UnitOfWork, Database Config,    │
│      Alembic Migrations, FastAPI Dependencies)              │
└─────────────────────────────────────────────────────────────┘
```

**의존성 방향**: `Presentation → Application → Domain ← Infrastructure`

- **Domain 레이어**는 외부에 의존하지 않습니다.
- **Infrastructure 레이어**는 Domain의 추상(ABC/Protocol)을 구현합니다.
  - `MemberRepository`(ABC) → `SqlAlchemyMemberRepository`(구현)
  - `AbstractUnitOfWork`(Protocol) → `UnitOfWork`(구현)

---

## 디렉토리 구조

```
fastapi-ddd/
├── fastapi_ddd/
│   ├── main.py                          # FastAPI 앱 진입점 (lifespan, middleware, CORS)
│   ├── application/                     # Application Layer
│   │   ├── member/
│   │   │   ├── member_request.py        # 요청 DTO (CreateMember, UpdateProfile, ChangeEmail 등)
│   │   │   ├── member_response.py       # 응답 DTO (MemberDTO)
│   │   │   └── member_service.py        # 애플리케이션 서비스 (유스케이스 오케스트레이션)
│   │   └── ports/
│   │       └── unit_of_work.py          # AbstractUnitOfWork (Protocol)
│   ├── common/                          # 공통 유틸리티
│   │   ├── config/
│   │   │   ├── app_config.py            # FastAPI, CORS 설정
│   │   │   ├── infra_config.py          # DB 설정 (pydantic-settings)
│   │   │   └── logger.py               # Loguru 초기화
│   │   └── exception/
│   │       ├── custom_exceptions.py     # 인프라 레벨 예외 (NotFoundException, DatabaseException)
│   │       └── exception_handlers.py    # 글로벌 예외 핸들러 (Domain → HTTP 매핑)
│   ├── domain/                          # Domain Layer
│   │   ├── entity.py                    # Base, EntityId, TimestampMixin, BaseWithTime
│   │   ├── events.py                    # Domain Events (MemberCreated, MemberEmailChanged 등)
│   │   ├── exceptions.py               # 도메인 예외 (DomainException, MemberNotFoundException 등)
│   │   ├── custom_types/
│   │   │   └── entity_id_type.py        # EntityIdType (SQLAlchemy TypeDecorator)
│   │   └── member/
│   │       ├── member.py                # Member 엔티티 (Aggregate Root)
│   │       ├── member_domain_service.py # 도메인 서비스 (이메일 유일성 검증)
│   │       ├── member_repository.py     # Repository 인터페이스 (ABC)
│   │       ├── member_validator.py      # EmailValidator, PasswordValidator, PasswordHasher
│   │       └── value_objects.py         # Value Objects (Email, Password)
│   ├── infra/                           # Infrastructure Layer
│   │   ├── dependencies.py              # FastAPI DI 함수 (get_session, get_uow, get_service)
│   │   └── database/
│   │       ├── database.py              # AsyncEngine, SessionMaker 관리
│   │       ├── init_db.py               # DB 초기화·종료
│   │       ├── member_repository_impl.py # SqlAlchemyMemberRepository (구현체)
│   │       ├── unit_of_work.py          # UnitOfWork (구현체)
│   │       └── alembic/
│   │           ├── env.py               # Alembic 설정
│   │           ├── script.py.mako       # 마이그레이션 템플릿
│   │           └── versions/
│   │               └── 001_create_member_table.py
│   └── presentation/                    # Presentation Layer
│       └── rest/
│           ├── routers.py               # API 라우터 집합 + Health Check
│           └── member_router.py         # Member REST 엔드포인트
├── tests/
│   ├── conftest.py                      # 공통 fixtures
│   ├── application/                     # Application Service 단위 테스트
│   ├── common/                          # Config, Exception Handler 테스트
│   ├── domain/                          # Domain 레이어 단위 테스트
│   ├── infra/                           # Infrastructure 단위 테스트
│   ├── integration/                     # 통합 테스트 (SQLite + Alembic)
│   └── presentation/                    # Router 단위 테스트
├── alembic.ini                          # Alembic 설정 파일
├── pyproject.toml                       # 프로젝트 메타데이터 및 도구 설정
├── .env.example                         # 환경 변수 예시
└── .python-version                      # Python 버전 (3.13)
```

---

## 핵심 DDD 패턴

### Entity & Value Objects

- **`EntityId`**: UUID를 래핑하는 식별자 타입. `EntityIdType`(SQLAlchemy TypeDecorator)으로 DB와 매핑
- **`Email`**: 이메일 형식 검증을 캡슐화한 Value Object
- **`Password`**: 생성 시 자동 해싱(bcrypt), `verify()` 메서드로 검증. `from_hashed()`로 DB에서 복원

### Domain Events

엔티티 상태 변경 시 도메인 이벤트가 발행됩니다:

| 이벤트 | 발생 시점 |
|--------|-----------|
| `MemberCreated` | 회원 생성 |
| `MemberEmailChanged` | 이메일 변경 |
| `MemberProfileUpdated` | 프로필(이름) 수정 |
| `MemberPasswordChanged` | 비밀번호 변경 |
| `MemberDeleted` | 회원 삭제 (소프트 삭제) |

이벤트는 `Member._domain_events` 리스트에 축적되며, `MemberService._publish_events()`에서 로깅 후 클리어됩니다.

### Domain Service

`MemberDomainService`는 단일 엔티티를 넘어서는 도메인 규칙을 처리합니다:
- **이메일 유일성 검증**: `ensure_email_unique()` — 중복 시 `DuplicateEmailException` 발생

### Repository Pattern

```python
# Domain Layer — 인터페이스 (ABC)
class MemberRepository(ABC):
    async def create(self, member: Member) -> None: ...
    async def find_by_id(self, entity_id: EntityId) -> Member: ...
    async def find_all(self, *, skip: int, limit: int) -> list[Member]: ...
    async def find_by_email(self, email: str) -> Optional[Member]: ...
    async def exists_by_email(self, email: str) -> bool: ...

# Infrastructure Layer — 구현체
class SqlAlchemyMemberRepository(MemberRepository):
    ...
```

### Unit of Work

```python
# Application Layer — Protocol
class AbstractUnitOfWork(Protocol):
    members: MemberRepository
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    async def refresh(self, instance: object) -> None: ...

# Infrastructure Layer — 구현체
class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
    async def refresh(self, instance: object) -> None: ...
```

`UnitOfWork`는 async context manager로 동작하며, 예외 발생 시 자동으로 롤백합니다.

### Exception 전략

도메인 예외가 HTTP 상태 코드로 자동 매핑됩니다:

| 도메인 예외 | HTTP 상태 코드 |
|-------------|---------------|
| `DuplicateEmailException` | `409 Conflict` |
| `EntityNotFoundException` | `404 Not Found` |
| `DomainException` | `400 Bad Request` |
| `ValueError` | `400 Bad Request` |

---

## API 엔드포인트

기본 경로: `/api/v1`

### Health Check

| Method | Path | 설명 | 상태 코드 |
|--------|------|------|----------|
| `GET` | `/api/v1/health` | 서버 상태 확인 | `200` |

### Member

| Method | Path | 설명 | 상태 코드 |
|--------|------|------|----------|
| `POST` | `/api/v1/members/` | 회원 생성 | `201` |
| `GET` | `/api/v1/members/` | 전체 회원 조회 | `200` |
| `GET` | `/api/v1/members/{member_id}` | 회원 단건 조회 | `200` |
| `PATCH` | `/api/v1/members/{member_id}` | 프로필(이름) 수정 | `200` |
| `PATCH` | `/api/v1/members/{member_id}/email` | 이메일 변경 | `200` |
| `PATCH` | `/api/v1/members/{member_id}/password` | 비밀번호 변경 | `200` |
| `DELETE` | `/api/v1/members/{member_id}` | 회원 삭제 | `204` |

### 요청/응답 예시

**회원 생성**

```bash
curl -X POST http://localhost:8000/api/v1/members/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "passwd": "password123",
    "name": "홍길동"
  }'
```

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "홍길동",
  "created_at": "2026-02-23T12:00:00Z",
  "updated_at": "2026-02-23T12:00:00Z"
}
```

**이메일 변경**

```bash
curl -X PATCH http://localhost:8000/api/v1/members/{member_id}/email \
  -H "Content-Type: application/json" \
  -d '{"email": "new@example.com"}'
```

---

## 시작하기

### 사전 요구사항

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (패키지 관리자)

### 설치 및 실행

```bash
# 1. 저장소 클론
git clone https://github.com/your-repo/fastapi-ddd.git
cd fastapi-ddd

# 2. uv 설치 (설치되지 않은 경우)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 의존성 설치
uv sync

# 4. 환경 변수 설정
cp .env.example .env

# 5. 서버 실행
uv run uvicorn fastapi_ddd.main:app --reload

# 6. API 문서 접근
# Swagger UI: http://localhost:8000/docs
# ReDoc:      http://localhost:8000/redoc
```

---

## 환경 변수

`.env.example` 참고:

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `DATABASE_URL` | 데이터베이스 연결 URL | `sqlite+aiosqlite:///fastapi_ddd.db` |
| `SQL_ECHO` | SQL 쿼리 로깅 활성화 | `false` |
| `AUTO_CREATE_TABLES` | 테이블 자동 생성 (운영에서는 `false`) | `true` |
| `CORS_ORIGINS` | 허용 Origin (쉼표 구분, `*` 전체 허용) | `*` |
| `CORS_ALLOW_CREDENTIALS` | 자격증명 허용 | `true` |
| `CORS_ALLOW_METHODS` | 허용 HTTP 메서드 | `*` |
| `CORS_ALLOW_HEADERS` | 허용 헤더 | `*` |

---

## 데이터베이스 & 마이그레이션

### SQLite (기본, 즉시 사용 가능)

별도 설정 없이 `sqlite+aiosqlite:///fastapi_ddd.db`로 동작합니다.

### PostgreSQL로 전환

`.env` 파일에서 `DATABASE_URL`을 변경합니다:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_ddd
```

### Alembic 마이그레이션

```bash
# 마이그레이션 실행 (최신까지)
uv run alembic upgrade head

# 새 마이그레이션 생성
uv run alembic revision --autogenerate -m "description"

# 마이그레이션 히스토리 확인
uv run alembic history

# 한 단계 롤백
uv run alembic downgrade -1
```

---

## 테스트

```bash
# 전체 테스트 실행
uv run pytest

# 상세 출력
uv run pytest -v

# 커버리지 포함
uv run pytest --cov=fastapi_ddd
```

### 테스트 분류 (총 112개)

| 분류 | 파일 | 수량 |
|------|------|------|
| **Domain** | `test_member.py` | 20 |
| | `test_member_validator.py` | 14 |
| | `test_value_objects.py` | 11 |
| | `test_events.py` | 5 |
| | `test_member_domain_service.py` | 2 |
| **Application** | `test_member_service.py` | 11 |
| **Presentation** | `test_member_router.py` | 8 |
| **Common** | `test_config.py` | 6 |
| | `test_exception_handlers.py` | 3 |
| **Infra** | `test_init_db.py` | 1 |
| **Integration** | `test_member_api.py` | 13 |
| | `test_member_repository.py` | 11 |
| | `test_member_service.py` | 4 |
| | `test_alembic_migrations.py` | 3 |

---

## 코드 품질

```bash
# 린트 검사
uv run ruff check .

# 자동 수정
uv run ruff check . --fix

# 포맷 검사
uv run ruff format --check .

# 포맷 적용
uv run ruff format .
```

---

## 의존성 흐름 (DI Chain)

```
Request
  │
  ▼
member_router.py ──Depends──▶ get_member_service()
                                    │
                                    ├──▶ get_uow()
                                    │       │
                                    │       ├──▶ get_async_session()
                                    │       │       └── SessionMaker → AsyncSession
                                    │       │
                                    │       └── UnitOfWork(session)
                                    │              └── .members = SqlAlchemyMemberRepository(session)
                                    │
                                    └── MemberService(uow)
                                           └── ._domain_service = MemberDomainService(uow.members)
```

FastAPI의 `Depends` 체인을 통해 `AsyncSession → UnitOfWork → MemberService` 순서로 의존성이 주입됩니다. 각 요청마다 새로운 세션과 UoW 인스턴스가 생성되며, 요청 종료 시 자동으로 정리됩니다.

---

## 라이선스

이 프로젝트는 [MIT License](LICENSE) 하에 배포됩니다.
