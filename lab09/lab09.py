"""Lab 09: Calculator Interpreter"""


class Link:
    """Represents the built-in Link data structure in Scheme."""
    empty = ()

    def __init__(self, first, rest=empty):
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is Link.empty:
            return f'Link({self.first!r})'
        return f'Link({self.first!r}, {self.rest!r})'

    def __str__(self):
        result = '('
        while self.rest is not Link.empty:
            result += str(self.first) + ' '
            self = self.rest
        result += str(self.first) + ')'
        return result


nil = Link.empty


def map_link(f, s):
    """Map function f over linked list s.
    >>> square = lambda x: x * x
    >>> map_link(square, Link(1, Link(2, Link(3, nil))))
    Link(1, Link(4, Link(9, nil)))
    """
    if s is Link.empty:
        return s
    return Link(f(s.first), map_link(f, s.rest))


scheme_t = True   # Scheme's #t
scheme_f = False  # Scheme's #f

bindings = {}


def sum_link(args):
    total = 0
    while args is not nil:
        total += args.first
        args = args.rest
    return total


def sub_link(args):
    if args.rest is nil:
        return -args.first
    total = args.first
    args = args.rest
    while args is not nil:
        total -= args.first
        args = args.rest
    return total


def mul_link(args):
    total = 1
    while args is not nil:
        total *= args.first
        args = args.rest
    return total


def div_link(args):
    total = args.first
    args = args.rest
    while args is not nil:
        total /= args.first
        args = args.rest
    return total


def floor_div(args):
    """
    >>> floor_div(Link(100, Link(10, nil)))
    10
    >>> floor_div(Link(5, Link(3, nil)))
    1
    >>> floor_div(Link(1, Link(1, nil)))
    1
    >>> floor_div(Link(5, Link(2, nil)))
    2
    >>> floor_div(Link(23, Link(2, Link(5, nil))))
    2
    >>> calc_eval(Link("//", Link(4, Link(2, nil))))
    2
    >>> calc_eval(Link("//", Link(100, Link(2, Link(2, Link(2, Link(2, Link(2, nil))))))))
    3
    >>> calc_eval(Link("//", Link(100, Link(Link("+", Link(2, Link(3, nil))), nil))))
    20
    """
    result = args.first
    args = args.rest
    while args is not nil:
        result = result // args.first
        args = args.rest
    return result


def eval_and(expressions):
    """
    >>> calc_eval(Link("and", Link(1, nil)))
    1
    >>> calc_eval(Link("and", Link(False, Link("1", nil))))
    False
    >>> calc_eval(Link("and", Link(1, Link(Link("//", Link(5, Link(2, nil))), nil))))
    2
    >>> calc_eval(Link("and", Link(Link('+', Link(1, Link(1, nil))), Link(3, nil))))
    3
    >>> calc_eval(Link("and", Link(Link('-', Link(1, Link(0, nil))), Link(Link('/', Link(5, Link(2, nil))), nil))))
    2.5
    >>> calc_eval(Link("and", Link(0, Link(1, nil))))
    1
    >>> calc_eval(Link("and", nil))
    True
    """
    if expressions is nil:
        return True
    val = calc_eval(expressions.first)
    if val is scheme_f:
        return scheme_f
    if expressions.rest is nil:
        return val
    return eval_and(expressions.rest)


def eval_define(expressions):
    """
    >>> eval_define(Link("a", Link(1, nil)))
    'a'
    >>> eval_define(Link("b", Link(3, nil)))
    'b'
    >>> eval_define(Link("c", Link("a", nil)))
    'c'
    >>> calc_eval("c")
    1
    >>> calc_eval(Link("define", Link("d", Link("//", nil))))
    'd'
    >>> calc_eval(Link("d", Link(4, Link(2, nil))))
    2
    """
    symbol = expressions.first
    value = calc_eval(expressions.rest.first)
    bindings[symbol] = value
    return symbol


def calc_eval(exp):
    """
    >>> calc_eval(Link("define", Link("a", Link(1, nil))))
    'a'
    >>> calc_eval("a")
    1
    >>> calc_eval(Link("+", Link(1, Link(2, nil))))
    3
    """
    if isinstance(exp, Link):
        operator = calc_eval(exp.first)
        operands = exp.rest
        if exp.first == 'and':  # and expressions
            return eval_and(operands)
        elif exp.first == 'define':  # define expressions
            return eval_define(operands)
        else:  # Call expressions
            evaluated_operands = map_link(calc_eval, operands)
            return calc_apply(operator, evaluated_operands)
    elif exp in OPERATORS:   # Looking up procedures
        return OPERATORS[exp]
    elif isinstance(exp, int) or isinstance(exp, bool):   # Numbers and booleans
        return exp
    elif isinstance(exp, str) and exp in bindings:  # variable lookup
        return bindings[exp]


def calc_apply(operator, args):
    return operator(args)


OPERATORS = {
    '+': sum_link,
    '-': sub_link,
    '*': mul_link,
    '/': div_link,
    '//': floor_div,
}


if __name__ == '__main__':
    import doctest
    doctest.testmod()
