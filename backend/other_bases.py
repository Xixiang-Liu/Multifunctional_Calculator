from decida import baseconvert
from decimal import Decimal


def convert(value: str, old_base: int, new_base: int) -> str:
    result = baseconvert(old_base, new_base, value)
    return result


def plus(num_1: str, num_2: str, base: int) -> str:
    num_1 = Decimal(baseconvert(base, 10, num_1))
    num_2 = Decimal(baseconvert(base, 10, num_2))
    result_base_ten = str(num_1 + num_2)
    result = baseconvert(10, base, result_base_ten)
    return result


def minus(num_1: str, num_2: str, base: int) -> str:
    num_1 = Decimal(baseconvert(base, 10, num_1))
    num_2 = Decimal(baseconvert(base, 10, num_2))
    result_base_ten = str(num_1 - num_2)
    result = baseconvert(10, base, result_base_ten)
    return result


def multiply(num_1: str, num_2: str, base: int) -> str:
    num_1 = Decimal(baseconvert(base, 10, num_1))
    num_2 = Decimal(baseconvert(base, 10, num_2))
    result_base_ten = str(num_1 * num_2)
    result = baseconvert(10, base, result_base_ten)
    return result


def divided_by(num_1: str, num_2: str, base: int) -> str:
    num_1 = Decimal(baseconvert(base, 10, num_1))
    num_2 = Decimal(baseconvert(base, 10, num_2))
    result_base_ten = str(num_1 // num_2)
    result = baseconvert(10, base, result_base_ten)
    return result


def check(num: str, base: int) -> bool:
    minus_appeared = False

    for digit in num:
        if digit == "-":
            if minus_appeared:
                return False
            else:
                minus_appeared = True
        elif "0" <= digit <= "9":
            if int(digit) >= base:
                return False
        elif "A" <= digit <= "Z":
            if ord(digit) - ord("A") >= base - 10:
                return False
        elif "a" <= digit <= "z":
            if ord(digit) - ord("a") >= base - 10:
                return False
        else:
            return False
    return True
