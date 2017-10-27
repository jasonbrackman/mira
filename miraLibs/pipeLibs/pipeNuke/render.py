# -*- coding: utf-8 -*-
import os
import nuke


def main():
    file_name = nuke.rawArgs[3]
    nuke.scriptOpen(file_name)
    write_node = nuke.toNode("Final_Render")
    if not write_node:
        print "Final_Render node not exist."
        return
    render_output = write_node["file"].getValue()
    if not render_output:
        print "Render output path not setting."
        return
    render_dir = os.path.dirname(render_output)
    if not os.path.isdir(render_dir):
        os.makedirs(render_dir)
    start_frame = nuke.root().firstFrame()
    end_frame = nuke.root().lastFrame()
    nuke.execute(write_node, start_frame, end_frame, continueOnError=True)
    nuke.scriptClose()


if __name__ == "__main__":
    main()
