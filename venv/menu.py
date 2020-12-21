
from main import *
import random
import copy
def menu_part():
    print("Hello, Please Enter Your Query")
    #query = input()
    #query = "SELECT R.D, S.E FROM R,S WHERE R.D>4 " ###not working -  the problem is on create query: condition of sigma is just R.D> and not R.D>4    :(
    #    query = "SELECT R.D, S.E FROM R,S WHERE (S.B>4 AND (R.A=10 AND S.E=2)) AND S.A=4 ;"
    #query = "SELECT R.D, S.E FROM R,S WHERE (S.B>4 OR (R.A=10 OR S.E=2)) AND S.A=4 ;" ##not working
    #query = "SELECT R.D, S.E FROM R,S WHERE S.E = R.E AND S.D = R.D;"
    query = "SELECT R.D, S.E FROM R,S WHERE S.B>4 AND S.B=12 ;"
  #  query = "SELECT R.D, S.E FROM R,S WHERE S.B>4 AND (S.B=12 AND S.C=6) ;"
   # query = "SELECT R.D, S.E FROM R,S WHERE S.B>4 OR (S.B=12 AND S.C=6) ;"
   #query = "SELECT R.D, S.E FROM R,S WHERE (S.B=12 AND S.C=6) OR (S.B=12 AND S.C=6) ;" ##not working


    my_option = Switch(query)
    while True:

        print("\nChoose One Of The Option:")
        print("[1] part 1")
        print("[2] part 2")
        print("[3] part 3")
        print("[4] Exit")
        option = input()

        if option == "4":
            print("Bye")
            break
        else:
            my_option.switch_function(option)


class Switch():
    def __init__(self, query):
        self.query = query
        self.list = None

    def switch_function(self, option):
        default = "Invalid Option"
        return getattr(self, 'function_part_' + str(option), lambda: print(default))()

    def switch_rule(self, rule):
        default = "Invalid Option"
        return getattr(self, 'rule_' + str(rule), lambda: print(default))()

    def menu_rule(self):
        print("Which Rule Would You Like To Run? ")
        rule = input()
        self.switch_rule(rule)

    def function_part_1(self):
        print("part 1", self.query)
        self.menu_rule()

    def function_part_2(self):
        # main_list1 = create_list(self.query)
        # main_list12 = create_list(self.query)
        # print(main_list1.head.is_equal(main_list12.head))

        lists_arr = [None, None, None, None]
        rules_arr = ["4a", "5a", "6", "6a", "11b"] #add 4
        #main_list = create_list(self.query)

        while lists_arr[3] is None:
            #main_list = None
            for i in range(10):
                rule = random.choice(rules_arr)
                main_list = self.switch_rule(rule)
                print(rule)
                main_list.print_query()
            index = lists_arr.index(None)
            flag = False
            for j in range(index):
                if lists_arr[j].head.is_equal(main_list.head):
                    flag = True
            if not flag:
                lists_arr[index] = copy.deepcopy(main_list)
            for y in range(4):
                print("arr[", y, "] ", end='', sep='')
                if lists_arr[y] is not None:
                    lists_arr[y].print_query()
                else:
                    print("None")
            self.list = None

        for y in range(4):
            print("arr[", y, "] ", end='', sep='')
            if lists_arr[y] is not None:
                lists_arr[y].print_query()
            else:
                print("None")


    def function_part_3(self):
        print("part 3")

    def rule_4(self):

        print("rule_4")

    def rule_4a(self):
        print("rule 4a")
        if self.list is None:
            main_list = create_list(self.query)
        else:
            main_list = self.list

        curr = main_list.head
        prev = None
        while curr is not None:
            if curr.name == "SIGMA":
                sigma_1 = curr
                if curr.next.name == "SIGMA":
                    sigma_2 = curr.next
                    prev.next = sigma_2
                    temp = sigma_2.next
                    sigma_2.next = sigma_1
                    sigma_1.next = temp
                    break
            prev = curr
            curr = curr.next
        self.list = main_list
        main_list.print_query()
        return main_list


    def rule_6(self):
        print("rule 6")

        if self.list is None:
            main_list = create_list(self.query)
        else:
            main_list = self.list
        main_list.print_query()
        curr = main_list.head
        prev = None
        arr = ["R.A", "R.B", "R.C", "R.D", "R.E"]
        while curr is not None:
            if curr.name == "SIGMA":
                sigma = curr.condition

                if curr.next.name == "CARTESIAN" or curr.next.name == "NJOIN":
                    if is_condition(sigma, arr):
                        add_to_R = Node()
                        add_to_R.name = "SIGMA"
                        add_to_R.condition = sigma
                        curr.next.list_sigma_R_inside.inset_node_to_begin_list(add_to_R)
                        main_list.delete_node_from_list(curr)
                        break
            prev = curr
            curr = curr.next

        #main_list.print_query()
        self.list = main_list
        return main_list

    def rule_6a(self):
        print("rule 6a")

        if self.list is None:
            main_list = create_list(self.query)
        else:
            main_list = self.list
        main_list.print_query()
        curr = main_list.head
        prev = None
        arr = ["S.D", "S.E", "S.F", "S.H", "S.I"]
        while curr is not None:
            if curr.name == "SIGMA":
                sigma = curr.condition

                if curr.next.name == "CARTESIAN" or curr.next.name == "NJOIN":
                    if is_condition(sigma, arr):
                        add_to_S = Node()
                        add_to_S.name = "SIGMA"
                        add_to_S.condition = sigma
                        curr.next.list_sigma_S_inside.inset_node_to_begin_list(add_to_S)
                        main_list.delete_node_from_list(curr)
                        break
            prev = curr
            curr = curr.next

        self.list = main_list
        #main_list.print_query()
        return main_list

    def rule_5a(self):
        print("rule 5a")

        if self.list is None:
            main_list = create_list(self.query)
        else:
            main_list = self.list
        main_list.print_query()
        curr = main_list.head
        prev = None
        while curr is not None:
            if curr.name == "PI":
                pi = curr.attributes
                if pi.find(',') != -1:
                    pi = pi.split(',')

                if curr.next.name == "SIGMA":
                    sigma = curr.next
                    condition = sigma.condition
                    if is_condition(condition, pi):
                        if prev is None:
                            main_list.head = sigma
                            temp = sigma.next
                            sigma.next = curr
                            curr.next = temp
                        else:
                            prev.next = sigma
                            temp = sigma.next
                            sigma.next = curr
                            curr.next = temp

                        break

            prev = curr
            curr = curr.next

        self.list = main_list
        #main_list.print_query()
        return main_list

    def rule_11b(self):
        print("rule 11b")

        if self.list is None:
            main_list = create_list(self.query)
        else:
            main_list = self.list
        #main_list = self.rule_6()
        main_list.print_query()
        curr = main_list.head
        prev = None
        while curr is not None:
            if curr.name == "SIGMA":
                sigma = curr.condition

                if curr.next.name == "CARTESIAN":
                    if is_NJOIN(sigma):
                        NJOIN_node = Node()
                        NJOIN_node.name = "NJOIN"
                        R_node = Node()
                        R_node.name = "NJOIN"
                        R_node.tables = "R"
                        NJOIN_node.list_sigma_R_inside.inset_node_to_begin_list(R_node)

                        S_node = Node()
                        S_node.name = "NJOIN"
                        S_node.tables = "S"
                        NJOIN_node.list_sigma_S_inside.inset_node_to_begin_list(S_node)

                        main_list.insert_node_to_end_list(NJOIN_node)
                        main_list.delete_node_from_list(curr.next)
                        main_list.delete_node_from_list(curr)
                        break
            prev = curr
            curr = curr.next

        #main_list.print_query()
        self.list = main_list
        return main_list

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
                if string[0] == '(' and string[ORindex-1] == ')':
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

    return  is_constant(left_exp, arr_of_table) and is_constant(right_exp, arr_of_table)


#check if the given string is int, attribute or string
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
                (string[0] == "’" and string[len(string) - 1] == "’") or\
                (string[0] == "'" and string[len(string) - 1] == "'"):
            return True

    return False

#function to find the operator in the string
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

def is_NJOIN(string):

    if string.find("AND") == -1:
        return False
    split_string = string.split("AND")
    if len(split_string) != 2:
        return False

    if split_string[0] == "R.D=S.D" or split_string[0] == "S.D=R.D":
        if split_string[1] == "R.E=S.E" or split_string[1] == "S.E=R.E":
            return True

    if split_string[0] == "R.E=S.E" or split_string[0] == "S.E=R.E":
        if split_string[1] == "R.D=S.D" or split_string[1] == "S.D=R.D":
            return True

    return False



menu_part()
