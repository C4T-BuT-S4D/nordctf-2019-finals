#!/usr/bin/env python3

import sys
import networkx as nx 
import matplotlib.pyplot as plt

from random import getrandbits, shuffle, random


def make_state_name():
    return 'KER_' + str(getrandbits(32))


def add_word(states, word, in_state, out_state):
    intermediate_states = [make_state_name() for i in range(len(word) - 1)]
    word_states = [in_state] + intermediate_states + [out_state]
    for i in range(len(word)):
        current_state, next_state = word_states[i], word_states[i + 1]
        for state in [current_state, next_state]:
            if state not in states:
                states[state] = {}
        states[current_state][word[i]] = next_state
    return word_states


def build_code(states, in_state, out_state):
    fail_state = make_state_name()
    states_items = list(states.items())
    shuffle(states_items)
    var_flag, var_index = '$flag', '$index'
    code = []
    code.extend([
        '<?php',
        '',
        'if (!isset($_GET["flag"])) {',
        '    include("dump.html");',
        '    exit();',
        '}',
        '',
        '%s = $_GET["flag"];' % var_flag,
        '%s = 0;' % var_index,
        '',
        'goto %s;' % in_state,
        ''
    ])
    for state, trans in states_items:
        if state == out_state:
            continue
        code.append('%s:' % state)
        if len(trans) == 0:
            code.append('goto %s;' % fail_state)
        else:
            code.append('switch(%s[%s++]) {' % (var_flag, var_index))
            for symbol, next_state in trans.items():
                code.extend([
                    '    case "%s":' % symbol,
                    '        goto %s;' % next_state
                ])
            code.extend([
                '    default:',
                '        goto %s;' % fail_state,
                '}'
            ])
        code.append('')
    code.extend([
        '%s:' % out_state,
        'die("Correct flag.\\n");',
        '',
        '%s:' % fail_state,
        'die("Wrong flag.\\n");',
        '',
        '?>'
    ])
    return '\n'.join(code)


def add_trash(states, word, word_states, prob=0.5):
    for state in word_states:
        if random() > prob:
            continue
        new_word = list(set(word) - set(states.get(state, {}).keys()))
        shuffle(new_word)
        new_word = ''.join(new_word)[:int(len(word)*random())]
        if random() < 0.5:
            new_word_states = add_word(states, new_word, make_state_name(), state)
        else:
            new_word_states = add_word(states, new_word, state, make_state_name())
        add_trash(states, new_word, new_word_states, prob*prob)


def get_color(state, word_states):
    if state in [word_states[0], word_states[-1]]:
        return 'red'
    if state in word_states:
        return 'green'
    return 'blue'


def visualize(states, word_states):
    edge_labels = {}
    state_list = []
    state_color = []
    for state, trans in states.items():
        state_list.append(state)
        state_color.append(get_color(state, word_states))
        for symbol, next_state in trans.items():
            edge_labels[(state, next_state)] = symbol
    g = nx.Graph()
    for state1, state2 in edge_labels:
        g.add_edge(state1, state2)
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, nodelist=state_list, node_color=state_color, node_size=1, alpha=0.5)
    nx.draw_networkx_edges(g, pos, width=0.1)
    nx.draw_networkx_edge_labels(g, pos, edge_labels, font_size=1.5)
    plt.savefig("graph.png", dpi=500)


def main(flag):
    states = {}
    in_state, out_state = make_state_name(), make_state_name()
    print('adding flag', file=sys.stderr)
    flag_states = add_word(states, flag, in_state, out_state)
    print('adding trash', file=sys.stderr)
    add_trash(states, flag, flag_states)
    print('building code', file=sys.stderr)
    code = build_code(states, in_state, out_state)
    print(code)
    print('visualizing', file=sys.stderr)
    visualize(states, flag_states)


if __name__ == '__main__':
    with open('flag.txt', 'r') as file:
        flag = file.read()
    main(flag)
