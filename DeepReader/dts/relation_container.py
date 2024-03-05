class Relation_Container(object):

    def __init__(self, relation_name = "", opposite_relation = "", name_to_save_with = ""):
        self.__relation_name = relation_name
        self.__opposite_relation = opposite_relation
        self.__name_to_save_with = name_to_save_with

    @property
    def relation_name(self):
        return self.__relation_name

    @property
    def opposite_relation(self):
        return self.__opposite_relation

    @property
    def name_to_save_with(self):
        return self.__name_to_save_with

    # @relation_name.setter
    # def relation_name(self, relation_name):
    #     self.__relation_name = relation_name
