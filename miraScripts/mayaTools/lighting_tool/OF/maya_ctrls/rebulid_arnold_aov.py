# coding utf-8
# __author__ = "heshuai"
# description="""  """


import re
import pymel.core as pm
import mtoa.aovs as aovs


def rebuild_arnold_aov():
    # arnold rebuild aov
    aov_lists = list()
    # get shading group's aovname
    sg_nodes = pm.ls(type='shadingEngine')
    if len(sg_nodes) > 200:
        sg_nodes = sg_nodes[:200]
    for se in sg_nodes:
        for aov in se.aiCustomAOVs:
            print '[OF] Info:find', aov, aov.aovName.get()
            aov_lists.append(aov.aovName.get())
    # get aiWriteColor's aovname
    for wc in pm.ls(type='aiWriteColor'):
        print wc.aovName.get()
        m = re.compile('(.*) \(Inactive\)').match(wc.aovName.get())
        if m:
            print '[OF] Info:find', wc, wc.aovName.get()
            aov_lists.append(m.groups()[0])
        else:
            if wc.aovName.get():
                print '[OF] Info:find', wc, wc.aovName.get()
                aov_lists.append(wc.aovName.get())
    aov_lists = list(set(aov_lists))
    for aov in aov_lists:
        if aov and aov not in get_aov_name_lists():
            try:
                aovs.AOVInterface().addAOV(aov)
                print '[OF] Info: Rebuild %s' % aov
            except:pass
                
                
def get_aov_name_lists():
    return [i.name for i in aovs.getAOVs()]