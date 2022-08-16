from decimal import Decimal
from math import inf, sqrt, pi

num_components = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "π"}
operators = {"+", "-", "*", "/", "(", ")", "√", "^", "%"}
valid_chars = num_components.union(operators)


# standardize the expression to the form that my algorithm can solve
# and check if there is some fatal errors
# This function only catches current error, later appearing errors are tackled later
# return vals: next_expression, changed, can_proceed
def standardize_and_check_error(expression: str) -> (str, bool, bool):
    # doesn't even have a number, have nothing to calculate
    if all(ord(c) < 48 or 57 < ord(c) and c != "π" for c in expression):
        return "Number needed error", True, False

    # have an invalid char?
    for i in range(len(expression)):
        if expression[i] not in valid_chars:
            return f"Invalid char error at position {i}", True, False

    # have problem with the num or positions of brackets?
    correct, error_idx = check_brackets(expression)
    if not correct:
        return f"Bracket error at position {error_idx}", True, False

    # have more operators than expected?
    correct, error_idx = check_num_of_operators(expression)
    if not correct:
        return f"Too many operators error at position {error_idx}", True, False

    next_expression, changed_1 = complement(expression)
    next_expression, changed_2 = convert_pi(next_expression)
    return next_expression, changed_1 or changed_2, True


# check if there are more operators than expected
# return vals: correct: error_idx
def check_num_of_operators(expression: str) -> (bool, int):
    allow_operator = False
    allow_negative_symbol = True
    allow_dot = False
    already_decimal = False

    for i in range(len(expression)):
        # some operators cannot be between two same brackets
        if expression[i] in ("(", ")"):
            if i <= len(expression) - 3:
                if expression[i + 2] == expression[i] and expression[i + 1] in ("+", "*", "/", "%", "^"):
                    return False, i

        # meet a digit:
        # can be before an operator
        # or before a negative number
        # or be part of a decimal
        if 48 <= ord(expression[i]) <= 57:
            allow_operator = True
            allow_negative_symbol = True
            if not already_decimal:
                allow_dot = True
        # meet a π:
        # can be before an operator
        # or before a negative number
        # Note that π is itself a single number
        elif expression[i] == "π":
            allow_operator = True
            allow_negative_symbol = True
        # meet a - :
        # can be an operator
        # or part of a negative number
        # can be before a decimal
        elif expression[i] == "-":
            if allow_operator:
                allow_operator = False
            elif allow_negative_symbol:
                allow_negative_symbol = False
            else:
                return False, i
            already_decimal = False
        # meet a +, *, /, %, ^
        # those can only be an operator
        # can be before a decimal
        if expression[i] in ("+", "*", "/", "%", "^"):
            if allow_operator:
                allow_operator = False
            else:
                return False, i
            already_decimal = False
        # meet a "."
        # must be part of a decimal
        if expression[i] == ".":
            if allow_dot:
                allow_dot = False
                already_decimal = False
            else:
                return False, i

    # some operators and the dot cannot be at the last position
    if expression[len(expression) - 1] in ("+", "-", "*", "/", "%", "^", "√", "."):
        return False, len(expression) - 1

    return True, -1


# add missed * before "("
# return vals: next_expression, changed
def complement(expression: str) -> (str, bool):
    next_expression = ""
    changed = False

    for i in range(len(expression) - 1):
        next_expression += expression[i]
        if 48 <= ord(expression[i]) <= 57 and expression[i + 1] == "(":
            next_expression += "*"
            changed = True
    next_expression += expression[-1]

    return next_expression, changed


# convert all the π's into actual numbers that can be used for calculation
# return vals: next_expression, changed
def convert_pi(expression: str) -> (str, bool):
    next_expression = ""
    changed = False
    for i in range(len(expression) - 1):
        is_pi = expression[i] == "π"
        is_num = is_pi or 48 <= ord(expression[i]) <= 57
        if is_pi:
            next_expression += str(pi)
            changed = True
        else:
            next_expression += expression[i]
        if is_num and expression[i + 1] in ("π", "("):
            next_expression += "*"
            changed = True
    if expression[-1] == "π":
        next_expression += str(pi)
        changed = True
    else:
        next_expression += expression[-1]

    return next_expression, changed


# check if the number and positions of left and right brackets are correct
# return vals: correct, error_idx
def check_brackets(expression: str) -> (bool, int):
    right_bracket_expect = 0
    for i in range(len(expression)):
        if expression[i] == "(":
            right_bracket_expect += 1
        elif expression[i] == ")":
            if right_bracket_expect == 0:
                return False, i
            right_bracket_expect -= 1

    if right_bracket_expect != 0:
        return False, len(expression) - 1
    else:
        return True, -1


# sometimes an expression has redundant zeros, like "0.100"
def remove_redundant_zeros(expression: str) -> str:
    if expression.find(".") == -1:
        return expression
    keep_idx = -1
    for i in range(len(expression) - 1, -1, -1):
        if expression[i] == "0":
            continue
        if expression[i] == ".":
            return expression[0: i]
        keep_idx = i
        break
    return expression[0: keep_idx + 1]


def interpret_only_add_subtract(expression: str) -> (str, bool):
    # recognize the first two numbers and one operator
    num_1 = expression[0]
    num_2 = ""
    operator = ""
    rest = ""
    for i in range(1, len(expression)):
        if expression[i] in num_components:
            num_1 += expression[i]
        else:
            operator = expression[i]
            num_2 = expression[i + 1]
            for j in range(i + 2, len(expression)):
                if expression[j] in num_components:
                    num_2 += expression[j]
                else:
                    rest = expression[j:]
                    break
            break

    # then additions and subtractions
    # careful of negative numbers
    if num_2 == "":
        return num_1, True
    else:
        num_1 = Decimal(num_1)
        num_2 = Decimal(num_2)

        # only addition and subtraction are possible here
        # other operations were considered and tackled before
        if operator == "+":
            changed_part = str(num_1 + num_2)
        else:
            changed_part = str(num_1 - num_2)
        changed_part = remove_redundant_zeros(changed_part)

    # construct the next expression and check if the calculation is finished
    next_expression = changed_part + rest
    return next_expression, check_if_finished(next_expression)


# check if the expression represents a final result
def check_if_finished(expression: str) -> bool:
    first_digit_qualified = expression[0] == "-" or 48 <= ord(expression[0]) <= 57
    other_digits_qualified = all(c in num_components for c in expression[1:])
    return first_digit_qualified and other_digits_qualified


# compare two non-negative numbers in strings
# return True if num_1 >= num_2
def compare(num_1: str, num_2: str) -> bool:
    if len(num_1) >= len(num_2) and num_1 >= num_2:
        return True
    return False


def interpret_bracket(expression: str, left_bracket_idx) -> (str, bool):
    right_bracket_need = 1
    for i in range(left_bracket_idx + 1, len(expression)):
        if expression[i] == "(":
            right_bracket_need += 1
            continue
        if expression[i] == ")":
            right_bracket_need -= 1
            if right_bracket_need == 0:
                left = ""
                if left_bracket_idx > 0:
                    left = expression[0: left_bracket_idx]
                right = ""
                if i < len(expression) - 1:
                    right = expression[i + 1: len(expression)]
                middle, middle_finished = interpret(expression[left_bracket_idx + 1: i])
                if middle_finished:
                    next_expression = left + middle + right
                    if left == right == "":
                        finished = True
                    else:
                        finished = False
                else:
                    next_expression = left + "(" + middle + ")" + right
                    finished = False

                return next_expression, finished


def interpret_power_and_sqrt(expression: str, idx: int) -> (str, bool):
    if expression[idx] == "^":
        power_idx = idx
        num_1, num_2, left_end_idx, right_start_idx = find_nums_for_operator(expression, power_idx)
        num_1 = Decimal(num_1)
        num_2 = Decimal(num_2)
        changed_part = str(num_1 ** num_2)
        next_expression = make_next_expression(expression, changed_part, left_end_idx, right_start_idx)

        return next_expression, check_if_finished(next_expression)
    else:
        sqrt_idx = idx
        while expression[sqrt_idx + 1] == "√":
            sqrt_idx += 1
        left_end_idx = sqrt_idx - 1
        right_start_idx = len(expression)
        num_2 = expression[sqrt_idx + 1]
        for i in range(sqrt_idx + 2, len(expression)):
            if expression[i] in num_components:
                num_2 += expression[i]
            else:
                right_start_idx = i
                break
        num_2 = Decimal(num_2)
        if num_2 < 0:
            error_msg = f"Sqrt a negative number error at position {sqrt_idx}"
            return error_msg, True
        changed_part = str(sqrt(num_2))
        if expression[left_end_idx] in num_components:
            changed_part = "*" + changed_part
        next_expression = make_next_expression(expression, changed_part, left_end_idx, right_start_idx)

        return next_expression, check_if_finished(next_expression)


def interpret_mul_div_mod(expression: str, idx: int) -> (str, bool):
    if expression[idx] == "*":
        mul_idx = idx
        num_1, num_2, left_end_idx, right_start_idx = find_nums_for_operator(expression, mul_idx)
        num_1 = Decimal(num_1)
        num_2 = Decimal(num_2)
        changed_part = str(num_1 * num_2)
        next_expression = make_next_expression(expression, changed_part, left_end_idx, right_start_idx)

        return next_expression, check_if_finished(next_expression)
    elif expression[idx] == "/":
        div_idx = idx
        num_1, num_2, left_end_idx, right_start_idx = find_nums_for_operator(expression, div_idx)
        num_1 = Decimal(num_1)
        num_2 = Decimal(num_2)
        if num_2 == 0:
            error_msg = f"Divided by 0 error at position {div_idx}"
            return error_msg, True
        changed_part = str(num_1 / num_2)
        next_expression = make_next_expression(expression, changed_part, left_end_idx, right_start_idx)

        return next_expression, check_if_finished(next_expression)
    else:
        mod_idx = idx
        num_1, num_2, left_end_idx, right_start_idx = find_nums_for_operator(expression, mod_idx)
        num_1 = Decimal(num_1)
        num_2 = Decimal(num_2)
        if num_2 == 0:
            error_msg = f"Mod by 0 error at position {mod_idx}"
            return error_msg, True
        changed_part = str(num_1 % num_2)
        next_expression = make_next_expression(expression, changed_part, left_end_idx, right_start_idx)

        return next_expression, check_if_finished(next_expression)


def get_min_valid_idx(idxs: tuple):
    min_valid_idx = inf
    for idx in idxs:
        if idx != -1:
            min_valid_idx = min(min_valid_idx, idx)

    return min_valid_idx


# for an expression, interpret what is the first step
# and get the new expression by executing the step
def interpret(expression: str) -> (str, bool):
    # if brackets exist, first eliminate them
    left_bracket_idx = expression.find("(")
    if left_bracket_idx != -1:
        return interpret_bracket(expression, left_bracket_idx)

    # then, eliminate ^ and √
    power_idx = expression.find("^")
    sqrt_idx = expression.find("√")
    idx = get_min_valid_idx((power_idx, sqrt_idx))
    if idx != inf:
        return interpret_power_and_sqrt(expression, idx)

    # then, eliminate *, /, and %
    mul_idx = expression.find("*")
    div_idx = expression.find("/")
    mod_idx = expression.find("%")
    idx = get_min_valid_idx((mul_idx, div_idx, mod_idx))
    if idx != inf:
        return interpret_mul_div_mod(expression, idx)

    # finally, only + and - remains, and eliminate them
    return interpret_only_add_subtract(expression)


def make_next_expression(expression: str, changed_part: str, left_end_idx: int, right_start_idx: int) -> str:
    changed_part = remove_redundant_zeros(changed_part)
    next_expression = ""
    if left_end_idx != -1:
        next_expression += expression[0: left_end_idx + 1]
    next_expression += changed_part
    if right_start_idx != len(expression):
        next_expression += expression[right_start_idx: len(expression)]

    return next_expression


# for operations like *, /, and ^
# return vals: num_1, num_2, left_start_idx, right_end_idx
def find_nums_for_operator(expression: str, op_idx: int) -> (str, str, int, int):
    print(expression, op_idx)
    num_1 = ""
    num_2 = expression[op_idx + 1]
    left_end_idx = -1
    right_start_idx = len(expression)

    for i in range(op_idx - 1, -1, -1):
        if expression[i] in num_components:
            continue
        elif expression[i] == "-":
            if i == 0 or expression[i - 1] not in num_components:
                left_end_idx = i - 1
                num_1 = expression[i: op_idx]
                break
            else:
                left_end_idx = i
                num_1 = expression[i + 1: op_idx]
                break
        else:
            left_end_idx = i
            num_1 = expression[i + 1: op_idx]
            break
    if num_1 == "":
        num_1 = expression[0: op_idx]

    for i in range(op_idx + 2, len(expression)):
        if expression[i] in num_components:
            num_2 += expression[i]
        else:
            right_start_idx = i
            break

    return num_1, num_2, left_end_idx, right_start_idx
