import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import re
from PySide import QtGui, QtCore

mat_dict = {'aiStandard': {'color': {'mr_name': 'diffuse', 'value': (1.0, 1.0, 1.0)},
                              'Kd': {'mr_name': 'diffuse_weight', 'value': 0.7},
                              'diffuseRoughness': {'mr_name': 'diffuse_roughness', 'value': 0.0},
                              'KsColor': {'mr_name': 'refl_color', 'value': (1.0, 1.0, 1.0)},
                              'Ks': {'mr_name': 'reflectivity', 'value': 0.0},
                              'specularRoughness': {'mr_name': 'refl_gloss', 'value': 0.467},
                              'specularFresnel': {'mr_name': 'brdf_fresnel', 'value': 0},
                              'KtColor': {'mr_name': 'refr_color', 'value': (1.0, 1.0, 1.0)},
                              'IOR': {'mr_name': 'refr_ior', 'value': 1.0},
                              'Kt': {'mr_name': 'transparency', 'value': 0.0},
                              'refractionRoughness': {'mr_name': 'refr_gloss', 'value': 0.0},
                              'opacity': {'mr_name': 'cutout_opacity', 'value': (1.0, 1.0, 1.0)},
                              'normalCamera': {'mr_name': 'overall_bump', 'value': None},
                              'emissionColor': {'mr_name': 'additional_color'}
                           },
            'aiSkinSss': {'color': {'mr_name': 'diffuse_color', 'value': (1.0, 1.0, 1.0)},
                          'diffuseWeight': {'mr_name': 'diffuse_weight', 'value': 0.3},
                          'shallowScatterColor': {'mr_name': 'front_sss_color', 'value': (1.0, 0.9089999794960022, 0.76899999380111694)},
                          'shallowScatterWeight': {'mr_name': 'front_sss_weight', 'value': 0.5},
                          'shallowScatterRadius': {'mr_name': 'front_sss_radius', 'value': 0.15},
                          'midScatterColor': {'mr_name': 'mid_sss_color', 'value': (0.94900000095367432, 0.71399998664855957, 0.56000000238418579)},
                          'midScatterWeight': {'mr_name': 'mid_sss_weight', 'value': 0.25},
                          'midScatterRadius': {'mr_name': 'mid_sss_radius', 'value': 0.25},
                          'deepScatterColor': {'mr_name': 'back_sss_color', 'value': (0.69999998807907104, 0.10000000149011612, 0.10000000149011612)},
                          'deepScatterWeight': {'mr_name': 'back_sss_weight', 'value': 1.0},
                          'deepScatterRadius': {'mr_name': 'back_sss_radius', 'value': 0.6},
                          'primaryReflectionColor': {'mr_name': 'primary_spec_color', 'value': (0.75, 0.89999997615814209, 1.0)},
                          'primaryReflectionWeight': {'mr_name': 'primary_weight', 'value': 0.8},
                          'secondaryReflectionColor': {'mr_name': 'secondary_spec_color', 'value': (0.75, 0.89999997615814209, 1.0)},
                          'secondaryReflectionWeight': {'mr_name': 'secondary_weight', 'value': 0.6},
                          'globalSssRadiusMultiplier': {'mr_name': 'scale_conversion', 'value': 10.0},
                          'normalCamera': {'mr_name': 'normalCamera', 'value': (0.0, 0.0, 0.0)},
                          },
            }

of_mat_dict = {'aiOf_aiLayerMixer':  {'Color0': {'mr_name': 'inputs[0].color', 'value': (1.0, 1.0, 1.0)},
                                      'Mask0': {'mr_name': 'inputs[0].transparency', 'value': 1.0},
                                      'Color1': {'mr_name': 'inputs[1].color', 'value': (0.0, 0.0, 0.0)},
                                      'Mask1': {'mr_name': 'inputs[1].transparency', 'value': 1.0},
                                      'Color2': {'mr_name': 'inputs[2].color', 'value': (0.0, 0.0, 0.0)},
                                      'Mask2': {'mr_name': 'inputs[2].transparency', 'value': 1.0},
                                      'Color3': {'mr_name': 'inputs[3].color', 'value': (0.0, 0.0, 0.0)},
                                      }
               }


def undo(func):
    def _undo(*args, **kwargs):
        try:
            mc.undoInfo(ock=1)
            result = func(*args, **kwargs)
        except Exception, e:
            raise e
        else:
            return result
        finally:
            mc.undoInfo(cck=1)
    return _undo


def create_mr_material(shader_type, shader_name):
    if not pm.objExists(shader_name):
        if shader_type == 'aiStandard':
            shader = pm.shadingNode('mia_material_x', asShader=1, name=shader_name)
        elif shader_type == 'aiSkinSss':
            mr_texture = pm.ls(type='mentalrayTexture')
            if mr_texture:
                shader = pm.shadingNode('misss_fast_skin_maya', asShader=1, name=shader_name)
                mr_texture[0].message >> shader.lightmap
            else:
                name = mel.eval("mrCreateCustomNode -asShader \"\" misss_fast_skin_maya;")
                pm.PyNode(name).rename(shader_name)
                shader = pm.PyNode(shader_name)
        elif shader_type == 'aiOf_aiLayerMixer':
            shader = pm.shadingNode('layeredShader', asShader=1, name=shader_name)
        return shader
    else:
        return pm.PyNode(shader_name)


def create_surface_shader():
    return pm.shadingNode('surfaceShader', asShader=1, name='ar_mr_surface_shader')
    

def create_reverse_shader():
    return pm.shadingNode('reverse', asUtility=1)


def get_source_attr(attr):
    source_attr_name = attr.connections(s=1, d=0, plugs=1)
    if source_attr_name:
        return 1, source_attr_name[0]
    else:
        return 0, attr.get()


def connect_forward_attr(ar_shader, mr_shader):
    destination_nodes = ar_shader.outputs()
    destination_nodes = [node for node in destination_nodes 
                        if node.type() not in ['defaultShaderList', 'materialInfo', 'unknown']]
    if ar_shader.type() == 'aiOf_aiLayerMixer':
        for node in destination_nodes:
            if node.type() == 'shadingEngine':
                mr_shader.outColor >> node.surfaceShader
            elif node.type() in ['aiOf_aiLayerMixer', 'layeredShader']:
                dst_attrs = ar_shader.outputs(type=node.type(), plugs=1)
                for attr in dst_attrs:
                    src_attr = attr.inputs(plugs=1)[0]
                    src_attr // attr
                    new_src_attr = re.sub(ar_shader.name(), mr_shader.name(), src_attr.name())
                    pm.PyNode(new_src_attr) >> attr
    else:      
        for node in destination_nodes:
            if node.type() == 'shadingEngine':
                mr_shader.message >> node.surfaceShader
                mr_shader.message >> node.miMaterialShader
                mr_shader.message >> node.miPhotonShader
                mr_shader.message >> node.miShadowShader
            elif node.type() in ['layeredShader', 'aiOf_aiLayerMixer']:
                dst_attrs = ar_shader.outputs(type=node.type(), plugs=1)
                for attr in dst_attrs:
                    src_attr = attr.inputs(plugs=1)[0]
                    src_attr // attr
                    if mr_shader.type() == 'mia_material_x':
                        mr_shader.result >> attr
                    elif mr_shader.type() == 'misss_fast_skin_maya':
                        mr_shader.outValue >> attr
            else:
                print '[OF] warning: %s is not under consideration' % node.type()


def delete_node(node):
    try:
        pm.delete(node)
        print "delete", node.name()
        return True
    except Exception as e:
        print '[OF] delete error:', e
        return False


def delete_nodes(nodes):
    if nodes:
        for node in nodes:
            if not node.outputs():
                delete_node(node)


def delete_unused_shader(shader):
    connections = shader.outputs()
    ret = None
    if not connections:
        ret = delete_node(shader)
    elif len(connections) == 1 and connections[0].name() == 'defaultShaderList1':
        ret = delete_node(shader)
    elif len(connections) == 2:
        connections = [i.name() for i in connections]
        if connections == ['defaultShaderList1', 'hyperLayout1']:
            ret = delete_node(shader)
    return ret


def convert_aistandard_sss(material):
    mat_type = material.type()
    ar_name = material.name()
    new_name = ar_name + '_mr'
    mr_material = create_mr_material(mat_type, new_name)
    connect_forward_attr(material, mr_material)
    for attr in mat_dict[mat_type]:
        total_attr = pm.PyNode('%s.%s' % (ar_name, attr))
        source_attr = get_source_attr(total_attr)
        mr_material_attr = pm.PyNode('%s.%s' % (new_name, mat_dict[mat_type][attr]['mr_name']))
        if source_attr[0]:
            if attr != 'opacity':
                try:
                    source_attr[1] >> mr_material_attr
                except:
                    try:
                        source_attr[1].node().outAlpha >> mr_material_attr
                    except Exception as e:
                        print '[OF] connect error:', e
            else:
                reverse_shader = create_reverse_shader()
                source_attr[1].node().outAlpha >> reverse_shader.inputX
                source_attr[1].node().outAlpha >> reverse_shader.inputY
                source_attr[1].node().outAlpha >> reverse_shader.inputZ
                reverse_shader.outputX >> mr_material_attr
        else:
            try:
                mr_material_attr.set(source_attr[1])
            except:
                try:
                    mr_material_attr.set(source_attr[1][0])
                except Exception as e:
                    print '[OF] set value error:', e
    return mr_material
    
    
def convert_aiRimFilter(material):
    source_attr = material.inputs(plugs=1)[0]
    target_attrs = material.outputs(plugs=1)
    for attr in target_attrs:
        if attr.node().type() not in ['defaultShaderList', 'materialInfo', 'unknown']:
            try:
                source_attr >> attr
            except Exception as e:
                print '[OF] warnning: ', e


def convert_ailayermixer(material):
    mat_type = material.type()
    ar_name = material.name()
    layershader_name = ar_name + '_mr'
    layered_shader_node = create_mr_material(mat_type, layershader_name)
    connect_forward_attr(material, layered_shader_node)
    all_attr = ['Color0', 'Mask0', 'Color1', 'Mask1', 'Color2', 'Mask2', 'Color3']
    for attr in all_attr:
        total_attr = pm.PyNode('%s.%s' % (ar_name, attr))
        source_attr = get_source_attr(total_attr)
        #has connection
        if source_attr[0]:
            mr_dst_attr = re.sub(ar_name, layered_shader_node.name(), '%s.%s' % (ar_name, attr))
            mr_dst_attr = re.sub(attr, of_mat_dict[mat_type][attr]['mr_name'], mr_dst_attr)
            if source_attr[1].node().type() == 'aiStandard':
                mr_material_new = convert_aistandard_sss(source_attr[1].node())
                mr_material_new.result >> pm.PyNode(mr_dst_attr)
            elif source_attr[1].node().type() == 'file':
                if not 'Mask' in attr:
                    source_attr[1] >> pm.PyNode(mr_dst_attr)
                else:
                    reverse_shader = create_reverse_shader()
                    source_attr[1] >> reverse_shader.inputX
                    source_attr[1] >> reverse_shader.inputY
                    source_attr[1] >> reverse_shader.inputZ
                    reverse_shader.output >> mr_dst_attr
            elif source_attr[1].node().type() == 'layeredShader':
                source_attr[1] >> mr_dst_attr
            elif source_attr[1].node().type() == 'mia_material_x':
                source_attr[1].node().result >> mr_dst_attr
            elif source_attr[1].node().type() == 'aiOf_aiLayerMixer':
                source_attr[1] >> mr_dst_attr
                

def close_addtional_color():
    for material in mc.ls(type='mia_material_x'):
        src_attr = mc.listConnections('%s.additional_color' % material, s=1, d=0)
        if not src_attr:
            mc.setAttr('%s.additional_color' % material, 0, 0, 0, type='double3')
        
        
# #@undo
# def convert():
#     for material in pm.ls(materials=1):
#         if not material.outputs():
#             delete_node(material)
#             continue
#         mat_type = material.type()
#         if mat_type in mat_dict:
#             if material.outColor.outputs()[0].type() == 'aiOf_aiLayerMixer':
#                 continue
#             convert_aistandard_sss(material)
#         elif mat_type in of_mat_dict:
#             convert_ailayermixer(material)


def get_shader_by_type(types):
    return [shader for shader in mc.ls(materials=1) if mc.nodeType(shader) == types]


def load_plugin(plugin_name):
    if not mc.pluginInfo(plugin_name, q=1, loaded=1):
        mc.loadPlugin(plugin_name, quiet=1)
        print "load plugin %s successful" % plugin_name
    

def get_maya_win():
    import maya.OpenMayaUI as mui
    main_window = None
    ptr = mui.MQtUtil.mainWindow()
    if 'PyQt4' in QtGui.__name__:
        import sip
        main_window = sip.wrapinstance(long(ptr), QtCore.QObject)
    if 'PySide' in QtGui.__name__:
        import shiboken
        main_window = shiboken.wrapInstance(long(ptr), QtCore.QObject)
    return main_window

#----------------------------------------------UI---------------------------------------------#


class MyItem(QtGui.QStandardItem):
    def __init__(self, text=None, color=QtCore.Qt.white, bold=False, font_size=10, parent=None):
        super(MyItem, self).__init__(parent)
        self.text = text
        self.setText(self.text)
        self.setForeground(color)
        font = QtGui.QFont()
        font.setPointSizeF(font_size)
        if bold:
            font.setWeight(QtGui.QFont.Bold)
        self.setData(font, QtCore.Qt.FontRole)
        self.setEditable(False)


class ArToMr(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ArToMr, self).__init__(parent)
        self.setWindowTitle('Arnold To MentalRay')
        self.setObjectName('Arnold To MentalRay')
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMinimizeButtonHint)
        self.resize(800, 400)
        self.model = None
        main_layout = QtGui.QVBoxLayout(self)

        refresh_layout = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel()
        self.refresh_btn = QtGui.QPushButton('Refresh')
        self.refresh_btn.setFixedWidth(50)
        refresh_layout.addWidget(self.label)
        refresh_layout.addWidget(self.refresh_btn)

        self.tree_view = QtGui.QTreeView()
        self.model = QtGui.QStandardItemModel()

        button_layout = QtGui.QHBoxLayout()
        #button_layout.setContentsMargins(2, 5, 2, 5)
        self.convert_btn = QtGui.QPushButton('Convert')
        self.delete_btn = QtGui.QPushButton('Delete Unused Nodes')
        button_layout.addWidget(self.convert_btn)
        button_layout.addWidget(self.delete_btn)

        main_layout.addLayout(refresh_layout)
        main_layout.addWidget(self.tree_view)
        main_layout.addLayout(button_layout)

        self.init_settings()
        self.set_signals()

    def init_settings(self):
        self.set_model()
        self.tree_view.setEditTriggers(QtGui.QTreeView.NoEditTriggers)
        self.tree_view.setSelectionMode(QtGui.QTreeView.ExtendedSelection)
        self.tree_view.resizeColumnToContents(0)
        self.tree_view.resizeColumnToContents(1)
        self.tree_view.resizeColumnToContents(2)
        self.label.setText('<font size=3 color=#00FF00><b>Usage: convert arnold shaders to mentalray shader.</b></font>')

    def set_signals(self):
        selection_model = self.tree_view.selectionModel()
        selection_model.selectionChanged.connect(self.select_node)
        self.refresh_btn.clicked.connect(self.init_settings)
        self.convert_btn.clicked.connect(self.do_convert)
        self.delete_btn.clicked.connect(self.delete_no_use)

    def set_model(self):
        self.model.clear()
        header_list = ['type', 'arnold shaders', 'mentalray shaders']
        self.model.setHorizontalHeaderLabels(header_list)
        shader_types = ['aiStandard', 'aiSkinSss', 'aiOf_aiLayerMixer', 'aiOf_aiRimFilter']
        for types in shader_types:
            type_item = MyItem(types, color=QtGui.QColor(255, 100, 0), bold=True)
            type_item.setBackground(QtGui.QColor(20, 10, 0))
            shaders = get_shader_by_type(types)
            ar_shader_num_item = MyItem(str(len(shaders)), color=QtGui.QColor(255, 100, 0), bold=True)
            ar_shader_num_item.setTextAlignment(QtCore.Qt.AlignCenter)
            ar_shader_num_item.setBackground(QtGui.QColor(20, 10, 0))
            num_mr_shader = 0
            for index, shader in enumerate(shaders):
                ar_child_item = MyItem(shader)
                type_item.setChild(index, 1, ar_child_item)
                mr_shader = shader+'_mr'
                if mc.objExists(mr_shader):
                    num_mr_shader += 1
                    ar_child_item.setForeground(QtCore.Qt.green)
                    mr_child_item = MyItem(mr_shader)
                    type_item.setChild(index, 2, mr_child_item)
                else:
                    ar_child_item.setForeground(QtCore.Qt.red)
            mr_shader_num_item = MyItem(str(num_mr_shader), color=QtGui.QColor(255, 100, 0), bold=True)
            mr_shader_num_item.setTextAlignment(QtCore.Qt.AlignCenter)
            mr_shader_num_item.setBackground(QtGui.QColor(20, 10, 0))
            items = [type_item, ar_shader_num_item, mr_shader_num_item]
            self.model.appendRow(items)
        self.tree_view.setModel(self.model)

    def select_node(self):
        for i in self.tree_view.selectedIndexes():
            if i.column() == 1:
                current_shader = self.model.itemFromIndex(i).text
                if pm.objExists(current_shader):
                    pm.select(current_shader, add=1)

    def do_convert(self):
        mc.renderThumbnailUpdate(False)
        all_materials = pm.ls(materials=1)
        if all_materials:
            pd = QtGui.QProgressDialog('Converting...', 'Cancel', 0, len(all_materials))
            pd.setWindowModality(QtCore.Qt.WindowModal)
            pd.show()
            value = 0
            for material in all_materials:
                ret = delete_unused_shader(material)
                if ret:
                    value += 1
                    continue
                mat_type = material.type()
                if mat_type in mat_dict:
                    if material.outColor.outputs():
                        if material.outColor.outputs()[0].type() == 'aiOf_aiLayerMixer':
                            value += 1
                            continue
                    convert_aistandard_sss(material)

                elif mat_type in of_mat_dict:
                    convert_ailayermixer(material)
                elif mat_type == 'aiOf_aiRimFilter':
                    convert_aiRimFilter(material)
                value += 1
        close_addtional_color()
        self.init_settings()
        self.label.setText('<font size=3 color=#00FF00><b>^o^Convert Successful!!!^o^</b></font>')

    def delete_no_use(self):
        #delete shader
        shaders = pm.ls(materials=1)
        if shaders:
            for shader in shaders:
                delete_unused_shader(shader)
        #delete file
        files = pm.ls(type='file')
        delete_nodes(files)

        self.init_settings()
        self.label.setText('<font size=3 color=#00FF00><b>^o^Delete Successful!!!^o^</b></font>')

    @classmethod
    def show_UI(cls):
        if mc.window('Arnold To MentalRay', q=1, exists=1):
            mc.deleteUI('Arnold To MentalRay')
        atm = cls(get_maya_win())
        atm.show()
        

def main():
    load_plugin('Mayatomr.mll')
    ArToMr.show_UI()

if __name__ == '__main__':
    main()