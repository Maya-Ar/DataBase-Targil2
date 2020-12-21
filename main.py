class Node:
    def __init__(self):
        self.name = "UNDEFINED"
        self.condition = None  # for sigma
        self.attributes = None  # for pi
        self.tables = None  # for cartesian
        self.list_sigma_R_inside = LinkedList()
        self.list_sigma_S_inside = LinkedList()
        self.n_join = None
        self.next = None

    def is_equal(self, other):
        if (self is None and other is not None) or (self is not None and other is None):
            return False

        if self is None and other is None:
            return True

        if self.name != other.name:
            return False
        if self.condition != other.condition:
            return False
        if self.attributes != other.attributes:
            return False
        if self.tables != other.tables:
            return False
        if self.n_join != other.n_join:
            return False
        if (self.list_sigma_R_inside.head is None and other.list_sigma_R_inside.head is not None) \
                or (self.list_sigma_R_inside.head is not None and other.list_sigma_R_inside.head is None):
            return False
        if (self.list_sigma_R_inside.head is not None) and (other.list_sigma_R_inside.head is not None):
            if not self.list_sigma_R_inside.head.is_equal(other.list_sigma_R_inside.head):
                return False
        if (self.list_sigma_S_inside.head is None and other.list_sigma_S_inside.head is not None) \
                or (self.list_sigma_S_inside.head is not None and other.list_sigma_S_inside.head is None):
            return False
        if (self.list_sigma_S_inside.head is not None) and (other.list_sigma_S_inside.head is not None):
            if not self.list_sigma_S_inside.head.is_equal(other.list_sigma_S_inside.head):
                return False

        if (self.next is None and other.next is not None) or (self.next is not None and other.next is None):
            return False

        if self.next is None and other.next is None:
            return True

        return self.next.is_equal(other.next)


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    # def is_equal_lists(self, other):
    #     if (self is None and other is not None) or (self is not None and other is None):
    #         return False
    #
    #     if self is None and other is None:
    #         return True
    #
    #     return self.head.is_equal(other.head)

    def print_query(self):
        counter = 0
        curr = self.head
        while curr:
            if curr.name == "PI":
                print(curr.name, '[', curr.attributes, '](', end='', sep='')
                counter = counter + 1
            elif curr.name == "SIGMA":
                print(curr.name, '[', curr.condition, '](', end='', sep='')
                counter = counter + 1
            elif curr.name == "CARTESIAN" or curr.name == "NJOIN":
                print(curr.name, '(', end='', sep='')
                curr.list_sigma_R_inside.print_list()
                print(",", end='', sep='')
                curr.list_sigma_S_inside.print_list()
                print(')', end='', sep='')

            curr = curr.next
        print(")" * counter)
        print('\n')

    def print_list(self):
        curr = self.head
        counter = 0
        while curr is not None:
            if self.size == 1:
                print(curr.tables, end='', sep='')
                return
            else:
                if curr.name == "CARTESIAN" or curr.name == "NJOIN":
                    print(curr.tables, ')', end='', sep='')
                if curr.name == "SIGMA":
                    print(curr.name, '[', curr.condition, '](', end='', sep='')
                    counter = counter + 1

            curr = curr.next

    def insert_node_to_end_list(self, node):
        if self.head is None:
            self.head = node
            return

        tail = self.head
        while tail.next:
            tail = tail.next
        tail.next = node

    def delete_node_from_list(self, node):
        temp = self.head

        # If head node itself holds the key to be deleted
        if temp is not None:
            if temp == node:
                self.head = temp.next
                temp = None
                return

        # Search for the key to be deleted, keep track of the
        # previous node as we need to change 'prev.next'
        while temp is not None:
            if temp == node:
                break
            prev = temp
            temp = temp.next

        # if key was not present in linked list
        if (temp == None):
            return

        # Unlink the node from linked list
        prev.next = temp.next

        temp = None

    def inset_node_to_begin_list(self, node):
        node.next = self.head
        self.head = node
        self.size = self.size + 1


def create_list(query):
    query = remove_spaces(query)
    # divide the query to parts
    attributes = query.split("FROM")
    PI = attributes[0].split("SELECT")[1]

    condition = query.split("WHERE")
    SIGMA = condition[1]
    SIGMA = SIGMA[0:-1]

    CARTESIAN = condition[0].split("FROM")[1]

    query_list = LinkedList()
    PI_node = Node()
    PI_node.name = "PI"
    PI_node.attributes = PI
    query_list.insert_node_to_end_list(PI_node)

    #################################################
    # SIGMA_node2 = Node()
    # SIGMA_node2.name = "SIGMA"
    # SIGMA_node2.condition = "S.E=2"
    # query_list.insert_node_to_end_list(SIGMA_node2)
    #################################################

    SIGMA_node = Node()
    SIGMA_node.name = "SIGMA"
    SIGMA_node.condition = SIGMA
    query_list.insert_node_to_end_list(SIGMA_node)

    CARTESIAN_node = Node()
    CARTESIAN_node.name = "CARTESIAN"
    # CARTESIAN_node.tables = CARTESIAN
    R_node = Node()
    R_node.name = "CARTESIAN"
    R_node.tables = "R"
    CARTESIAN_node.list_sigma_R_inside.inset_node_to_begin_list(R_node)

    S_node = Node()
    S_node.name = "CARTESIAN"
    S_node.tables = "S"
    CARTESIAN_node.list_sigma_S_inside.inset_node_to_begin_list(S_node)

    # temp = Node()
    # temp.name = "SIGMA"
    # temp.condition = "S.E>10"
    # CARTESIAN_node.list_sigma_S_inside.inset_node_to_begin_list(temp)

    query_list.insert_node_to_end_list(CARTESIAN_node)

    # query_list.print_query()

    return query_list


def remove_spaces(string):
    if len(string) == 0:
        return ""
    else:
        new_string = ""
        for char in string:
            if char != " ":
                new_string += char
        return new_string


def rule_4(sigma_list):
    ANDindex = find_and(sigma_list[1])

    if ANDindex == -1:
        return False

    left_exp = sigma_list[1][0:ANDindex]
    right_exp = sigma_list[1][ANDindex + 3:]

    newSelectionList = ["SIGMA", right_exp, sigma_list[2]]
    SelectionList = ["SIGMA", left_exp, newSelectionList]

    return SelectionList


def find_and(sigma):
    ANDindex = sigma.find("AND")

    if ANDindex == -1:
        return -1

    if sigma[0] == '(':
        right_exp = sigma[ANDindex + 3:]
        ANDindex = ANDindex + 3 + find_and(right_exp)

    return ANDindex

# query = "SELECT R.D, S.E FROM R,S WHERE R.E=S.E AND R.D=S.D ;"
# query = "SELECT R.D, S.E FROM R,S WHERE S.E > 3;"
# create_list(query)
