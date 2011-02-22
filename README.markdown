## About *chartreuse*	

Chartreuse is a simple [context free](http://en.wikipedia.org/wiki/Context-free_grammars) [top-down](http://en.wikipedia.org/wiki/Top-down_parsing) [chart parser](http://en.wikipedia.org/wiki/Chart_parser) that constructs a [parse tree](http://en.wikipedia.org/wiki/Parse_tree) when presented with an input string and a grammar. The algorithm used is the straight-forward [Earley parser](http://en.wikipedia.org/wiki/Earley_parser).

## Motivation

I wanted to write a chart parser to teach myself more about computational linguistics and to do simple experiments. This project actually turned out to be much easier than I expected, and I completed it in about two weekend afternoons.

I also intend to rewrite this simple parser to JavaScript to provide an open-source parser library that can perform non-trivial work in the browser.

## About the grammar

Chartreuse grammar follows a very simple syntax and corresponds to a slight extension to [Chomky normal form](http://en.wikipedia.org/wiki/Chomsky_normal_form).

All grammar rules are of either of the following forms:

    symbol0: [symbol1 symbol2 ... symboln]
    symbol0: symbol1

A seperate module can compile more complicated grammar rules down into this simple form. The more complicated syntax includes the following constructs:

    [expr0, expr1, ...]
    (expr0, expr1, ...)
    (expr, )
    {"name0" : expr0, "name1" : expr1, ...}

The constructs can be composed, so that a list may contain tuples and vice versa. The terminal objects of this syntax are always single
strings that refer to existing grammar symbols.

### List

A lists such as `[expr0, expr1, ...]` corresponds to a series of expressions in a fixed order that must be matched left-to-right.

### Tuple

A tuple such as `(expr0, expr1, ...)` corresponds to a series of alternative expressions, exactly one of which has to match.

### Singleton tuple

The special tuple `(expr,)` (which indicates a single-item tuple in Python) refers to an optional expression that may or may not match.

### Dictionary

A dictionary such as `{"name0": expr0, "name1": expr1}` corresponds to a "bag" of clauses. 

Only one clause is required to match, which is taken to be the first clause, but subsequent clauses can also match, in any order and combination. 
The value of the resulting symbol is once again a dictionary with the same keys, but with the expressions replaced 
with the values of their corresponding matched symbols.

## Examples

To come...
