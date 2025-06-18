from parsimonious.grammar import Grammar

try:
    grammar = Grammar(r'Test = "a"')
    print("Parsimonious loaded and grammar created successfully.")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")