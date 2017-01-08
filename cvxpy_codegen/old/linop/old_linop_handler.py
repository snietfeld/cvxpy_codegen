import cvxpy_codegen.linop.lin_to_mat as l2m
import cvxpy.lin_ops as lo
import cvxpy_codegen.linop.sym_matrix as sym
from cvxpy_codegen import Variable
#from sprs_data import SparsityData


DEFAULT_TEMPLATE_VARS = {'SymAdd'    : sym.SymAdd,
                         'SymMult'   : sym.SymMult,
                         'SymDiv'    : sym.SymDiv,
                         'SymParam'  : sym.SymParam,
                         'SymConst'  : sym.SymConst,
                         'Variable'  : Variable }

class LinOpHandler():


    def __init__(self, sym_data, obj, eq_constr, leq_constr):
        self.sym_data = sym_data
        self.obj = obj
        self.eq_constr = eq_constr
        self.leq_constr = leq_constr
        self.template_vars = DEFAULT_TEMPLATE_VARS
        #self.named_vars = []
        #self.sprs_data = SparsityData() # TODO


    def obj_to_mat(self, obj):
        obj_coeff, obj_offset = self.process_linop(obj, 
                                    horz_size=self.sym_data.x_length)
        return obj_coeff, obj_offset


    def constrs_to_mat(self, constraints):
        constr_size = sum([c.size[0] for c in constraints])
        x_len = self.sym_data.x_length
        matrix = sym.zeros(constr_size, x_len)
        offset = sym.zeros(constr_size, 1)
        vert_offset = 0

        for constr in constraints:
            c_mat, c_off = self.process_linop(constr.expr, x_len,
                               vert_offset=vert_offset, vert_size=constr_size)
            matrix += c_mat
            offset += c_off
            vert_offset += constr.size[0] * constr.size[1]
        return matrix, -offset


    def get_template_vars(self):
        obj_coeff, obj_offset = self.obj_to_mat(self.obj)
        eq_coeff, eq_offset = self.constrs_to_mat(self.eq_constr)
        leq_coeff, leq_offset = self.constrs_to_mat(self.leq_constr)

        #self.sprs_data.update_eq_constr(eq_coeff)
        #self.sprs_data.update_leq_constr(leq_coeff)

        #print("\n\nEQ_COEFF")
        #print(eq_coeff.Ap)
        #print(eq_coeff.Ai)
        #print(eq_coeff.Ax)
        #print(eq_coeff.m)
        #print(eq_coeff.n)
        #print("\n\nEQ_OFFSET")
        #print(eq_offset.Ap)
        #print(eq_offset.Ai)
        #print(eq_offset.Ax)
        #print(eq_offset.m)
        #print(eq_offset.n)
        #print(eq_offset.Ax[0].args)

        #print("\n\nTHIS")
        #print(self.named_vars)
        #print(self.named_vars)

        self.template_vars.update({'obj_coeff': obj_coeff,
                                   'obj_offset': obj_offset,
                                   'eq_coeff': eq_coeff,
                                   'eq_offset': eq_offset,
                                   'leq_coeff': leq_coeff,
                                   'leq_offset': leq_offset})
                                   #'named_vars': self.named_vars})
        return self.template_vars


    def process_linop(self, linop, horz_size, vert_offset=0, vert_size=1):
        ## Get the variables.
        #self.get_var_names(linop)

        # Get the coefficients.
        coeffs = l2m.get_coefficients(linop) 
        offset = sym.zeros(vert_size, 1)
        matrix = sym.zeros(vert_size, horz_size)
        for id_, sym_mat in coeffs:
            vert_start = vert_offset 
            vert_end = vert_start + linop.size[0]*linop.size[1] 
            if id_ is lo.CONSTANT_ID: 
                sym_mat.zero_pad((vert_size, 1),
                                 (vert_start, 0))
                offset += sym_mat
            else: 
                horiz_offset = self.sym_data.var_offsets[id_] 
                sym_mat.zero_pad((vert_size, horz_size),
                                 (vert_start, horiz_offset))
                matrix += sym_mat

        return matrix, offset


    #def get_var_names(self, expr):
    #    #if isinstance(expr, Variable): # TODO keep for later
    #    if expr.type == 'variable':
    #        if not expr.name() == "%s%d" % (s.VAR_NAME, expr.id):
    #            self.named_vars += [expr]
    #    else:
    #        for arg in expr.args:
    #            self.get_var_names(arg)




