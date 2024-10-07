# read text file and put all values into a list with each line as its own list
file_in = open('test0.txt', 'r').read()
split_file = file_in.split('\n')
CNF_formula_list = [list(map(int, line.split(' '))) for line in split_file]


# finds m which is the max absolute value of CNF_formula_list 
m = max(CNF_formula_list[0])
for i in range(len(CNF_formula_list)):
    sublist = (CNF_formula_list[i])
    for j in range (len(sublist)):
        if (m < abs(sublist[j])):
            m = abs(sublist[j])


# make edges_list which is a list of lists that stores the edges between the nodes of size 2m
edges_list = [[] for _ in range (2*m)]

# make assignments_list which stores the assignments of each variable of size 2m (currently all 0)
# 0  means unknown if true or false (not checked yet)
# 2  means currently true
# -2 means currently false
# 1  means permanently true
# -1 means permanently false
assignments_list = [0] * 2 * m


# edges(a,b): stores edges in edges_list
# a and b are the two values from each line of the input file
# if a = b, then automatically set permanent true and permenent false values, but still add to edges_list
def edges(a,b):
    if (a > 0):
        edges_list[2*a-1].append(b)
    else: 
        edges_list[2*abs(a)-2].append(b)
    if (b > 0):
        edges_list[2*b-1].append(a)
    else: 
        edges_list[2*abs(b)-2].append(a)


# first_unknown(): finds the first variable in assignments_list that is 0 and passes it twice through check_assignments to check assignments             
def first_unknown():
    for i in range(len(assignments_list)):
        if (assignments_list[i] == 0):
            first_unknown_variable = int((i+2)/2)
            check_assignments(first_unknown_variable, first_unknown_variable)
            break


# check_assignments(n, original): checks the current assignments using recursion 
# current_assignment is what is changing in each check_assignments call
# original assignment is the original assignment value that is used for the base case 
def check_assignments(current_assignment, original_assignment):
    # for postive current assignments 
    if current_assignment > 0:
        # positive_index: turns current_assignment into index
        #             ex. 1 -> 0
        #                 3 -> 4
        #                 8 -> 14
        positive_index = 2 * current_assignment - 2  

        # if the assignment at positive_index is 0 then set as 2 and its negation as -2 and then make the recursive call with its edges 
        if (assignments_list[positive_index] == 0):
            assignments_list[positive_index] = 2
            assignments_list[2 * current_assignment - 1] = -2
            for i in range (len(edges_list[positive_index])):                  
                # if the edge equals the original_assignment then skip check_assignment for this edge (it will keep looping)
                if (edges_list[positive_index][i] == original_assignment):
                    continue
                check_assignments(edges_list[positive_index][i], original_assignment)
        # if the assignment at positive_index is -2 or -1, then this is a contradiction
        elif ((assignments_list[positive_index] == -2)):
            # if the original_assignment is greater than 0 (hasn't been reset yet), then quick_reset() and check_assignments for - original assignment
            if (original_assignment > 0):    
                quick_reset()
                check_assignments(- original_assignment, - original_assignment)
            # if the original_assigment is less than 0 (already has been reset once), then print "FALSE" and exit program
            else:    
                print("FALSE")
                exit()
    
    # for negative current assignments            
    elif current_assignment < 0:
        # negative_index: turns current_assignment into index
        #             ex. -1 -> 1
        #                 -3 -> 5
        #                 -8 -> 15
        negative_index = 2 * abs(current_assignment) - 1 

        # if the assignment at negative_index is 0 then set as 2 and its negation as -2 and then make the recursive call with its edges 
        if (assignments_list[negative_index] == 0):
            assignments_list[negative_index] = 2
            assignments_list[2 * abs(current_assignment) - 2] = -2
            for i in range (len(edges_list[negative_index])):
                # if the edge equals the original_assignment then skip check_assignment for this edge (it will keep looping)
                if (edges_list[negative_index][i] == original_assignment):
                    continue
                check_assignments(edges_list[negative_index][i], original_assignment)
        # if the assignment at negative_index is -2 or -1, then this is a contradiction
        elif ((assignments_list[negative_index] == -2)):
            # if the original_assignment is greater than 0 (hasn't been reset yet), then quick_reset() and check_assignments for - original assignment
            if (original_assignment > 0):    
                quick_reset()
                next_check = - original_assignment 
                check_assignments(next_check, next_check)
            # if the original_assigment is less than 0 (already has been reset once), then print "FALSE" and exit program
            else:    
                print("FALSE")
                exit()
   
   # BASE CASE: if current assignment = original_assignment then no contradictions and make_perms and after first_unknown() to check next 0
    if (current_assignment == original_assignment):
        make_perm()
        first_unknown()


# quick_reset(): make every -2 or 2 in assignments_lists to 0
def quick_reset():
    for i in range(len(assignments_list)):
        if ((assignments_list[i] == 2) or (assignments_list[i] == -2)):
            assignments_list[i] = 0


# make_perm(): make every -2 or 2 in assignments_lists to -1 and 1, respectively
def make_perm():
    for i in range(len(assignments_list)):
        if (assignments_list[i] == 2):
            assignments_list[i] = 1
        elif (assignments_list[i] == -2):
            assignments_list[i] = -1


# gets a and b, the two values from each line of the input file
for i in range(len(CNF_formula_list)):
    sublist = CNF_formula_list[i]
    a = sublist[0]
    b = sublist[1]
    edges(a,b) 


# calling first_unknown starts the entire checking assignments process
first_unknown()


# if no contradictions exist, then print "TRUE ASSIGNMENTS: " and assignments_list
print("TRUE ASSIGNMENTS: ")
print(assignments_list)   
