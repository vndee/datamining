from datamining.rule import AssociationRule


if __name__ == '__main__':
    assoc = AssociationRule()
    assoc.data = assoc.load_data('media/data.txt')
    assoc.exc_cal_ls_max_itemset()
    assoc.get_ls_assoc()
    print('ls_max_itemset:', assoc.ls_max_itemset)
    print('ls_assoc:', assoc.ls_assoc)