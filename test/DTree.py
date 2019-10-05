from datamining.tree import DTree


if __name__ == '__main__':
    dtree = DTree()
    dtree.load_data('media/processed.cleveland.data')
    dtree.training()
    dtree.validate()
    dtree.plot()
    print(dtree.predict([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]]))
