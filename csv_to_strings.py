#!/usr/bin/env python3
import argparse
import csv
import pathlib
import re
from collections import defaultdict
from pathlib import Path
from typing import List, Dict
from xml.etree import ElementTree


def to_strings(csv_path: Path, res_path: Path):
    print(f"Going to convert csv from {csv_path} to {res_path}")

    known_langs_with_indices: Dict[str, int] = {}
    basic_strings: Dict[str, List[ElementTree]] = defaultdict(list)
    plurals: Dict[str, Dict[str, Dict[str, str]]] = defaultdict(lambda: defaultdict(dict))

    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header_row = next(reader)
        if header_row[0] != 'key':
            raise Exception('The csv file does not have key as the first element of the first row')
        for i, lang in enumerate(header_row[1:]):
            if not lang:
                break
            known_langs_with_indices[lang] = i + 1
        print(f'Found languages: {", ".join(known_langs_with_indices.keys())}')
        for row in reader:
            row_key = row[0]
            plural_match = re.match(r'plural__(?P<plural_name>.*)__(?P<plural_quantity>.*)', row_key)
            for lang, index in known_langs_with_indices.items():
                contents_in_lang = row[index]
                if plural_match:
                    plural_name = plural_match.group('plural_name')
                    plural_quantities = plural_match.group('plural_quantity')
                    plurals[lang][plural_name][plural_quantities] = contents_in_lang
                elif contents_in_lang:
                    elem = f"""<string name="{row_key}">{contents_in_lang.replace('&', '&amp;')}</string>"""
                    try:
                        basic_strings[lang].append(ElementTree.fromstring(elem))
                    except Exception as e:
                        print(f"Could not parse: {elem}")
                        raise e

    plurals_elems: Dict[str, List[ElementTree]] = defaultdict(list)
    for lang in known_langs_with_indices.keys():
        plurals_in_lang = plurals[lang]
        for (plural_key, plural_quantities) in plurals_in_lang.items():
            plurals_elem = ElementTree.Element('plurals')
            plurals_elem.set('name', plural_key)
            for (quantity, txt) in plural_quantities.items():
                elem = f"""<item quantity="{quantity}">{txt}</item>"""
                plurals_elem.append(ElementTree.fromstring(elem))
            plurals_elems[lang].append(plurals_elem)

    for lang in known_langs_with_indices.keys():
        root = ElementTree.Element('resources')
        root.extend(basic_strings[lang])
        root.extend(plurals_elems[lang])
        target_path_for_lang = res_path / ('values' if lang == 'en' else f'values-{lang}')
        target_path_for_lang.mkdir(exist_ok=True)
        target_file = target_path_for_lang / 'strings.xml'
        tree = ElementTree.ElementTree(root)
        ElementTree.indent(tree)
        tree.write(target_file, encoding='utf-8')
        with open(target_file, mode='a') as open_target:
            open_target.write('\n')
        print(f'Wrote {target_file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Convert a previously exported csv file back to strings.xml files'''
    )
    parser.add_argument('csv_path', type=pathlib.Path, help='input csv file')
    parser.add_argument('res_path', type=pathlib.Path,
                        help='path to target res -directory, For example "~/AndroidStudioProjects/MyApp/app/src/main/res"')
    args = parser.parse_args()
    to_strings(args.csv_path, args.res_path)
