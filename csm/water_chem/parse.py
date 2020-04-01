#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Date   : 2020-03-27
Purpose: Parse water chemistry data
"""

import argparse
import os
import re
import sys
import io
from itertools import chain, starmap
from pprint import pprint
from collections import defaultdict, Counter
from typing import Dict, List, TextIO, NamedTuple


class Args(NamedTuple):
    file: TextIO
    outdir: str


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Parse water chemistry data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        nargs='+',
                        type=argparse.FileType('rt', encoding='utf-8'),
                        help='Input file')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='DIR',
                        type=str,
                        default='out')

    args = parser.parse_args()

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    return Args(args.file, args.outdir)


# --------------------------------------------------
def main() -> None:
    """Make a jazz noise here"""

    args = get_args()

    file_num = 0
    for i, file in enumerate(args.file, start=1):
        print(f'{i:3}: {file.name}')

        sections = find_sections(file)
        basename = os.path.basename(file.name)
        root, _ = os.path.splitext(basename)

        icp = 'icp_aes'
        if icp not in sections:
            print(f'File "{file.name}" missing section "{icp}"!',
                  file=sys.stderr)
            continue

        icp_aes = sections[icp]
        master_header = icp_aes.pop(0)
        sections[icp] = icp_aes

        for section, raw in sections.items():
            hdrs, data = parse_section(section, master_header, raw)
            if data:
                out_file = write_out(data, hdrs, args.outdir,
                                     f'{root}_{section}.csv')

                if out_file:
                    file_num += 1

    print(f'Done, see output in "{args.outdir}".')


# --------------------------------------------------
def write_out(data: List[dict], headers: List[str], out_dir: str,
              filename: str) -> bool:
    """ Write data to file """

    if not data:
        return

    # Get rid of the empty fields
    headers = list(filter(lambda s: len(s) > 0, headers))

    out_file = os.path.join(out_dir, filename)
    fh = open(out_file, 'wt')
    fh.write(','.join(headers) + '\n')

    for rec in data:
        fh.write(','.join(map(lambda f: rec.get(f, ''), headers)) + '\n')

    fh.close()

    return out_file


# --------------------------------------------------
def expand_master_header(hdr: str) -> List[str]:
    """ Expand the master header """

    flds = re.split('([^,]+)', hdr[2:])[1:]

    new_flds = []
    while flds:
        name, commas = flds.pop(0), flds.pop(0)
        new_flds.append(replicate(name, len(commas)))

    return list(chain.from_iterable(new_flds))


# --------------------------------------------------
def test_expand_master_header() -> None:
    """ Test """

    sub = (',,Ref1,,,,,,,,ANT,,,,,,,,RAP,,,,,,,,RBP,,,,,,,,'
           'ARG,,,,,,,,USGS,,,,,,,')

    expected = list(
        chain.from_iterable(
            map(lambda s: replicate(s, 8),
                ['Ref1', 'ANT', 'RAP', 'RBP', 'ARG', 'USGS'])))

    assert expand_master_header(sub) == expected


# --------------------------------------------------
def replicate(s, n):
    """ Replicate a value n times """

    return [s for _ in range(n)]


# --------------------------------------------------
def test_replicate() -> None:
    """ Replicate a value n times """

    assert replicate('foo', 1) == ['foo']
    assert replicate('bar', 2) == ['bar', 'bar']


# --------------------------------------------------
def parse_section(name: str, master_header: List[str],
                  data: List[str]) -> (str, List[Dict[str, str]]):
    """ Parse a section """
    def split(line):
        return line.split(',')

    this_header = split(data.pop(0))
    master_header = split(master_header)

    # print(f'name "{name}"')
    # print(f'master_header "{master_header}"')
    # print(f'header "{this_header}"')

    # start off with the 1st 2 flds
    headers = this_header[:2] + unique_names(
        merge_headers(repeater(master_header[2:]), this_header[2:]))
    headers[0] = 'measurement'
    headers = list(map(normalize, headers))

    # print(headers)

    def num_col(i, val):
        if i >= 2:
            try:
                val = str(float(val))
            except Exception:
                val = ''
        return val

    ret = []
    for row in map(split, data):
        row = starmap(num_col, enumerate(row))
        ret.append(dict(filter(all, zip(headers, row))))

    return headers, ret


# --------------------------------------------------
def merge_headers(hdr1: List[str], hdr2: List[str]) -> List[str]:
    """ Merge sub/headers """
    def join(t):
        return '_'.join(t) if all(t) else t[1] if t[1] else ''

    return list(map(join, filter(any, zip(hdr1, popper(hdr2)))))


# --------------------------------------------------
def test_merge_headers() -> None:
    """ Test """

    master_header = repeater(',,BNT,,,ATP,,,RG,,,'.split(','))
    header = 'Analyte Name,DL (mg/l),RA,FA,Tox,RA,FA,Tox,RA,FA,Tox,'.split(',')

    # trim to the shortest
    wanted = min(len(master_header), len(header))

    def trimmer(l):
        if len(l) > wanted:
            l = l[:wanted]
        return l

    master_header = trimmer(master_header)
    header = trimmer(header)

    assert merge_headers(master_header, header) == [
        'Analyte Name', 'DL (mg/l)', 'BNT_RA', 'BNT_FA', 'BNT_Tox', 'ATP_RA',
        'ATP_FA', 'ATP_Tox', 'RG_RA', 'RG_FA', 'RG_Tox'
    ]


# --------------------------------------------------
def popper(vals: List[str]) -> List[str]:
    """ Remove missing values from the end of a list """

    while vals and not vals[-1]:
        vals.pop()

    return vals


# --------------------------------------------------
def test_popper() -> None:
    """ Test """

    assert popper(['foo']) == ['foo']
    assert popper(['foo', 'bar']) == ['foo', 'bar']
    assert popper(['foo', 'bar', '']) == ['foo', 'bar']
    assert popper(['foo', 'bar', '', None]) == ['foo', 'bar']


# --------------------------------------------------
def repeater(names: List[str]) -> List[str]:
    """ Repeat a value until the next """

    last = ''
    ret = []
    for name in names:
        ret.append(name or last)
        last = name if name else last
    return ret


# --------------------------------------------------
def test_repeater() -> None:
    """ Test """

    assert repeater(',,BNT,,,ATP,,,RG,,,'.split(',')) == [
        '', '', 'BNT', 'BNT', 'BNT', 'ATP', 'ATP', 'ATP', 'RG', 'RG', 'RG',
        'RG'
    ]


# --------------------------------------------------
def reader(fh):
    """ Handle BOM (byte order mark) in Excel output """

    BOM = "\ufeff"
    text = fh.read()
    if text.startswith(BOM):
        text = text[1:]

    return io.StringIO(text)


# --------------------------------------------------
def find_sections(fh: TextIO) -> Dict[str, List[str]]:
    """ Find the major sections: ICP-AES, IC, Field Data, DOC/TOC """

    sections = defaultdict(list)
    header = re.compile("^(ICP-AES|IC|Field Data|DOC/TOC),{1,}$")
    all_commas = re.compile("^,{1,}$")
    last_header = ''

    for line in map(str.rstrip, reader(fh)):
        hdr = header.match(line)
        empty_line = all_commas.match(line)

        if hdr:
            group = normalize(hdr.group(1))
            last_header = group
        elif last_header and not empty_line:
            sections[last_header].append(line)

    return sections


# --------------------------------------------------
def normalize(s):
    """ Normalize a string """

    return re.sub('[^a-z0-9_]', '_', re.sub('[()]', '', s.lower()))


# --------------------------------------------------
def unique_names(names):
    """ Make all names unique """

    counts = Counter(names)
    seen = {}
    new_names = []
    for name in names:
        if name and counts[name] > 1:
            n = seen.get(name, 1)
            seen[name] = n + 1
            name += f'_{n}'
        new_names.append(name)

    return new_names


# --------------------------------------------------
def test_unique_names():
    """ Test """

    assert unique_names('foo bar foo'.split()) == ['foo_1', 'bar', 'foo_2']
    assert unique_names('DOC1 DOC2 Avg StDev TOC1 TOC2 Avg StDev'.split(
    )) == 'DOC1 DOC2 Avg_1 StDev_1 TOC1 TOC2 Avg_2 StDev_2'.split()


# --------------------------------------------------
if __name__ == "__main__":
    main()
