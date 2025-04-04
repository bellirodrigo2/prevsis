from typing import Annotated

from pydantic import BeforeValidator, TypeAdapter


def validar_nome(v: str) -> str:

    if v is None:  # type: ignore
        raise ValueError("Nome não pode ser nulo")

    v = v.strip()

    palavras = v.split()

    if len(palavras) < 2:
        raise ValueError("Informe pelo menos nome e sobrenome (mínimo duas palavras)")

    if len(palavras[0]) < 3:
        raise ValueError("O primeiro nome deve ter no mínimo 3 letras")

    if not all(p.isalpha() for p in palavras):
        raise ValueError(
            "O nome deve conter apenas letras e espaços (sem números ou símbolos)"
        )

    return " ".join(p.capitalize() for p in palavras)


Name = Annotated[str, BeforeValidator(validar_nome)]

name_adapter = TypeAdapter(Name)


def name_validator(cpf: str) -> str:
    return name_adapter.validate_python(cpf)
