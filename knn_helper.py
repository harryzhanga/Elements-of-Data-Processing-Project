#pick your weights if you want to make your own distance metric for k-nn
TYPE_WEIGHT = 600000
ROOMS_WEIGHT = 25000
INVERSE_DIST_POWER = 2.5
MEDIAN_WEIGHT = 0.00001
CAR_WEIGHT = 15000
LAND_WEIGHT = 0.05
CBD_WEIGHT = 791.7735725641251
BATH_WEIGHT = 15000
UNIT_WEIGHT = 0.5
PROPERTY_OWNED_WEIGHT = 0
INCOME_WEIGHT = 200
SCHOOL_WEIGHT = 10000
SUBURB_WEIGHT = 1000


def calc_distance(row1, row2):
    median_dist = MEDIAN_WEIGHT*(row1["HouseMedian($)"]-row2["HouseMedian($)"])**2
    rooms_dist = ROOMS_WEIGHT*(row1["Rooms"]-row2["Rooms"])**2
    land_dist = LAND_WEIGHT*(row1["Landsize"]-row2["Landsize"])**2
    car_dist = CAR_WEIGHT*(row1["Car"]-row2["Car"])**2
    bath_dist = BATH_WEIGHT*(row1["Bathroom"]-row2["Bathroom"])**2
    type_dist = 0
    suburb_weight = 0
    if row1["Suburb"] != row2["Suburb"]:
        suburb_weight = SUBURB_WEIGHT
    if row1["Type"] != row2["Type"]:
        type_dist = TYPE_WEIGHT
    return 1000+suburb_weight+median_dist + rooms_dist + bath_dist + car_dist + land_dist+type_dist
     
def sort_by_distance(neighbours):
    return sorted(neighbours, key = lambda neighbour:(-neighbour[0]))
 
 
def neighbour_finder(k, Train_DF, myrow):
    neighbours = []
    for index, row in Train_DF.iterrows():
        distance = calc_distance(myrow, row)
        if len(neighbours) < k:
            neighbours.append([distance]+[list(row)])
        elif neighbours[0][0] > distance:
            neighbours[0] = ([distance]+[list(row)])
        neighbours = sort_by_distance(neighbours)
    return neighbours
 
def dictify(row):
    dict = {}
    cols = ["Bathroom", "Car", "Landsize", "Price", "Rooms", "Suburb", "Type", "HouseMedian($)", "40+ Percentage"]
    for i in range(len(cols)):
        dict[cols[i]] = row[i]
    return dict
         
 
def nicify(house, df):
    cols = list(df.columns)
    string = ""
    for col, val in zip(cols, house):
        string += str(col)+":"+str(val)+"  "
    return string
 
def print_neighbours(neighbours):
    for row in neighbours:
        print(nicify(row[1])+"Distance:"+str(row[0]))
 
def get_price(neighbours):
    sum = 0
    inverse_dis_sum = 0
    for row in neighbours:
        print(row)
        price = row[1][5]
        distance = row[0]
        if distance == 0:
            return price
        sum += price/(distance**INVERSE_DIST_POWER)
        inverse_dis_sum += 1/(distance**INVERSE_DIST_POWER)
    tentative_price = sum/inverse_dis_sum
    return tentative_price
 
 

def same(row1, row2):
    for col in ["Suburb", "Rooms", "Type", "Price", "Bathroom", "Car", "Landsize", "HouseMedian($)", "40+ Percentage"]:
            if row2[col] != row1[col]:
                return False
    return True