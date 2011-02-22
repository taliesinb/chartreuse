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

A famous example of an ambiguous sentence in linguistics is the ["buffalo buffalo" sentence](http://en.wikipedia.org/wiki/Buffalo_buffalo_Buffalo_buffalo_buffalo_buffalo_Buffalo_buffalo). The high degree of ambiguity stems from the many meanings of the word "Buffalo", which can interpreted as an adjective ("born in the city of Buffalo"), a noun ("the animal also known as a bison"), and a verb ("to bully").

Let's construct a fake sentence that has 8 consecutive "buffalo"s. All will have the same token, though we will tag them with values that indicate the interpretation we, as the speakers of the sentence, *intended*.

    tokens = [
      symbol("buffalo", "Buffalo-born", (0,1)),
      symbol("buffalo", "Bison",        (1,2)),  
      symbol("buffalo", "Buffalo-born", (2,3)),
      symbol("buffalo", "Bison",        (3,4)),
      symbol("buffalo", "bully",        (4,5)),
      symbol("buffalo", "bully",        (5,6)),
      symbol("buffalo", "Buffalo-born", (6,7)),
      symbol("buffalo", "Bison",        (7,8))
    ]    

We use the following grammar rules to define nouns, noun phrases, adjectives, and sentences. Each grammar rule has an associated "action" that determines how to construct a meaning from its constituent parts. This
idea is quite a common one in computational linguistics but has as its basis the theory of [generative semantics](http://en.wikipedia.org/wiki/Generative_semantics).

    rules = [
      rule("start", ["sentence"]),
      rule("sentence", ["noun_phrase", "verb", "noun_phrase"], lambda n1, v, n2: flatten_values(["<", n1, "> performs the action ", v, " to <", n2, ">"])),
      rule("noun_phrase", ["noun"]),
      rule("noun_phrase", ["adjective", "noun"], lambda a, n: [n, " with property ", a]),
      rule("noun_phrase", ["noun_phrase", "noun_phrase", "verb"], lambda n1, n2, v: ["<", n1, "> which is ", v, "'d by <", n2, ">"]),
      rule("noun", ["buffalo"]),
      rule("verb", ["buffalo"]),
      rule("adjective", ["buffalo"])
    ]

We now feed these rules into chartreuse and have it parse our ambigious sentence:

    ch = chart(tokens, rules)
    winners = ch.parse(tokens)

Many valid interpretations of the sentence are possible, but number 15 is the one that actually matches the canonical one:

    winners:
    0 	<Buffalo-born> performs the action Bison to <<Bison with property Buffalo-born> which is Bison'd by <<bully> which is Buffalo-born'd by <bully>>>
    1 	<Buffalo-born> performs the action Bison to <<Buffalo-born> which is Bison'd by <<bully with property Bison> which is Buffalo-born'd by <bully>>>
    2 	<<Buffalo-born> which is Buffalo-born'd by <Bison>> performs the action Bison to <<bully> which is Bison'd by <Buffalo-born with property bully>>
    3 	<<Buffalo-born> which is Bison'd by <Buffalo-born with property Bison>> performs the action bully to <<bully> which is Bison'd by <Buffalo-born>>
    4 	<<Bison with property Buffalo-born> which is Bison'd by <Buffalo-born>> performs the action bully to <<bully> which is Bison'd by <Buffalo-born>>
    5 	<Buffalo-born> performs the action Bison to <<Buffalo-born> which is Bison'd by <<Bison> which is Buffalo-born'd by <bully with property bully>>>
    6 	<Buffalo-born> performs the action Bison to <<<Bison with property Buffalo-born> which is bully'd by <bully>> which is Bison'd by <Buffalo-born>>
    7 	<Bison with property Buffalo-born> performs the action Buffalo-born to <<Bison> which is Bison'd by <<bully> which is Buffalo-born'd by <bully>>>
    8 	<Buffalo-born> performs the action Bison to <<<Buffalo-born> which is bully'd by <bully with property Bison>> which is Bison'd by <Buffalo-born>>
    9 	<Bison with property Buffalo-born> performs the action Buffalo-born to <<<Bison> which is bully'd by <bully>> which is Bison'd by <Buffalo-born>>
    10 	<Buffalo-born> performs the action Bison to <<<Buffalo-born> which is bully'd by <Bison>> which is Bison'd by <Buffalo-born with property bully>>
    11 	<Bison with property Buffalo-born> performs the action Buffalo-born to <<bully with property Bison> which is Bison'd by <Buffalo-born with property bully>>
    12 	<<Buffalo-born> which is Buffalo-born'd by <Bison>> performs the action Bison to <<bully with property bully> which is Bison'd by <Buffalo-born>>
    13 	<<<Buffalo-born> which is Buffalo-born'd by <Bison>> which is bully'd by <Bison>> performs the action bully to <Bison with property Buffalo-born>
    14 	<<Bison with property Buffalo-born> which is bully'd by <Bison with property Buffalo-born>> performs the action bully to <Bison with property Buffalo-born>
    15 	<<Buffalo-born> which is bully'd by <<Bison> which is Bison'd by <Buffalo-born>>> performs the action bully to <Bison with property Buffalo-born>
    16 	<<Buffalo-born> which is bully'd by <<Bison> which is bully'd by <Bison with property Buffalo-born>>> performs the action Buffalo-born to <Bison>
    17 	<<Bison with property Buffalo-born> which is bully'd by <<Buffalo-born> which is bully'd by <Bison>>> performs the action Buffalo-born to <Bison>
    18 	<<<Bison with property Buffalo-born> which is Bison'd by <Buffalo-born>> which is bully'd by <bully>> performs the action Buffalo-born to <Bison>
    19 	<<<Buffalo-born> which is Bison'd by <Buffalo-born with property Bison>> which is bully'd by <bully>> performs the action Buffalo-born to <Bison>
    20 	<<Buffalo-born> which is bully'd by <<Buffalo-born with property Bison> which is bully'd by <Bison>>> performs the action Buffalo-born to <Bison>
    21 	<<<Buffalo-born> which is Buffalo-born'd by <Bison>> which is bully'd by <bully with property Bison>> performs the action Buffalo-born to <Bison>
