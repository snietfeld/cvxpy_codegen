"""
Copyright 2017 Nicholas Moehle

This file is part of CVXPY-CODEGEN.

CVXPY-CODEGEN is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY-CODEGEN is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY-CODEGEN.  If not, see <http://www.gnu.org/licenses/>.
"""



class SymExpr():
    "abstract class"

    def __mul__(self, expr):
        return SymMult(self, expr)

    def __rmul__(self, expr):
        return SymMult(expr, self)

    def __add__(self, expr):
        return SymAdd(self, expr)

    def __div__(self, expr):
        return SymDiv(self, expr)

    def __neg__(self):
        return SymConst(-1.0) * self


# TODO remove?
def as_sym_const(expr):
    if isinstance(expr, float) or isinstance(expr, int):
        return SymConst(expr)
    elif isinstance(expr, SymConst):
        return expr



class SymConst(SymExpr):
    def __init__(self, value):
        self.value = float(value)

    def print(self):
        return str(self.value)
        

class SymParam(SymExpr):
    def __init__(self, param, idx, nz_idx):
        self.param = param
        #if isinstance(param, callbackparam):
        #  self.name = param.cbp_
        self.idx = idx
        self.nz_idx = nz_idx

    def print(self):
        return(self.param.name()+'['+str(self.idx[0])+','+str(self.idx[1])+']')

    @property
    def value(self): # TODO test this:
        if self.param.size == (1,1):
            return self.param.value
        else:
            return self.param.value[self.idx[0], self.idx[1]]


class SymAdd(SymExpr):
    def __init__(self, arg1, arg2):
        self.args = [arg1, arg2]

    @property
    def value(self):
        return self.args[0].value + self.args[1].value

    def print(self):
        return '( ' + self.args[0].print() + ' + ' + self.args[1].print() + ' )'

class SymMult(SymExpr):
    def __init__(self, arg1, arg2):
        self.args = [arg1, arg2]

    @property
    def value(self):
        return self.args[0].value * self.args[1].value

    def print(self):
        return '( ' + self.args[0].print() + ' * ' + self.args[1].print() + ' )'


class SymDiv(SymExpr):
    def __init__(self, arg1, arg2):
        self.args = [arg1, arg2]

    @property
    def value(self):
        return self.args[0].value / self.args[1].value

    def print(self):
        return '( ' + self.args[0].print() + ' / ' + self.args[1].print() + ' )'

