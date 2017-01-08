import numpy as np
import scipy.sparse as sp


class ExprData():

    def __init__(self, sparsity=None, inplace=False, make_copy=False, macro_name=None,
                       work_int=0, work_float=0, size=(1,1)):
        if sparsity == None:
            sparsity = sp.csr_matrix(np.full(size, True, dtype=bool))
        self.sparsity = sparsity
        self.inplace = inplace
        self.make_copy = make_copy
        self.macro_name = macro_name
        self.work_int = work_int
        self.work_float = work_float

    def force_copy(self):
        self.copy = True



#def get_expr_data(expr, data_args=[]):
#    if isinstance(expr, Variable):
#        return VariableData(expr, data_args)
#    elif isinstance(expr, CallbackParam):
#        return CallbackParamData(expr, data_args)
#    elif isinstance(expr, Parameter):
#        return ParameterData(expr, data_args)
#    elif isinstance(expr, Constant):
#        return ConstantData(expr, data_args)
#    else:
#        print(EXPR_TO_EXPRDATA[type(expr)](expr))
#        return EXPR_TO_EXPRDATA[type(expr)](expr, data_args)


#TODO remove?  not necessary?
#class VariableData(ExprData):
#    def __init__(self, expr, data_args):
#        self.sparsity = sp.csr_matrix(np.full(expr.size, True, dtype=bool))
#        self.work_float = 0
#        self.work_int = 0
#
#
#class ParameterData(ExprData):
#    def __init__(self, expr, data_args):
#        self.sparsity = sp.csr_matrix(np.full(expr.size, True, dtype=bool))
#        self.work_float = 0
#        self.work_int = 0
#
#
#class ConstantData(ExprData):
#    def __init__(self, expr, data_args):
#        self.sparsity = sp.csr_matrix(expr.value, shape=expr.size, dtype=bool)
#        self.work_float = 0
#        self.work_int = 0
#
#
#class CallbackParamData(ExprData):
#    def __init__(self, expr, data_args):
#        self.sparsity = data_args[0].sparsity 
#        self.work_float = 0
#        self.work_int = 0
