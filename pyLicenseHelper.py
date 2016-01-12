#! /usr/bin/python
import pkg_resources
import sys
import getopt
import argparse
import csv

HEADERS = ["Version", "Homepage", "License", "package"]


def get_parser():
    description = 'Get the licenses for your requirements.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--package',
                        dest='package',
                        action='store',
                        help='name of the package to be scanned')
    parser.add_argument('--csv',
                        dest='csv_file',
                        action='store',
                        help='name of the file to write to')
    parser.add_argument('--req',
                        dest='requirements_file',
                        action='store',
                        help='name of the requirements.txt file')
    return parser


def main(initial_args):
    parser = get_parser()
    cooked_args = parser.parse_args(initial_args)

    if cooked_args.package:
        get_pkg_license(cooked_args.package)
    elif cooked_args.requirements_file:
        package_infos = [HEADERS]
        with open(cooked_args.requirements_file) as f:
            content = f.readlines()
            for line in content:
                package = line.split('==', 1)[0]
                package_infos.append(get_pkg_license(package))
        if cooked_args.csv_file:
            write_csv(package_infos, cooked_args.csv_file)
        else:
            print package_infos
    else:
        parser.print_help()


def write_csv(data, file):
    with open(file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def get_pkg_license(package):
    info = {"License": "Unknown",
            "Package": package,
            "Home-page": "Unkown",
            "Version": "Unkown"}
    try:
        pkgs = pkg_resources.require(package)
    except pkg_resources.DistributionNotFound:
        return info.values()
        return
    pkg = pkgs[0]
    meta_files_to_check = ['PKG-INFO', 'METADATA']
    try:
        for metafile in meta_files_to_check:
            if not pkg.has_metadata(metafile):
                continue
            for line in pkg.get_metadata_lines(metafile):
                try:
                    (k, v) = line.split(': ', 1)
                    if k in ["License", "Home-page", "Version"]:
                        info[k] = v
                except:
                    pass
    except:
        pass
    return info.values()


if __name__ == "__main__":
    main(sys.argv[1:])
