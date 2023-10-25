""" This module contains the Printable class, which is used to print the contents of a class object to the console."""


class Printable:
    def __repr__(self):
        return str(self.__dict__)