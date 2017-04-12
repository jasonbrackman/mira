import sys
import os


if len(sys.argv) < 2:
    sys.exit(1)
    

maketx_path = r'C:\tools\aas_tools\aas_tools\mtoadeploy\1.2.3.1\2015\bin\maketx.exe'


def get_tx_name():
    tx_name = os.path.splitext(sys.argv[1])[0] + '_final.exr'
    return tx_name
    
    
def get_cmd():
    cmd = '%s -v --oiio --colorconvert sRGB linear -unpremult %s -o %s' % \
          (maketx_path, sys.argv[1], get_tx_name())
    return cmd
    

def main():
    cmd = get_cmd()
    print cmd
    os.system(cmd)
    
    
if __name__ == '__main__':
    main()