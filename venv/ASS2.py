def is_int(string):
    if string[0] == '-':
        return is_unsigned(string[1:])
    return is_unsigned(string)


def is_unsigned(string):
    if not string:
        return True
    elif is_digit(string[0]):
        return is_unsigned(string[1:])
    return False


def is_digit(digit):
    return digit.isdigit()


def is_attribute_list(string, arr_of_table):
    if (string == "*"):
        return True
    else:
        return is_att_list(string, arr_of_table)


# recursive function which check the attributes
def is_att_list(string, arr_of_table):
    if (is_single_attribute(string, arr_of_table) == True):
        return True
    elif not string:
        return False

    else:
        i = string.find(",")
        if i == -1:
            i = 0
        if (is_single_attribute(string[0:i], arr_of_table) == True):
            return (is_att_list(string[i + 1:], arr_of_table))


def compare_attribute(string):
    if string == "R.A":
        return True
    elif string == "R.B":
        return True
    elif string == "R.C":
        return True
    elif string == "R.D":
        return True
    elif string == "R.E":
        return True
    elif string == "S.D":
        return True
    elif string == "S.E":
        return True
    elif string == "S.F":
        return True
    elif string == "S.H":
        return True
    elif string == "S.I":
        return True
    else:
        return False


# checking if its the right attribute and table
def is_single_attribute(string, arr_of_table):
    flag = False
    # in case there is only one table
    if isinstance(arr_of_table, str):
        if string.split(".")[0] != arr_of_table:
            return False

    else:
        # in case there are more then one table
        for arr_i in arr_of_table:
            if arr_i == string:
                flag = True
                return True
        if not flag:
            return False


########################################################################

# checking if its the correct table
def is_single_table(string):
    if string == "R":
        return True
    elif string == "S":
        return True
    else:
        return False


# recursive func which check the tables
def is_table_list(string):
    if (is_single_table(string) == True):
        return True
    elif not string:
        return False
    else:
        i = string.find(",")
        if i == -1:
            i = 0
        if (is_single_table(string[0:i]) == True):
            return (is_table_list(string[i + 1:]))


#############################################################################


def is_condition(string, arr_of_table):
    if is_simple_condition(string, arr_of_table):
        return True

    elif string[0] == '(' and string[len(string) - 1] == ')':
        new_string = string[1:-1]
        if is_condition(new_string, arr_of_table):
            return True

    ANDindex = string.find("AND")
    ORindex = string.find("OR")

    if ANDindex != -1 or ORindex != -1:

        if ORindex != -1 and ANDindex != -1:
            if ANDindex < ORindex:
                if string[0] == '(' and string[ORindex - 1] == ')':
                    left_exp = string[:ORindex]
                    right_exp = string[ORindex + 2:]
                else:
                    left_exp = string[:ANDindex]
                    right_exp = string[ANDindex + 3:]
            else:
                if string[0] == '(' and string[ANDindex - 1] == ')':
                    left_exp = string[:ANDindex]
                    right_exp = string[ANDindex + 3:]
                else:
                    left_exp = string[:ORindex]
                    right_exp = string[ORindex + 2:]

        elif ORindex == -1:
            left_exp = string[:ANDindex]
            right_exp = string[ANDindex + 3:]

        else:
            left_exp = string[:ORindex]
            right_exp = string[ORindex + 2:]

        if len(left_exp) == 0 or len(right_exp) == 0:
            return False

        else:
            return is_condition(left_exp, arr_of_table) and is_condition(right_exp, arr_of_table)

    else:
        return False


def is_simple_condition(string, arr_of_table):
    op = find_op(string)
    if not op:
        return False
    splited_string = string.split(op)
    left_exp = splited_string[0]
    right_exp = splited_string[1]

    if len(left_exp) == 0 or len(right_exp) == 0:
        return False

    return is_constant(left_exp, arr_of_table) and is_constant(right_exp, arr_of_table)


# check if the given string is int, attribute or string
def is_constant(string, arr_of_table):
    if is_int(string):
        return True
    elif is_single_attribute(string, arr_of_table):
        return True
    elif is_string(string):
        return True

    else:
        return False


def is_string(string):
    if len(string) > 2:
        if (string[0] == '"' and string[len[string] - 1] == "'") or \
                (string[0] == "’" and string[len(string) - 1] == "’") or \
                (string[0] == "'" and string[len(string) - 1] == "'"):
            return True

    return False


# function to find the operator in the string
def find_op(string):
    op = False
    for x in string:
        if op != False:
            if is_rel_op(op + x):
                op = op + x
            return op

        if is_rel_op(x):
            op = x

    return op


# checking the operations
def is_rel_op(string):
    if string == "=":
        return True
    elif string == "<>":
        return True
    elif string == ">=":
        return True
    elif string == "<=":
        return True
    elif string == ">":
        return True
    elif string == "<":
        return True
    else:
        return False