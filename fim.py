import sys
import hashlib
import os
import json
from pathlib import Path
import logging
import argparse
import time

logging.basicConfig(filename="change.log", filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")

path = os.getcwd()
hash_exist = Path("hash.json")
change_log = Path("change.log")

type_of_hash_algorithm = ['sha224', 'sha256', 'sha384', 'sha512', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'blake2b', 'blake2s', 'sha1', 'md5']


def hashfile(fi, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)

    with open(fi, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)

    return hash_func.hexdigest()


def list_file(path):
    dir_list = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file in {'hash.json', 'change.log'}:
                continue

            dir_list.append(os.path.join(root, file))

    return dir_list


def dict_hash(dir_list, algorithm):
    x = {}
    x['algorithm'] = algorithm

    for i in dir_list:
        x[i] = {
            'hash': hashfile(i, algorithm),
            'filesize': os.path.getsize(i),
            'modification_time': os.path.getmtime(i)
        }

    return x


def write_in_json_file(path_hash):
    with open('hash.json', 'w') as f:
        json.dump(path_hash, f, indent=4)


def read_json():
    with open('hash.json', 'r') as f:
        hashf = json.load(f)

    return hashf


def compare_d(path_hash, hashf):
    current_algorithm = path_hash.get('algorithm')
    stored_algorithm = hashf.get('algorithm')

    if current_algorithm != stored_algorithm:
        print(f'Algorithm mismatch: current={current_algorithm}, stored={stored_algorithm}')
        return

    path_hash.pop('algorithm', None)
    hashf.pop('algorithm', None)

    for key in path_hash:
        if key not in hashf:
            print(f'The file {key} is new')
            logging.warning(f'The file {key} is new')
            continue

        if path_hash[key]['hash'] != hashf[key]['hash']:
            print(f'Content changed: {key}')
            logging.warning(f'Content changed: {key}')
        else:
            print(f'No content change: {key}')

        if path_hash[key]['filesize'] != hashf[key]['filesize']:
            print(f'Size changed: {key}')
            logging.warning(f'Size changed: {key}')

        if path_hash[key]['modification_time'] != hashf[key]['modification_time']:
            print(f'Modification time changed: {key}')
            logging.warning(f'Modification time changed: {key}')

    for key in hashf:
        if key not in path_hash:
            print(f'The file {key} was deleted')
            logging.warning(f'The file {key} was deleted')


def check_hash_json():
    if not hash_exist.exists():
        print('hash.json does not exist. Please use --init first.')
        return

    hashf = read_json()
    stored_algorithm = hashf.get('algorithm')

    if stored_algorithm not in type_of_hash_algorithm:
        print('Invalid or missing algorithm in hash.json.')
        return

    if args.algorithm and args.algorithm.lower() != stored_algorithm:
        print(f'Algorithm mismatch: hash.json uses {stored_algorithm}, but you selected {args.algorithm.lower()}.')
        sys.exit(1)

    dir_list = list_file(path)
    path_hash = dict_hash(dir_list, stored_algorithm)

    compare_d(path_hash, hashf)

    

parser = argparse.ArgumentParser(description='File Integrity Monitoring Program')

parser.add_argument('-i', '--init', action='store_true', help='Initialize the program')
parser.add_argument('-u', '--update', action='store_true', help='Update hash values')
parser.add_argument('-c', '--check', action='store_true', help='Check for changes')
parser.add_argument('-w', '--watch', action='store_true', help='real time check')
parser.add_argument("-t", "--time", type=int, help="time of real time check in second")
parser.add_argument('algorithm', nargs='?', help='Hash algorithm')

args = parser.parse_args()

algorithm = 'sha256'
t = 60

if args.time is not None and not args.watch:
    parser.error('--time can only be used with --watch')

if args.algorithm:
    algorithm = args.algorithm.lower()

    if algorithm not in type_of_hash_algorithm:
        print('Choose one of these algorithms: [sha224, sha384, sha512, sha256, sha1, md5]')
        sys.exit(1)


if args.init:
    if hash_exist.exists():
        print('hash.json already exists. Please use --update.')
    else:
        dir_list = list_file(path)
        path_hash = dict_hash(dir_list, algorithm)
        write_in_json_file(path_hash)
        print(f'Program initialized using {algorithm}.')
        print('hash.json created successfully.')

elif args.update:
    if not hash_exist.exists():
        print('hash.json does not exist. Please use --init first.')
    else:
        hashf = read_json()
        stored_algorithm = hashf.get('algorithm')

        if stored_algorithm not in type_of_hash_algorithm:
            print('Invalid or missing algorithm in hash.json.')
            sys.exit(1)

        if args.algorithm and args.algorithm.lower() != stored_algorithm:
            print(f'Algorithm mismatch: hash.json uses {stored_algorithm}, 'f'but you selected {args.algorithm.lower()}.')
            sys.exit(1)

        dir_list = list_file(path)
        path_hash = dict_hash(dir_list, stored_algorithm)
        write_in_json_file(path_hash)

        print(f'Hash values updated using {stored_algorithm}.')

elif args.check:
    check_hash_json()

elif args.watch:
    if not hash_exist.exists():
        print('hash.json does not exist. Please use --init first.')
        sys.exit(1)

    if args.time is not None:
        if args.time <= 0:
            parser.error('--time must be greater than 0')
        t = args.time

    print(f'Watch mode started. Checking every {t} seconds.')
    print('Press Ctrl+C to stop.') 
    try:
        while True:
            check_hash_json()
            time.sleep(t)

    except KeyboardInterrupt:
        print('\nWatch stopped by user.')

else:
    parser.print_help()
