import csv

def csv_open(fname):
    with open(fname, 'r') as file:
        reader = csv.DictReader(file)
        outer_d = {}
        for row in reader:
            key = row[reader.fieldnames[0]]
            inside_d = {field: row[field] for field in reader.fieldnames[1:]}
            outer_d[key] = inside_d
        for i, row in enumerate(reader, start = 1):
            outer_d[i] = row
    return outer_d


def get_value(variable, outer_d):
    values_list = []
    for ids in outer_d.values():
        for key, value in ids.items():
            if variable == key:
                values_list.append(value.strip())
    return values_list

# Calculation #1 - How many penguins come from each island as a percentage
def island_percentage(data):
    isle_list = get_value('island', data)
    counter = {}

    for island in isle_list:
        counter[island] = counter.get(island, 0) + 1

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
import math
def avg_weight(data):
    weight = get_value('body_mass_g', data)
    species = get_value('species', data)
    sex = get_value('sex', data)
    individual_list = list(zip(species, sex, weight))
    cleaned_list = []

    for species, sex, weight in individual_list:
        try:
          w = float(weight)
          if math.isnan(w):
              continue
        except(ValueError, TypeError):
             continue   
        cleaned_list.append((species, sex, w))

    if not cleaned_list:
        return {}

    d1 = {}

    for species, sex, w in cleaned_list:
        d1.setdefault((species, sex), []).append(w)

    d2 = {}

    for (species, sex), weights in d1.items():
        if not weights:
            continue
        avg_weight = sum(weights) / len(weights)
        d2[(species, sex)] = round(avg_weight, 2)

    return d2

# Calculation #4 - Find the percentage of penguins in a given species that are heavier than the average penguin
def percent_over_weight(data):
    weight_list = get_value('body_mass_g', data)
    species_list = get_value('species', data)
    cleaned_data = []

    for s, w in zip(species_list, weight_list):
        try:
            w_float = float(w)
        except (ValueError, TypeError):
            continue
        cleaned_data.append((s, w_float))

    all_weights = [w for _, w in cleaned_data]
    if not all_weights:
        return {}
    global_avg = sum(all_weights) / len(all_weights)
    species_total = {}
    species_above = {}

    for s, w in cleaned_data:
        species_total[s] = species_total.get(s, 0) + 1
        if w > global_avg:
            species_above[s] = species_above.get(s, 0) + 1
    percentage_dict = {}

    for s in species_total:
        above = species_above.get(s, 0)
        total = species_total[s]
        percentage = (above / total) * 100
        percentage_dict[s] = str(round(percentage, 2)) + "%"

    return percentage_dict

# Calculation #5 - Calculates correlations between body mass and each of bill_length, bill_depth, and flipper_length. 
# Returns tuples with feature most associated and the correlation to be used for final output.
#def weight_predictors_ranking(data):



# Calculation #6 - Computes bill_length_mm / bill_depth_mm per penguin then it summarizes by species and finds global extremes.
#def bill_shape_ratio_summary(data):



def main():
    data = csv_open('penguins.csv')
    species_list = get_value('species', data)
    counting_dict = island_percentage(data)
    counting_dict = island_percentage(data)
    b_size = bill_size(data)
    average_weight = avg_weight(data)
    print("average Weight", average_weight)
    print("average Bill size", b_size)
    print("island counter", counting_dict)
    over_weight = percent_over_weight(data)
    print("percent of penguins over the average weight by species:", over_weight)

if __name__ == '__main__':
    main()








