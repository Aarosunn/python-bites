class Transformer:
    def transform(self, my_list: list[str]) -> list[str]:
        return [word[::-1] for word in my_list]


def main() -> None:
    words = ["code", "python", "ai", "refactor", "bug"]
    print(words)

    length_map: dict[str, int] = {word: len(word) for word in words if len(word) > 4}
    print(length_map)

    for i, word in enumerate(words):
        print(f"{word} is {i} in the list")

    transformer = Transformer()
    new_words = transformer.transform(words)
    print(new_words)


if __name__ == "__main__":
    main()
