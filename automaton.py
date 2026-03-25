from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Iterable, Optional
from collections import defaultdict, deque
import itertools

EPSILON = "λ"


@dataclass
class StateVisual:
    x: float = 0.0
    y: float = 0.0


@dataclass
class Automaton:
    alphabet: Set[str] = field(default_factory=set)
    states: Set[str] = field(default_factory=set)
    initial_state: Optional[str] = None
    accept_states: Set[str] = field(default_factory=set)
    transitions: Dict[str, Dict[str, Set[str]]] = field(default_factory=lambda: defaultdict(lambda: defaultdict(set)))
    visuals: Dict[str, StateVisual] = field(default_factory=dict)
    automaton_type: str = "dfa"  # dfa, nfa, nfae

    def add_state(self, name: str, initial: bool = False, accept: bool = False, x: float = 0.0, y: float = 0.0) -> None:
        self.states.add(name)
        self.visuals.setdefault(name, StateVisual(x=x, y=y))
        if initial:
            self.initial_state = name
        if accept:
            self.accept_states.add(name)

    def add_transition(self, source: str, symbol: str, target: str) -> None:
        self.states.update({source, target})
        if symbol != EPSILON and symbol != "":
            self.alphabet.add(symbol)
        self.transitions[source][symbol].add(target)
        self._update_type()

    def set_transition(self, source: str, symbol: str, target: str) -> None:
        self.transitions[source][symbol] = {target}
        if symbol != EPSILON and symbol != "":
            self.alphabet.add(symbol)
        self.states.update({source, target})
        self._update_type()

    def _update_type(self) -> None:
        has_epsilon = False
        deterministic = True
        for src, by_symbol in self.transitions.items():
            for symbol, targets in by_symbol.items():
                if symbol in (EPSILON, ""):
                    has_epsilon = True
                if len(targets) > 1:
                    deterministic = False
        if has_epsilon:
            self.automaton_type = "nfae"
        elif deterministic:
            self.automaton_type = "dfa"
        else:
            self.automaton_type = "nfa"

    def validate_basic(self) -> List[str]:
        errors = []
        if not self.states:
            errors.append("No hay estados definidos.")
        if not self.initial_state:
            errors.append("No hay estado inicial definido.")
        elif self.initial_state not in self.states:
            errors.append("El estado inicial no pertenece al conjunto de estados.")
        for st in self.accept_states:
            if st not in self.states:
                errors.append(f"El estado de aceptación {st} no existe.")
        return errors

    def is_dfa(self) -> bool:
        if self.validate_basic():
            return False
        for st in self.states:
            for symbol in self.alphabet:
                targets = self.transitions.get(st, {}).get(symbol, set())
                if len(targets) != 1:
                    return False
        for by_symbol in self.transitions.values():
            if EPSILON in by_symbol or "" in by_symbol:
                return False
        return True

    def simulate_dfa(self, string: str) -> Tuple[bool, List[dict]]:
        if not self.is_dfa():
            raise ValueError("El autómata actual no es un AFD completo.")
        current = self.initial_state
        trace = [{"step": 0, "symbol": "ε", "from": None, "to": current}]
        for idx, ch in enumerate(string, start=1):
            if ch not in self.alphabet:
                trace.append({"step": idx, "symbol": ch, "from": current, "to": None, "error": "Símbolo fuera del alfabeto"})
                return False, trace
            nxt = next(iter(self.transitions[current][ch]))
            trace.append({"step": idx, "symbol": ch, "from": current, "to": nxt})
            current = nxt
        return current in self.accept_states, trace

    def epsilon_closure(self, states: Iterable[str]) -> Set[str]:
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            for nxt in self.transitions.get(state, {}).get(EPSILON, set()) | self.transitions.get(state, {}).get("", set()):
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
        return closure

    def move(self, states: Iterable[str], symbol: str) -> Set[str]:
        result = set()
        for st in states:
            result |= self.transitions.get(st, {}).get(symbol, set())
        return result

    def determinize(self) -> "Automaton":
        errors = self.validate_basic()
        if errors:
            raise ValueError("; ".join(errors))
        start_set = frozenset(self.epsilon_closure({self.initial_state}))
        dfa = Automaton(alphabet=set(self.alphabet), automaton_type="dfa")

        def name_of(state_set: frozenset[str]) -> str:
            if not state_set:
                return "∅"
            return "{" + ",".join(sorted(state_set)) + "}"

        queue = deque([start_set])
        visited = {start_set}
        dfa.add_state(name_of(start_set), initial=True, accept=bool(set(start_set) & self.accept_states))

        while queue:
            current_set = queue.popleft()
            current_name = name_of(current_set)
            for symbol in sorted(self.alphabet):
                moved = self.move(current_set, symbol)
                closed = frozenset(self.epsilon_closure(moved))
                next_name = name_of(closed)
                if closed not in visited:
                    visited.add(closed)
                    queue.append(closed)
                    dfa.add_state(next_name, accept=bool(set(closed) & self.accept_states))
                dfa.set_transition(current_name, symbol, next_name)

        dfa.complete_with_sink()
        dfa.layout_states()
        return dfa

    def complete_with_sink(self, sink_name: str = "q_sink") -> None:
        if not self.states:
            return
        need_sink = False
        for st in list(self.states):
            for symbol in self.alphabet:
                if len(self.transitions.get(st, {}).get(symbol, set())) != 1:
                    need_sink = True
        if not need_sink:
            return
        self.add_state(sink_name)
        for symbol in self.alphabet:
            self.set_transition(sink_name, symbol, sink_name)
        for st in list(self.states):
            for symbol in self.alphabet:
                targets = self.transitions.get(st, {}).get(symbol, set())
                if len(targets) != 1:
                    self.set_transition(st, symbol, sink_name)
        self.automaton_type = "dfa"

    def layout_states(self, width: int = 700, height: int = 320) -> None:
        if not self.states:
            return
        cx, cy = width / 2, height / 2
        radius = min(width, height) * 0.35
        ordered = sorted(self.states)
        n = len(ordered)
        for i, st in enumerate(ordered):
            angle = 2 * 3.1415926535 * i / max(n, 1)
            x = cx + radius * __import__('math').cos(angle)
            y = cy + radius * __import__('math').sin(angle)
            self.visuals[st] = StateVisual(x=x, y=y)

    def transition_table(self) -> List[List[str]]:
        header = ["Estado"] + sorted(self.alphabet)
        rows = [header]
        for st in sorted(self.states):
            name = st
            if st == self.initial_state:
                name = "→" + name
            if st in self.accept_states:
                name = "*" + name
            row = [name]
            for symbol in sorted(self.alphabet):
                targets = sorted(self.transitions.get(st, {}).get(symbol, set()))
                row.append(", ".join(targets) if targets else "—")
            rows.append(row)
        return rows

    def to_serializable(self) -> dict:
        return {
            "type": self.automaton_type,
            "alphabet": sorted(self.alphabet),
            "states": [
                {
                    "name": st,
                    "initial": st == self.initial_state,
                    "accept": st in self.accept_states,
                    "x": self.visuals.get(st, StateVisual()).x,
                    "y": self.visuals.get(st, StateVisual()).y,
                }
                for st in sorted(self.states)
            ],
            "transitions": [
                {"from": src, "symbol": sym, "to": dst}
                for src in sorted(self.states)
                for sym in sorted(self.transitions.get(src, {}).keys(), key=lambda s: (s != EPSILON, s))
                for dst in sorted(self.transitions[src][sym])
            ],
        }


def prefixes(s: str) -> List[str]:
    return [s[:i] for i in range(len(s) + 1)]


def suffixes(s: str) -> List[str]:
    return [s[i:] for i in range(len(s) + 1)]


def substrings(s: str) -> List[str]:
    seen = []
    found = set()
    for i in range(len(s) + 1):
        for j in range(i, len(s) + 1):
            piece = s[i:j]
            if piece not in found:
                found.add(piece)
                seen.append(piece)
    return seen


def kleene_closure(alphabet: List[str], max_len: int, positive: bool = False) -> List[str]:
    results = []
    start = 1 if positive else 0
    if not alphabet:
        return [""] if not positive else []
    for length in range(start, max_len + 1):
        for prod in itertools.product(alphabet, repeat=length):
            results.append("".join(prod))
    if not positive:
        results.insert(0, "ε")
    return results
