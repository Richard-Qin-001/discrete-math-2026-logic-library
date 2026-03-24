#include <immintrin.h>

#include <algorithm>
#include <array>
#include <cctype>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

const size_t SIGMA = 26;
const size_t BLOCK_SIZE = 256;
const size_t STACK_SIZE = 65536;
const __m256i ALL_ONES_VEC = _mm256_set1_epi64x(-1LL);

inline int get_precedence(const char op) {
    if (op == '!') return 4;
    if (op == '&') return 3;
    if (op == '|') return 2;
    if (op == '>') return 1;
    if (op == '-') return 0;
    return -1;
}

std::string infix_to_postfix(std::string&& infix) {
    std::string postfix, ops;
    for (const char c : infix) {
        if (std::isspace(c)) continue;
        if (std::islower(c)) {
            postfix += c;
        } else if (c == '(') {
            ops.push_back(c);
        } else if (c == ')') {
            while (!ops.empty() && ops.back() != '(') {
                postfix += ops.back();
                ops.pop_back();
            }
            if (!ops.empty()) ops.pop_back();
        } else {
            while (!ops.empty() && ops.back() != '(') {
                int top_p = get_precedence(ops.back());
                int cur_p = get_precedence(c);
                if (c == '!' ? top_p > cur_p : top_p >= cur_p) {
                    postfix += ops.back();
                    ops.pop_back();
                } else
                    break;
            }
            ops.push_back(c);
        }
    }
    while (!ops.empty()) {
        postfix += ops.back();
        ops.pop_back();
    }
    return postfix;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string expr;
    std::cin >> expr;

    std::vector<char> vars;
    for (const char c : expr)
        if (std::islower(c)) vars.push_back(c);
    std::sort(vars.begin(), vars.end());
    vars.erase(std::unique(vars.begin(), vars.end()), vars.end());

    std::string postfix = infix_to_postfix(std::move(expr));
    const size_t vars_count = vars.size();
    const uint64_t total_combinations = 1ULL << vars_count;

    alignas(64) __m256i precomputed_masks[SIGMA];
    for (int v = 0; v < vars_count; ++v) {
        int k = vars_count - 1 - v;
        if (k < 8) {
            alignas(64) uint64_t raw[4] = {0};
            for (int bit = 0; bit < 256; ++bit) {
                if ((bit >> k) & 1) raw[bit >> 6] |= (1ULL << (bit & 63));
            }
            precomputed_masks[v] = _mm256_load_si256((__m256i*)raw);
        }
    }
    
    std::vector<uint8_t> results(total_combinations);
    std::array<__m256i, STACK_SIZE> eval_stack;
    std::array<__m256i, SIGMA> var_values;

    for (uint64_t i = 0; i < total_combinations; i += BLOCK_SIZE) {
        for (int v = 0; v < vars_count; ++v) {
            char c = vars[v];
            int k = vars_count - 1 - v;
            if (k >= 8) {
                var_values[c - 'a'] = ((i >> k) & 1) ? ALL_ONES_VEC : _mm256_setzero_si256();
            } else {
                var_values[c - 'a'] = precomputed_masks[v];
            }
        }

        int top = -1;
        for (const char c : postfix) {
            if (std::islower(c)) {
                eval_stack[++top] = var_values[c - 'a'];
            } else if (c == '!') {
                eval_stack[top] = _mm256_xor_si256(eval_stack[top], ALL_ONES_VEC);
            } else {
                __m256i right = eval_stack[top--];
                __m256i left = eval_stack[top];
                if (c == '&') {
                    eval_stack[top] = _mm256_and_si256(left, right);
                } else if (c == '|') {
                    eval_stack[top] = _mm256_or_si256(left, right);
                } else if (c == '>') {
                    __m256i not_left = _mm256_andnot_si256(left, ALL_ONES_VEC);
                    eval_stack[top] = _mm256_or_si256(not_left, right);
                } else if (c == '-') {
                    __m256i xor_lr = _mm256_xor_si256(left, right);
                    eval_stack[top] = _mm256_xor_si256(xor_lr, ALL_ONES_VEC);
                }
            }
        }

        alignas(64) uint64_t out_raw[4];
        _mm256_store_si256((__m256i*)out_raw, eval_stack[0]);
        for (size_t k = 0; k < BLOCK_SIZE && (i + k) < total_combinations; ++k) {
            results[i + k] = (out_raw[k >> 6] >> (k & 63)) & 1ULL;
        }
    }

#ifndef NDEBUG
    for (uint8_t res : results) std::cout << (int)res;
    std::cout << "\n";
#endif

    return 0;
}
