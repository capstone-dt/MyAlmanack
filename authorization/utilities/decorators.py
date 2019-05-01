# @classproperty decorator: https://stackoverflow.com/a/39542816/8060864
class classproperty(property):
    def __get__(self, object, type=None): return super().__get__(type)
    def __set__(self, object, value): super().__set__(type(object), value)
    def __delete__(self, object): super().__delete__(type(object))