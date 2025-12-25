import ast


class ExprEvaluator(ast.NodeVisitor):
    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_BinOp(self, node):
        if type(node.op) == ast.Mult:
            return self.visit(node.left) * self.visit(node.right)
        elif type(node.op) == ast.Add:
            return self.visit(node.left) + self.visit(node.right)
        elif type(node.op) == ast.Div:
            return self.visit(node.left) + self.visit(node.right)
        elif type(node.op) == ast.Pow:
            return self.visit(node.left) + self.visit(node.right)

    def visit_Constant(self, node):
        return node.value


def solve1(data: list[str]):
    evaluator = ExprEvaluator()
    res = 0
    for line in data:
        # Just to hack the operator precedence
        line = line.replace("+", "/")
        tree = ast.parse(line, mode="eval")
        res += evaluator.visit(tree)
    print(res)


def solve2(data: list[str]):
    evaluator = ExprEvaluator()
    res = 0
    for line in data:
        # Just to hack the operator precedence
        line = line.replace("+", "**")
        tree = ast.parse(line, mode="eval")
        res += evaluator.visit(tree)
    print(res)
