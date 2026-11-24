import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path


def signed_weight(value):
    value = abs(value)
    weight = 0
    while value:
        if value % 2:
            digit = 2 - value % 4
            value -= digit
            weight += 1
        value //= 2
    return weight


@lru_cache(None)
def frid_cost(length):
    if length == 0:
        return 0
    quotient, residue = divmod(length, 4)
    if residue == 0:
        return frid_cost(quotient)
    if residue == 1:
        return frid_cost(quotient) + 1
    if residue == 2:
        return min(frid_cost(quotient), frid_cost(quotient + 1)) + 2
    return frid_cost(quotient + 1) + 1


def finite_minima(bound):
    word = [position.bit_count() % 2 for position in range(bound)]
    weights = [signed_weight(position) for position in range(bound + 1)]
    ordinary = [0]
    combined = [0]
    previous_pal = bytearray(bound + 1)
    previous_anti = bytearray(bound + 1)
    allowed_cuts = 0
    predicate_checks = 0
    first_sharp = {}
    first_equal = {}
    for end in range(1, bound + 1):
        palindrome = bytearray(bound + 1)
        antipalindrome = bytearray(bound + 1)
        ordinary_best = end
        combined_best = end
        for start in range(end - 1, -1, -1):
            length = end - start
            palindrome[start] = word[start] == word[end - 1] and (
                length <= 2 or previous_pal[start + 1]
            )
            antipalindrome[start] = word[start] != word[end - 1] and (
                length == 2 or length > 2 and previous_anti[start + 1]
            )
            if end <= 128:
                substring = word[start:end]
                assert bool(palindrome[start]) == (substring == substring[::-1])
                assert bool(antipalindrome[start]) == (
                    substring == [1 - letter for letter in substring[::-1]]
                )
                predicate_checks += 2
            if palindrome[start]:
                ordinary_best = min(ordinary_best, ordinary[start] + 1)
            if palindrome[start] or antipalindrome[start]:
                combined_best = min(combined_best, combined[start] + 1)
                assert weights[end] <= weights[start] + 1, (start, end)
                allowed_cuts += 1
        ordinary.append(ordinary_best)
        combined.append(combined_best)
        assert combined_best == weights[end], end
        assert combined_best <= ordinary_best <= 2 * combined_best, end
        assert ordinary_best == frid_cost(end), end
        if ordinary_best == combined_best:
            assert end >= (2 * 4 ** (combined_best - 1) + 1) // 3
        if end <= 128:
            prefix = word[:end]
            power_of_two = end & (end - 1) == 0
            even_exponent = (end.bit_length() - 1) % 2 == 0
            assert (prefix == prefix[::-1]) == (power_of_two and even_exponent)
            assert (prefix == [1 - letter for letter in prefix[::-1]]) == (
                power_of_two and not even_exponent
            )
        if ordinary_best == 2 * combined_best:
            first_sharp.setdefault(combined_best, end)
        if ordinary_best == combined_best:
            first_equal.setdefault(combined_best, end)
        previous_pal = palindrome
        previous_anti = antipalindrome
    values = [[index, ordinary[index], combined[index]] for index in range(bound + 1)]
    for cost, length in first_equal.items():
        assert length == (2 * 4 ** (cost - 1) + 1) // 3
    return {
        'bound': bound,
        'arithmetic': 'exact integers',
        'intervals_examined': bound * (bound + 1) // 2,
        'allowed_cuts_checked': allowed_cuts,
        'direct_predicate_comparisons': predicate_checks,
        'prefix_values_sha256': hashlib.sha256(
            json.dumps(values, separators=(',', ':')).encode()
        ).hexdigest(),
        'sharp_first_occurrences_in_window': first_sharp,
        'equal_first_occurrences_in_window': first_equal,
    }


def other_checks(bound):
    source_sharp = [2, 10, 118, 630, 7542, 40310, 482678, 2579830, 30891382]
    sharp_rows = []
    for cost, length in enumerate(source_sharp, 1):
        assert signed_weight(length) == cost
        assert frid_cost(length) == 2 * cost
        sharp_rows.append([length, 2 * cost, cost])
    source_equal = []
    length = 1
    for cost in range(1, 15):
        assert signed_weight(length) == cost
        assert frid_cost(length) == cost
        source_equal.append([length, cost, cost])
        length = 4 * length - 1
    for length in range(100001):
        assert signed_weight(length) == (length ^ (3 * length)).bit_count()
        assert frid_cost(64 * length + 10) == frid_cost(length) + 4
        assert signed_weight(64 * length + 10) == signed_weight(length) + 2
    for base in [0, 2]:
        length = base
        for index in range(32):
            expected = 2 * index + (1 if base == 2 else 0)
            assert signed_weight(length) == expected
            assert frid_cost(length) == 2 * expected
            length = 64 * length + 10
    factor = [position.bit_count() % 2 for position in range(1, 7)]
    assert factor == [1, 1, 0, 1, 0, 0]
    assert factor == [1 - letter for letter in factor[::-1]]
    assert factor != factor[::-1]
    for cut in range(1, len(factor)):
        assert not (
            factor[:cut] == factor[:cut][::-1]
            and factor[cut:] == factor[cut:][::-1]
        )
    assert [1, 1] + [0, 1, 0] + [0] == factor
    return {
        'table_1_values_from_frid_and_signed_formula': source_sharp,
        'table_1_rows': sharp_rows,
        'table_2_rows': source_equal,
        'table_values_scope': 'word minima through the stated window; recurrence evaluations beyond it',
        'first_equal_cost_formula': '(2 * 4 ** (k - 1) + 1) // 3 for k >= 1',
        'first_equal_cost_formula_scope': 'written proof for all k; actual word checks within the stated window',
        'general_first_sharp_occurrence_formula': 'not established',
        'signed_weight_xor_formula_test_domain': '0 <= n <= 100000',
        'prefix_type_classification_direct_test_domain': '1 <= n <= 128',
        'affine_identity_test_domain': '0 <= n <= 100000',
        'attaining_family_members_checked_per_base': 32,
        'shifted_factor': {'start': 1, 'length': 6, 'word': '110100', 'ordinary': 3, 'combined': 1},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bound', type=int, default=8192)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.bound < 128 or args.bound > 16384:
        parser.error('Choose an exact word-check bound between 128 and 16384.')
    result = {'schema_version': 1, 'status': 'pass', 'word_minima': finite_minima(args.bound),
              'additional_exact_checks': other_checks(args.bound)}
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
