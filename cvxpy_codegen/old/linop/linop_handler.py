from cvxpy.lin_ops.lin_utils import get_expr_params
from cvxpy.expressions.constants.callback_param import CallbackParam
from cvxpy.expressions.constants.parameter import Parameter
from cvxpy.expressions.constants.constant import Constant
from cvxpy_codegen.templates.atoms.atoms import GET_ATOMDATA
from cvxpy_codegen.templates.linops.linops import GET_LINOPDATA
from cvxpy_codegen.param.expr_data import ParamData, ConstData, CbParamData, VarData, LinOpData, LinOpCoeffData, CONST_ID
from copy import copy
import numpy
from cvxpy.lin_ops.lin_op import SCALAR_CONST, DENSE_CONST, SPARSE_CONST, PARAM, VARIABLE
from cvxpy_codegen.linop.constr_data import ConstrData
import scipy.sparse as sp
import numpy as np
from cvxpy_codegen.utils import spzeros
#from cvxpy.lin_ops.lin_utils import get_expr_vars



class LinOpHandler():

    
    def __init__(self, objective, eq_constr, leq_constr, sym_data):

        self.vars = [] # TODO delete?
        self.linop_coeffs = []
        self.named_params = []
        self.param_ids = []
        self.var_ids = [] # TODO delete?
        self.callback_params = []
        self.cbparam_ids = []
        self.constants = []
        self.linops = []
        self.linop_ids = []
        self.unique_linops = []
        self.id2var = dict()

        self.sym_data = sym_data

        # Get the roots of the linop trees.
        # self.root_linops = []
        # self.root_linops += [self.process_expression(objective)]
        # for constr in eq_constr:
        #     self.root_linops += [self.process_expression(constr.expr)]
        # for constr in leq_constr:
        #     self.root_linops += [self.process_expression(constr.expr)]

        self.objective  = self.process_expression(objective)
        self.eq_constr  = self.process_constr(eq_constr)
        self.leq_constr = self.process_constr(leq_constr)

        # # Get the coefficients for the linop roots.
        # self.root_coeffs = []
        # for lo in self.root_linops:
        #     for var in lo.vars:
        #         self.root_coeffs += [self.process_linop(lo, var)]



    def process_constr(self, constrs):
        constr_data = []
        vert_offset = 0
        for constr in constrs:
            expr_data = self.process_expression(constr.expr)
            constr_data += [ConstrData(constr, expr_data, vert_offset=vert_offset)]
            vert_offset += expr_data.size[0] * expr_data.size[1] 
        return constr_data



    def get_template_vars(self):

        work_int   = max([c.work_int   for c in self.linop_coeffs])
        work_float = max([c.work_float for c in self.linop_coeffs])

        obj_coeff, eq_coeff, leq_coeff = self.get_sparsity()

        #print('\n')
        #print(eq_coeff)
        #print(eq_coeff.indptr)
        #print('\n\n')
        #for c in self.eq_constr:
        #  for coeff in c.linop.coeffs.values():
        #    print(coeff.sparsity.shape)

        #print(dir(leq_coeff))
        #print(dir(self.sym_data))
        print([v.name for v in self.vars])
        print([i for i in self.var_ids])
        print(self.var_ids)

        template_vars = {'vars': self.vars,
                         'linop_coeffs': self.linop_coeffs,
                         'objective': self.objective,
                         'eq_constr': self.eq_constr,
                         'leq_constr': self.leq_constr,
                         'work_int': work_int,
                         'work_float': work_float,
                         'obj_coeff': obj_coeff,
                         'eq_coeff': eq_coeff,
                         'leq_coeff': leq_coeff,
                         'work_float': work_float,
                         'unique_linops': self.unique_linops,
                         'var_offsets' : self.sym_data.var_offsets,
                         'CONST_ID' : CONST_ID}

        return template_vars



    def get_sparsity(self):
        #print("\n\n")
        #print(self.sym_data.x_length)

        obj_coeff = self.objective.get_matrix(self.sym_data)
        
        eq_coeff = spzeros(0, self.sym_data.x_length, dtype=bool)
        for c in self.eq_constr:
            eq_coeff = sp.vstack([eq_coeff, c.get_matrix(self.sym_data)])
        
        leq_coeff = spzeros(0, self.sym_data.x_length, dtype=bool)
        for c in self.leq_constr:
            leq_coeff = sp.vstack([leq_coeff, c.get_matrix(self.sym_data)])

        return obj_coeff, eq_coeff, leq_coeff
        
        #objective = spzeros(self.sym_data, self.sym_data.x_length, dtype=bool) 
        #for c in leq_constr:
        #    obj_coeff, obj_offset = np.vcat([leq_coeff, c.get_mat])
        
            




    def process_expression(self, expr):

        if expr.type == PARAM:
            if isinstance(expr.data, CallbackParam):
                if expr.id not in self.cbparam_ids: # Check if already there.
                    data = CbParamData(expr, [data_arg]) # TODO need sparsity pattern of the param.
                    self.callback_params += [data]
                    self.cbparam_ids += [expr.id]

            elif isinstance(expr.data, Parameter):
                if expr.id not in self.param_ids: # Check if already there.
                    data = ParamData(expr)
                    self.named_params += [data]
                    self.param_ids += [expr.id]

        elif expr.type in [SCALAR_CONST, DENSE_CONST, SPARSE_CONST]:
            data = ConstData(expr)
            self.constants += [data]

        elif expr.type == VARIABLE:
            id_ = expr.data
            if id_ not in self.id2var.keys(): # Check if already there.
                data = VarData(expr)
                self.vars += [data] # TODO remove
                self.id2var[id_] = data
            else:
                data = self.id2var[id_]

        else:  # expr is a LinOp:
            if id(expr) in self.linop_ids: # Check if already there.
                idx = self.linop_ids.index(id(expr))
                self.expressions[idx].force_copy() # TODO remove [1]
                data = self.expressions[idx]
            else:
                arg_data = []
                for arg in expr.args:
                    arg_data += [self.process_expression(arg)] # recurse on args
                data = LinOpData(expr, arg_data)
                self.linop_coeffs += [data.coeffs[v] for v in data.coeffs]
                #data = LinOpData(expr, arg_data)
                self.linops += [data]
                for coeff in data.coeffs.values():
                    if coeff.macro_name not in self.unique_linops: # Check if already there.
                         self.unique_linops += [coeff.macro_name]
 

        return data


    #def process_linop(self, linop, arg_data, var):
    #    arg_data = []
    #    for idx, arg in enumerate(arg_data):
    #        if var in arg.vars:
    #            if isinstance(arg, VarData):
    #                arg_data += [arg]
    #            else:
    #                arg_data += [self.process_linop(arg, var)] # TODO should take into account the arg position, wihch is idx
    #    data = GET_LINOPDATA[linop.opname](linop, arg_data, var)
    #    self.linop_coeffs += [data]
    #    if data.macro_name not in self.unique_linops: # Check if already there.
    #        self.unique_linops += [data.macro_name]
    #    return lo_data




    #def process_linop(self, linop, var):
    #    arg_data = []
    #    for idx, arg in enumerate(linop.args):
    #        if var in arg.vars:
    #            if isinstance(arg, VarData):
    #                arg_data += [arg]
    #            else:
    #                arg_data += [self.process_linop(arg, var)] # TODO should take into account the arg position, wihch is idx
    #    data = GET_LINOPDATA[linop.opname](linop, arg_data, var)
    #    self.linop_coeffs += [data]
    #    if data.macro_name not in self.unique_linops: # Check if already there.
    #        self.unique_linops += [data.macro_name]
    #    return data


   # def assemble_matrices(self):
   #     for


    # TODO deprecated?
    def del_duplicates(self):
        #print([param.name() for param,data in  self.named_params])
        #self.named_params = list(set(self.named_params))

        # Delete duplicate params according to id.
        keys = [param.id for param,data in self.named_params]
        self.named_params = self.list_del(self.named_params, keys)[0]

        # Delete duplicate constants according to id.
        keys = [id(const) for const,data in self.constants]
        self.constants = self.list_del(self.constants, keys)[0]

        # Delete duplicate callback parameters according to id.
        keys = [param.id for param,data in self.callback_params]
        self.callback_params = self.list_del(self.callback_params, keys)[0]

        # Delete duplicate expressions according to id.
        keys = [id(expr) for expr,data in self.expressions]
        self.expressions, force_copy = self.list_del(self.expressions, keys)
        for expr,data in force_copy:
            if data.inplace:
                data.force_copy()

        self.unique_exprs = list(set([data.macro_name for (expr,data) in self.expressions]))

        #print([data.name for expr,data in self.expressions])



    # TODO could be more efficient??
    # Delete duplicate expressions, preserving order,
    # preserving earliest ocurrance:
    @staticmethod
    def list_del(l, keys):
        delete = []
        l_dup = []
        for idx1, key1 in enumerate(keys):
            for idx2, key2 in enumerate(keys[:idx1]):
                if key1 == key2:
                    delete += [idx2]
                    l_dup += [l[idx1]]
        if delete:
            delete.reverse()
            for idx in delete:
                del l[idx]
        return l, l_dup
    


    #def list_delete(l):
    #    delete = []
    #    for idx1, expr1 in enumerate(l):
    #        for idx2, expr2 in enumerate(self.expressions[:idx1]):
    #            if expr1 is expr2:
    #                delete += [idx2]
    #                expr1[1].force_copy()

    #    if delete:
    #        for idx in delete.reverse(): 
    #            del self.expressions[idx]


# TODO should this be random? How to make the code deterministic
def get_val_or_rand(param):
    if not param.value is None:
        return param.value
    else:
        return numpy.ones(param.size)













