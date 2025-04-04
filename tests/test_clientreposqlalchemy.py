from email.headerregistry import Address

import pytest
from pydantic import EmailStr
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from app.repository.clientrepo import ClientAlreadyExistsError
from domain.entity.client import Client
from domain.vo.cpf import cpf_validator
from domain.vo.personname import name_validator
from infra.database.models import AddressModel, Base, ClientModel
from infra.repository.sqlalchemy_adapter import SQLAlchemyClientAdapter


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def repo(session):
    return SQLAlchemyClientAdapter(session=session)


def make_client(
    id: int = -1,
    name="João Silva",
    email="joao@email.com",
    phone="1234-5678",
    cpf="97456321558",
    addr=None,
) -> Client:
    return Client(
        id=id,
        name=name_validator(name),
        email=EmailStr(email),
        phone=phone,
        cpf=cpf_validator(cpf),
        addr=addr,
    )


def test_save_and_search_success(repo):
    client = make_client()
    repo.save(client)

    results = repo.search(name_contains="João")
    assert len(results) == 1
    assert results[0].email == client.email


def test_save_duplicate_email_raises(repo):
    client1 = make_client()
    client2 = make_client(
        email="joao@email.com", cpf="71428793860", name="Carlos Souza"
    )

    repo.save(client1)

    with pytest.raises(ClientAlreadyExistsError) as e:
        repo.save(client2)

    assert e.value.field == "email"


def test_save_duplicate_cpf_raises(repo):
    client1 = make_client()
    client2 = make_client(
        email="carlos@email.com", cpf="97456321558", name="Carlos Souza"
    )

    repo.save(client1)

    with pytest.raises(ClientAlreadyExistsError) as e:
        repo.save(client2)

    assert e.value.field == "cpf"


def test_save_duplicate_name_raises(repo):
    client1 = make_client()
    client2 = make_client(email="outro@email.com", cpf="71428793860", name="João Silva")

    repo.save(client1)

    with pytest.raises(ClientAlreadyExistsError) as e:
        repo.save(client2)

    assert e.value.field == "name"


def test_search_partial_match(repo):
    client = make_client(
        name="Maria Fernanda", email="maria@example.com", cpf="87748248800"
    )
    repo.save(client)

    results = repo.search(name_contains="Maria")
    assert len(results) == 1

    results = repo.search(email_contains="example")
    assert len(results) == 1

    results = repo.search(cpf_contains="877")
    assert len(results) == 1

    results = repo.search(name_contains="João")
    assert len(results) == 0
