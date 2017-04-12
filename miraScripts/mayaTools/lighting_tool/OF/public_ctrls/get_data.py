#coding=utf-8
#__author__ = 'heshuai'
#description='''  '''


def get_data(data):
    if isinstance(data, basestring):
        data = data.split(',')
        dai_gang = [x for x in data if '-' in x]
        final = list(set(data)-set(dai_gang))
        final = [int(x) for x in final if x]
        for x in dai_gang:
            x = x.split('-')
            x = range(int(x[0]), int(x[1])+1)
            final.extend(x)
        final.sort()
        return final
    else:
        raise TypeError('the data must be a string')