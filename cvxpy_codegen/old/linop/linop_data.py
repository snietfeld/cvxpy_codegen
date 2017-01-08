from cvxpy_codegen.params.expr_data import ExprData


class VarData(ExprData):
    def __init__(self, expr):
        self.type = 'var'
        self.id = expr.data
        self.name = 'var%d' % self.id # TODO
        #self.name = expr.name()
        self.arg_data = []
        self.size = expr.size
        self.length = expr.size[0] * expr.size[1]
        self.sparsity = sp.csr_matrix(sp.eye(self.length, dtype=bool))
        self.var_ids = [self.id]

    #@property
    #def vars(self):
    #    return [self]

    #@property
    #def var(self):
    #    return self



class LinOpData(ExprData):
    def __init__(self, expr, arg_data):
        super(LinOpData, self).__init__(expr, arg_data)
        self.type = 'linop'
        self.opname = expr.type
        self.name = 'linop%d' % LINOP_COUNT.get_count()
        #self.vars = set().union(*[a.vars for a in arg_data])
        self.data = expr.data
        self.args = arg_data
        self.coeffs = dict()

        # Get leaf vars for this linop.
        #self.vars = []
        self.var_ids = []
        for a1 in self.args:
            for vid in a1.var_ids:
                if vid not in self.var_ids:
                    #self.vars += [var]
                    self.var_ids += [vid]


        # Get the coefficient for each var
        for vid in self.var_ids:
            coeff_args = []
            #print(var.name)
            for arg in self.args:
                if vid in arg.var_ids:
                    if isinstance(arg, LinOpData):
                        coeff_args += [arg.coeffs[vid]]
                    else:
                        coeff_args += [arg]
            coeff_props = GET_LINOPDATA[self.opname](self, coeff_args, vid)
            coeff = LinOpCoeffData(self, coeff_args, vid, **coeff_props)
            self.coeffs.update({vid : coeff})

        #print("\n")
        #print(self.name)
        #print(self.opname)
        #print(self.args[0])
        #print(self.coeffs[0].sparsity.shape)

    def get_matrix(self, sym_data):
        coeff_height = self.size[0] * self.size[1]
        mat = spzeros(coeff_height, sym_data.x_length, dtype=bool)
        for vid, coeff in self.coeffs.items():
            if not (vid == CONST_ID): # TODO
                start = sym_data.var_offsets[vid]
                coeff_width = coeff.sparsity.shape[1]
                pad_left = start
                pad_right = sym_data.x_length - coeff_width
                #print('\n')
                #print(spzeros(coeff_height, pad_left, dtype=bool).shape)
                #print(coeff.sparsity.shape)
                #print(coeff.sparsity)
                #print(spzeros(coeff_height, pad_right, dtype=bool).shape)
                #print(coeff.macro_name)
                #print(coeff.name)
                #print(coeff.size)
                mat += sp.hstack([spzeros(coeff_height, pad_left, dtype=bool),
                                  coeff.sparsity,
                                  spzeros(coeff_height, pad_right, dtype=bool)])
        return mat




                



class LinOpCoeffData:
    def __init__(self, linop, args, vid,
                 sparsity=None,
                 inplace=False,
                 macro_name=None,
                 work_int=0,
                 work_float=0,
                 data=None):
        self.sparsity = sparsity
        self.inplace = inplace
        self.macro_name = macro_name
        self.work_int = work_int
        self.work_float = work_float
        self.data = data
        self.args = args
        #print(linop)
        #print(var)

        #if isinstance(vid, VarData):
        #    self.name = linop.name + '_' + var.name
        #else:
        #    self.name = linop.name + '_const'
        self.name = linop.name + '_var' + str(vid) # TODO
        self.type = 'coeff'
        self.vid = vid
        self.size = linop.size

#        # Constant subsumes Parameter:
#        has_c = any([type(a)=='const' or type(a)=='param' for a in arg_data])
#        if inplace and has_c:
#            self.make_copy = True
#        else:
#            self.make_copy = False
#    def force_copy(self):
#        self.make_copy = True
