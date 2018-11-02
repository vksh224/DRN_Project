import random
import math
import turtle
from constants import *

def euclideanDistance(coor1X, coor1Y, coor2X, coor2Y):
    return (math.sqrt((float(coor1X) - float(coor2X))**2 + (float(coor1Y) - float(coor2Y))**2))

def write_paths_to_a_file(Res_path_list, type):
    f = open('Bhaktapur/responder_paths.txt', type)
    path_count = 1
    for res_path in Res_path_list:
        line_str = "Group.waypoints" + str(path_count) +" = "
        for coor in res_path:
            line_str += str(coor[0]) + ", " + str(coor[1]) + ", "
        f.write(line_str + "\n")
        path_count += 1
    f.close()

def get_responder_paths(CC_locs, PoI_locs):
    Res_path_list = []
    for r in range(no_of_R):
        curr_res_path = []
        no_of_assigned_PoIs = random.randint(min_no_PoIs_for_R, max_no_PoI_for_R)
        curr_res_path.append(random.choice(CC_locs))
        for poi in range(no_of_assigned_PoIs):
            curr_res_path.append(random.choice(PoI_locs))
        Res_path_list.append(curr_res_path)
    return Res_path_list

#---------------------------------- Survivor location --------------------------
def initial_survivor_loc(PoI_locs, PoI_radii, S_count_in_PoI):
    S_locs = []
    for i in range(len(PoI_locs)):
        for j in range(S_count_in_PoI[i]):
            # random angle
            alpha = 2 * math.pi * random.random()
            r = PoI_radii[i] * math.sqrt(random.random())
            # calculating coordinates
            x = r * math.cos(alpha) + PoI_locs[i][0]
            y = r * math.sin(alpha) + PoI_locs[i][1]
            S_locs.append((int(x), int(y)))
    return S_locs

def update_survivor_loc (S_locs, prev_time, curr_time):
    for i in range(len(S_locs)):
        moving_prob = random.uniform(0, 1)
        if moving_prob > moving_S_prob:
            # random angle
            alpha = 2 * math.pi * random.random()
            curr_speed = random.uniform (min_S_speed, max_S_speed)
            r = curr_speed * (curr_time - prev_time) * math.sqrt(random.random())
            x = r * math.cos(alpha) + S_locs[i][0]
            y = r * math.sin(alpha) + S_locs[i][1]
            S_locs[i] = (int(x), int(y))
    return S_locs
#-------------------End: Survivor related -------------------------------------


#------------ Volunteer path, initial location, and updated location -----------------------
def get_volunteer_paths(PoI_locs, PoI_radii, Vol_count_In_PoI):
    Vol_path_list = []
    for poi_id in range(len(PoI_locs)):
        for vol_id in range(Vol_count_In_PoI[poi_id]):
            polygon = turtle.Turtle()

            num_sides = random.randint(min_num_sides, max_num_sides)
            side_length = random.randint(min_side_length, PoI_radii[poi_id])
            angle = random.randint(min_side_angle, max_side_angle) / num_sides

            polygon.setposition(PoI_locs[poi_id])

            curr_vol_path = []
            #print("Number of sides: ", num_sides)
            for i in range(num_sides):
                # print(i, polygon.position())
                curr_vol_path.append((int(polygon.position()[0]), int(polygon.position()[1])))
                polygon.forward(side_length)
                polygon.right(angle)

        Vol_path_list.append(curr_vol_path)
    return Vol_path_list

def initial_volunteer_loc(Vol_path_list):
    Vol_locs = []
    for path in Vol_path_list:
        Vol_locs.append(path[0])
    return Vol_locs

def update_volunteer_loc(Vol_locs, Vol_path_list, prev_time, curr_time):
    for i in range(len(Vol_locs)):
        curr_loc = Vol_locs[i]
        curr_speed = random.uniform(min_V_speed, max_V_speed)
        dist_trav = curr_speed * (curr_time - prev_time)
        pos = Vol_path_list[i].index(curr_loc)

        while True:
            next_loc = Vol_path_list[pos]
            if (euclideanDistance(next_loc[0], next_loc[1], curr_loc[0], curr_loc[1]) < dist_trav):
                Vol_locs[i] = curr_loc
                break
            else:
                pos = (pos + 1)%len(Vol_path_list[i])

#--------------------------------------------------------------------------------


def initial_setup():
    CC_locs = []
    PoI_locs = []
    PoI_radii = []
    Vol_count_In_PoI = []
    S_count_in_PoI = []

    #Get CC location
    for i in range(no_of_CC):
        CC_locs.append((random.randint(lX, hX), random.randint(lY, hY)))

    #Get PoI locations
    for i in range(no_of_PoI):
        PoI_locs.append((random.randint(lX, hX), random.randint(lY, hY)))
        PoI_radii.append(random.randint(min_PoI_radius, max_PoI_radius))
        Vol_count_In_PoI.append(random.randint(min_V_in_PoI, max_V_in_PoI))
        S_count_in_PoI.append(random.randint(min_S_in_PoI, max_S_in_PoI))

    #Get Responder paths
    Res_path_list = get_responder_paths(CC_locs, PoI_locs)

    #Get Volunteer paths
    Vol_path_list = get_volunteer_paths(PoI_locs, PoI_radii, Vol_count_In_PoI)

    #Get survivors locations
    S_locs = initial_survivor_loc(PoI_locs, PoI_radii, S_count_in_PoI)

    #Get volunteer locations
    Vol_locs = initial_volunteer_loc(Vol_path_list)

    return CC_locs, PoI_locs, PoI_radii, Vol_count_In_PoI, Res_path_list, Vol_path_list, S_locs, Vol_locs
