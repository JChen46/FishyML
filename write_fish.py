import fish_map
import csv
import itertools
import params

file_num = 1
def write_fish(fish_map_input):
    with open('data/fish_map_{}.csv'.format(file_num), 'w') as f:
        fish_writer = csv.writer(f)
        columns = {
            'normal': [
                'state'
            ],
            'traits': params.TRAIT_LIST
        }
        fish_writer.writerow(columns['normal'] + columns['traits'])
        for fish in fish_map_input.fish_list + fish_map_input.dead_list:
            row = [getattr(fish, attr) for attr in columns['normal']]
            row += [fish.traits[key] for key in columns['traits']]
            fish_writer.writerows(row)