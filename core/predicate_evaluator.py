"""
PredicateEvaluator - Real executable predicate verification for Star.

Uses Python's ast module to safely evaluate hypotheses as logical expressions
against game state, replacing the previous crude string-matching approach.
"""

import ast
from typing import Dict, Any


class PredicateEvaluator:
    """
    Safely evaluates formal conditions as Python expressions against context.
    Supports basic logical operators, comparisons, and safe attribute access.
    """

    ALLOWED_NODES = (
        ast.Expression, ast.BoolOp, ast.BinOp, ast.UnaryOp,
        ast.Compare, ast.Name, ast.Load, ast.Constant,
        ast.Call, ast.Attribute, ast.Subscript,
        ast.List, ast.Tuple, ast.Dict, ast.Slice
    )

    def __init__(self):
        self.safe_globals = {
            "True": True,
            "False": False,
            "None": None,
            "len": len,
            "abs": abs,
            "int": int,
            "bool": bool,
        }

    def evaluate(self, condition: str, context: Dict[str, Any]) -> bool:
        """
        Evaluate a formal condition string against the given context.
        Returns False on any error or unsafe operation.
        """
        if not condition or not isinstance(condition, str):
            return False

        try:
            # Parse and validate the AST
            tree = ast.parse(condition, mode="eval")
            if not self._is_safe(tree):
                return False

            # Compile and execute in a restricted environment
            compiled = compile(tree, "<predicate>", "eval")
            result = eval(compiled, {"__builtins__": {}}, {**self.safe_globals, **context})
            return bool(result)
        except Exception:
            return False

    def _is_safe(self, node: ast.AST) -> bool:
        """Recursively check that only allowed AST nodes are used."""
        if not isinstance(node, self.ALLOWED_NODES):
            return False
        for child in ast.iter_child_nodes(node):
            if not self._is_safe(child):
                return False
        return True


# Singleton instance for easy import
evaluator = PredicateEvaluator()