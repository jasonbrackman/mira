__author__ = 'heshuai'


def re_group(file_list, n):
    if not isinstance(file_list, list) or not isinstance(n, int):
        return False
    elif n <= 0 or len(file_list) == 0:
        return False
    elif n >= len(file_list):
        return [[i] for i in file_list]
    elif n < len(file_list):
        new_list = []
        for x in xrange(n):
            new_list.append(list())
        while file_list:
            for x in xrange(n):
                if file_list:
                    new_list[x].append(file_list.pop())
        for i in new_list:
            i.sort()
        return new_list