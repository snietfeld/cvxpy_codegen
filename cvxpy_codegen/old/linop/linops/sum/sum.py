def getdata_sum_lo(linop, args, var):
    #print("\n\nSUM")
    #print(linop.name)
    #print(args[0].name)
    #print(args[0].sparsity.shape)
    #print(args[1].name)
    #print(args[1].sparsity.shape)
    #print("\n")
    #print(linop.name)
    #print(var.name)
    #print("SUM")
    #for a in args:
    #  print("arg:")
    #  print(a.sparsity)
    #  print("result:")
    #print(sparsity)
    #print(sparsity.shape)
    #print(linop.size)

    if len(args) == 1:
        return { "sparsity"    : args[0].sparsity,
                 "work_int"    : 0,
                 "work_float"  : 0,
                 'inplace'     : True,
                 "macro_name"  :'null'}
    else:
        work_int   = linop.size[0] * linop.size[1]
        work_float = linop.size[0] * linop.size[1]
        sparsity = sum([a.sparsity for a in args])
        return { "sparsity"    : sparsity,
                 "work_int"    : work_int,
                 "work_float"  :  work_float,
                 "macro_name"  :'sum'}
