## About *Cinema-AI*	

Cinema-AI is a website which uses the Chartreuse parser and the Freebase API to answer questions about movies.

## About the grammar

Chartreuse grammar follows a very simple syntax and corresponds to a slight extension to [Chomky normal form](http://en.wikipedia.org/wiki/Chomsky_normal_form).

All grammar rules are of either of the following forms:

    symbol0: [symbol1 symbol2 ... symboln]
    symbol0: symbol1

A seperate module can compile more complicated grammar rules down into this simple form. The more complicated syntax includes the following constructs:

    [expr0, expr1, ...] or seq(expr0, expr1, ...)
    alt(expr0, expr1, ...)
    opt(expr)
    bag(name=expr0, name1=expr1, ...)

The constructs can be composed, so that a seq may contain bags, etc. Intermediate symbols will be produced by the compiler to represent various "fragments" of a compound grammar rule. 
The terminal objects of this syntax are always single strings that refer to existing grammar symbols.

### Sequence

An instance of class seq `seq(expr0, expr1, ...)` corresponds to a series of expressions in a fixed order that must be matched left-to-right.

### Alternatives

An instance of class alt `alt(alexpr0, expr1, ...)` corresponds to a series of alternative expressions, exactly one of which has to match.

### Optional

An instance of class opt `opt(expr)` refers to an optional expression that can but need not match. Multiple terms can also be used, indicating a series of alternatives, one or zero of which must match.

### Bag

An instance of class bag `bag(name=expr0, name1=expr1, ...)` corresponds to a "bag" of clauses. 

Only one clause is required to match, which is taken to be the first clause, but subsequent clauses can also match, in any order and combination. 
The value of the resulting symbol is once again a dictionary with the same keys, but with the expressions replaced 
with the values of their corresponding matched symbols.

## Examples

