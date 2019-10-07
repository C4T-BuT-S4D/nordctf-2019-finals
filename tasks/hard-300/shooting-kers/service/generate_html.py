#!/usr/bin/env python3

import re

from html import escape 


def get_offsets(line):
    parts = re.findall(r'\S+\s+', line)
    offsets = [0]
    for part in parts:
        offsets.append(offsets[-1] + len(part))
    return offsets


def read_table():
    length_header = [input() for i in range(4)][2]
    length = int(re.search('\d+', length_header).group(0))
    header = input().replace('line     #*', 'line #*    ')
    offsets = get_offsets(header)
    header = header.split()
    input()
    table = [[] for i in range(len(offsets))]
    for i, title in enumerate(header):
        table[i].append(title)
    for i in range(length):
        line = input()
        for k, (x, y) in enumerate(zip(offsets, offsets[1:] + [len(line)*2])):
            table[k].append(line[x:y].strip())
    return table


def build_code(table):
    code = []
    styles = '''        <style type="text/css">
            body {
                background-color: #fff; 
                color: #222; 
                font-family: sans-serif;
                font-size: 12pt;
            }
            table {
                margin:0 auto;
                text-align: left;
                border-collapse: collapse; 
                border: 0; 
                width: 934px; 
                box-shadow: 1px 2px 3px #ccc;
            }
            td, th {
                border: 1px solid #666; 
                vertical-align: baseline; 
                padding: 4px 5px;
            }
            thead tr {
                background-color: #99c; 
                font-weight: bold;
                font-size: 14pt;
            }
            tbody tr {
                background-color: #ddd; 
                max-width: 300px; 
                overflow-x: auto; 
                word-wrap: break-word;
            }
            </style>'''
    code.extend([
        '<!DOCTYPE html>',
        '<html>',
        '    <head>',
        '        <title>Shooting Kers</title>',
        styles,
        '    </head>',
        '    <body>',
        '        <table>',
        '            <thead>',
        '                <tr>'
    ])
    for i in range(len(table)):
        code.append('                    <td>%s</td>' % table[i][0].upper())
    code.extend([
        '                </tr>',
        '            </thead>',
        '            <tbody>',
    ])
    table_iter = zip(*table)
    next(table_iter)
    for line in table_iter:
        code.append('                <tr>')
        for element in line:
            code.append('                    <td><pre>%s</pre></td>' % escape(element))
        code.append('                </tr>')
    code.extend([
        '            </tbody>',
        '        </table>',
        '    </body>',
        '<html>'
    ])
    return '\n'.join(code)


def main():
    table = read_table()
    html = build_code(table)
    print(html)


if __name__ == '__main__':
    main()
