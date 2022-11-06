#!/opt/homebrew/bin/python3
from collections import namedtuple

# Findings
#  * There are 6088846 rows
#  * There are 130512 unique traceids

CallGraphRow = namedtuple('CallGraphRow', ['traceid', 'timestamp', 'rpcid', 'um', 'rpctype', 'dm', 'interface', 'rt'])
IGNORED_MSNAMES = ['', '(?)']

def read_in_call_graph_table(fname, num_to_read=None):
    cg_tab = []

    with open(fname, 'r') as f:
        for line in f:
            if line[0] == ',': # only the first row looks like this
                continue

            splitted = line.strip().split(',')
            splitted = splitted[1:] # ignore first column
            row = CallGraphRow._make(splitted)
            cg_tab.append(row)

            if num_to_read != None and len(cg_tab) >= num_to_read:
                break

    return cg_tab

def write_call_graph_table(fname, cg_tab):
    lines = [',traceid,timestamp,rpcid,um,rpctype,dm,interface,rt\n']
    lines += [f'{i},' + ','.join(row) + '\n' for i, row in enumerate(cg_tab)]

    with open(fname, 'w') as f:
        f.writelines(lines)

def write_el(fname, el):
    lines = ['\t'.join(edge) + '\n' for edge in el]

    with open(fname, 'w') as f:
        f.writelines(lines)

def write_chord_data(fname, el):
    lines = [','.join(edge) + ',1\n' for edge in el]

    with open(fname, 'w') as f:
        f.writelines(lines)

def create_el(cg_tab):
    el = set()

    for row in cg_tab:
        if row.um not in IGNORED_MSNAMES and row.dm not in IGNORED_MSNAMES:
            el.add((row.um, row.dm))

    return list(el)

def get_msnames(cg_tab):
    ums = {row.um for row in cg_tab if row.um not in IGNORED_MSNAMES}
    dms = {row.dm for row in cg_tab if row.dm not in IGNORED_MSNAMES}
    return ums.union(dms)

if __name__ == '__main__':
    cg_tab = read_in_call_graph_table('../data/MSCallGraph_0.csv', num_to_read=1000)
    el = create_el(cg_tab)
    print(len(el))
    write_chord_data('../ourdata/MSCallGraph_0.el', el)
