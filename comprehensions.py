def main():
    # For Loops

    numbers = [1, 2, 3, 4, 5]

    squared_odds = []
    for n in numbers:
        if n % 2 == 1:
            squared_odds.append(n ** 2)

    print("squared odds: ", squared_odds)

    # List Comphrehension
    compre_squared_odds = [n ** 2 
                           for n in numbers 
                           if n % 2 == 1
    ]
    print("list comprehension: ", compre_squared_odds)

    # Since python variables act as references, lists of other lists are often
    # created, hence the importance of list comprehensions which seek to make
    # everything more readable

    squared_numbers = [
        n**2
        for n in numbers
    ]

    print("squared numbers(no filtering):", squared_numbers)

    # Set Comprehensions
    numbers = {1, 2, 3, 4, 5}

    squared_odds = set()
    for n in numbers:
        if n % 2 == 1:
            squared_odds.add(n**2)

    print("Set Loop:", squared_odds)

    compre_set_sqr_odds= {
        n ** 2
        for n in numbers
        if n % 2 == 1
    }

    print("Set Comprehension: ", compre_set_sqr_odds)

    # Dict Comprehensions

    from string import ascii_lowercase

    letter_positions = {}
    for n, letter in enumerate(ascii_lowercase, start=1):
        letter_positions[letter] = n;

    print("Dict Loop: ", letter_positions)

    compre_letter_positions = {
        letter: n
        for n, letter in enumerate(ascii_lowercase, start=1)
    }

    print("Dict Comprehension: ", compre_letter_positions)

    # Generator Comprehensions = Generator Expressions
    # Generators are lazy single-use iterables
    # Use if looping over a list exactly once

    numbers = [1, 2, 3, 4, 5]
    gen_sqr_nums = (n ** 2 for n in numbers)
    print(*gen_sqr_nums)

    # No len()
    # Can't index
    # Only loop over once
    # Generators are lazy

    new_nums = (n ** 3 for n in numbers)
    print(next(new_nums))
    print(next(new_nums))
    print(next(new_nums))

    new_nums = (n ** 4 for n in numbers)
    print(sum(new_nums))

    # Right away looping - most common practice
    print(sum(n ** 5 for n in numbers))

    sum(n ** 2 for n in numbers)

    # Comprehensions should only be used when making a list out of old lists
    # Don't overuse

if __name__ == "__main__":
    main()