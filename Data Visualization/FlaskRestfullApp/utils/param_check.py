
def check_params(req_args, args):
    all_checked = True
    errors = []
    for arg in req_args:
        if args[arg] is None:
            all_checked = all_checked and False
            errors.append('Error: {} is missing'.format(arg))

    return [all_checked, errors]
