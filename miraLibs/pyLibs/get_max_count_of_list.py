# -*- coding: utf-8 -*-


def get_max_count_of_list(sample):
    return max(set(sample), key=sample.count)
