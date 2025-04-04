from typing import Annotated

from pydantic import BaseModel, BeforeValidator, TypeAdapter


def validate_cpf(cpf: str) -> str:
    CPF_LENGTH = 11
    FACTOR_FIRST_DIGIT = 10
    FACTOR_SECOND_DIGIT = 11

    if not cpf:
        raise ValueError(f"Invalid cpf - empty value. {cpf}")

    cpf = "".join(filter(str.isdigit, cpf))  # Remove non-digit characters
    if len(cpf) != CPF_LENGTH:
        raise ValueError(f"Invalid cpf - length is not {CPF_LENGTH}. {cpf}")

    if all(digit == cpf[0] for digit in cpf):  # Check if all digits are the same
        raise ValueError(f"Invalid cpf - all digits are the same. {cpf}")

    def calculate_digit(cpf: str, factor: int) -> int:
        total = 0
        for digit in cpf[: factor - 1]:
            total += int(digit) * factor
            factor -= 1
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    digit1 = calculate_digit(cpf, FACTOR_FIRST_DIGIT)
    digit2 = calculate_digit(cpf, FACTOR_SECOND_DIGIT)

    if cpf[-2:] != f"{digit1}{digit2}":
        raise ValueError(f"Invalid cpf - digits do not match. {cpf}")
    return cpf


CPF = Annotated[str, BeforeValidator(validate_cpf)]

cpf_adapter = TypeAdapter(CPF)


def cpf_validator(cpf: str) -> str:
    return cpf_adapter.validate_python(cpf)
