# -*- coding: utf-8 -*-

import sys

def main():
    a = sys.argv[1]
    b = sys.argv[2]
    with open(r'z:\mira\miraScripts\pipeTools\background_operate\fuck.txt','w') as f:
        f.write(a)
        f.write(b)

if __name__ == '__main__':
    main()