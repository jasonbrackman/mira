import maya.cmds as mc
import re


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

    
def assign_to_new_obj(objs, new_objs):
    obj_sg_dict = get_object_sg_detail(objs)[1]
    new_dict = dict()
    for i in obj_sg_dict:
        if objs in i:
            new_key = re.sub(objs, new_objs, i)
            new_dict[new_key] = obj_sg_dict[i]
    if new_dict:
        for i in new_dict:
            mc.sets(i, e=1, fe=new_dict[i])