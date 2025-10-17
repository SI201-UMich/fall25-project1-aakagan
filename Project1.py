# Names: Isaac Abrams, Zeke Butler, Andrew Kagan 
# Student ID: {Zeke: 93856849, Isaac: 96832526, Andrew: 61021214} 
# Email:zfbutler@umich.edu, isaacab@umich.edu, aakagan@umich.edu

# Zeke summary: 
# Wrote csv open, main, get value, island percentage, bill size, and tests for the variables I wrote. 
# Asked ChatGPT hints for debugging and suggesting the general sturcture of the code, this came in the form of getting help with writing to a new file as well as structuring my test cases
# I also used it to help me with some of the exceptions in handling unique data or missing data from the original csv. 

# Isaac summary:
# Wrote bill_corr_strength, species_flipper_length_range, helped with fwrite, and unit tests for variables I wrote.
# Asked ChatGPT hints for debugging and suggesting the general sturcture of the code, also used ChatGPT to help me with numpy library concepts I learned from SI325. LLM's also were used with helping write my test cases

#Andrew summary: 
# Worked specifically on the avg_weigth() and percent_over_weight() functions implementing those calculations and test cases. 
# Also contributed to the rest of the program (csv open, get value, main, some of the other test cases as well)
# I used chatgpt to help me debug a lot of the code and help me write some of the aspects of the functions when I got stuck
# I wasn't sure how to deal with the "NA" problem for some of the data in the avg_weight() function so I asked chatgpt to help me 
# and it suggested using the import math library and isnan() function to solve the problem so that the function continues 
# if not a number is listed in the data and not include it in the results



import csv
import numpy as np 
import math


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

def avg_weight(data):
    import math
    weight = get_value('body_mass_g', data)
    species = get_value('species', data)
    sex = get_value('sex', data)

    individual_list = list(zip(species, sex, weight))
    cleaned_list = []

    valid_sexes = ("male", "female")

    for s, sex, w in individual_list:
        if not sex:
            continue
        sex_clean = sex.strip().lower()
        if sex_clean not in valid_sexes:
            continue
        try:
            w_float = float(w)
            if math.isnan(w_float):
                continue
        except (ValueError, TypeError):
            continue
        cleaned_list.append((s, sex_clean.capitalize(), w_float))

    if not cleaned_list:
        return {}

    grouped_weights = {}
    for s, sex, w in cleaned_list:
        grouped_weights.setdefault((s, sex), []).append(w)

    result = {}
    for (s, sex), weights in grouped_weights.items():
        avg_w = sum(weights) / len(weights)
        result[(s, sex)] = round(avg_w, 2)

    return result

# Calculation #4 - Find the percentage of penguins in a given species that are heavier than the average penguin
def percent_over_weight(data):
    weight_list = get_value('body_mass_g', data)
    species_list = get_value('species', data)
    has_sex = 'sex' in next(iter(data.values()), {})
    if has_sex:
        sex_list = get_value('sex', data)
    else:
        sex_list = [''] * len(species_list)

    cleaned_data = []

    for s, sex, w in zip(species_list, sex_list, weight_list):
        try:
            w_float = float(w)
            if math.isnan(w_float):
                continue
        except (ValueError, TypeError):
            continue
        cleaned_data.append((s, sex, w_float))
    if not cleaned_data:
        return {}
    all_weights = [w for _, _, w in cleaned_data]
    global_avg = sum(all_weights) / len(all_weights)
    species_total = {}
    species_above = {}

    for s, sex, w in cleaned_data:
        species_total[s] = species_total.get(s, 0) + 1
        if w > global_avg:
            species_above[s] = species_above.get(s, 0) + 1
    
    percentage_dict = {}
    for s in species_total:
        total = species_total[s]
        above = species_above.get(s, 0)
        percent = (above / total) * 100
        percentage_dict[s] = f"{round(percent, 1)}%"

    return percentage_dict

# Calculation #5 - Calculates correlation strength between flipper length and penguin weight
def flipper_corr_strength(data):
    f_length_list = get_value("flipper_length_mm", data)
    weight_list = get_value("body_mass_g", data)

    clean_f_length = []
    clean_weight = []

    for flipper, weight in zip(f_length_list, weight_list):
        try:
            updated_flipper = float(flipper)
            updated_weight = float(weight)
        except (ValueError, TypeError):
            continue
        clean_f_length.append(updated_flipper)
        clean_weight.append(updated_weight)

    if len(clean_f_length) < 2 or len(clean_weight) < 2:
        return {
            "correlation": None,
            "interpretation": "Not enough data to find correlation."
        }

    #get correlation between flipper length and weight using numpy library to create corr matrix
    corr_matrix = np.corrcoef(clean_f_length, clean_weight)
    r = float(corr_matrix[0,1])
    r = round(r, 2)
    
    direction = ""
    if r > 0:
        direction = "positive"
    elif r < 0:
        direction = "negative"
    else:
        direction = "neutral"

    if abs(r) >= 0.7:
        strength = "strong"
    elif abs(r) >= 0.4:
        strength = "moderate"
    elif abs(r) >= 0.2:
        strength = "weak"
    else:
        strength = "very weak or none"
    
    return {
        "correlation": r,
        "interpretation": f"{strength} {direction} correlation between flipper length and penguin weight"
    }



# Calculation #6: Find the minimum, maximum, and range of body mass for each species
def species_flipper_length_range(data):
    f_length_list = get_value("flipper_length_mm", data)
    species_list = get_value("species", data)

    species_flipper_len = {}

    #get weight for each species
    for species, flipper in zip(species_list, f_length_list):
        try:
            updated_flipper = float(flipper)
        except (ValueError, TypeError):
            continue
        species_flipper_len.setdefault(species, []).append(updated_flipper)

    result = {}
    for species, flipper_len_list in species_flipper_len.items():
        min_flipper_len = float(min(flipper_len_list))
        max_flipper_len = float(max(flipper_len_list))
        range = max_flipper_len - min_flipper_len

        #put stats into final dictionary with outer keys species and inner keys the stats "min", "max", and "range"
        result[species] = {"min": round(min_flipper_len, 2),
                           "max": round(max_flipper_len),
                           "range": round(range, 2)}
    
    return result




        
def fwrite(file, average_weight, b_size, counting_dict, bill_corr, flipper , over_weight):        
        file.write(f"Final Analysis for Calculations\nQuestion: How do penguin species differ across physical and geographical traits \n\n\n")
        file.write(f"Island Proportions of Total Penguin Population: {str(counting_dict)}\n\n")
        file.write(f"Average Bill Size for Penguins Sorted by Species: {str(b_size)}\n\n")
        file.write(f"Average Weight for Penguins, Sorted by Sex and Species: {str(average_weight)}\n\n")
        file.write(f"Proportion of Penguin Species by Body Mass over the Global Mean Mass: {str(over_weight)}\n\n\n")
        file.write(f"Correlation Between Flipper Length and Penguin Mass: {str(bill_corr)}\n\n")
        file.write(f"Spread Metrics for Flipper Lengths of Penguins Sorterd by Species: {str(flipper)}\n\n")
        file.write("Conclusion: Based on these results, Gentoo penguins tend to be the largest and heaviest species overall, Adelie penguins show more\nmoderate physical traits, and Chinstrap penguins have the smallest body mass, with clear positive correlations between flipper length and overall weight across all species.")
def main():
        data = csv_open('penguins.csv')
        counting_dict = island_percentage(data)
        b_size = bill_size(data)
        average_weight = avg_weight(data)
        over_weight = percent_over_weight(data)
        flip_corr = flipper_corr_strength(data)
        flipper = species_flipper_length_range(data)

        with open("output.txt", "w") as file:
            fwrite(file, average_weight, b_size, counting_dict, flip_corr, flipper , over_weight)

if __name__ == '__main__':
    main()








