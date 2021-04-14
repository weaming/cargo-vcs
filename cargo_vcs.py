#!/usr/bin/env python3
# Author    : weaming

import os, sys
import requests
import tarfile
import argparse
from io import BytesIO


def get_versions(name):
    return requests.get(f'https://crates.io/api/v1/crates/{name}').json()['versions']


def main():
    # fix called by cargo
    if 'vcs' == sys.argv[1]:
        sys.argv[1:2] = []

    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("-v", "--version", default='latest')
    args = parser.parse_args()

    name = args.name
    version = args.version

    versions = get_versions(name)
    print('versions:', ', '.join(x['num'] for x in versions), file=sys.stderr)
    if args.version == 'latest':
        version = versions[0]
    else:
        for v in versions:
            if v['num'] == args.version:
                version = v

    dl_url = 'https://crates.io' + version['dl_path']

    print(dl_url, file=sys.stderr)
    tf = BytesIO(requests.get(dl_url).content)

    fname = '.cargo_vcs_info.json'
    with tarfile.open(fileobj=tf, mode='r') as tar:
        for x in tar.getmembers():
            if fname in x.name:
                print('found', x.name, file=sys.stderr)
                f = tar.extractfile(x)
                print(f.read().decode())
                break
        else:
            print('not found', fname, file=sys.stderr)


if __name__ == "__main__":
    main()
