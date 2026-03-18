import logic

wff = input()
print(*(logic.get_prop_var(wff) + [wff]))
for row in logic.get_truth_table(wff):
    print(" ".join([str(int(v)) for v in row]))
