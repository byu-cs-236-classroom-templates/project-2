"""Representation for a Datalog program.

The module includes abstractions for the `Parameter`, `Predicate`, `RuleType`,
and a `DatalogProgram`. New is the listener pattern for interacting with a
datalog program. See the `DatalogProgram.PrintListener` for an example.
"""

from typing import Literal

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


class Listener:
    """Base listener class for a visitor pattern.

    The visitor pattern is a convenient abstraction for decoupling traversal
    of a data structure and the computation performed during the traversal.
    The pattern is useful for printing a Datalog program for testing (see
    the `DatalogProgram.PrintListener`) and for interpreting a Datalog
    program as is required in later projects. The associated enter/exit
    functions are called by the walker as it traverses the Datalog program.
    The enter function is called pre-order in the traversal -- before visiting
    any children, and the exit function is called post-order in the traversal --
    after visiting children.
    """

    def enter_datalog_program(self, datalog_program: "DatalogProgram") -> None:
        """Called before visiting anything in the program."""
        pass

    def exit_datalog_program(self, datalog_program: "DatalogProgram") -> None:
        """Called after visiting everything in the program."""
        pass

    def enter_schemes(self, schemes: list[Predicate]) -> None:
        """Called before visiting any schemes."""
        pass

    def exit_schemes(self, schemes: list[Predicate]) -> None:
        """Called after visiting all schemes."""
        pass

    def enter_facts(self, facts: list[Predicate]) -> None:
        """Called before visiting any facts."""
        pass

    def exit_facts(self, facts: list[Predicate]) -> None:
        """Called after visiting all facts."""
        pass

    def enter_rules(self, rules: list[RuleType]) -> None:
        """Called before visiting any rules."""
        pass

    def exit_rules(self, rules: list[RuleType]) -> None:
        """Called after visiting all rules."""
        pass

    def enter_queries(self, queries: list[Predicate]) -> None:
        """Called before visiting any queries."""
        pass

    def exit_queries(self, queries: list[Predicate]) -> None:
        """Called after visiting all queries."""
        pass

    def enter_scheme(self, scheme: Predicate) -> None:
        """Called first on a scheme."""
        pass

    def exit_scheme(self, scheme: Predicate) -> None:
        """Called last on a scheme."""
        pass

    def enter_fact(self, fact: Predicate) -> None:
        """Called first on a fact."""
        pass

    def exit_fact(self, fact: Predicate) -> None:
        """Called last on a fact."""
        pass

    def enter_rule(self, rule: RuleType) -> None:
        """Called first on a rule."""
        pass

    def exit_rule(self, rule: RuleType) -> None:
        """Called last on a rule."""
        pass

    def enter_query(self, query: Predicate) -> None:
        """Called first on a query."""
        pass

    def exit_query(self, query: Predicate) -> None:
        """Called last on a query."""
        pass


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

    class PrintListener(Listener):
        """Listener to turn a Datalog program into a string.

        The listener captures the domain during the traversal and includes
        the domain in the final string representation of the Datalog
        program.

        Attributes:
            strings: A list holding the string representation of each component of the program.
            domain: The collected strings in the domain of the program -- strings in facts.
        """

        __slots__ = ["strings", "domain"]

        def __init__(self) -> None:
            self.strings: list[str] = []
            self.domain: set[str] = set()

        def _header(self, name: str, size: int) -> str:
            return f"{name}({str(size)}):"

        def enter_schemes(self, schemes: list[Predicate]) -> None:
            header = self._header("Schemes", len(schemes))
            self.strings.append(header)

        def exit_schemes(self, schemes: list[Predicate]) -> None:
            """Append an newline to the strings.

            It's easy to add the newline here rather than figure out
            if a particular scheme is the last in the list. The pattern
            is followed for the other list elements.
            """
            self.strings.append("\n")

        def enter_facts(self, facts: list[Predicate]) -> None:
            header = self._header("Facts", len(facts))
            self.strings.append(header)

        def exit_facts(self, facts: list[Predicate]) -> None:
            self.strings.append("\n")

        def enter_rules(self, rules: list[RuleType]) -> None:
            header = self._header("Rules", len(rules))
            self.strings.append(header)

        def exit_rules(self, rules: list[RuleType]) -> None:
            self.strings.append("\n")

        def enter_queries(self, queries: list[Predicate]) -> None:
            header = self._header("Queries", len(queries))
            self.strings.append(header)

        def exit_queries(self, queries: list[Predicate]) -> None:
            self.strings.append("\n")

        def exit_datalog_program(self, datalog_program: "DatalogProgram") -> None:
            """Add the domain to the string.

            The exit listener is a good place to generate the part of the string
            that belongs to the domain. Some care is taken for when the domain
            is empty in order to not add a non-necessary newline.
            """
            header = self._header("Domain", len(self.domain)) + (
                "\n  " if len(self.domain) > 0 else ""
            )
            self.strings.append(header)
            self.strings.append("\n  ".join(sorted(self.domain)))

        def enter_scheme(self, scheme: Predicate) -> None:
            self.strings.append(f"\n  {str(scheme)}")

        def enter_fact(self, fact: Predicate) -> None:
            """Add literals to the domain and update the string.

            Any literal (STRING) in a fact belongs to the domain of the program.
            These are each of the parameters in the predicate associated with
            the fact.
            """
            self.domain.update([i.value for i in fact.parameters])
            self.strings.append(f"\n  {str(fact)}.")

        def enter_rule(self, rule: RuleType) -> None:
            predicates = ",".join([str(i) for i in get_predicates(rule)])
            self.strings.append(f"\n  {str(get_head(rule))} :- {predicates}.")

        def enter_query(self, query: Predicate) -> None:
            self.strings.append(f"\n  {str(query)}?")

        def __str__(self) -> str:
            return "".join(self.strings)

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
        listener = DatalogProgram.PrintListener()
        Walker().walk(listener, self)
        return str(listener)

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


class Walker:
    """Walker to define the Datalog program traversal.

    The `Walker` class defines the order of traversal for a Datalog program.
    It requires a `Listener` for the traversal so that it can call the
    `Listener` at the appropriate times with the correct data.
    """

    def walk(self, listener: "Listener", program: DatalogProgram) -> None:
        """Default traversal for a Datalog program.

        The traversal here follows the interpretation order: schemes to create
        the relations, facts to populate the relations, rules to generate new
        facts, and finally queries to answer questions about the relations. It
        calls enter functions pre-order, before visiting any children, and exit
        functions post-order, after visiting all children.
        """
        listener.enter_datalog_program(program)
        listener.enter_schemes(program.schemes)
        for i in program.schemes:
            listener.enter_scheme(i)
            listener.exit_scheme(i)
        listener.exit_schemes(program.schemes)

        listener.enter_facts(program.facts)
        for i in program.facts:
            listener.enter_fact(i)
            listener.exit_fact(i)
        listener.exit_facts(program.schemes)

        listener.enter_rules(program.rules)
        for r in program.rules:
            listener.enter_rule(r)
            listener.exit_rule(r)
        listener.exit_rules(program.rules)

        listener.enter_queries(program.queries)
        for i in program.queries:
            listener.enter_query(i)
            listener.exit_query(i)
        listener.exit_queries(program.queries)
        listener.exit_datalog_program(program)
