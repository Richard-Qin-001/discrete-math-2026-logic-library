// this code is a recursive descent parser for propositional logic formulas. It evaluates the formula for all possible combinations of variable assignments and prints the results.
// author: https://github.com/xiaoyuer5126

#include <cmath>
#include <cstring>
#include <iostream>

char formula[131072];
int pos = 0;

bool parse_equivalence(const char* s, const bool vals[]);
bool parse_implication(const char* s, const bool vals[]);
bool parse_disjunction(const char* s, const bool vals[]);
bool parse_conjunction(const char* s, const bool vals[]);
bool parse_negation(const char* s, const bool vals[]);
bool parse_primary(const char* s, const bool vals[]);

bool parse_equivalence(const char* s, const bool vals[]) {
    bool left = parse_implication(s, vals);
    while (s[pos] == '-') {
        pos++;
        bool right = parse_implication(s, vals);
        left = (left == right);
    }
    return left;
}

bool parse_implication(const char* s, const bool vals[]) {
    bool left = parse_disjunction(s, vals);
    while (s[pos] == '>') {
        pos++;
        bool right = parse_disjunction(s, vals);
        left = !left || right;
    }
    return left;
}

bool parse_disjunction(const char* s, const bool vals[]) {
    bool left = parse_conjunction(s, vals);
    while (s[pos] == '|') {
        pos++;
        bool right = parse_conjunction(s, vals);
        left = left || right;
    }
    return left;
}

bool parse_conjunction(const char* s, const bool vals[]) {
    bool left = parse_negation(s, vals);
    while (s[pos] == '&') {
        pos++;
        bool right = parse_negation(s, vals);
        left = left && right;
    }
    return left;
}

bool parse_negation(const char* s, const bool vals[]) {
    int num = 0;
    while (s[pos] == '!') {
        num++;
        pos++;
    }
    bool result = parse_primary(s, vals);
    if (num % 2) result = !result;
    return result;
}

bool parse_primary(const char* s, const bool vals[]) {
    if (s[pos] >= 'a' && s[pos] <= 'z') {
        return vals[s[pos++] - 'a'];
    } else {
        pos++;
        bool result = parse_equivalence(s, vals);
        pos++;
        return result;
    }
}

int main() {
    std::cin >> formula;
    int len = std::strlen(formula);

    bool seen[26] = {false};
    for (int i = 0; i < len; i++) {
        if (formula[i] >= 'a' && formula[i] <= 'z') seen[formula[i] - 'a'] = true;
    }
    int num = 0;
    char vars[26];
    for (int i = 0; i < 26; i++) {
        if (seen[i]) vars[num++] = 'a' + i;
    }

    int on = 0;
    int total = 1 << num;
    for (int i = 0; i < total; i++) {
        bool vals[26] = {false};
        int temp = i;
        for (int j = num - 1; j >= 0; j--) {
            vals[vars[j] - 'a'] = temp & 1;
            temp >>= 1;
        }

        pos = 0;
        bool result = parse_equivalence(formula, vals);
#ifndef NDEBUG
        std::cout << result;
#endif
    }

#ifndef NDEBUG
    std::cout << "\n";
#endif

    return 0;
}
