import os
from itertools import combinations


class AssociationRule:
    def __init__(self, min_sup=0.3, min_conf=1):
        self.data = [[]]
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.ls_max_itemset = list()
        self.ls_assoc = list()

    @staticmethod
    def is_in_set(set_a, set_b):
        for item in set_a:
            if item not in set_b:
                return False

        return True

    def freq_of_set(self, set_a):
        freq_set = 0
        for itemset in self.data:
            freq_item = 0
            for item in set_a:
                if item in itemset:
                    freq_item += 1

            if freq_item == set_a.__len__():
                freq_set += 1

        return freq_set

    def is_satisf_minsup(self, set_a):
        return self.freq_of_set(set_a) / self.data.__len__() >= self.min_sup

    def can_make_newest(self, set_a, set_b):
        if not self.is_satisf_minsup(set_a) or not self.is_satisf_minsup(set_b):
            return None

        num_item = 0
        add_item = list()

        for item in set_b:
            if item in set_a:
                num_item += 1
            else:
                add_item.append(item)

        if add_item.__len__() == 1 and self.is_satisf_minsup(set_a + add_item):
            return set_a + add_item

        return None

    @staticmethod
    def is_set_in_ls(set_a, ls_itemset):
        for itemset in ls_itemset:
            if AssociationRule.is_in_set(set_a, itemset):
                return True

        return False

    def generation(self, ls_itemset):
        new_ls_itemset = list()
        for itemset_a in ls_itemset:
            for itemset_b in ls_itemset[ls_itemset.index(itemset_a):]:
                new_set = self.can_make_newest(itemset_a, itemset_b)
                if new_set is not None and not AssociationRule.is_set_in_ls(new_set, new_ls_itemset):
                    new_ls_itemset.append(new_set)

        return new_ls_itemset

    def load_initial(self):
        first_set = list()
        for itemset in self.data:
            for item in itemset:
                if [item, ] not in first_set and self.is_satisf_minsup([item, ]):
                    first_set.append([item, ])

        return first_set

    def clear_old_set(self, ls_itemset):
        new_ls_max_itemset = list()
        for old_itemset in self.ls_max_itemset:
            if not self.is_set_in_ls(old_itemset, ls_itemset):
                new_ls_max_itemset.append(old_itemset)

        return new_ls_max_itemset + ls_itemset

    def exc_cal_ls_max_itemset(self):
        ls_itemset = self.load_initial()
        self.ls_max_itemset = ls_itemset

        while ls_itemset.__len__() > 0:
            # print(ls_itemset)
            ls_itemset = self.generation(ls_itemset)
            self.ls_max_itemset = self.clear_old_set(ls_itemset)

    @staticmethod
    def get_ls_item(itemset, num_item):
        return [[j for j in i] for i in combinations(itemset, num_item)]

    def get_ls_assoc(self):
        for itemset in self.ls_max_itemset:
            for i in range(1, itemset.__len__()):
                ls_src = AssociationRule.get_ls_item(itemset, i)
                for j in range(1, itemset.__len__() - i + 1):
                    ls_des = AssociationRule.get_ls_item(itemset, j)
                    self.make_assoc(ls_src, ls_des, self.ls_assoc)

    def make_assoc(self, ls_src, ls_des, ls_assoc):
        for item_src in ls_src:
            for item_des in ls_des:
                if self.can_make_newest(item_src, item_des):
                    self.ls_assoc.append(','.join(item_src) + '->' + ','.join(item_des))

    def can_make_assoc(self, p, q):
        return not AssociationRule.is_in_set(p, q) and not AssociationRule.is_in_set(q, p) and \
               AssociationRule.freq_of_set(p + q)/AssociationRule.freq_of_set(p) >= self.min_conf

    @staticmethod
    def load_data(file_name):
        if not os.path.exists(file_name):
            print('Could not found', file_name)

        return [[j for j in i.split(', ')] for i in open(file_name, 'r').read().split('\n')]

