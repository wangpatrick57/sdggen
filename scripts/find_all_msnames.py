#!/opt/homebrew/bin/python3
import subprocess
import os
from cg_tab_helpers import *

def get_chunk_header(chunk_num):
    return f'MSCallGraph_{chunk_num}'

def assert_chunk_num(chunk_num):
    assert 0 <= chunk_num <= 144

def get_msnames_path(ci, cj):
    assert ci <= cj
    return f'../ourdata/msnames_{ci}_{cj}.txt'

def create_nodes_for_chunk(chunk_num):
    assert_chunk_num(chunk_num)

def unzip_chunk_targz(chunk_num):
    assert_chunk_num(chunk_num)
    targz_path = f'../data/{get_chunk_header(chunk_num)}.tar.gz'
    csv_path = f'../data/{get_chunk_header(chunk_num)}.csv'

    if os.path.exists(csv_path):
        print(f'csv exists for {chunk_num}')
    else:
        print(f'unzipping {targz_path}')
        subprocess.run(f'tar -xvf {targz_path}'.split())

def write_msnames(path, msnames):
    lines = [msname + '\n' for msname in msnames]

    with open(path, 'w') as f:
        f.writelines(lines)

def read_in_msnames(path):
    msnames = set()

    with open(path, 'r') as f:
        for line in f:
            msname = line.strip()
            msnames.add(msname)

    return msnames

def merge_msnames(i, j, k):
    path1 = get_msnames_path(i, j)
    path2 = get_msnames_path(j + 1, k)
    assert os.path.exists(path1) and os.path.exists(path2)
    msnames1 = read_in_msnames(path1)
    msnames2 = read_in_msnames(path2)
    merged_path = get_msnames_path(i, k)
    merged_msnames = msnames1.union(msnames2)
    write_msnames(merged_path, merged_msnames)
    os.remove(path1)
    os.remove(path2)

def create_base_msnames(chunk_num):
    assert_chunk_num(chunk_num)

    csv_path = f'../ourdata/{get_chunk_header(chunk_num)}.csv'
    msnames_path = get_msnames_path(chunk_num, chunk_num)

    if os.path.exists(msnames_path):
        print(f'msnames exists for {chunk_num}')
    else:
        print(f'creating {msnames_path}')
        cg_tab = read_in_call_graph_table(csv_path)
        msnames = get_msnames(cg_tab)
        write_msnames(msnames_path, msnames)

def mass_create_base_msnames(start, end):
    for i in range(start, end):
        unzip_chunk_targz(i)
        create_base_msnames(i)

def incrementally_merge_msnames(start_i, start_j, target):
    assert start_i <= start_j and start_j <= target
    i = start_i
    j = start_j

    while j < target:
        merge_msnames(i, j, j + 1)
        j += 1

if __name__ == '__main__':
    incrementally_merge_msnames(0, 6, 39)
