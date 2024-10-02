# Partition the string according addition or subtraction operator
def partition_add_minus_op(string, stringlist, oplist):

    # If the first value is not negative then put positive sign in front of it
    check_first_op = string.find("-")
    if check_first_op != 0 and string.find("+") != 0:
        #print(string)
        string = "+" + string
        #print(string)

    count_add = string.count("+")
    count_minus = string.count("-")
    #print(f"The count add is {count_add}")
    #print(f"The count minus is {count_minus}")

    # Use the number of the add and sub op to determine how many times of loop that are needed to do
    while count_add or count_minus != 0:

        index_add = string.find("+")
        index_minus = string.find("-")
        if count_add > 0:
            if count_minus == 0:
                #****** Use append instead of assigning to the list directly, cuz lists are dynamically sized
                # Insert the operator first
                oplist.append(string[index_add : index_add + 1])
                next_add_op = string.find("+", 1)
                # To make sure the index of the string between the first op and second op
                if next_add_op != -1:
                    stringlist.append(string[index_add + 1 : next_add_op])  
                    string = string[next_add_op : ] # Remove the part that has already save in list
                elif next_add_op == -1: # When this part of polynomial is the last
                    stringlist.append(string[index_add + 1 : ]) 
                    string = ""  # Remove the part that has already save in list

                count_add -= 1  #count_add--
                
            elif count_minus > 0:
                if string.find("+") < string.find("-"): # When count_add != 0 and the index number of add op is smaller than the index number of sub op
                    oplist.append(string[index_add : index_add + 1])
                    next_add_op = string.find("+", 1)

                    if next_add_op != -1:
                        if string.find("+", 1) < string.find("-", 1):
                            next_op = string.find("+", 1)
                        elif string.find("+", 1) > string.find("-", 1):
                            next_op = string.find("-", 1)
                    elif next_add_op == -1: # So there is only sub op left 
                        next_op = string.find("-", 1)

                    stringlist.append(string[index_add + 1 : next_op])
                    string = string[next_op : ]  # Remove the part that has already save in list
                    
                    count_add -= 1  #count_add--

                elif string.find("+") > string.find("-"):
                    oplist.append(string[index_minus : index_minus + 1])
                    next_sub_op = string.find("-", 1)

                    if next_sub_op != -1:   # Means that there is still at least one sub op remains in the polynomial
                        if string.find("+", 1) < string.find("-", 1):
                            next_op = string.find("+", 1)
                        elif string.find("+", 1) > string.find("-", 1):
                            next_op = string.find("-", 1)
                    elif next_sub_op == -1:
                        next_op = string.find("+", 1)   # So there is only add op left

                    stringlist.append(string[index_minus + 1 : next_op])
                    string = string[next_op : ]  # Remove the part that has already save in list

                    count_minus -= 1  #count_minus--

        elif count_add == 0:
            if count_minus > 0:

                oplist.append(string[index_minus : index_minus + 1])
                next_sub_op = string.find("-", 1)
                # To make sure the index of the string between the first op and second op
                if next_sub_op != -1:
                    stringlist.append(string[index_minus + 1 : next_sub_op])  
                    string = string[next_sub_op : ] # Remove the part that has already save in list
                elif next_sub_op == -1: # when this part of polynomial is the last
                    stringlist.append(string[index_minus + 1 : ]) 
                    string = ""  # Remove the part that has already save in list

                count_minus -= 1  #count_minus--
            
# Extract the coefficients of each term
def extract_coef(stringlist, coef_stringlist):
    length_of_list1 = len(stringlist)
    for i in range(length_of_list1):
        only_digits = stringlist[i].isdigit()

        if only_digits == True:     # Means that this term is a constant, dont have any variables
            coef_stringlist.append(stringlist[i])
            #print("Only digits")
            stringlist[i] = "1"  # Remove the coef from the list
        elif only_digits == False:
            string_length = len(stringlist[i])
            #print(string_length)
            for j in range(string_length):
                if j != 0 and stringlist[i][j].isalpha() == True:   # coef != 1
                    coef_stringlist.append(stringlist[i][ : j])
                    #print("not only digits")
                    stringlist[i] = stringlist[i][j : ]
                    break
                elif j == 0 and stringlist[i][j].isalpha() == True:  # When coef = 1
                    coef_stringlist.append("1")
                    #print("Coef is 1")
                    # Nothing to remove from the list
                    break
        else:
            print("Error")
            coef_stringlist[i] = ""

# Find the powers of the variables
def find_power(stringlist, i, a, same_alphabet):
    length = len(stringlist[i])
    if length == a + 1: # Means that this variable is the last character in this term and the length indicate that its power will not more than 1
        ans_power = 1
    else:
        next_alphabet = find_next_alphabet(stringlist, i, same_alphabet)
        if next_alphabet == a + 1:
            ans_power = 1
        elif next_alphabet == -1:
            string_power = stringlist[i][a + 1 : ] 
            ans_power = int(string_power)
        else:
            string_power = stringlist[i][a + 1 : next_alphabet] 
            ans_power = int(string_power)
    
    return ans_power

# Find the index of the next alphabet
def find_next_alphabet(list, count, same_alphabet):

    index = list[count].find(same_alphabet)
    length = len(list[count])

    ans = -1
    if length > index + 1:
        for i in range(index + 1, length):
            if list[count][i].isalpha() == True:
                ans = i
                break

    return ans

# Replace the final answer of the power of that term
def replace_power(list, count, answer_power, same_alphabet):
    
    index = list[count].find(same_alphabet)
    next_alphabet = find_next_alphabet(list, count, same_alphabet)
    #print(f"The index of the next alphabet is {next_alphabet}")
    if next_alphabet != -1: # Means that there still has the next alphabet(variable)
        list[count] = list[count][ : index + 1] + str(answer_power) + list[count][next_alphabet : ]
    elif next_alphabet == -1:
        list[count] = list[count][ : index + 1] + str(answer_power)

# Sorting according the alphabet(lowercase/uppercase)
def char_sort(list):
    length = len(list)
    for i in range(length):
        for j in range(0, length-i-1):
            if list[j] > list[j+1]:
                list[j], list[j+1] = list[j+1], list[j]
    return list

# Sort the alphabet in order to do addition and subtraction for the same variable term
def sorting(list, count):
    for i in range(count):
        string_length = len(list[i])
        temp_list = []
        if string_length == 1:
            temp_list.append(list[i])
        else:
            for j in range(string_length):
                if list[i][j].isalpha() == True:
                    next_alphabet_index = find_next_alphabet(list, i, list[i][j])
                    if next_alphabet_index != -1:
                        temp_list.append(list[i][j : next_alphabet_index])
                    elif next_alphabet_index == -1:
                        temp_list.append(list[i][j : ])
        
        temp_list = char_sort(temp_list)
        list_length = len(temp_list)
        list[i] = ""
        for a in range(list_length):
            list[i] = list[i] + temp_list[a]

# Addition or Subtraction of the same variable term
def add_sub_same_term(answer_op_coef, answer_list, count):
    temp_answer_list = answer_list.copy()
    #print(answer_op_coef)
    for i in range(count):
        while True:
            if temp_answer_list[i] != "" and temp_answer_list[i] in temp_answer_list[i + 1 : ]:
                    index = temp_answer_list.index(temp_answer_list[i], i + 1)

                    # Op and Coef.
                    temp = int(answer_op_coef[i]) + int(answer_op_coef[index])
                    if temp > 0:
                        answer_op_coef[i] = "+" + str(temp)
                    elif temp < 0:
                        answer_op_coef[i] = str(temp)
                    elif temp == 0:
                        answer_op_coef[i] = ""
                        temp_answer_list[i] = ""

                    answer_op_coef[index] = ""

                    #Term
                    temp_answer_list[index] = ""

            else:
                break

    #print(f"add_sub_same_term: {answer_op_coef}")
    #print(f"add_sub_same_term: {temp_answer_list}") 

    # Modify the list of Op, Coef., Variable term   
    return temp_answer_list
    # Op, Coef. no need

# Remove blank string
def remove_blank_string(list):
    count_empty = list.count("")
    #print(f"The list has {count_empty} empty string")
    while count_empty != 0:
        index = list.index("")
        list = list[ : index] + list[index + 1 : ]
        count_empty -= 1

    return list

#operate the multiplication
def multiplication_of_polynomials(string1, string2):

    #print(string1)
    #print(string2)
    
    coef_stringlist1 = []
    coef_stringlist2 = []
    string_list1 = []
    string_list2 = []
    op_list1 = []
    op_list2 = []
        
    partition_add_minus_op(string1, string_list1, op_list1)
    partition_add_minus_op(string2, string_list2, op_list2)    

    #print(string_list1)
    #print(op_list1)
    #print(string_list2)
    #print(op_list2)

    # Extract the coef. of every terms
    extract_coef(string_list1, coef_stringlist1)
    extract_coef(string_list2, coef_stringlist2)
    #print(string_list1)
    #print(coef_stringlist1)
    #print(string_list2)
    #print(coef_stringlist2)

    length_of_list1 = len(string_list1)
    #print(f"The first string list has {length_of_list1} elements now")
    length_of_list2 = len(string_list2)
    #print(f"The second string list has {length_of_list2} elements now")

    size = length_of_list1 * length_of_list2 
    answer_op = []
    answer_coef = []
    answer_list = [""] * size # Set the size first
    answer_list_count = 0

    # Multiplication of coef. & each term variables
    for i in range(length_of_list1):
        for j in range(length_of_list2):

            # Coef.
            answer_coef.append(int(coef_stringlist1[i]) * int(coef_stringlist2[j]))

            # Op.
            if op_list1[i] == op_list2[j]:  # Remain the same operator
                answer_op.append("+")
            elif op_list1[i] != op_list2[j]:    # Negative operator
                answer_op.append("-")

            # Each term variables
            len_string1 = len(string_list1[i])
            len_string2 = len(string_list2[j])
            # Save the second string at the answer list first
            if string_list2[j].isdigit() == True:
                answer_list[answer_list_count] = string_list1[i]   
                #print(f"The string that being loaded is {answer_list[answer_list_count]}")
            elif string_list2[j].isdigit() == False:
                answer_list[answer_list_count] = string_list2[j] 

                #print(f"The string that being loaded is {answer_list[answer_list_count]}")
                if string_list1[i].isdigit() != True: # Only if this term is not 1 constant(means that there is at least one variable in this term)
                    for a in range(len_string1):
                        if string_list1[i][a].isalpha() == True:
                            find_same_var = string_list2[j].find(string_list1[i][a])
                            if find_same_var != -1:  # means that there has the same variables in string list 2 
                                # Find the power after the multiplication
                                #print(f"The same variable is {string_list1[i][a]}")
                                ans_pow = find_power(string_list1, i, a, string_list1[i][a]) + find_power(string_list2, j, find_same_var, string_list1[i][a])
                                #print(f"The current string is {answer_list[answer_list_count]}")
                                replace_power(answer_list, answer_list_count, ans_pow, string_list1[i][a])
                            elif find_same_var == -1: # Add the variable to the answer list
                                next_alphabet = find_next_alphabet(string_list1, i, string_list1[i][a])
                                if next_alphabet != -1: # Means there still has at least one variable left
                                    answer_list[answer_list_count] = answer_list[answer_list_count] +  string_list1[i][a : next_alphabet]
                                elif next_alphabet == -1:
                                    answer_list[answer_list_count] = answer_list[answer_list_count] +  string_list1[i][a : ]

            answer_list_count += 1

    #print(answer_coef)
    #print(answer_op)
    #print(answer_list)
    
    # Sort the answer
    sorting(answer_list, answer_list_count)

    answer_op_coef = [answer_op[i] + str(answer_coef[i]) for i in range(answer_list_count)]
    answer_list = add_sub_same_term(answer_op_coef, answer_list, answer_list_count)
    answer_op_coef = remove_blank_string(answer_op_coef)
    answer_list = remove_blank_string(answer_list)

    #print(f"The op coef list is {answer_op_coef}")
    #print(f"The temporary variable term is {answer_list}")
    final_answer = ""
    length_of_answer_list = len(answer_list)
    for answer in range(length_of_answer_list):
        coef_eq_one = False
        # For operator and coef. final answer
        if answer == 0 and answer_op_coef[answer][0] == "-":
            final_answer = final_answer + answer_op_coef[answer][0]
        elif answer > 0:
            final_answer = final_answer + answer_op_coef[answer][0]
        # For coef. final answer
        if len(answer_op_coef[answer]) == 2:
            if answer_op_coef[answer][1] != "1":
                final_answer = final_answer + answer_op_coef[answer][1 :]
            elif answer_op_coef[answer][1] == "1":
                coef_eq_one = True
        else:
            final_answer = final_answer + answer_op_coef[answer][1 :]
        # For String final answer
        if answer_list[answer] != "1":
            final_answer = final_answer + answer_list[answer]
        elif answer_list[answer] == "1" and coef_eq_one == True:
            final_answer = final_answer + answer_list[answer]

        #print(f"The final answer is {final_answer}")    

    return final_answer

#partition the string according bracket and call multiplication function
def partition_bracket_and_calculation(string): 
    bracket_count = string.count("(")
    index_first_right_bracket = string.find(")")
    first_string = string[1 : index_first_right_bracket]
    for i in range(bracket_count - 1):
        index_second_left_bracket = index_first_right_bracket + 1
        index_second_right_bracket = string.find(")", index_second_left_bracket)
        
        #print(index_second_left_bracket)
        #print(index_second_right_bracket)

        second_string = string[index_second_left_bracket + 1 : index_second_right_bracket]

        first_string = multiplication_of_polynomials(first_string, second_string)
        index_first_right_bracket = index_second_right_bracket

    #print(f"The answer is {first_string}")
    return first_string

# Main
polynomial_input = input("Input the polynomials: ")

if polynomial_input ==  "" :   
    print("You didnt type anything!")

else:
    # Remove spaces if it exists
    polynomial_input = polynomial_input.replace(" ", "")

    # Get rid of * ^ 
    polynomial_input = polynomial_input.replace("*", "")
    polynomial_input = polynomial_input.replace("^", "")

    # Start calculating the answer
    answer = partition_bracket_and_calculation(polynomial_input)

    # Print the answer withou "*" "^" first
    print(f"The first answer is {answer}")

    # Add "*" "^" back to the answer
    answer_list = []
    answer_op_list = []
    answer_coef_list = []
    partition_add_minus_op(answer, answer_list, answer_op_list)
    extract_coef(answer_list, answer_coef_list)
    #print(answer_list)
    #print(answer_op_list)
    #print(answer_coef_list)
    answer = ""
    length = len(answer_coef_list)
    for i in range(length):
        answer_coef_list[i] = str(answer_coef_list[i])
        answer_coef_list[i] = answer_coef_list[i] + "*"

        length_term = len(answer_list[i])
        new_term = ""   # Temporary term
        for j in range(length_term):
            new_term += answer_list[i][j]  # Add the current character to temp var
            if answer_list[i][j].isalpha() == True and (j + 1) != length_term:
                if answer_list[i][j + 1].isdigit() == True:
                    new_term += "^"
        answer_list[i] = new_term

        coef_eq_one = False
        # For operator 
        if i == 0 and answer_op_list[i] == "-":
            answer = answer + answer_op_list[i]
        elif i > 0:
            answer = answer + answer_op_list[i]
        # For coef. final answer
        if len(answer_coef_list[i]) == 2:
            if answer_coef_list[i][0] != "1":
                answer = answer + answer_coef_list[i]
            elif answer_coef_list[i][0] == "1":
                coef_eq_one = True
        else:
            answer = answer + answer_coef_list[i]
        # For String final answer
        if answer_list[i] != "1":
            answer = answer + answer_list[i]
        elif answer_list[i] == "1" and coef_eq_one == True:
            answer = answer + answer_list[i]
        elif answer_list[i] == "1" and coef_eq_one == False:    # To eliminate "*"
            length_ans = len(answer)
            answer = answer[ : length_ans - 1]
    
    print(f"The \"Bonus\" answer is {answer}")