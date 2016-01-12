#! /usr/bin/python
import pkg_resources
import sys
import getopt


def main(initial_args):
    requirements_file = ""
    package = ""
    try:
        opts, args = getopt.getopt(initial_args,
                                   "hr:p:",
                                   [])
    except getopt.GetoptError:
        print 'test.py -r <requirements file> -p <individual package>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -r <requirements file> -p <individual package>'
            sys.exit()
        elif opt in ("-r"):
            requirements_file = arg
            if len(requirements_file) > 0:
                with open(requirements_file) as f:
                    content = f.readlines()
                    for line in content:
                        stuff = line.split('==', 1)
                        get_pkg_license(stuff[0])
        elif opt in ("-p"):
            package = arg
            get_pkg_license(package)


def get_pkg_license(package):
    info = {"License": "Unknown",
            "Package": package,
            "Home-page": "Unkown",
            "Version": "Unkown"}
    try:
        pkgs = pkg_resources.require(package)
    except pkg_resources.DistributionNotFound:
        print info.values()
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
    print info.values()


if __name__ == "__main__":
    main(sys.argv[1:])
