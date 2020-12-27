from main import *
from ASS2 import *
import random
import copy


def menu_part():
    print("Hello, Please Enter Your Query")
    # query = input()
    # query = "SELECT R.D, S.E FROM R,S WHERE R.D>4 " ###not working -  the problem is on create query: condition of sigma is just R.D> and not R.D>4    :(
    # query = "SELECT R.D, S.E FROM R,S WHERE (S.B>4 AND (R.A=10 AND S.E=2)) AND S.A=4 ;"
    # query = "SELECT R.D, S.E FROM R,S WHERE (S.B>4 OR (R.A=10 OR S.E=2)) AND S.A=4 ;" ##not working
    # query = "SELECT R.D, S.E FROM R,S WHERE S.E = R.E AND S.D = R.D;"
    # query = "SELECT R.D, S.E FROM R,S WHERE R.D=4 AND R.A=10 ;"
    # query = "SELECT R.D, S.E FROM R,S WHERE S.B>4 AND (S.B=12 AND S.C=6) ;"
    # query = "SELECT R.D, S.E FROM R,S WHERE S.B>4 OR (S.B=12 AND S.C=6) ;"
    #query = "SELECT R.D, S.E FROM R,S WHERE (S.E=12 AND S.H=6) OR (S.I=12 AND S.D=6) ;"  ##not working
    query = "SELECT R.A, R.B, R.C. R.D, R.E, S.D, S.E, S.F, S.G, S.I, S.H FROM R,S WHERE (R.A=10 AND S.H=12)  AND (S.E = 2 AND S.D = 3) ;"

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
        self.four_lists = None

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
        print(self.query)
        self.menu_rule()

    def function_part_2(self):

        lists_arr = [None, None, None, None]
        rules_arr = ["4", "4a", "5a", "6", "6a", "11b"]

        while lists_arr[3] is None:
            for i in range(10):
                rule = random.choice(rules_arr)
                main_list = self.switch_rule(rule)
            index = lists_arr.index(None)
            flag = False
            for j in range(index):
                if lists_arr[j].head.is_equal(main_list.head):
                    flag = True
            if not flag:
                lists_arr[index] = copy.deepcopy(main_list)

            self.list = None

        for y in range(4):
            print("arr[", y, "] ", end='', sep='')
            if lists_arr[y] is not None:
                lists_arr[y].print_query()
            else:
                print("None")
        self.four_lists = lists_arr

    def function_part_3(self):
        f = open("statistics.txt", "r+")
        file_arr = f.readlines()
        n_R = (int)(file_arr[2].split("=")[1])
        n_S = (int)(file_arr[11].split("=")[1])
        arr_R = [0, 0, 0, 0, 0]
        arr_S = [0, 0, 0, 0, 0]

        line1 = 3
        line2 = 12
        for i in range(5):
            arr_R[i] = int(file_arr[line1].split("=")[1])
            arr_S[i] = int(file_arr[line2].split("=")[1])
            line1 = line1 + 1
            line2 = line2 + 1

        f.close()
        self.function_part_2()

        for j in range(4):
            main_list = self.four_lists[j]
            print(f"query number {j + 1}:")
            main_list.print_query()
            print('\n')
            new_list = main_list.reverse_list()

            variables = information_for_3()
            variables_R = information_for_3()
            variables_S = information_for_3()
            curr = new_list.head
            while curr:
                if curr.name == "CARTESIAN" or curr.name == "NJOIN":
                    new_R_list = curr.list_sigma_R_inside.reverse_list()
                    new_S_list = curr.list_sigma_S_inside.reverse_list()

                    curr_S = new_S_list.head
                    curr_S = curr_S.next
                    variables_S.input_n = n_S
                    variables_S.input_r = 20
                    while curr_S:
                        if curr_S.name == "SIGMA":
                            print_sigma(curr_S, variables_S, arr_R, arr_S)

                        curr_S = curr_S.next

                    curr_R = new_R_list.head
                    variables_R.input_n = n_R
                    variables_R.input_r = 20
                    curr_R = curr_R.next
                    while curr_R:
                        if curr_R.name == "SIGMA":
                            print_sigma(curr_R, variables_R, arr_R, arr_S)
                        curr_R = curr_R.next

                    print_cartesian(curr, variables, variables_R, variables_S)

                if curr.name == "SIGMA":
                    print_sigma(curr, variables, arr_R, arr_S)

                if curr.name == "PI":
                    print_pi(curr, variables)

                curr = curr.next

    def rule_4(self):
        print("rule_4")
        if self.list is None:
            main_list = create_list(self.query)
        else:
            main_list = self.list

        curr = main_list.head

        while curr is not None:
            if curr.name == "SIGMA":
                condition = curr.condition
                ANDindex = find_and(condition)
                if ANDindex != -1:
                    left_exp = condition[:ANDindex]
                    right_exp = condition[ANDindex + 3:]
                    temp = curr.next
                    add_sigma = Node()
                    add_sigma.name = "SIGMA"
                    add_sigma.condition = right_exp
                    curr.condition = left_exp
                    curr.next = add_sigma
                    add_sigma.next = temp
                    break
            curr = curr.next

        self.list = main_list
        main_list.print_query()
        return main_list

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
                    if prev:
                        prev.next = sigma_2
                    else:
                        main_list.head = sigma_2
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
        curr = main_list.head
        arr = ["R.A", "R.B", "R.C", "R.D", "R.E"]
        while curr is not None:
            if curr.name == "SIGMA":
                sigma = curr.condition
                if curr.next:
                    if curr.next.name == "CARTESIAN" or curr.next.name == "NJOIN":
                        if is_condition(sigma, arr):
                            add_to_R = Node()
                            add_to_R.name = "SIGMA"
                            add_to_R.condition = sigma
                            curr.next.list_sigma_R_inside.inset_node_to_begin_list(add_to_R)
                            main_list.delete_node_from_list(curr)
                            break
            curr = curr.next

        main_list.print_query()
        self.list = main_list
        return main_list

    def rule_6a(self):
        print("rule 6a")

        if self.list is None:
            main_list = create_list(self.query)
        else:
            main_list = self.list
        curr = main_list.head
        arr = ["S.D", "S.E", "S.F", "S.H", "S.I"]
        while curr is not None:
            if curr.name == "SIGMA":
                sigma = curr.condition
                if curr.next:
                    if curr.next.name == "CARTESIAN" or curr.next.name == "NJOIN":
                        if is_condition(sigma, arr):
                            add_to_S = Node()
                            add_to_S.name = "SIGMA"
                            add_to_S.condition = sigma
                            curr.next.list_sigma_S_inside.inset_node_to_begin_list(add_to_S)
                            main_list.delete_node_from_list(curr)
                            break

            curr = curr.next

        self.list = main_list
        main_list.print_query()
        return main_list

    def rule_5a(self):
        print("rule 5a")

        if self.list is None:
            main_list = create_list(self.query)
        else:
            main_list = self.list
        curr = main_list.head
        prev = None
        while curr is not None:
            if curr.name == "PI":
                pi = curr.attributes
                if pi.find(',') != -1:
                    pi = pi.split(',')
                if curr.next:
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
        main_list.print_query()
        return main_list

    def rule_11b(self):
        print("rule 11b")

        if self.list is None:
            main_list = create_list(self.query)
        else:
            main_list = self.list
        curr = main_list.head
        while curr is not None:
            if curr.name == "SIGMA":
                sigma = curr.condition
                if curr.next:
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

            curr = curr.next

        main_list.print_query()
        self.list = main_list
        return main_list


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


def find_and(sigma):
    ANDindex = sigma.find("AND")

    while ANDindex != -1:
        left_exp = sigma[:ANDindex]
        right_exp = sigma[ANDindex + 3:]

        count_left_par = left_exp.count("(")
        count_right_par = left_exp.count(")")

        if count_left_par == count_right_par:
            count_left_par = right_exp.count("(")
            count_right_par = right_exp.count(")")

            if count_left_par == count_right_par:
                return ANDindex

        temp_index = right_exp.find("AND")
        if temp_index == -1:
            return -1

        ANDindex = ANDindex + 3 + temp_index

    return -1


def print_sigma(curr, variables, arr_R, arr_S):
    print(curr.name + "[" + curr.condition + "]")
    print('\t', f"input: n_Scheme{variables.i}={variables.input_n} R_Scheme{variables.i}={variables.input_r}")
    variables.i = variables.i + 1
    variables.input_n = variables.input_n * replace_chars(curr.condition, arr_R, arr_S)
    print('\t', f"output: n_Scheme{variables.i}={variables.input_n} R_Scheme{variables.i}={variables.input_r}")
    print('\n')

def print_cartesian(curr, variables, variables_R, variables_S):
    print(curr.name)
    print('\t', f"input: n_R={variables_R.input_n} n_S={variables_S.input_n} "
                f"r_R={variables_R.input_r} r_S={variables_S.input_r}")
    variables.input_n = variables_S.input_n * variables_R.input_n
    variables.input_r = variables_S.input_r + variables_R.input_r
    print('\t', f"output: n_Scheme{variables.i}={variables.input_n} R_Scheme{variables.i}={variables.input_r} ")
    print('\n')

def print_pi(curr, variables):
    print(curr.name + "[" + curr.attributes + "]")
    print('\t', f"input: n_Scheme{variables.i}={variables.input_n} R_Scheme{variables.i}={variables.input_r}")
    variables.i = variables.i + 1
    if curr.attributes.find(",") == -1:
        variables.input_r = 4
    else:
        pi_arr = curr.attributes.split(",")
        variables.input_r = len(pi_arr) * 4
    print('\t', f"output: n_Scheme{variables.i}={variables.input_n} R_Scheme{variables.i}={variables.input_r}")
    print('\n')

def replace_chars(string, arr_R, arr_S):
    new_string = copy.deepcopy(string)
    new_string = new_string.replace("=", "")
    for c in new_string:
        if '0' <= c <= '9':
            new_string = new_string.replace(c, "")

    new_string = new_string.replace("R.A", "(1/" + str(arr_R[0]) + ")")
    new_string = new_string.replace("R.B", "(1/" + str(arr_R[1]) + ")")
    new_string = new_string.replace("R.C", "(1/" + str(arr_R[2]) + ")")
    new_string = new_string.replace("R.D", "(1/" + str(arr_R[3]) + ")")
    new_string = new_string.replace("R.E", "(1/" + str(arr_R[4]) + ")")
    new_string = new_string.replace("S.D", "(1/" + str(arr_S[0]) + ")")
    new_string = new_string.replace("S.E", "(1/" + str(arr_S[1]) + ")")
    new_string = new_string.replace("S.F", "(1/" + str(arr_S[2]) + ")")
    new_string = new_string.replace("S.H", "(1/" + str(arr_S[3]) + ")")
    new_string = new_string.replace("S.I", "(1/" + str(arr_S[4]) + ")")
    new_string = new_string.replace("AND", "*")
    new_string = new_string.replace("OR", "+")

    return eval(new_string)


menu_part()
