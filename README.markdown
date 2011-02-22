#README

## About *chartreuse*	

Chartreuse is a simple [chart parser](http://en.wikipedia.org/wiki/Chart_parser) that constructs a parse tree when presented with an input string and a grammar.

## About the grammar

Chartreuse grammar follows a very simple syntax and corresponds to a slight extension to [Chomky normal form](http://en.wikipedia.org/wiki/Chomsky_normal_form).

All grammar rules are of either of the following forms:

    symbol0: [symbol1 symbol2 ... symboln]
    symbol0: symbol1

A seperate module can compile more complicated grammar rules down into this simple form. The more complicated syntax includes the following constructs:

    [expr0, expr1, ...]
    (expr0, expr1, ...)
    (expr0, )
    {"name0" : expr0, "name1" : expr1, ...}

## Motivation

I wanted to write a chart parser to teach myself more about computational linguistics and do simple experiments.

I also intend to rewrite this simple parser to JavaScript to provide an open-source parser library that can perform non-trivial work in the browser.

## Examples

To come...