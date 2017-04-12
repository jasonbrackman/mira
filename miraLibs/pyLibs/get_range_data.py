# -*- coding: utf-8 -*-


def get_range_data(data):
    """
    use for get a data list
    :param data: 1,5-7
    :return: [1, 5, 6, 7]
    """
    if data:
        data = data.split(',')
        dai_gang = [x for x in data if '-' in x]
        final = list(set(data) - set(dai_gang))
        final = [int(x) for x in final if x]
        for x in dai_gang:
            x = x.split('-')
            x = range(int(x[0]), int(x[1]) + 1)
            final.extend(x)
        final.sort()
        return final


if __name__ == "__main__":
    pass
