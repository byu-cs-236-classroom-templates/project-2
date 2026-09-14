# Adding Arithmetic Comparison Expressions to the Simplified Datalog Language

## Overview

This extension adds a deliberately small expression language to the
simplified Datalog parser.

**Scope for Project 2.** This document is part of the [Deeper
Learning](../README.md#deeper-learning) discussed in the README. Project 2
only *parses* Datalog programs -- it does not evaluate them. This
extension is scoped the same way: you extend the grammar and the lexer,
and you build a recursive expression tree while parsing. You are **not**
implementing evaluation of expressions in Project 2. Evaluating rules,
including these comparison expressions, is Project 4's job. Wherever this
document talks about what an expression "means," that discussion is only
there to motivate *why* the grammar and tree are shaped the way they are.

The goal for Project 2 is to introduce:

-   a lexer rule for signed integer literals,
-   arithmetic expressions with operator precedence,
-   parenthesized subexpressions, and
-   a recursive expression-tree representation built by the parser.

The extension is intentionally restricted. Expressions do not replace
ordinary Datalog parameters and are not used to compute values in rule
heads. Instead, a rule may have one optional comparison expression at
the **end of its body**.

A comparison has exactly one binary `<` operator. The operands of `<`
are arithmetic expressions containing variables, integer constants, `+`,
`*`, and parentheses.

For example:

``` text
small(X) :- value(X), X * 2 + 1 < 10.
```

------------------------------------------------------------------------

## Original Grammar

The original simplified Datalog grammar is:

``` text
datalogProgram  -> SCHEMES COLON scheme schemeList FACTS COLON factList RULES COLON ruleList QUERIES COLON query queryList EOF

schemeList      -> scheme schemeList | lambda
factList        -> fact factList | lambda
ruleList        -> rule ruleList | lambda
queryList       -> query queryList | lambda

scheme          -> ID LEFT_PAREN ID idList RIGHT_PAREN
fact            -> ID LEFT_PAREN STRING stringList RIGHT_PAREN PERIOD
rule            -> headPredicate COLON_DASH predicate predicateList PERIOD
query           -> predicate Q_MARK

headPredicate   -> ID LEFT_PAREN ID idList RIGHT_PAREN
predicate       -> ID LEFT_PAREN parameter parameterList RIGHT_PAREN

predicateList   -> COMMA predicate predicateList | lambda
parameterList   -> COMMA parameter parameterList | lambda
stringList      -> COMMA STRING stringList | lambda
idList          -> COMMA ID idList | lambda
parameter       -> STRING | ID
```

------------------------------------------------------------------------

## Lexer Extension

The expression extension needs one new lexer rule, `INT`, along with
three new single-character tokens: `PLUS`, `MULTIPLY`, and `LESS`.
`LEFT_PAREN` and `RIGHT_PAREN` already exist.

`INT` is a (possibly negative) sequence of digits:

``` text
INT     -> MINUS? DIGIT DIGIT*
MINUS   -> '-'
DIGIT   -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
```

This lexer rule matches `0`, `10`, and `-10`. There is no separate
`MINUS` token in this extension -- a leading `-` is only recognized as
part of an `INT`, never as a standalone subtraction operator, so the
FSM for `INT` should consume the optional leading `-` itself.

------------------------------------------------------------------------

## Grammar Extension

The rule grammar is extended so that a rule may end with an optional
comparison expression:

``` text
rule                 -> headPredicate COLON_DASH predicate predicateList expressionOpt PERIOD

expressionOpt        -> COMMA expression
                      | lambda

expression           -> addExpression LESS addExpression

addExpression        -> multiplyExpression addExpressionList
addExpressionList    -> PLUS multiplyExpression addExpressionList
                      | lambda

multiplyExpression   -> factor multiplyExpressionList
multiplyExpressionList
                     -> MULTIPLY factor multiplyExpressionList
                      | lambda

factor               -> ID
                      | INT
                      | LEFT_PAREN addExpression RIGHT_PAREN
```

The comma in `expressionOpt` makes the comparison another body condition
syntactically:

``` text
p(X) :- q(X), X < 10.
```

while still requiring it to be the final condition in the rule.

All other productions remain unchanged.

------------------------------------------------------------------------

## What Expressions Are Allowed?

A rule without an expression remains valid:

``` text
answer(X) :- value(X).
```

A rule may have one comparison at the end:

``` text
answer(X) :- value(X), X < 10.
```

Arithmetic may occur on either side, and integer literals may be
negative:

``` text
answer(X) :- value(X), X * 2 + 1 < -10.
```

Variables from multiple predicates may be used:

``` text
answer(X) :- left(X), right(Y), X + Y * 2 < 20.
```

Parentheses may override normal arithmetic precedence:

``` text
answer(X) :- left(X), right(Y), (X + Y) * 2 < 20.
```

The following are intentionally not part of the language:

``` text
answer(X) :- value(X), X < 10, other(X).
```

The comparison must be last.

``` text
answer(X) :- value(X), X + 10.
```

A comparison must contain `<`.

``` text
answer(X) :- value(X), X < 10 < 20.
```

`<` cannot be chained. A comparison has exactly one `<`.

``` text
answer(X) :- value(X), X + (Y < 10) < 20.
```

`<` cannot occur inside an arithmetic expression.

Each of these restrictions is enforced by the grammar itself, so they
are rejected during parsing, not during some later semantic check.

------------------------------------------------------------------------

## Precedence

The operators have the following precedence, from highest to lowest:

1.  Parentheses
2.  `*`
3.  `+`
4.  `<`

Thus:

``` text
X + Y * 2 < 20
```

means:

``` text
(X + (Y * 2)) < 20
```

and not:

``` text
((X + Y) * 2) < 20
```

Parentheses can explicitly change the structure:

``` text
(X + Y) * 2 < 20
```

------------------------------------------------------------------------

## Expression Trees

Arithmetic expressions are structurally recursive. Their natural
representation is an inductive tree that the parser builds as it
recognizes `expression`.

Conceptually, an arithmetic expression can be defined as:

``` text
ArithmeticExpression :=
      Integer(value)
    | Variable(name)
    | Add(left, right)
    | Multiply(left, right)
```

The comparison can be represented separately:

``` text
Comparison :=
    Less(left: ArithmeticExpression,
         right: ArithmeticExpression)
```

Keeping `Less` separate is particularly natural for this language
because `<` is not a general arithmetic operator. Every rule expression
is exactly one top-level binary comparison.

### Example: Precedence

The expression

``` text
X + Y * 2 < 20
```

has the tree:

``` text
             Less
            /    \
          Add     20
         /   \
        X   Multiply
            /      \
           Y        2
```

Equivalently:

``` text
Less(
    Add(
        Variable("X"),
        Multiply(
            Variable("Y"),
            Integer(2)
        )
    ),
    Integer(20)
)
```

The multiplication occurs below the addition in the tree, which is what
will later let it be evaluated first (in Project 4).

### Example: Parentheses

The expression

``` text
(X + Y) * 2 < 20
```

has a different tree:

``` text
             Less
            /    \
      Multiply    20
       /     \
     Add      2
    /   \
   X     Y
```

Equivalently:

``` text
Less(
    Multiply(
        Add(
            Variable("X"),
            Variable("Y")
        ),
        Integer(2)
    ),
    Integer(20)
)
```

Parentheses do not need to appear as nodes in the expression tree. They
only determine how the tree is constructed during parsing.

------------------------------------------------------------------------

## Why a Recursive Data Structure Is Required

Expressions may contain expressions recursively:

``` text
(X + Y) * (Z + 2 * W)
```

An `Add` node contains two arithmetic expressions. A `Multiply` node
also contains two arithmetic expressions. Those children may themselves
be `Add` or `Multiply` nodes.

Consequently, an arithmetic expression is naturally an inductive data
structure:

``` text
expression
    = integer
    | variable
    | addition(expression, expression)
    | multiplication(expression, expression)
```

This is why the expression tree, and the parsing functions that build
it, must be recursive rather than iterative: `addExpression` calls
`multiplyExpression`, which calls `factor`, and `factor` can call
`addExpression` again through a parenthesized subexpression. There is no
bound on how deeply this nesting can go, so no fixed amount of iteration
can replace the recursion.

------------------------------------------------------------------------

## Semantic Intuition (context only -- implemented in Project 4)

Project 2 stops once the expression has been parsed into a tree attached
to the `Rule`. The rest of this section is only meant to give intuition
for why the grammar is shaped this way; none of it is implemented until
Project 4.

Conceptually, expressions are **filters**, not mechanisms for generating
new variable bindings. Rule evaluation is imagined as two stages: the
ordinary predicates in the rule body produce tuples and bindings for
variables, and then the trailing comparison is evaluated using those
bindings to decide whether to keep each tuple.

For example, suppose `value` contains:

``` text
value(2).
value(4).
value(7).
```

Then for the rule:

``` text
small(X) :- value(X), X * 2 + 1 < 10.
```

`value(X)` supplies values for `X`, and `X * 2 + 1 < 10` is later
evaluated for each value:

``` text
2 * 2 + 1 < 10    true
4 * 2 + 1 < 10    true
7 * 2 + 1 < 10    false
```

so the resulting relation would contain the values corresponding to
`X = 2` and `X = 4`. In relational-algebra terms, the comparison behaves
like a **selection** over the relation produced by the ordinary
predicates in the rule body.

Every variable used in the comparison must already be bound by an
ordinary predicate earlier in the body:

``` text
answer(X) :- value(X), X + Y < 10.
```

is not valid, because nothing in the body binds `Y`. Expressions are
never solved backwards to discover values for unbound variables -- this
is also why expressions are not allowed as predicate parameters (e.g.
`foo(X + 2 * 3)?`), since that would require solving an equation instead
of evaluating an expression with known bindings.

This intuition is also why the comparison is restricted to a single,
optional, trailing position in the body: it keeps the "predicates
establish bindings, then one filter checks them" model simple.

------------------------------------------------------------------------

## Summary

The extended grammar supports rules such as:

``` text
result(X) :- p(X), q(Y), (X + Y) * 2 < Z + 10.
```

For Project 2, this extension introduces two concepts:

**Lexing.** A new `INT` token, including a leading `-` for negative
literals, plus single-character `PLUS`, `MULTIPLY`, and `LESS` tokens.

**Parsing and representation.** Operator precedence and parentheses
determine the structure of a recursive expression tree, built from
integer, variable, addition, and multiplication nodes, with a comparison
node on top.

Evaluating that tree -- **interpretation** -- is deferred to Project 4.
