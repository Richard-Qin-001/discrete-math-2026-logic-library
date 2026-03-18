import logic.constants
import logic.truth_table

def generate_minmaxterms_from_truth_table(
    table, 
    target
):
    """
    Extract min/maxterms from a truth table based on a target output value.
    
    Args:
        table: Truth table with rows ending in boolean values
        target: Boolean value to match (True for minterms, False for maxterms)
    
    Returns:
        List of decimal representations of matching rows' input combinations
    """
    maxterms = []
    for v in table:
        if v[-1] == target:
            maxterms.append(int("".join(map(str, map(int, v[:-1]))), 2))
    return maxterms

def generate_pdnf_minterms_from_truth_table(table):
    """
    Generate minterms for Perfect Disjunctive Normal Form (PDNF).
    
    Args:
        table: Truth table with boolean outputs
    
    Returns:
        List of minterms (rows where output is True)
    """
    return generate_minmaxterms_from_truth_table(table, target=True)

def generate_pcnf_maxterms_from_truth_table(table):
    """
    Generate maxterms for Perfect Conjunctive Normal Form (PCNF).
    
    Args:
        table: Truth table with boolean outputs
    
    Returns:
        List of maxterms (rows where output is False)
    """
    return generate_minmaxterms_from_truth_table(table, target=False)

def convert_wff_to_pdnf(
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
    Convert a Well-Formed Formula (WFF) to Perfect Disjunctive Normal Form (PDNF).
    PDNF is a disjunction (OR) of conjunctions (AND) of literals representing all True cases.
    
    Args:
        wff: The well-formed formula to convert
        neg_logic_op, and_logic_op, or_logic_op, if_then_logic_op, iff_logic_op: Logic operators
        logic_op: List of all logic operators
        left_paren, right_paren: Parenthesis symbols
    
    Returns:
        List representing the formula in PDNF
    """
    table = logic.truth_table.get_truth_table(wff, 
                            neg_logic_op, 
                            and_logic_op, 
                            or_logic_op, 
                            if_then_logic_op, 
                            iff_logic_op, 
                            logic_op, 
                            left_paren, 
                            right_paren)
    maxterms = generate_pcnf_maxterms_from_truth_table(table)

    prop_var = logic.truth_table.get_prop_var(wff, logic_op, left_paren, right_paren)
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
    Convert a Well-Formed Formula (WFF) to Perfect Conjunctive Normal Form (PCNF).
    PCNF is a conjunction (AND) of disjunctions (OR) of literals representing all False cases.
    
    Args:
        wff: The well-formed formula to convert
        neg_logic_op, and_logic_op, or_logic_op, if_then_logic_op, iff_logic_op: Logic operators
        logic_op: List of all logic operators
        left_paren, right_paren: Parenthesis symbols
    
    Returns:
        List representing the formula in PCNF
    """
    table = logic.truth_table.get_truth_table(wff, 
                                        neg_logic_op, 
                                        and_logic_op, 
                                        or_logic_op, 
                                        if_then_logic_op, 
                                        iff_logic_op, 
                                        logic_op, 
                                        left_paren, 
                                        right_paren)

    minterms = generate_pcnf_maxterms_from_truth_table(table)

    prop_var = logic.truth_table.get_prop_var(wff, logic_op, left_paren, right_paren)
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

def test_wff_is_always_true(
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
    Test whether a Well-Formed Formula (WFF) is a tautology (always true).
    
    Args:
        wff: The well-formed formula to test
        neg_logic_op, and_logic_op, or_logic_op, if_then_logic_op, iff_logic_op: Logic operators
        logic_op: List of all logic operators
        left_paren, right_paren: Parenthesis symbols
    
    Returns:
        True if the formula is always true (tautology), False otherwise
    """
    return all([v[-1] == True for v in logic.truth_table.get_truth_table(wff, 
                                                       neg_logic_op, 
                                                       and_logic_op, 
                                                       or_logic_op, 
                                                       if_then_logic_op, 
                                                       iff_logic_op, 
                                                       logic_op, 
                                                       left_paren, 
                                                       right_paren)])
