#! /usr/bin/env python
import collections, hashlib, os, sys


def scanFileSizes(paths):
    fileSizeDict = collections.defaultdict(list)
    for path in paths:
        if not os.path.exists(path):
            raise Exception('Invalid path: %s' % path)
        for root, dirs, files in os.walk(path):
            print('Scanning: ', root)
            for shortName in files:
                fullName = os.path.join(root, shortName)
                fileSize = os.path.getsize(fullName)
                fileSizeDict[fileSize].append(fullName)
    #print(fileSizeDict)
    return fileSizeDict

def file_md5(filename):
    hashAlg = hashlib.md5()
    with open(filename, 'rb') as f:
        buf = f.read(256 * 1024)
        while len(buf) > 0:
            hashAlg.update(buf)
            buf = f.read(256 * 1024)
    return hashAlg.hexdigest()

def findDups(fileSizeDict):
    # dict: (file size, dict: (md5, filenames))
    result = {}
    for size, files in fileSizeDict.items():
        if len(files) > 1:
            hashes = collections.defaultdict(list)
            for f in files:
                print('Hashing: ', f)
                md5 = file_md5(f)
                hashes[md5].append(f)
            for md5, dups in hashes.items():
                if len(dups) > 1:
                    result[size] = {md5: dups}
    return result


if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileSizeDict = scanFileSizes(sys.argv[1:])
        fileDups = findDups(fileSizeDict)
        #print(fileDups)
        if fileDups:
            print('Duplicates:')
            for size, dups in sorted(fileDups.items()):
                print('Size: ', size)
                for md5, files in dups.items():
                    print('MD5: ', md5)
                    for f in files:
                        print(f)
                print('---')
        else:
            print('No duplicates found')
    else:
        print('Usage: python dupFinder.py <directories...>')
