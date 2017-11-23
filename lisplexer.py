"""Lexer and Parser for LispFuck."""
import ox
import click
import pprint

tokens = [
    'OPEN_PARANTHESIS',
    'CLOSE_PARANTHESIS',
    'TEXT',
    'DIGITS',
    'ignore_NEWLINE',
    'ignore_COMMENT',
]

lexer_rules = [
    ('OPEN_PARANTHESIS', r'\('),
    ('CLOSE_PARANTHESIS', r'\)'),
    ('TEXT', r'[-a-zA-Z]+'),
    ('DIGITS', r'\d+'),
    ('ignore_NEWLINE', r'\s+'),
    ('ignore_COMMENT', r';[^\n]*'),
]

parser_rules = [
    ('block : OPEN_PARANTHESIS CLOSE_PARANTHESIS', lambda x, y: '()'),
    ('block : OPEN_PARANTHESIS expr CLOSE_PARANTHESIS', lambda x, y, z: y),
    ('atom : TEXT', lambda x: x),
    ('atom : DIGITS', lambda x: x),
    ('expr : atom expr', lambda x, y: (x,) + y),
    ('expr : atom', lambda x: (x,)),
    ('atom : block', lambda x: x),
]

lexer = ox.make_lexer(lexer_rules)
parser = ox.make_parser(parser_rules, tokens)


@click.command()
@click.argument('lispfcktree', type=click.File('r'))
def ast(lispfcktree):
    """Create ast."""
    lispcode = lispfcktree.read()
    tokens = lexer(lispcode)
    tree = parser(tokens)
    pprint.pprint(tree)

if __name__ == '__main__':
    ast()
