class Type:
    name: str
    type_id: int

    def __str__(self):
        return f"<Type name={self.name}, type_id={self.type_id}>"

