#include <immintrin.h>

#include <algorithm>
#include <array>
#include <cctype>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stack>
#include <vector>

const size_t SIGMA = 26;
const size_t BLOCK_SIZE = 256;
const size_t STACK_SIZE = 65536;
const __m256i ALL_ONES_VEC = _mm256_set1_epi64x(-1);

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
        if (std::islower(c)) {
            postfix += c;
        } else if (c == '(') {
            ops.push_back(c);
        } else if (c == ')') {
            while (!ops.empty() && ops.back() != '(') {
                postfix += ops.back();
                ops.pop_back();
            }
            if (!ops.empty()) {
                ops.pop_back();
            }
        } else {
            while (!ops.empty() && ops.back() != '(') {
                int top_p = get_precedence(ops.back());
                int cur_p = get_precedence(c);
                if (c == '!' && top_p <= cur_p) {
                    break;
                }
                if (c != '!' && top_p < cur_p) {
                    break;
                }
                postfix += ops.back();
                ops.pop_back();
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
    for (const char c : expr) {
        if (std::islower(c)) vars.push_back(c);
    }
    std::sort(vars.begin(), vars.end());
    vars.erase(std::unique(vars.begin(), vars.end()), vars.end());

    std::string postfix = infix_to_postfix(std::move(expr));
    const std::size_t vars_count = vars.size();
    const std::uint64_t total_combinations = 1ULL << vars_count;

    std::array<__m256i, SIGMA> value{};
    std::array<std::array<std::uint64_t, 4>, SIGMA> lane_bits{};
    std::array<__m256i, STACK_SIZE> eval_stack;
    std::vector<uint8_t> results(total_combinations);

    for (std::uint64_t i = 0; i < total_combinations; i += BLOCK_SIZE) {
        for (auto& lanes : lane_bits) {
            lanes = {0, 0, 0, 0};
        }
        for (std::uint64_t j = i; j < i + BLOCK_SIZE && j < total_combinations; ++j) {
            for (int v = 0; v < vars_count; ++v) {
                const std::size_t bit_flag = (j >> (vars_count - 1 - v)) & 1ULL;
                if (!bit_flag) continue;
                const std::size_t offset = j - i;
                const std::size_t lane = offset >> 6;
                const std::size_t bit_pos = offset & 63ULL;
                lane_bits[vars[v] - 'a'][lane] |= 1ULL << bit_pos;
            }
        }
        for (size_t v = 0; v < SIGMA; ++v) {
            value[v] = _mm256_set_epi64x(
                static_cast<long long>(lane_bits[v][3]),
                static_cast<long long>(lane_bits[v][2]),
                static_cast<long long>(lane_bits[v][1]),
                static_cast<long long>(lane_bits[v][0]));
        }

        int top = -1;
        for (const char c : postfix) {
            if (std::islower(c)) {
                eval_stack[++top] = value[c - 'a'];
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
        alignas(32) std::uint64_t result_lanes[4];
        _mm256_store_si256(reinterpret_cast<__m256i*>(result_lanes), eval_stack[top]);
        for (size_t k = 0; k < BLOCK_SIZE && i + k < total_combinations; ++k) {
            const std::size_t lane = k >> 6;
            const std::size_t bit_pos = k & 63ULL;
            results[i + k] = (result_lanes[lane] >> bit_pos) & 1ULL;
        }
    }

#ifndef NDEBUG
    for (int i = 0; i < total_combinations; ++i) {
        std::cout << (int)results[i];
    }
    std::cout << "\n";
#endif

    return 0;
}
