from pprint import pprint, pformat


class Type:
    __name: str
    __type_id: int

    _fields = (
        'name',
        'type_id',
    )

    def setup(self, name: str, type_id: int):
        self.__name = name
        self.__type_id = type_id

    @property
    def name(self):
        return self.__name

    @property
    def type_id(self):
        return self.__type_id

    def __str__(self):
        return f"<Type name={self.name}, type_id={self.type_id}>"
