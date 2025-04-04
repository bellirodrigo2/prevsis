import pytest

from src.domain.vo.cpf import CPF


@pytest.mark.parametrize("cpf", ["97456321558", "71428793860", "87748248800"])  # type: ignore
def test_valid_cpf(cpf: str) -> None:

    assert CPF(value=cpf) is not None


@pytest.mark.parametrize(
    "cpf", ["", None, "123456", "12345678901234567890", "11111111111"]  # type: ignore
)
def test_invalid_cpf(cpf: str | None) -> None:
    with pytest.raises(ValueError, match="Invalid cpf"):
        CPF(value=cpf)
