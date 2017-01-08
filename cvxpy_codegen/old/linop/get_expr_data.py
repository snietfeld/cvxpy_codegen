from cvxpy.expressions.constants.callback_param import CallbackParam
from cvxpy.expressions.constants.parameter import Parameter
from cvxpy.expressions.constants.constant import Constant
from cvxpy.expressions.variables.variable import Variable
from cvxpy_codegen.templates.atoms.atoms import EXPR_TO_EXPRDATA
from cvxpy_codegen.param.expr_data import ExprData


def get_expr_data(expr, data_args=[]):
    if isinstance(expr, Variable):
        return getdata_variable(expr, data_args)
    elif isinstance(expr, CallbackParam):
        return getdata_callbackparam(expr, data_args)
    elif isinstance(expr, Parameter):
        return getdata_parameter(expr, data_args)
    elif isinstance(expr, Constant):
        return getdata_constant(expr, data_args)
    else:
        return EXPR_TO_EXPRDATA[type(expr)](expr, data_args)


def getdata_variable(expr, data_args):
    return ExprData(size=expr.size)


def getdata_parameter(expr, data_args):
    return ExprData(size=expr.size)


def getdata_constant(expr, data_args):
    return ExprData(size=expr.size)


def getdata_callbackparam(expr, data_args):
    return ExprData(sparsity = data_args[0].sparsity)
