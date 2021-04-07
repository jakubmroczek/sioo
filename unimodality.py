from function import FunctionInterval

def is_function_unimodal_in_interval(function, functionInterval, unimodal_check_n):
    x1, x2 = functionInterval.low, functionInterval.high
    function_x1, function_x2 = function.evalute(x1), function.evalute(x2)
    step = abs(x2 - x1) / unimodal_check_n

    minimum_found = False

    for i in range(1, unimodal_check_n + 1):
        x = x1 + step * i
        function_x = function.evalute(x)

        if not minimum_found:
            if function_x1 < function_x:
                minimum_found = True
            # Function has to be strictly unimodal, hence it can not be constant on some interval
            if function_x1 == function_x:
                return False
        else:
            if not function_x1 <= function_x:
                return False

        function_x1 = function_x

    return True

def exhaustive_search_method(function, functionInterval, n):
    # Step 1
    x_1 = functionInterval.low
    delta_x = (functionInterval.high - functionInterval.low) / n

    x_2 = x_1 + delta_x
    x_3 = x_2 + delta_x

    # Step 2
    function_x_1 = function.evalute(x_1)
    function_x_2 = function.evalute(x_2)
    function_x_3 = function.evalute(x_3)

    while True:
        if function_x_1 >= function_x_2 and function_x_2 <= function_x_3:
            return FunctionInterval(x_1, x_3)
        else:
            x_1 = x_2
            x_2 = x_3
            x_3 = x_2 + delta_x

            # Cache the already computed stuff
            function_x_1 = function_x_2
            function_x_2 = function_x_3
            function_x_3 = function.evalute(x_3)

        if x_3 > functionInterval.high:
            raise Exception(f'Nie istnieje minimum wprzedziale {functionInterval} lub punkt brzegowy {functionInterval} jest '
                            f'punktem '
                            f'minimalnym')

