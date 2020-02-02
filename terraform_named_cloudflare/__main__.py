#!/usr/bin/env python3

import argparse
import jinja2
import re

A = re.compile(pattern=r'^([*a-zA-z0-9.-]+)\s+(\d+)?\s+?IN\s+A\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})')
AAAA = re.compile(pattern=r'^([*a-zA-z0-9.-]+)\s+(\d+)?\s+IN\s+AAAA\s+(.[^$]*)')
CNAME = re.compile(pattern=r'^([*a-zA-z0-9.-]+)\s+(\d+)?\s+?IN\s+CNAME\s+([a-zA-z0-9.-]+)')
MX = re.compile(pattern=r'^([a-zA-z0-9.-]+)\s+(\d+)?\s+?IN\s+MX\s+(\d+)\s+([a-zA-z0-9.-]+)')
SRV = re.compile(pattern=r'^(((_.[^.]*).(_[^.][a-z]+)(.[^\s]*)?)\s+(\d+)\s+IN\s+SRV\s+(\d+)\s+(\d+)\s+(\d+)\s+(.*))')
TXT = re.compile(pattern=r'^([a-zA-z0-9.-]+)\s+(\d+)?\s+?IN\s+TXT\s+(.*)')

records = {
    'A': {},
    'AAAA': {},
    'CNAME': {},
    'MX': {},
    'SRV': {},
    'TXT': {}
}


def comment(record):
    match = re.match(r'^;.*', record)
    if match:
        return True
    return False


def a(record):
    match = re.match(A, record)
    if match:
        records['A'][match.group(1)] = {
            'name': match.group(1),
            'ttl': match.group(2),
            'value': match.group(3)
        }
        return True
    return False


def aaaa(record):
    match = re.match(AAAA, record)
    if match:
        records['AAAA'][match.group(1)] = {
            'name': match.group(1),
            'ttl': match.group(2),
            'value': match.group(3)
        }
        return True
    return False


def cname(record):
    match = re.match(CNAME, record)
    if match:
        records['CNAME'][match.group(1)] = {
            'name': match.group(1),
            'ttl': match.group(2),
            'value': match.group(3)
        }
        return True
    return False


def mx(record):
    match = re.match(MX, record)
    if match:
        records['MX'][match.group(1)] = {
            'name': match.group(1),
            'priority': match.group(3),
            'ttl': match.group(2),
            'value': match.group(4)
        }
        return True
    return False


def srv(record):
    match = re.match(SRV, record)
    if match:
        records['SRV'][match.group(2)] = {
            'name': match.group(2),
            'port': match.group(9),
            'priority': match.group(7),
            'proto': match.group(4),
            'service': match.group(3),
            'target': match.group(10),
            'ttl': match.group(6),
            'weight': match.group(8)
        }
        return True
    return False


def txt(record):
    match = re.match(TXT, record)
    if match:
        value = match.group(3).replace('"', '')
        if re.match(r'.*DKIM', value):
            value = '; '.join(re.sub(pattern=r'\s+|\\;', repl='', string=value).split(';'))
        records['TXT'][match.group(1)] = {
            'name': match.group(1),
            'ttl': match.group(2),
            'value': value
        }
        return True
    return False


def parse_arguments():
    """
    Function to handle argument parser configuration (argument definitions, default values and so on).
    :return: :obj:`argparse.ArgumentParser` object with set of configured arguments.
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--file',
        help='Path to the Bind9 zone file to be converted',
        required=True,
        type=str
    )
    parser.add_argument(
        '-i',
        '--zone-id',
        default=str(),
        help='Optional CloudFlare zone ID',
        type=str
    )
    parser.add_argument(
        '-n',
        '--zone-name',
        default=str(),
        help='Optional CloudFlare zone name',
        type=str
    )
    return parser


def parse_zone(zone_file):
    with open(zone_file, 'r') as fp:
        for record in fp.read().split('\n'):
            if not comment(record=record):
                if a(record=record):
                    continue
                if aaaa(record=record):
                    continue
                if cname(record=record):
                    continue
                if mx(record=record):
                    continue
                if srv(record=record):
                    continue
                if txt(record=record):
                    continue
                print(record)


def render(known_args):
    env = jinja2.Environment(loader=jinja2.PackageLoader('terraform_named_cloudflare', 'templates'))
    template = env.get_template('variables.tf.j2')
    with open('variables.tf', 'w') as target:
        target.write(template.render(cloudflare_zone_id=known_args.zone_id, cloudflare_zone_name=known_args.zone_name))
    for item in records:
        template = env.get_template('{}.tf.j2'.format(item))
        with open('{}.tf'.format(item), 'w') as target:
            target.write(template.render(records=records[item]))


def main():
    known_args, unknown_args = parse_arguments().parse_known_args()
    parse_zone(zone_file=known_args.file)
    render(known_args)


if __name__ == '__main__':
    main()
