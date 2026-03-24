LOWER_LETTERS = "abcdefghijklmnopqrstuvwxyz"
UPPER_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERS = LOWER_LETTERS + UPPER_LETTERS

NEG_LOGIC_OP = '!'
AND_LOGIC_OP = '&'
OR_LOGIC_OP = '|'
IF_THEN_LOGIC_OP = '>'
IFF_LOGIC_OP = '-'
EMPTY_LOGIC_OP = ""

LOGIC_OP_TYPES = 5
LOGIC_OP_LIST = [NEG_LOGIC_OP, AND_LOGIC_OP, OR_LOGIC_OP, IF_THEN_LOGIC_OP, IFF_LOGIC_OP]
LOGIC_OP = "".join(LOGIC_OP_LIST)

LEFT_PAREN = '('
RIGHT_PAREN = ')'
PARENS_LIST = [LEFT_PAREN, RIGHT_PAREN]
PARENS = "".join(PARENS_LIST)

class LogicExprError(Exception):
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return super().__str__()

def convert_wff_to_suffix_expr(
    wff, 
    logic_op = LOGIC_OP_LIST, 
    left_paren = LEFT_PAREN, 
    right_paren = RIGHT_PAREN
):

    if wff == None:
        return None

    if type(wff) == str:
        wff = list(wff)
    if type(logic_op) == str:
        logic_op = list(logic_op)
    if len(set(logic_op)) < len(logic_op):
        raise LogicExprError("logic_op contains duplicates")

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
                raise LogicExprError("invalid well formed formula")
            candidate.pop()
        else:
            finished.append(term)
    return finished + list(reversed(candidate))

def calc_suffix_expr_value(
    suffix_expr, 
    neg_logic_op = NEG_LOGIC_OP, 
    and_logic_op = AND_LOGIC_OP, 
    or_logic_op = OR_LOGIC_OP, 
    if_then_logic_op = IF_THEN_LOGIC_OP, 
    iff_logic_op = IFF_LOGIC_OP, 
    mask = 0
):

    if suffix_expr == None:
        return None

    is_bool = any([type(term) == bool for term in suffix_expr])
    is_int = any([type(term) == int for term in suffix_expr])
    
    if is_bool and is_int:
        raise LogicExprError("suffix expression type abuse")
    
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
            raise LogicExprError("invalid well formed formula suffix expression")        
    
    if len(stack) != 1:
        raise LogicExprError("invalid well formed formula suffix expression")
    
    return bool(stack[0]) if is_bool else stack[0]

def generate_rademacher_numbers(n):
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
    logic_op = LOGIC_OP_LIST, 
    left_paren = LEFT_PAREN, 
    right_paren = RIGHT_PAREN
):
    if wff == None:
        return None
    if type(wff) == str:
        wff = list(wff)
    return sorted(list(set([term for term in wff if type(term) == str and term not in set(logic_op + [left_paren, right_paren])])))

def get_truth_table(
    wff, 
    neg_logic_op = NEG_LOGIC_OP, 
    and_logic_op = AND_LOGIC_OP, 
    or_logic_op = OR_LOGIC_OP, 
    if_then_logic_op = IF_THEN_LOGIC_OP, 
    iff_logic_op = IFF_LOGIC_OP, 
    logic_op = LOGIC_OP, 
    left_paren = LEFT_PAREN, 
    right_paren = RIGHT_PAREN
):

    if wff == None:
        return None

    if type(wff) == str:
        wff = list(wff)
    if type(logic_op) == str:
        logic_op = list(logic_op)
    if len(set(logic_op)) < len(logic_op):
        raise LogicExprError("logic_op contains duplicates")
    if set(logic_op) != set([neg_logic_op, and_logic_op, or_logic_op, if_then_logic_op, iff_logic_op]) - set([EMPTY_LOGIC_OP, None]):
        raise LogicExprError("logic_op is not a permutation of all valid operators")
    
    suffix_expr = convert_wff_to_suffix_expr(wff, logic_op, left_paren, right_paren)

    prop_var = sorted(list(set([term for term in wff if type(term) == str and term not in set(logic_op + [left_paren, right_paren])])))
    prop_var_count = len(prop_var)
    column_count = pow(2, prop_var_count)
    prop_instance = list(reversed(generate_rademacher_numbers(prop_var_count)))

    suffix_expr = [dict(zip(prop_var, prop_instance)).get(term, term) for term in suffix_expr]
    result = calc_suffix_expr_value(suffix_expr, neg_logic_op, and_logic_op, or_logic_op, if_then_logic_op, iff_logic_op, pow(2, column_count) - 1)

    return list(reversed([[char == '1' for char in "".join(chars)] for chars in zip(*[f"{term:b}".zfill(column_count) for term in prop_instance + [result]])]))

def generate_minmaxterms_from_truth_table(
    table, 
    target
):
    maxterms = []
    for v in table:
        if v[-1] == target:
            maxterms.append(int("".join(map(str, map(int, v[:-1]))), 2))
    return maxterms

def generate_pdnf_minterms_from_truth_table(table):
    return generate_minmaxterms_from_truth_table(table, target=True)

def generate_pcnf_maxterms_from_truth_table(table):
    return generate_minmaxterms_from_truth_table(table, target=False)

def convert_wff_to_pdnf(
    wff, 
    neg_logic_op = NEG_LOGIC_OP, 
    and_logic_op = AND_LOGIC_OP, 
    or_logic_op = OR_LOGIC_OP, 
    if_then_logic_op = IF_THEN_LOGIC_OP, 
    iff_logic_op = IFF_LOGIC_OP, 
    logic_op = LOGIC_OP_LIST, 
    left_paren = LEFT_PAREN, 
    right_paren = RIGHT_PAREN
):
    table = get_truth_table(wff, neg_logic_op, and_logic_op, or_logic_op, if_then_logic_op, iff_logic_op, logic_op, left_paren, right_paren)
    maxterms = generate_pcnf_maxterms_from_truth_table(table)

    prop_var = get_prop_var(wff, logic_op, left_paren, right_paren)
    prop_var_count = len(prop_var)

    pcnf = []
    for v in maxterms:
        pcnf.append(left_paren)
        for i, c in enumerate(prop_var):
            if ((v >> (prop_var_count - 1 - i)) & 1) == False:
                pcnf.append(neg_logic_op)
            pcnf.append(c)
            pcnf.append(and_logic_op)
        pcnf.pop()
        pcnf.append(right_paren)
        pcnf.append(or_logic_op)

    return pcnf[:-1]

def convert_wff_to_pcnf(
    wff, 
    neg_logic_op = NEG_LOGIC_OP, 
    and_logic_op = AND_LOGIC_OP, 
    or_logic_op = OR_LOGIC_OP, 
    if_then_logic_op = IF_THEN_LOGIC_OP, 
    iff_logic_op = IFF_LOGIC_OP, 
    logic_op = LOGIC_OP_LIST, 
    left_paren = LEFT_PAREN, 
    right_paren = RIGHT_PAREN
):
    table = get_truth_table(wff, neg_logic_op, and_logic_op, or_logic_op, if_then_logic_op, iff_logic_op, logic_op, left_paren, right_paren)
    minterms = generate_pcnf_maxterms_from_truth_table(table)

    prop_var = get_prop_var(wff, logic_op, left_paren, right_paren)
    prop_var_count = len(prop_var)

    pcnf = []
    for v in minterms:
        pcnf.append(left_paren)
        for i, c in enumerate(prop_var):
            if ((v >> (prop_var_count - 1 - i)) & 1) == True:
                pcnf.append(neg_logic_op)
            pcnf.append(c)
            pcnf.append(or_logic_op)
        pcnf.pop()
        pcnf.append(right_paren)
        pcnf.append(and_logic_op)

    return pcnf[:-1]

wff = "|".join(['(' + term + ')' for term in input().split('|')])
print("|".join([f"m{term}" for term in generate_pdnf_minterms_from_truth_table(get_truth_table(wff))]))
