import logic.constants
import logic.exception

def convert_wff_to_suffix_expr(
    wff, 
    logic_op = logic.constants.LOGIC_OP_LIST, 
    left_paren = logic.constants.LEFT_PAREN, 
    right_paren = logic.constants.RIGHT_PAREN
):
    """
    Convert a Well-Formed Formula (WFF) from infix notation to suffix notation (Reverse Polish Notation).
    Uses the Shunting Yard algorithm for conversion.
    
    Args:
        wff: The well-formed formula to convert (string or list)
        logic_op: List of logic operators
        left_paren: Left parenthesis symbol
        right_paren: Right parenthesis symbol
    
    Returns:
        List representing the formula in suffix notation
    
    Raises:
        LogicExprError: If logic_op contains duplicates or formula is invalid
    """
    if wff == None:
        return None

    if type(wff) == str:
        wff = list(wff)
    if type(logic_op) == str:
        logic_op = list(logic_op)
    if len(set(logic_op)) < len(logic_op):
        raise logic.exception.LogicExprError("logic_op contains duplicates")

    candidate, finished = [], []

    for term in wff:
        if term in logic_op:
            while len(candidate) != 0 and candidate[-1] != left_paren and logic_op.index(term) >= logic_op.index(candidate[-1]):
                finished.append(candidate.pop())
            candidate.append(term)
        elif term == left_paren:
            candidate.append(term)
        elif term == right_paren:
            while len(candidate) != 0 and candidate[-1] != left_paren:
                finished.append(candidate.pop())
            if len(candidate) == 0:
                raise logic.exception.LogicExprError("invalid well formed formula")
            candidate.pop()
        else:
            finished.append(term)
    return finished + list(reversed(candidate))

def calc_suffix_expr_value(
    suffix_expr, 
    neg_logic_op = logic.constants.NEG_LOGIC_OP, 
    and_logic_op = logic.constants.AND_LOGIC_OP, 
    or_logic_op = logic.constants.OR_LOGIC_OP, 
    if_then_logic_op = logic.constants.IF_THEN_LOGIC_OP, 
    iff_logic_op = logic.constants.IFF_LOGIC_OP, 
    mask = 0
):
    """
    Evaluate a suffix expression (Reverse Polish Notation) using a stack-based approach.
    
    Args:
        suffix_expr: Expression in suffix notation to evaluate
        neg_logic_op, and_logic_op, or_logic_op, if_then_logic_op, iff_logic_op: Logic operators
        mask: Bitmask for operations (used for batch evaluation across multiple rows)
    
    Returns:
        Computed value of the suffix expression (integer or boolean)
    
    Raises:
        LogicExprError: If expression type is mixed or suffix expression is invalid
    """

    if suffix_expr == None:
        return None

    is_bool = any([type(term) == bool for term in suffix_expr])
    is_int = any([type(term) == int for term in suffix_expr])
    
    if is_bool and is_int:
        raise logic.exception.LogicExprError("suffix expression type abuse")
    
    if is_bool:
        mask = True
    
    suffix_expr = [int(term) if type(term) == bool else term for term in suffix_expr]
    
    NEG = lambda a: mask ^ a
    AND = lambda a, b: a & b
    OR = lambda a, b: a | b
    IF_THEN = lambda a, b: NEG(a) | b
    IFF = lambda a, b: IF_THEN(a, b) & IF_THEN(b, a)

    stack = []
    for term in suffix_expr:
        if type(term) == int:
            stack.append(term)
        elif term == neg_logic_op:
            stack, operand = stack[:-1], stack[-1:]
            stack.append(NEG(operand[0]))
        elif term == and_logic_op:
            stack, operand = stack[:-2], stack[-2:]
            stack.append(AND(operand[0], operand[1]))
        elif term == or_logic_op:
            stack, operand = stack[:-2], stack[-2:]
            stack.append(OR(operand[0], operand[1]))
        elif term == if_then_logic_op:
            stack, operand = stack[:-2], stack[-2:]
            stack.append(IF_THEN(operand[0], operand[1]))
        elif term == iff_logic_op:
            stack, operand = stack[:-2], stack[-2:]
            stack.append(IFF(operand[0], operand[1]))
        else:
            raise logic.exception.LogicExprError("invalid well formed formula suffix expression")        
    
    if len(stack) != 1:
        raise logic.exception.LogicExprError("invalid well formed formula suffix expression")
    
    return bool(stack[0]) if is_bool else stack[0]

def generate_rademacher_numbers(n):
    """
    Generate Rademacher numbers (binary patterns for truth table columns).
    Used for efficiently generating all combinations of truth values for n variables.
    
    Args:
        n: Number of variables
    
    Returns:
        List of Rademacher numbers as integers, one for each variable
    """

    length = 1 << n
    results = []
    
    for i in range(n):
        half_len = 1 << i
        ones = (1 << half_len) - 1
        unit = ones << half_len
        current_num = unit
        current_len = 1 << (i + 1)
    
        while current_len < length:
            current_num = (current_num << current_len) | current_num
            current_len <<= 1

        results.append(current_num)
        
    return results

def get_prop_var(
    wff, 
    logic_op = logic.constants.LOGIC_OP_LIST, 
    left_paren = logic.constants.LEFT_PAREN, 
    right_paren = logic.constants.RIGHT_PAREN
):
    """
    Extract and return all unique propositional variables from a WFF in sorted order.
    
    Args:
        wff: The well-formed formula (string or list)
        logic_op: List of logic operators
        left_paren: Left parenthesis symbol
        right_paren: Right parenthesis symbol
    
    Returns:
        Sorted list of propositional variables found in the formula
    """
    if wff == None:
        return None
    if type(wff) == str:
        wff = list(wff)
    return sorted(list(set([term for term in wff if type(term) == str and term not in set(logic_op + [left_paren, right_paren])])))

def get_truth_table(
    wff, 
    neg_logic_op = logic.constants.NEG_LOGIC_OP, 
    and_logic_op = logic.constants.AND_LOGIC_OP, 
    or_logic_op = logic.constants.OR_LOGIC_OP, 
    if_then_logic_op = logic.constants.IF_THEN_LOGIC_OP, 
    iff_logic_op = logic.constants.IFF_LOGIC_OP, 
    logic_op = logic.constants.LOGIC_OP_LIST, 
    left_paren = logic.constants.LEFT_PAREN, 
    right_paren = logic.constants.RIGHT_PAREN
):
    """
    Generate the complete truth table for a Well-Formed Formula (WFF).
    Each row contains boolean values for all variables and the formula result.
    
    Args:
        wff: The well-formed formula to evaluate
        neg_logic_op, and_logic_op, or_logic_op, if_then_logic_op, iff_logic_op: Logic operators
        logic_op: List of all logic operators
        left_paren, right_paren: Parenthesis symbols
    
    Returns:
        List of lists where each inner list represents one row of the truth table
        (one boolean for each variable, plus one for the formula result)
    
    Raises:
        LogicExprError: If operators are invalid or duplicated
    """
    if wff == None:
        return None

    if type(wff) == str:
        wff = list(wff)
    if type(logic_op) == str:
        logic_op = list(logic_op)
    if len(set(logic_op)) < len(logic_op):
        raise logic.exception.LogicExprError("logic_op contains duplicates")
    if set(logic_op) != set([neg_logic_op, and_logic_op, or_logic_op, if_then_logic_op, iff_logic_op]) - set([logic.constants.EMPTY_LOGIC_OP, None]):
        raise logic.exception.LogicExprError("logic_op is not a permutation of all valid operators")
    
    suffix_expr = convert_wff_to_suffix_expr(wff, logic_op, left_paren, right_paren)

    prop_var = get_prop_var(wff, logic_op, left_paren, right_paren)
    prop_var_count = len(prop_var)
    column_count = pow(2, prop_var_count)
    prop_instance = list(reversed(generate_rademacher_numbers(prop_var_count)))

    suffix_expr = [dict(zip(prop_var, prop_instance)).get(term, term) for term in suffix_expr]
    result = calc_suffix_expr_value(suffix_expr, neg_logic_op, and_logic_op, or_logic_op, if_then_logic_op, iff_logic_op, pow(2, column_count) - 1)

    return list(reversed([[char == '1' for char in "".join(chars)] for chars in zip(*[f"{term:b}".zfill(column_count) for term in prop_instance + [result]])]))
