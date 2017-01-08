from cvxpy_codegen.templates.linops.sum.sum import *
from cvxpy_codegen.templates.linops.neg.neg import *
from cvxpy_codegen.templates.linops.index.index import *


#GET_LINOPDATA = {'sum'  : getdata_sum_lo,
#                 'neg'  : getdata_neg_lo}

GET_LINOPDATA = {'sum'      : getdata_sum_lo,
                 'index'    : getdata_index_lo,
                 'neg'      : getdata_neg_lo}
