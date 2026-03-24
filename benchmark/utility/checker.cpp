#include <iostream>
#include <string>
#include <stack>
#include <cctype>

bool is_binary_op(char c) {
    return c == '&' || c == '|' || c == '>' || c == '-';
}

bool is_legal_wff(const std::string& expr) {
    if (expr.empty()) return false;

    std::stack<char> parentheses;
    int n = expr.length();
    
    int last_type = 0; 

    for (int i = 0; i < n; ++i) {
        char c = expr[i];
        if (std::isspace(c)) continue;

        if (std::islower(c)) {
            if (last_type == 1 || last_type == 5) return false;
            last_type = 1;
        } else if (c == '(') {
            if (last_type == 1 || last_type == 5) return false;
            parentheses.push('(');
            last_type = 4;
        } else if (c == ')') {
            if (parentheses.empty() || last_type == 2 || last_type == 3 || last_type == 4) return false;
            parentheses.pop();
            last_type = 5;
        } else if (c == '!') {
            if (last_type == 1 || last_type == 5) return false;
            last_type = 3;
        } else if (is_binary_op(c)) {
            if (last_type == 0 || last_type == 2 || last_type == 3 || last_type == 4) return false;
            last_type = 2;
        } else {
            return false;
        }
    }

    return parentheses.empty() && (last_type == 1 || last_type == 5);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string input;
    std::cin >> input;

    bool result = is_legal_wff(input);
    std::cout << result << "\n";
    return !result;
}
