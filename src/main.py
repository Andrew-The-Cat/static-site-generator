from textnode import *
from htmlnode import *
from doc_parser import *

import os
import shutil

def reset():
    src_path = "static"
    public_path = "public"

    shutil.rmtree(public_path)
    os.mkdir(public_path)

    entries = os.listdir(src_path)

    def recursive(entries, src_path, public_path):
        print(f"copying from {src_path} to {public_path}\n============================================\n")

        for entry in entries:
            src_file = os.path.join(".", src_path, entry)
            public_file = os.path.join(".", public_path, entry)
            if not os.path.exists(src_file):
                return None

            if os.path.isfile(src_file):
                print(f"copying {os.path.realpath(src_file)}  \n\t---> {os.path.realpath(public_file)}")
                shutil.copy(src_file, public_file)
                continue
 
            # source is not a file, so it must be a directory
            if not os.path.exists(public_file):
                os.mkdir(public_file)

            print(f"found directory {src_file} ; copying recursively \n\n")
            recursive (os.listdir(src_file), src_file, public_file)

    recursive(entries, src_path, public_path)

def main():
    reset()


main()