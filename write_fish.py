import fish_map
import csv
import itertools
import params

def write_fish(fish_map_input, generation):
    with open('data/fish_map_{}.csv'.format(generation), 'w') as f:
        fish_writer = csv.writer(f)
        columns = {
            'normal': [
                'state',
                'fitness',
                'energy'
            ],
            'traits': params.TRAIT_LIST
        }
        fish_writer.writerow(columns['normal'] + columns['traits'])
        for fish in fish_map_input.fish_list + fish_map_input.dead_list:
            row = [getattr(fish, attr) for attr in columns['normal']]
            row = row + [fish.traits[key] for key in columns['traits']]
            fish_writer.writerow(row)