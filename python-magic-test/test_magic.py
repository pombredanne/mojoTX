#!/usr/bin/env python2
# Test program for Python magic
# https://github.com/ahupp/python-magic
import os, sys, codecs, magic, argparse, pprint

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple test of Python magic (sudo pip install python-magic)")
    parser.add_argument("input_directory", type=str, nargs=1, help="Name of directory to parse")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-d", "--debug", help="launch interactive debugger before magic", action="store_true")
    parser.add_argument("-u", "--unicode", help="Specify whether to use Unicode for initializing source directory", action="store_true")

    args=parser.parse_args()
    verbose = args.verbose
    debug   = args.debug
    if args.unicode:
        SOURCEDIR = unicode(args.input_directory[0] )
    else:
        SOURCEDIR = args.input_directory[0]

    all_files={}

    for dirname, dirnames, filenames in os.walk(SOURCEDIR):
        for file in filenames:

            filename = os.path.join(dirname, file )

            if verbose:
                print "getfilesystemencoding() = %s" % sys.getfilesystemencoding()
                print "Filename: %s" % pprint.pformat(filename)
                print " Dirname: %s" % pprint.pformat(dirname)

            try:
                if debug:
                    import pdb; pdb.set_trace()
                mime_type = magic.from_file(filename, mime=True)
                file_type = magic.from_file(filename, mime=False)
            except UnicodeDecodeError as e:
                print >> sys.stderr, "SKIPPING FILE %s:  Unicode Decode Error for encoding %s between index %d and %d:  %s" % ( e.object, e.encoding, e.start, e.end, e.reason )
                continue
            except magic.MagicException as e:
                print >> sys.stderr, "SKIPPING FILE %s:  Weird MagicException caused by libmagic1 Ubuntu package (working on this) " % filename
                continue

            if verbose:
                print >> sys.stderr, "Found %s (%s):  %s" % ( filename, mime_type, file_type )

            file_data = {
                    'file-name': filename,
                    'mime-type': mime_type,
                    'file_type': file_type
            }

            all_files[filename] = file_data

    if len(all_files) > 0:
        pprint.pprint( all_files, indent=2 )
    else:
        print "No files found to test."

