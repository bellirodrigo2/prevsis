import pytest
from pydantic import TypeAdapter

from domain.vo.cpf import CPF, cpf_validator

cpf_adapter = TypeAdapter(CPF)


@pytest.mark.parametrize("cpf", ["97456321558", "71428793860", "87748248800"])
def test_valid_cpf(cpf: str) -> None:
    assert cpf_validator(cpf) == cpf


@pytest.mark.parametrize(
    "cpf", ["", None, "123456", "12345678901234567890", "11111111111"]
)
def test_invalid_cpf(cpf: str | None) -> None:
    with pytest.raises(ValueError, match="Invalid cpf"):
        cpf_validator(cpf)
