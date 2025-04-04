import pytest

from domain.vo.personname import name_validator


@pytest.mark.parametrize(
    "nome_entrada,nome_esperado",
    [
        ("joão silva", "João Silva"),
        ("  maria clara  ", "Maria Clara"),
        ("luiz henrique", "Luiz Henrique"),
        ("ANA BEATRIZ", "Ana Beatriz"),
        ("éverton costa", "Éverton Costa"),
    ],
)
def test_valid_names(nome_entrada: str, nome_esperado: str) -> None:
    assert name_validator(nome_entrada) == nome_esperado


@pytest.mark.parametrize(
    "nome_invalido",
    [
        "",  # vazio
        "ana",  # só um nome
        " a ",  # um nome com espaços
        "jo 3ao silva",  # contém número
        "joão!",  # contém símbolo
        "an silva",  # primeiro nome < 3 letras
        "1a 2b",  # só números e letras misturados
        None,  # None
    ],
)  # type: ignore
def test_invalid_names(nome_invalido: str | None) -> None:
    with pytest.raises(ValueError):
        name_validator(nome_invalido)  # type: ignore[arg-type]
