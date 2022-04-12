from typing import Dict, List
from pyswip import *
from random import choice

from map import Map


def setup_map(N: int, M: int) -> Map:
    w_map = Map(N, M, "rnorth")
    w_map.reposition_agent(3, 2)

    w_map.add_wumpus(5, 4)

    w_map.add_coin(1, 1)
    w_map.add_coin(3, 2)

    w_map.add_portal(2, 1)
    w_map.add_portal(4, 1)
    w_map.add_portal(4, 4)

    return w_map


def setup_prolog(filename: str, w_map: Map) -> Prolog:
    prolog = Prolog()
    prolog.consult(filename)
    list(prolog.query("reborn"))

    perceptions = w_map.get_cell_perceptions()
    list(prolog.query(f"reposition([{perceptions.get_query_str()}])"))
    return prolog


def get_action(action: str = None) -> str:
    if action:
        return action
    return choice(["moveforward", "turnleft", "turnright"])


def make_action(prolog: Prolog, w_map: Map, action: str = None, print_map: bool = True):
    # preemptively clears bumps to prevent old bumps from showing
    w_map.clear_bumps()

    action = get_action(action=action)
    w_map.do_action(action)
    perceptions = w_map.get_cell_perceptions()

    query_str = f"move({action}, [{perceptions.get_query_str()}])"
    list(prolog.query(query_str))

    if w_map.check_portal():
        w_map.reposition_agent(2, 3)
        perceptions = w_map.get_cell_perceptions()
        list(prolog.query(f"reposition([{perceptions.get_query_str()}])"))

    if print_map:
        print(f"[Driver] {perceptions.get_sense_printout()}")
        w_map.print_absolute_map(prolog)
        w_map.print_relative_map(prolog)


# continues using explore(L) until no safe cells are left
def auto_explore(prolog: Prolog, w_map: Map):
    path_exists = True

    while path_exists:
        L = list(prolog.query("explore(L)"))
        print(L[0]['L'])
        path_exists = handle_explore_result(prolog, w_map, L)

    return


def handle_explore_result(prolog: Prolog, w_map: Map, L: List[Dict[str, List[Atom]]]) -> bool:
    if len(L) == 0:
        print("[Driver] Nothing from explore(L) anymore...")
        return False

    actions = L[0]['L']
    for action in actions:
        print(atoms_to_strings(action))
        make_action(prolog, w_map, atoms_to_strings(action), print_map=True)

    return True


def atoms_to_strings(answer):
    if isinstance(answer, dict):
        result = {}
        for k in answer.keys():
            result[k] = atoms_to_strings(answer[k])
    elif isinstance(answer, list):
        result = [atoms_to_strings(val) for val in answer]
    elif isinstance(answer, Atom):
        result = answer.value
    elif isinstance(answer, int) or isinstance(answer, str):
        result = answer
    else:
        print("Unsupported result from Prolog: " +
              str(type(answer)) + str(answer))
    return result


def main():
    w_map = setup_map(7, 6)
    prolog = setup_prolog("agent.pl", w_map)

    w_map.print_init_map()
    w_map.reset_absolute_map(full_clear=True)
    w_map.print_relative_map(prolog)

    auto_explore(prolog, w_map)


if __name__ == "__main__":
    main()
