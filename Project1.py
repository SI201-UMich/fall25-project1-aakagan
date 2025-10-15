import csv

def csv_open(fname):
    with open(fname, 'r') as file:
        reader = csv.DictReader(file)
        outer_d = {}
        for row in reader:
            key = row[reader.fieldnames[0]]
            inside_d = {field: row[field] for field in reader.fieldnames[1:]}
            outer_d[key] = inside_d
    return outer_d


def get_value(variable, outer_d):
    values_list = []
    for ids in outer_d.values():
        for key, value in ids.items():
            if variable == key:
                # normalize strings (strip) and keep non-numeric as-is
                values_list.append(value.strip())
            else:
                values_list.append(value)
    return values_list

# Calculation #1 - How many penguins come from each island as a percentage
def island_percentage(data):
    isle_list = get_value('island', data)
    counter = {}
    
    for i in isle_list:
        counter[i] = counter.get(i, 0) + 1

    total = len(isle_list)
    for key, value in counter.items():
        counter[key] = str(round(((value / total) * 100), 2))+ "%"
    return counter 

# Calculation #2 - What species has on average the biggest bills 
# (calculated by multiplying the penguins bill length by depth)
def bill_size(data):
    b_length = get_value('bill_length_mm', data)
    b_depth = get_value('bill_depth_mm', data)
    species = get_value('species', data)
    
    per_individual = []  
    
    for s, l, d in zip(species, b_length, b_depth):
        try:
            lnum = float(l)
            dnum = float(d)
        except (ValueError, TypeError):
            continue
        
        area = lnum * dnum
        per_individual.append((s, area))
    
    species_areas = {}
    
    for s, area in per_individual:
        species_areas.setdefault(s, []).append(area)

    result = {}
    
    for s, areas in species_areas.items():
        avg = sum(areas) / len(areas)
        result[s] = round(avg, 2)    
    
    return result

#Calculation #3 - Find the average weight in grams based on the penguins sex and species
def avg_weight(data):
    weight = get_value('body_mass_g', data)
    species = get_value('species', data)
    sex = get_value('sex', data)
    individual_list = list(zip(species, sex, weight))
    cleaned_list = []
    
    for species, sex, weight in individual_list:
        try:
          w = float(weight)
        except(ValueError, TypeError):
             continue   
        cleaned_list.append((species, sex, w))
    
    d1 = {}
    
    for species, sex, w in cleaned_list:
        d1.setdefault((species, sex), []).append(w)
    
    d2 = {}
    
    for (species, sex), weights in d1.items():
        avg_weight = sum(weights) / len(weights)
        d2[(species, sex)] = round(avg_weight, 2)
    
    return d2

# Calculation #4 - Find the percentage of penguins in a given species that are heavier than the average penguin
def percent_over_weight(data):


# Calculation #5 - Calculates correlations between body mass and each of bill_length, bill_depth, and flipper_length. 
# Returns tuples with feature most associated and the correlation to be used for final output.
def weight_predictors_ranking(data):


# Calculation #6 - Computes bill_length_mm / bill_depth_mm per penguin then it summarizes by species and finds global extremes.
def bill_shape_ratio_summary(data):

                               

    

    


def main():
    data = csv_open('penguins.csv')
    species_list = get_value('species', data)
    counting_dict = island_per(data)
    b_size = bill_size(data)
    average_weight = avg_weight(data)
    print("average Weight", average_weight)
    print("average Bill size", b_size)
    print("island counter", counting_dict)
    

if __name__ == '__main__':
    main()






