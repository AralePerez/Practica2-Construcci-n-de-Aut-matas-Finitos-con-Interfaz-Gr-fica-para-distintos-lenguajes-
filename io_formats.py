from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional
from automaton import Automaton, EPSILON


def load_automaton(path: str | Path) -> Automaton:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".jff":
        return load_jff(path)
    if suffix == ".json":
        return load_json(path)
    if suffix == ".xml":
        return load_xml(path)
    raise ValueError(f"Formato no soportado: {suffix}")


def save_automaton(automaton: Automaton, path: str | Path) -> None:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".jff":
        save_jff(automaton, path)
    elif suffix == ".json":
        save_json(automaton, path)
    elif suffix == ".xml":
        save_xml(automaton, path)
    else:
        raise ValueError(f"Formato no soportado: {suffix}")


def load_json(path: str | Path) -> Automaton:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    a = Automaton()
    for state in data.get("states", []):
        a.add_state(
            state["name"],
            initial=state.get("initial", False),
            accept=state.get("accept", False),
            x=state.get("x", 0),
            y=state.get("y", 0),
        )
    for symbol in data.get("alphabet", []):
        a.alphabet.add(symbol)
    for t in data.get("transitions", []):
        a.add_transition(t["from"], t.get("symbol", ""), t["to"])
    a.automaton_type = data.get("type", a.automaton_type)
    return a


def save_json(automaton: Automaton, path: str | Path) -> None:
    Path(path).write_text(json.dumps(automaton.to_serializable(), ensure_ascii=False, indent=2), encoding="utf-8")


def load_xml(path: str | Path) -> Automaton:
    root = ET.parse(path).getroot()
    a = Automaton(automaton_type=root.attrib.get("type", "dfa"))
    for st in root.findall("./states/state"):
        a.add_state(
            st.attrib["name"],
            initial=st.attrib.get("initial", "false").lower() == "true",
            accept=st.attrib.get("accept", "false").lower() == "true",
            x=float(st.attrib.get("x", 0)),
            y=float(st.attrib.get("y", 0)),
        )
    for sym in root.findall("./alphabet/symbol"):
        val = (sym.text or "").strip()
        if val:
            a.alphabet.add(val)
    for tr in root.findall("./transitions/transition"):
        a.add_transition(
            tr.attrib["from"],
            tr.attrib.get("symbol", ""),
            tr.attrib["to"],
        )
    return a


def save_xml(automaton: Automaton, path: str | Path) -> None:
    root = ET.Element("automaton", {"type": automaton.automaton_type})
    alpha = ET.SubElement(root, "alphabet")
    for sym in sorted(automaton.alphabet):
        el = ET.SubElement(alpha, "symbol")
        el.text = sym
    states = ET.SubElement(root, "states")
    for st in sorted(automaton.states):
        vis = automaton.visuals.get(st)
        ET.SubElement(states, "state", {
            "name": st,
            "initial": str(st == automaton.initial_state).lower(),
            "accept": str(st in automaton.accept_states).lower(),
            "x": str(getattr(vis, 'x', 0)),
            "y": str(getattr(vis, 'y', 0)),
        })
    trans = ET.SubElement(root, "transitions")
    for src in sorted(automaton.states):
        for sym in sorted(automaton.transitions.get(src, {}).keys(), key=lambda s: (s != EPSILON, s)):
            for dst in sorted(automaton.transitions[src][sym]):
                ET.SubElement(trans, "transition", {"from": src, "symbol": sym, "to": dst})
    ET.indent(root)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def load_jff(path: str | Path) -> Automaton:
    root = ET.parse(path).getroot()
    automaton_node = root.find("./automaton")
    if automaton_node is None:
        raise ValueError("Archivo .jff inválido: no se encontró el nodo automaton")
    a = Automaton()
    id_to_name = {}
    for state in automaton_node.findall("state"):
        sid = state.attrib["id"]
        name = state.attrib["name"]
        x = float(state.findtext("x", default="0"))
        y = float(state.findtext("y", default="0"))
        initial = state.find("initial") is not None
        accept = state.find("final") is not None
        a.add_state(name, initial=initial, accept=accept, x=x, y=y)
        id_to_name[sid] = name
    for tr in automaton_node.findall("transition"):
        src_id = tr.findtext("from")
        dst_id = tr.findtext("to")
        symbol = tr.findtext("read")
        symbol = symbol if symbol is not None else ""
        symbol = symbol if symbol != "" else EPSILON
        a.add_transition(id_to_name[src_id], symbol, id_to_name[dst_id])
    a._update_type()
    return a


def save_jff(automaton: Automaton, path: str | Path) -> None:
    structure = ET.Element("structure")
    t = ET.SubElement(structure, "type")
    t.text = "fa"
    automaton_node = ET.SubElement(structure, "automaton")
    state_ids = {st: str(i) for i, st in enumerate(sorted(automaton.states))}
    for st in sorted(automaton.states):
        node = ET.SubElement(automaton_node, "state", {"id": state_ids[st], "name": st})
        x = ET.SubElement(node, "x")
        y = ET.SubElement(node, "y")
        vis = automaton.visuals.get(st)
        x.text = str(getattr(vis, 'x', 0.0))
        y.text = str(getattr(vis, 'y', 0.0))
        if st == automaton.initial_state:
            ET.SubElement(node, "initial")
        if st in automaton.accept_states:
            ET.SubElement(node, "final")
    for src in sorted(automaton.states):
        for sym in sorted(automaton.transitions.get(src, {}).keys(), key=lambda s: (s != EPSILON, s)):
            for dst in sorted(automaton.transitions[src][sym]):
                tr = ET.SubElement(automaton_node, "transition")
                ET.SubElement(tr, "from").text = state_ids[src]
                ET.SubElement(tr, "to").text = state_ids[dst]
                ET.SubElement(tr, "read").text = None if sym == EPSILON else sym
    ET.indent(structure)
    ET.ElementTree(structure).write(path, encoding="utf-8", xml_declaration=True)
