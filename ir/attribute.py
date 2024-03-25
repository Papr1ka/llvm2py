class Attribute:
    kind: int
    value: int
    value_str: str

    def __str__(self):
        for i in self.__dict__:
            if "value" in i:
                return f"<Attribute {self.__dict__[i]}>"

    def __repr__(self):
        return self.__str__()
