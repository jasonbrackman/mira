import maya.cmds as cmds


def clear_namespace():
    def remove(name):
        children = cmds.namespaceInfo(name, lon=1)
        if children:
            for child in children:
                remove(child)
        try:
            cmds.namespace(mv=(name, ':'), f = 1)
            cmds.namespace(rm=name)
        except:
            print "## Failed:", name
        else:
            print "// Removed:", name

    cmds.namespace(set=':')
    for name in cmds.namespaceInfo(lon=1):
        if name not in ('UI', 'shared'):
            remove(name)
    print '// Namespaces Clean-Up Completed'

if __name__ == '__main__':
    clear_namespace()
