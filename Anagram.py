import math
from collections import defaultdict


# Read file

with open("0098_words.txt", "r") as file:
    text = file.read()

words = [word.strip('"') for word in text.split(",")]

anagram_groups = defaultdict(list)

for word in words:
    key = "".join(sorted(word))
    anagram_groups[key].append(word)


# Only keep groups that contain multiple words
anagram_pairs = []

for group in anagram_groups.values():
    if len(group) > 1:
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                anagram_pairs.append((group[i], group[j]))


# Create squares for each word length 
# (Ex: A 3-letter word should have a square with 3 digits)

squares_by_length = {}

word_lengths = set(len(word) for word in words)

for length in word_lengths:

    # Smallest N-digit number
    min_number = 10 ** (length - 1)

    # Largest N-digit number
    max_number = 10 ** length - 1

    # Smallest integer whose square has N digits
    min_root = math.isqrt(min_number - 1) + 1

    # Largest integer whose square has N digits
    max_root = math.isqrt(max_number)

    squares = set()

    for root in range(min_root, max_root + 1):
        squares.add(root * root)

    squares_by_length[length] = squares


# Map words to squares

def create_mapping(word, square):
    digits = str(square)

    # Avoid leading zeros
    if digits[0] == "0":
        return None

    letter_to_digit = {}
    digit_to_letter = {}

    for letter, digit in zip(word, digits):

        # Same letter must always map to the same digit
        if letter in letter_to_digit:
            if letter_to_digit[letter] != digit:
                return None

        # Different letters cannot map to the same digit
        else:
            if digit in digit_to_letter:
                return None

            letter_to_digit[letter] = digit
            digit_to_letter[digit] = letter

    return letter_to_digit


# Create anagram pairs

results = []

for word1, word2 in anagram_pairs:

    length = len(word1)

    for square1 in squares_by_length[length]:

        # Map word1 -> square1
        mapping = create_mapping(word1, square1)

        if mapping is None:
            continue

        # Apply the same mapping to word2
        number2_string = ""

        for letter in word2:
            number2_string += mapping[letter]

        # Avoid leading 0's
        if number2_string[0] == "0":
            continue

        square2 = int(number2_string)

        # Check if the second number is also a square.
        root2 = math.isqrt(square2)

        if root2 * root2 == square2:

            results.append(
                (word1, square1, math.isqrt(square1),
                 word2, square2, root2)
            )


# Sort by the largest square in each pair
results.sort(key=lambda x: max(x[1], x[4]))

largest_square = 0

for word1, square1, root1, word2, square2, root2 in results:

    print(
        f"{word1} = {square1} = {root1}^2; "
        f"{word2} = {square2} = {root2}^2"
    )

    largest_square = max(largest_square, square1, square2)

print()
print("Largest square:", largest_square)