import maya.cmds as mc


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


def get_object_sg(objs):
    all_sg = list()
    if not objs:
        all_sg = mc.ls(type='shadingEngine')
    else:
        real_obj = mc.ls(objs, dag=1, shapes=1)
        sgs = mc.listConnections(real_obj, s=0, d=1, type='shadingEngine')
        all_sg += sgs
    all_sg = list(set(all_sg))
    return all_sg


def get_sg_objects(sg):
    sg_set = sg + '.dagSetMembers'
    sg_me_ele = mc.listConnections(sg_set, s=1, d=0, p=1)

    real_obj = []
    if not sg_me_ele:
        return real_obj

    for sme in sg_me_ele:
        obj_grp_id = sme+'.objectGroupId'
        comp_obj_grp_id = sme+'.compObjectGroupId'
        query_id = []
        if mc.objExists(obj_grp_id):
            query_id.append(obj_grp_id)
        elif mc.objExists(comp_obj_grp_id):
            query_id.append(comp_obj_grp_id)

        if not query_id:
            temp_obj = sme.split('.')[0]
            real_obj = real_obj + [temp_obj]
        else:
            for queryId in query_id:
                tem = mc.listConnections(queryId, s=1, d=0)
                if not tem:
                    temp_obj = sme.split('.')[0]
                    real_obj = real_obj + [temp_obj]
                    continue

                grp_id = tem[0]
                temp_obj_set = mc.createNode('objectSet')

                mc.connectAttr(sme, (temp_obj_set + '.dagSetMembers'), na=1)
                mc.connectAttr((grp_id + '.message'), (temp_obj_set + '.groupNodes'))

                temp_obj = mc.sets(temp_obj_set, q=1)
                if temp_obj:
                    real_obj = real_obj + temp_obj

                in_cons = mc.listConnections(temp_obj_set, s=1, d=0, c=1, p=1)
                for i in range(0, len(in_cons), 2):
                    mc.disconnectAttr(in_cons[i + 1], in_cons[i])

                mc.delete(temp_obj_set)

    real_obj = list(set(real_obj))
    return real_obj


def get_object_sg_detail(objs):
    sg_obj_dict = {}
    obj_sg_dict = {}
    sgs = get_object_sg(objs)
    for sg in sgs:
        objs = get_sg_objects(sg)
        if not objs:
            continue

        sg_obj_dict[sg] = objs
        for obj in objs:
            obj_sg_dict[obj] = sg

    return sg_obj_dict, obj_sg_dict


def get_surface_material(sg_node):
    attr = mc.listConnections('%s.surfaceShader' % sg_node, s=1, d=0, plugs=1)
    if attr:
        return attr[0]
    else:
        return


def get_dis(sg_node):
    attr = mc.listConnections('%s.displacementShader' % sg_node, s=1, d=0, plugs=1)
    if attr:
        return attr[0]
    else:
        return


def create_sg_node():
    sg_node = mc.sets(noSurfaceShader=1, renderable=1, empty=1)
    return sg_node


@undo
def main():
    selected_objs = [i for i in mc.ls(sl=1) if mc.nodeType(i) == 'transform']
    if selected_objs:
        my_dict = get_object_sg_detail(selected_objs)[0]
        for sg_node in my_dict:
            if sg_node not in ['initialParticleSE', 'initialShadingGroup']:
                surface_material = get_surface_material(sg_node)
                dis = get_dis(sg_node)
                new_sg_node = create_sg_node()
                try:
                    mc.sets(my_dict[sg_node], fe=new_sg_node)
                except Exception as e:
                    print '[OF] assign error:', e
                else:
                    if surface_material:
                        mc.connectAttr(surface_material, '%s.surfaceShader' % new_sg_node, f=1)
                    if dis:
                        mc.connectAttr(dis, '%s.displacementShader' % new_sg_node, f=1)
                    try:
                        mc.delete(sg_node)
                        mc.rename(new_sg_node, sg_node+'_new')
                        print '[OF] info %s has been replaced' % sg_node
                    except Exception as e:
                        print '[OF] delete error:', e


if __name__ == '__main__':
    main()