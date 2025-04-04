from typing import Generator

import pytest
from pydantic import EmailStr, TypeAdapter
from sqlalchemy.orm import Session, sessionmaker

from app.repository.clientrepo import ClientAlreadyExistsError, ClientRepository
from domain.entity.client import Client
from domain.vo.address import Address  # Caso você tenha Address separado
from domain.vo.cpf import cpf_validator
from domain.vo.personname import name_validator
from infra.database.db import get_db, make_session
from infra.database.models.client import Base
from infra.repository.clientrepo import SQLAlchemyClientAdapter

# ---------- Session Helpers ----------


def drop_all(sessionLocal: sessionmaker[Session], base: type[Base]) -> None:
    engine = sessionLocal.kw["bind"]
    base.metadata.drop_all(engine)


# ---------- Pytest Fixtures ----------
@pytest.fixture(scope="function")
def session_local() -> Generator[sessionmaker[Session], None, None]:
    session_local = make_session("sqlite:///:memory:", Base)
    yield session_local
    drop_all(session_local, Base)


@pytest.fixture(scope="function")
def session(session_local: sessionmaker[Session]) -> Generator[Session, None, None]:
    db_gen = get_db(session_local)
    db = next(db_gen)
    yield db
    db.rollback()
    db.close()


@pytest.fixture
def repo(session: Session) -> ClientRepository:
    return SQLAlchemyClientAdapter(session=session)


# ---------- Test Helpers ----------
def make_client(
    id: int = -1,
    name: str = "João Silva",
    email: str = "joao@email.com",
    phone: str = "1234-5678",
    cpf: str = "97456321558",
    addr: Address | None = None,
) -> Client:
    return Client(
        id=id,
        name=name_validator(name),
        email=TypeAdapter(EmailStr).validate_python(email),
        phone=phone,
        cpf=cpf_validator(cpf),
        addr=addr,
    )


# ---------- Tests ----------
def test_save_and_search_success(repo: ClientRepository) -> None:
    client = make_client()
    repo.save(client)

    results = repo.search(name_contains="João")
    assert len(results) == 1
    assert results[0].email == client.email


def test_save_duplicate_email_raises(repo: ClientRepository) -> None:
    client1 = make_client()
    client2 = make_client(
        email="joao@email.com", cpf="71428793860", name="Carlos Souza"
    )

    repo.save(client1)

    with pytest.raises(ClientAlreadyExistsError) as e:
        repo.save(client2)

    assert e.value.field == "email"


def test_save_duplicate_cpf_raises(repo: ClientRepository) -> None:
    client1 = make_client()
    client2 = make_client(
        email="carlos@email.com", cpf="97456321558", name="Carlos Souza"
    )

    repo.save(client1)

    with pytest.raises(ClientAlreadyExistsError) as e:
        repo.save(client2)

    assert e.value.field == "cpf"


def test_save_duplicate_name_raises(repo: ClientRepository) -> None:
    client1 = make_client()
    client2 = make_client(email="outro@email.com", cpf="71428793860", name="João Silva")

    repo.save(client1)

    with pytest.raises(ClientAlreadyExistsError) as e:
        repo.save(client2)

    assert e.value.field == "name"


def test_search_partial_match(repo: ClientRepository) -> None:
    client = make_client(
        name="Maria Fernanda", email="maria@example.com", cpf="87748248800"
    )
    repo.save(client)

    assert len(repo.search(name_contains="Maria")) == 1
    assert len(repo.search(email_contains="example")) == 1
    assert len(repo.search(cpf_contains="877")) == 1
    assert len(repo.search(name_contains="João")) == 0
