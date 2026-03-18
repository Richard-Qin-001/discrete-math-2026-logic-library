# Discrete Mathematics Logic Processor

A Python library for processing and analyzing propositional logic formulas, including truth table generation and conversion to normal forms.

## Project Structure

```
.
├── README.md                    # Project documentation
├── test.py                      # Test suite
└── logic/
    ├── __init__.py             # Package initialization
    ├── constants.py            # Logic operator constants and symbols
    ├── exception.py            # Custom exception definitions
    ├── primary_normal_form.py   # DNF and CNF conversion functions
    └── truth_table.py          # Truth table generation and evaluation
```

## Features

### Truth Table Generation
- Generate complete truth tables for well-formed formulas (WFF)
- Support for multiple logic operators: negation, conjunction, disjunction, implication, biconditional
- Extract propositional variables from formulas
- Evaluate formulas using suffix notation

### Normal Form Conversion
- **PDNF (Perfect Disjunctive Normal Form)**: Convert formulas to disjunction of conjunctions of literals
- **PCNF (Perfect Conjunctive Normal Form)**: Convert formulas to conjunction of disjunctions of literals
- Extract minterms and maxterms from truth tables
- Test for tautologies (formulas that are always true)

## Usage

### Import the Library
```python
import logic.constants
import logic.truth_table
import logic.primary_normal_form
```

### Generate a Truth Table
```python
from logic.truth_table import get_truth_table

# Define a formula: (A ∧ B) ∨ ¬C
formula = ['A', logic.constants.AND_LOGIC_OP, 'B', 
           logic.constants.OR_LOGIC_OP, 
           logic.constants.NEG_LOGIC_OP, 'C']

# Get the truth table
table = get_truth_table(formula)

# Each row contains boolean values for variables A, B, C, and the result
for row in table:
    print(row)
```

### Convert to Normal Forms
```python
from logic.primary_normal_form import convert_wff_to_pdnf, convert_wff_to_pcnf

formula = ['A', logic.constants.IF_THEN_LOGIC_OP, 'B']

# Convert to Perfect Disjunctive Normal Form
pdnf = convert_wff_to_pdnf(formula)

# Convert to Perfect Conjunctive Normal Form
pcnf = convert_wff_to_pcnf(formula)
```

### Test for Tautologies
```python
from logic.primary_normal_form import test_wff_is_always_true

# Test if a formula is always true (tautology)
formula = ['A', logic.constants.OR_LOGIC_OP, 
           logic.constants.NEG_LOGIC_OP, 'A']

is_tautology = test_wff_is_always_true(formula)
print(f"Is tautology: {is_tautology}")  # Output: True
```

## Constants

Available logic operators defined in `logic.constants`:

- `NEG_LOGIC_OP`: Negation (¬)
- `AND_LOGIC_OP`: Conjunction (∧)
- `OR_LOGIC_OP`: Disjunction (∨)
- `IF_THEN_LOGIC_OP`: Implication (→)
- `IFF_LOGIC_OP`: Biconditional (↔)
- `LEFT_PAREN`: Left parenthesis (
- `RIGHT_PAREN`: Right parenthesis )
- `LOGIC_OP_LIST`: List of all standard operators

## API Reference

### truth_table.py

- `convert_wff_to_suffix_expr()` - Convert infix WFF to suffix notation (RPN)
- `calc_suffix_expr_value()` - Evaluate suffix expressions using stack-based approach
- `generate_rademacher_numbers()` - Generate binary patterns for truth table columns
- `get_prop_var()` - Extract propositional variables from a formula
- `get_truth_table()` - Generate complete truth table for a WFF

### primary_normal_form.py

- `generate_minmaxterms_from_truth_table()` - Extract min/maxterms from truth table
- `generate_pdnf_minterms_from_truth_table()` - Get minterms for PDNF
- `generate_pcnf_maxterms_from_truth_table()` - Get maxterms for PCNF
- `convert_wff_to_pdnf()` - Convert WFF to Perfect Disjunctive Normal Form
- `convert_wff_to_pcnf()` - Convert WFF to Perfect Conjunctive Normal Form
- `test_wff_is_always_true()` - Test if formula is a tautology

## Testing

Run the test suite with:
```bash
python test.py
```

## Advanced Features

### Batch Evaluation
The library uses bitmasking techniques for efficient batch evaluation of formulas across multiple truth assignments, making it fast even for complex formulas with many variables.

### Custom Operators
All functions support custom logic operator symbols through optional parameters, allowing you to define your own syntax.

## Requirements

- Python 3.6+
- No external dependencies

## Notes

- Formulas must be well-formed (properly balanced parentheses, valid operator usage)
- Propositional variables are automatically extracted and sorted alphabetically
- The library validates operator consistency and prevents duplicate operators
