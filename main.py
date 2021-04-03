# assume we look for miniums

def get_function():
    pass


def get_function_range():
    pass


def is_function_unimodal_in_range(function, range):
    pass


def get_unimodal_range(function, range):
    pass


def run_function(function, range):
    pass


def visualize_result(result):
    pass


if __name__ == '__main__':
    function = get_function()
    range = get_function_range()


    if not is_function_unimodal_in_range(function, range):
        range = get_unimodal_range(function, range)


    result =  run_function(function, range)
    visualize_result(result)