class RuleMutator:
    """
    Applies various mutation rules to a given word to generate potential password candidates.
    """
    def __init__(self):
        self.rules = [
            self._append_numbers,
            self._prepend_numbers,
            self._capitalize_first,
            self._toggle_case,
            self._leet_speak,
            self._append_symbols,
            self._duplicate_word,
            self._reverse_word,
        ]

    def apply_rules(self, word):
        mutations = set()
        mutations.add(word) # Always include the original word
        for rule_func in self.rules:
            mutations.update(rule_func(word))
        return list(mutations)

    def _append_numbers(self, word):
        return [f"{word}{i}" for i in range(10)] + \
               [f"{word}{i}{i}" for i in range(10)] + \
               [f"{word}123", f"{word}2023", f"{word}2024"]

    def _prepend_numbers(self, word):
        return [f"{i}{word}" for i in range(10)] + \
               [f"123{word}", f"2023{word}", f"2024{word}"]

    def _capitalize_first(self, word):
        return [word.capitalize()]

    def _toggle_case(self, word):
        return [word.lower(), word.upper()]

    def _leet_speak(self, word):
        # Basic leet speak substitutions
        leet_map = {
            'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 's': ['5', '$'],
            't': ['7'], 'A': ['4', '@'], 'E': ['3'], 'I': ['1', '!'], 'O': ['0'], 'S': ['5', '$'],
            'T': ['7']
        }
        mutated_words = {word}
        for char, substitutions in leet_map.items():
            new_mutations = set()
            for current_word in mutated_words:
                if char in current_word:
                    for sub in substitutions:
                        new_mutations.add(current_word.replace(char, sub))
            mutated_words.update(new_mutations)
        return list(mutated_words)

    def _append_symbols(self, word):
        return [f"{word}!", f"{word}@", f"{word}#", f"{word}$", f"{word}%", f"{word}^", f"{word}&", f"{word}*"]

    def _duplicate_word(self, word):
        return [f"{word}{word}"]

    def _reverse_word(self, word):
        return [word[::-1]]

if __name__ == "__main__":
    mutator = RuleMutator()
    test_word = "password"
    print(f"Original word: {test_word}")
    mutations = mutator.apply_rules(test_word)
    print("Mutations:")
    for m in mutations:
        print(m)
    print(f"Total mutations: {len(mutations)}")

    test_word_2 = "test"
    print(f"\nOriginal word: {test_word_2}")
    mutations_2 = mutator.apply_rules(test_word_2)
    print("Mutations:")
    for m in mutations_2:
        print(m)
    print(f"Total mutations: {len(mutations_2)}")
