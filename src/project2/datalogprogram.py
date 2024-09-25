"""Representation for a Datalog program.

The module includes abstractions for the `Parameter`, `Predicate`, `RuleType`,
and a `DatalogProgram`. New is the listener pattern for interacting with a
datalog program. See the `DatalogProgram.PrintListener` for an example.
"""

from typing import Any, Literal

ParameterType = Literal["ID", "STRING"]
"""
Parameters can be either an ID naming a part of a relation or a string naming
a literal value.
"""


class Parameter:
    """Parameter class for all predicates.

    There are two types of parameters: ID and STRING. These correspond to their
    token counterparts.

    Attributes:
        value: The actual text for the parameter taken from the associated token.
        parameter_type: The type of the parameter: ID or STRING.
    """

    __slots__ = ["value", "parameter_type"]

    def __init__(self, value: str, parameter_type: ParameterType) -> None:
        self.value = value
        self.parameter_type = parameter_type

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Parameter):
            return False
        return (self.parameter_type == other.parameter_type) and (
            self.value == other.value
        )

    def __repr__(self) -> str:
        return (
            f"Parameter(value={self.value!r}, parameter_type={self.parameter_type!r})"
        )

    def is_id(self) -> bool:
        """True iff it is an ID parameter."""
        return "ID" == self.parameter_type

    def is_string(self) -> bool:
        """Create iff it is a STRING parameter."""
        return "STRING" == self.parameter_type

    @staticmethod
    def id(name: str) -> "Parameter":
        """Create an ID parameter."""
        return Parameter(name, "ID")

    @staticmethod
    def string(name: str) -> "Parameter":
        """Create a STRING parameter."""
        return Parameter(name, "STRING")


class Predicate:
    """Predicate class for all datalog entities.

    The predicate is a general structure that is used for schemes, facts,
    rules, and queries. The only difference is in the type of parameters
    allowed in the predicates where facts, rules, and queries allow for
    both the ID and STRING parameters --- the former for parts of a relation
    and the later for literals.

    Attributes:
        name: The name of the predicate.
        parameters: The parameter list.
    """

    __slots__ = ["name", "parameters"]

    def __init__(self, name: str, parameters: list[Parameter] = []) -> None:
        self.name = name
        self.parameters = parameters

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Predicate):
            return False
        return (self.name == other.name) and (self.parameters == other.parameters)

    def __repr__(self) -> str:
        return f"Predicate(name={self.name!r}, parameters={self.parameters!r})"

    def __str__(self) -> str:
        parameters: str = ",".join([i.value for i in self.parameters])
        return f"{self.name}({parameters})"

    def add_parameter(self, parameter: Parameter) -> None:
        """Add a parameter to the predicate.

        Helper function if the `__init__` doesn't provide parameters or a
        complete parameter list.

        Args:
            parameter: The parameter to add.
        """
        self.parameters.append(parameter)


RuleType = tuple[Predicate, list[Predicate]]
"""
`RuleType` is the abstraction for a rule. It consists of the head predicate
and a list of predicates. The head predicate names the destination for any
facts created by the rule. The list of predicates define how to create
facts.
"""


def get_head(rule: RuleType) -> Predicate:
    """Return the head predicate from a rule."""
    return rule[0]


def get_predicates(rule: RuleType) -> list[Predicate]:
    """Return the predicate list from a rule."""
    return rule[1]


class DatalogProgram:
    """Class for a Datalog program

    The `Datalog` program class holds all the schemes, rules, facts, and
    queries for the program.

    Attributes:
        schemes: The list of schemes as predicates.
        facts: The list of facts as predicates.
        rules: The list of rules as `RuleType` instances.
        queries: The list of queries as predicates.
    """

    __slots__ = ["schemes", "facts", "rules", "queries"]

    def __init__(
        self,
        schemes: list[Predicate] = [],
        facts: list[Predicate] = [],
        rules: list[RuleType] = [],
        queries: list[Predicate] = [],
    ):
        self.schemes = schemes
        self.facts = facts
        self.rules = rules
        self.queries = queries

    def __str__(self) -> str:
        """Returns the string representation of the program."""
        raise NotImplementedError

    def add_scheme(self, scheme: Predicate) -> None:
        """Add a scheme to the list of schemes."""
        self.schemes.append(scheme)

    def add_fact(self, fact: Predicate) -> None:
        """Add a fact to the list of facts."""
        self.facts.append(fact)

    def add_rule(self, rule: RuleType) -> None:
        """Add rule to the list of rules."""
        self.rules.append(rule)

    def add_query(self, query: Predicate) -> None:
        """Add a query to the list of queries."""
        self.queries.append(query)
