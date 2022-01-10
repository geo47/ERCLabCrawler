

def count_vowels(word):

    if not word:
        return -1

    if len(word) < 4:
        return -1

    if len(word) > 10:
        return -1

    vowel_counts = {}

    for vowel in "aeiou":
        count = word.lower().count(vowel)
        vowel_counts[vowel] = count

    counts = vowel_counts.values()
    total_vowels = sum(counts)
    return total_vowels


def check_most_vowels(string_1, string_2):
    vowels_count_1 = count_vowels(string_1)
    vowels_count_2 = count_vowels(string_2)

    if vowels_count_1 == -1 or vowels_count_2 == -1:
        return "error"

    if vowels_count_1 > vowels_count_2:
        return string_1

    if vowels_count_1 < vowels_count_2:
        return string_2

    if vowels_count_1 == vowels_count_2:
        return '=='

print(check_most_vowels('cake', 'special'))