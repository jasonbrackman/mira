# -*- coding: utf-8 -*-
from Qt import QtWidgets
import maya.cmds as mc
import maya.mel as mel
import maya.utils as mu
from miraLibs.mayaLibs import get_maya_win


def show_as_panel(widget_instance, title=None):
    if not isinstance(widget_instance, QtWidgets.QWidget):
        raise ValueError("%s is not a Qt Widget." % widget_instance)

    obj_name = widget_instance.objectName()
    # parent current dialog to maya win
    maya_main_window = get_maya_win.get_maya_win()
    widget_instance.setParent(maya_main_window)
    # dock the panel on maya
    if not title:
        title = widget_instance.windowTitle() or widget_instance.objectName()
    dock_panel(obj_name, widget_instance, title)

    return widget_instance


def dock_panel(object_name, widget_instance, title):
    maya_panel_name = "panel_%s" % object_name
    # delete existed panel
    if mc.control(maya_panel_name, query=True, exists=True):
        mc.deleteUI(maya_panel_name)

    if int(str(mc.about(api=True))[:4]) < 2017:

        # Create a new Maya window.
        maya_window = mc.window()

        # Add a layout to the Maya window.
        maya_layout = mc.formLayout(parent=maya_window)

        # Reparent the Shotgun app panel widget under the Maya window layout.
        mc.control(object_name, edit=True, parent=maya_layout)

        # Keep the Shotgun app panel widget sides aligned with the Maya window layout sides.
        mc.formLayout(maya_layout,
                      edit=True,
                      attachForm=[(object_name, 'top', 1),
                                  (object_name, 'left', 1),
                                  (object_name, 'bottom', 1),
                                  (object_name, 'right', 1)])

        # Dock the Maya window into a new tab of Maya Channel Box dock area.
        mc.dockControl(maya_panel_name, area="right", content=maya_window, label=title)

        # Once Maya will have completed its UI update and be idle,
        # raise (with "r=True") the new dock tab to the top.
        mu.executeDeferred("cmds.dockControl('%s', edit=True, r=True)" % maya_panel_name)

    else:  # Maya 2017 and later
        # Delete any default workspace control state that might have been automatically
        # created by Maya when a previously existing Maya panel was closed and deleted.
        if mc.workspaceControlState(maya_panel_name, exists=True):
            mc.workspaceControlState(maya_panel_name, remove=True)

        # Retrieve the Channel Box dock area, with error reporting turned off.
        # This MEL function is declared in Maya startup script file UIComponents.mel.
        # It returns an empty string when this dock area cannot be found in the active Maya workspace.
        dock_area = mel.eval('getUIComponentDockControl("Channel Box / Layer Editor", false)')

        # This UI script will be called to build the UI of the new dock tab.
        # It will embed the Shotgun app panel widget into a Maya workspace control.
        # Maya 2017 expects this script to be passed in as a string, not as a function pointer.
        # See function _build_workspace_control_ui() below for a commented version of this script.
        ui_script = "import pymel.core as pm\n" \
                    "workspace_control = pm.setParent(query=True)\n" \
                    "pm.control('%s', edit=True, parent=workspace_control)" \
                    % object_name

        # The following UI script can be used for development and debugging purposes.
        # This script has to retrieve and import the current source file in order to call
        # function _build_workspace_control_ui() below to build the workspace control UI.
        # ui_script = "import imp\n" \
        #             "panel_generation = imp.load_source('%s', '%s')\n" \
        #             "panel_generation._build_workspace_control_ui('%s')" \
        #             % (__name__, __file__.replace(".pyc", ".py"), object_name)

        # Give an initial width to the docked Shotgun app panel widget when first shown.
        # Otherwise, the workspace control would use the width of the currently displayed tab.
        size_hint = widget_instance.sizeHint()
        if size_hint.isValid():
            # Use the widget layout preferred size.
            widget_width = size_hint.width()
        else:
            # Since no size is recommended for the widget, use its current width.
            widget_width = widget_instance.width()

        # Dock the Shotgun app panel widget into a new tab of the Channel Box dock area.
        # When this dock area was not found in the active Maya workspace,
        # the Shotgun app panel widget is embedded into a floating workspace control window.
        # This floating workspace control can then be docked into an existing dock area by the user.
        dock_tab = mc.workspaceControl(maya_panel_name,
                                       tabToControl=(dock_area, -1),  # -1 to append a new tab
                                       uiScript=ui_script,
                                       loadImmediately=True,
                                       retain=False,  # delete the dock tab when it is closed
                                       label=title,
                                       initialWidth=widget_width,
                                       minimumWidth=True,  # set the minimum width to the initial width
                                       r=True  # raise the new dock tab to the top
                   )

        # Now that the workspace dock tab has been created, let's update its UI script.
        # This updated script will be saved automatically with the workspace control state
        # in the Maya layout preference file when the user will choose to quit Maya,
        # and will be executed automatically when Maya is restarted later by the user.

        # The script will delete the empty workspace dock tab that Maya will recreate on startup
        # when the user previously chose to quit Maya while the panel was opened.
        deferred_script = "import maya.cmds as cmds\\n" \
                          "if cmds.workspaceControl('%(id)s', exists=True):\\n" \
                          "    cmds.deleteUI('%(id)s')" \
                          % {"id": maya_panel_name}

        # The previous script will need to be executed once Maya has completed its UI update and be idle.
        ui_script = "import maya.utils\n" \
                    "maya.utils.executeDeferred(\"%s\")\n" \
                    % deferred_script

        # Update the workspace dock tab UI script.
        mc.workspaceControl(maya_panel_name, edit=True, uiScript=ui_script)


if __name__ == "__main__":
    show_as_panel()