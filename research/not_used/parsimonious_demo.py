from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

# 1. Define the Extended Grammar (including subtraction and division)
grammar = Grammar(r"""
    Expression = Term (("+" / "-") Term)*
    Term       = Factor (("*" / "/") Factor)*
    Factor     = Number/ "(" Expression ")"
    Number = ~"[0-9]+"
    +          = "+"
    -          = "-"
    * = "*"
    / = "/"
    (          = "("
    )          = ")"
    ws         = ~"\s*"
""")

# Explanation of the Grammar (Extended):
# - Expression: One or more Terms, possibly separated by
#   "+" or "-". This gives addition and subtraction the
#   same precedence and left-to-right associativity.
# - Term: One or more Factors, possibly separated by "*"
#   or "/". This gives multiplication and division the same
#   precedence (higher than addition/subtraction) and
#   left-to-right associativity.
# - Factor: Either a Number or a parenthesized Expression.
# - Number: One or more digits.
# - "+", "-", "*", "/", "(", ")": Literal matches for
#   operators and parentheses.
# - ws: Optional whitespace.

# 2. Create a NodeVisitor to evaluate the parse tree (Extended)
class ArithmeticEvaluator(NodeVisitor):
    def visit_Number(self, node, visited_children):
        return int(node.text)

    def visit_Factor(self, node, visited_children):
        return visited_children[0]

    def visit_Term(self, node, visited_children):
        result = visited_children[0]
        for i in range(1, len(visited_children), 2):
            operator = node.children[i].text
            right = visited_children[i + 1]
            if operator == "*":
                result *= right
            elif operator == "/":
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                result /= right
        return result

    def visit_Expression(self, node, visited_children):
        result = visited_children[0]
        for i in range(1, len(visited_children), 2):
            operator = node.children[i].text
            right = visited_children[i + 1]
            if operator == "+":
                result += right
            elif operator == "-":
                result -= right
        return result

    def generic_visit(self, node, visited_children):
        return visited_children or node.text

# 3. Parse and Evaluate Expressions (Extended)
expressions_to_test = [
    "10 + 2 * 3",
    "(10 + 2) * 3",
    "10 - 5 + 2",
    "20 / 4 * 3",
    "10 + 6 / 2 - 1",
    "(7 - 2) * (8 / 4)"
]

evaluator = ArithmeticEvaluator()

for expression_string in expressions_to_test:
    try:
        tree = grammar.parse(expression_string)
        result = evaluator.visit(tree)
        print(f"The result of '{expression_string}' is: {result}")
    except Exception as e:
        print(f"Parsing or evaluation error for '{expression_string}': {e}")
        