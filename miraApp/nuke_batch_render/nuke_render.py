import nuke
import sys
import re
import os


def switch_node_path(node):
    file_name = node['file'].getValue()
    if nuke.env['LINUX']:
        file_name = re.sub('^[vV]:', '/mnt/v', file_name)
    else:
        file_name = re.sub('^/mnt/[Vv]', 'V:', file_name)
    node['file'].setValue(file_name)
    

def switch_path():
    nodes = nuke.allNodes('Read') + nuke.allNodes('Write')
    for node in nodes:
        switch_node_path(node)

            
def main():
    file_name = sys.argv[1]
    nuke.scriptOpen(file_name.replace('\\', '/'))
    
    if not os.path.isdir(os.path.dirname(sys.argv[4])):
        os.makedirs(os.path.dirname(sys.argv[4]))

    nuke.toNode(sys.argv[2])['file'].setValue(sys.argv[4])
    nuke.toNode(sys.argv[2])['disable'].setValue(False)

    frames = sys.argv[3].split('-')
    first_frame, last_frame = int(frames[0]), int(frames[1])
    
    switch_path()
    #nuke.scriptSave()

    nuke.execute(sys.argv[2], first_frame, last_frame, continueOnError=True)

    nuke.scriptClose(file_name)
    
if __name__ == '__main__':
    main()