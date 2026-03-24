import logic_lib

wff = input()
print(*(logic_lib.get_prop_var(wff) + [wff]))
for row in logic_lib.get_truth_table(wff):
    print(" ".join([str(int(v)) for v in row]))
