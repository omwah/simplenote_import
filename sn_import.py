#!/usr/bin/env python

import os
import sys
from ever2simple.converter import EverConverter
import argparse
import simplenote
import dateutil.parser as date_parser

def import_simplenote(enex_filename, sn_username, sn_password):
    converter = EverConverter(enex_filename)

    with open(enex_filename) as enex_file:
        xml_tree = converter._load_xml(enex_file)
    ev_notes = converter.prepare_notes(xml_tree)

    sn = simplenote.Simplenote(sn_username, sn_password)
    
    for ev_note in ev_notes:
        sn_note = {}

        # Convert times to Unix timestamps
        sn_note['createdate'] = date_parser.parse(ev_note['createdate']).strftime('%s')
        sn_note['modifydate'] = date_parser.parse(ev_note['modifydate']).strftime('%s')

        # Encode as UTF-8 as that is what simplenote expects, it doesn't
        # like taking unicode strings in directly
        sn_note['content'] = ev_note['content'].encode('utf-8')
        sn_note['tags'] = ev_note['tags']

        sn.add_note(sn_note)

def main():
    parser = argparse.ArgumentParser(prog=None, description="Import Evernote.enex files into simplenote", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('enex_file', help="the path to the Evernote.enex file")
    parser.add_argument('-u', '--username', help='simplenote username', required=True)
    parser.add_argument('-p', '--password', help='simplenote password', required=True)

    args = parser.parse_args()

    import_simplenote(args.enex_file, args.username, args.password)

if __name__ == '__main__':
    main()
