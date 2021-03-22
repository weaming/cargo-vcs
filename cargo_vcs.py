#!/usr/bin/env python3
# Author    : weaming

import os, sys
import requests
import tarfile
import argparse


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
    tf = f'{name}-{version}.tar'

    try:
        if not os.path.isfile(tf):
            versions = get_versions(name)
            print('versions:', ', '.join(x['num'] for x in versions), file=sys.stderr)
            if args.version == 'latest':
                version = versions[-1]
            else:
                for v in versions:
                    if v['num'] == args.version:
                        version = v

            dl_url = 'https://crates.io' + version['dl_path']

            print(dl_url, file=sys.stderr)
            with open(tf, 'wb') as f:
                f.write(requests.get(dl_url).content)

        fname = '.cargo_vcs_info.json'
        with tarfile.open(tf, "r") as tar:
            for x in tar.getmembers():
                if fname in x.name:
                    print('found', x.name, file=sys.stderr)
                    f = tar.extractfile(x)
                    print(f.read().decode())
                    break
            else:
                print('not found', fname, file=sys.stderr)
    finally:
        if os.path.isfile(tf):
            os.remove(tf)


if __name__ == "__main__":
    main()
