#!/usr/bin/env python3
import argparse
import csv
import pathlib
import re
from collections import defaultdict
from pathlib import Path
from typing import List, Set, Dict, Tuple
from xml.etree import ElementTree


def to_csv(out_file: Path, res_path: Path):
    print(f"Looking up strings.xmls from {res_path}")
    strings_files: List[pathlib.Path] = list(res_path.rglob('strings.xml'))
    print(f"Found files {['/'.join(list(f.parts)[-2:]) for f in strings_files]}")

    known_langs: Set[str] = set()
    keys_to_translations: Dict[str, Dict[str, str]] = defaultdict(dict)

    strings_file_for_lang: Path
    for strings_file_for_lang in strings_files:
        lang = re.match(r"values-?(?P<lang>.+)?", strings_file_for_lang.parent.name).group('lang') or 'en'
        known_langs.add(lang)
        for element in ElementTree.parse(strings_file_for_lang).getroot():
            type_tag = element.tag
            if type_tag == 'string':
                string_key = element.attrib['name']
                if len(element) > 0:
                    concatenated = ""
                    if element.text:
                        concatenated += element.text
                    for e in element:
                        concatenated += ElementTree.tostring(e, encoding='unicode', method='xml')
                    keys_to_translations[string_key][lang] = concatenated
                else:
                    keys_to_translations[string_key][lang] = element.text
            elif type_tag == 'plurals':
                plural_name = element.attrib['name']
                for plural_variation in element:
                    plural_key = f"plural__{plural_name}__{plural_variation.attrib['quantity']}"
                    keys_to_translations[plural_key][lang] = plural_variation.text
            else:
                print(f"Unknown strings.xml entry: '{type_tag}'")

    # noinspection PyTypeChecker
    sorted_keys_with_translations: List[Tuple[str, Dict[str, str]]] = sorted(keys_to_translations.items())
    with open(out_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        sorted_known_langs = sorted(known_langs)
        writer.writerow(['key'] + list(sorted_known_langs))
        for key_with_item in sorted_keys_with_translations:
            writer.writerow([key_with_item[0]] + [key_with_item[1].get(_lang) for _lang in sorted_known_langs])
    print(f"Wrote {len(sorted_keys_with_translations)} keys in {len(sorted_known_langs)} languages to {out_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Convert strings.xml -files to csv'''
    )
    parser.add_argument('out_file', type=pathlib.Path, help='output file')
    parser.add_argument('res_path', type=pathlib.Path,
                        help='path to res -directory, For example "~/AndroidStudioProjects/MyApp/app/src/main/res"')
    args = parser.parse_args()
    to_csv(args.out_file, args.res_path)
