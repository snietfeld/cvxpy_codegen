from cvxpy_codegen.utils import Counter, spzeros
from cvxpy_codegen.param.expr_data import CONST_ID
import scipy.sparse as sp
import numpy as np


CONSTR_COUNT = Counter()


class ConstrData():
    
    def __init__(self, constr, linop, vert_offset):
        self.name = 'constr%d' % CONSTR_COUNT.get_count()
        self.linop = linop
        self.size = linop.size[0] * linop.size[1]
        self.vert_offset = vert_offset

    def get_matrix(self, sym_data):
        return self.linop.get_matrix(sym_data)
        #mat = spzeros(self.size, sym_data.x_length, dtype=bool)
        #coeff_height = self.linop.size[0] * self.linop.size[1]
        #for vid, coeff in self.linop.coeffs.items():
        #    if not (vid == CONST_ID): # TODO
        #        start = sym_data.var_offsets[vid]
        #        coeff_width = coeff.sparsity.shape[1]
        #        pad_left = start
        #        pad_right = sym_data.x_length - coeff_width
        #        #print('\n')
        #        #print(spzeros(coeff_height, pad_left, dtype=bool).shape)
        #        #print(coeff.sparsity.shape)
        #        #print(coeff.sparsity)
        #        #print(spzeros(coeff_height, pad_right, dtype=bool).shape)
        #        #print(coeff.macro_name)
        #        #print(coeff.name)
        #        #print(coeff.size)
        #        mat += sp.hstack([spzeros(coeff_height, pad_left, dtype=bool),
        #                          coeff.sparsity,
        #                          spzeros(coeff_height, pad_right, dtype=bool)])
        #return mat
