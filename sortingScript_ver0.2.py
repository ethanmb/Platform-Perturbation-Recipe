import random
import csv


#randomizes list, parameter is array list, returns list
def randomize_list(input_list):
    randomized_list = input_list.copy()
    random.shuffle(randomized_list)
    return randomized_list

#checks for 2 repeated items in a row and returns repeated items and list inputted
def get_repeated_items(input_list):
    repeated_items = []
    pre_sorted_list = []
    last_item = ""
    lastest_item = ""
    for item in input_list:
        if last_item and lastest_item and item == last_item and item== lastest_item:
            repeated_items.append(item)
            continue
        pre_sorted_list.append(item)
        lastest_item = last_item
        last_item = item
    return repeated_items, pre_sorted_list

def recycle_repeated_items(repeated_items, pre_sorted_list):
    sorted_list = []
    last_item = ""
    changed = False
    for item in pre_sorted_list:
        filtered_types = [item] + ([last_item] if last_item else [])
        eligible_repeated_item = next(filter(lambda t: t not in filtered_types, repeated_items), None)
        if eligible_repeated_item:
            changed = True
            repeated_items.remove(eligible_repeated_item)
            sorted_list.append(eligible_repeated_item)
        sorted_list.append(item)
        last_item = item
    return repeated_items, sorted_list, changed

def randomized_non_repeating_sort(input_list):
    randomized_list = randomize_list(input_list)
    repeated_items, sorted_list = get_repeated_items(randomized_list)
    repeated_items, sorted_list, changed = recycle_repeated_items(repeated_items, sorted_list)
    while repeated_items and changed:
        repeated_items, sorted_list, changed = recycle_repeated_items(repeated_items, sorted_list)
    return sorted_list + repeated_items


cardinalDirections = [
"L",
"R",
"F",
"B",
]

sagittalDirections = [
"F",
"B",
]

frontalDirections = [
"L",
"R",
]

diagonalDirections = [
"FL",
"FR",
"BL",
"BR",
]

sagittalGVS = [
"F,Anode", "F,Cathode", "F,OFF",
"B,Anode", "B,Cathode", "B,OFF",
]

frontalGVS = [
"R,Anode", "R,Cathode", "R,OFF",
"L,Anode", "L,Cathode", "L,OFF",
]

recipe_random = []
recipe_pseudoRandom = []
original_list = []

print("GVS? 0 = No, 1 = Yes *NOTE* only supports AP or ML")
gvs_bool = int(input())

print("Which directions? 0 = AP, 1 = ML, 2 = Cardinal, 3 = Cardinal + Diagonal")
dir_bool = int(input())


print("How many trials of each direction?")
trials_direction = int(input())

####################################
#to do
#add magnitude support
####################################

if gvs_bool == 0:
    if dir_bool == 3:
        for x in range(trials_direction):
            for y in range(len(cardinalDirections)):
                recipe_random.append(cardinalDirections[y])
            for y in range(len(diagonalDirections)):
                recipe_random.append(diagonalDirections[y])
        original_list = recipe_random

    elif dir_bool == 0:
        for x in range(trials_direction):
            for y in range(len(sagittalDirections)):
                recipe_random.append(sagittalDirections[y])
        original_list = recipe_random
        for x in range(trials_direction):
            for y in range(len(sagittalGVS)):
                recipe_random.append(sagittalGVS[y])
        original_list = recipe_random


    elif dir_bool == 1:
        for x in range(trials_direction):
            for y in range(len(frontalDirections)):
                recipe_random.append(frontalDirections[y])
        original_list = recipe_random

    elif dir_bool == 2:
        for x in range(trials_direction):
            for y in range(len(cardinalDirections)):
                recipe_random.append(cardinalDirections[y])
        original_list = recipe_random
else:
    if dir_bool == 0:
        for x in range(trials_direction):
            for y in range(len(sagittalGVS)):
                recipe_random.append(sagittalGVS[y])
        original_list = recipe_random
    elif dir_bool == 1:
        for x in range(trials_direction):
            for y in range(len(frontalGVS)):
                recipe_random.append(frontalGVS[y])
        original_list = recipe_random

for x in range(len(original_list)):
    output_list = randomized_non_repeating_sort(original_list)
    repeated_items = get_repeated_items(output_list)[0]
    if repeated_items:
        raise Exception('CONSECUTIVE REPEATED ITEM FOUND!')
    if len(output_list) != len(original_list):
        raise Exception('LIST LENGTH MISMATCH!')


recipe_pseudoRandom = original_list
#check out pandas library to write to excel
with open('directions.csv', 'w') as f:
    thewriter = csv.writer(f)
    y = 1
    for x in recipe_pseudoRandom:
        if y < 10:
            z = "Trial_00" + str(y)
        else:
            z = "Trial_0" + str(y)
        if gvs_bool == 0:
            thewriter.writerow([z]+[x])
        else:
            r = x.split(",")
            thewriter.writerow([z]+[r[0]] + [r[1]])
        y = y + 1

print("Done")