"""Calculates pokemon teams based on maximizing advantageous type matchup possibilities"""
import os
import copy
from itertools import combinations
from math import comb
import argparse
import timeit
import tomllib
from dataclasses import dataclass
from pokedex import Pokemon, full_dex, region_nums, types, alltypes, score_dex


start = timeit.default_timer()

region_choices = []
for region in region_nums:
    region_choices.append(region)
region_choices.append("national")
region_choices.append("hypothetical")

default_settings_path = os.path.join(os.path.dirname(__file__), "default_settings.toml")
with open(default_settings_path, "rb") as f:
    config_data = tomllib.load(f)
settings_path = os.path.join(os.path.dirname(__file__), "settings.toml")
if os.path.isfile(settings_path):
    with open(settings_path, "rb") as f:
        custom_config_data = tomllib.load(f)
    config_data.update(custom_config_data)

parser = argparse.ArgumentParser()
parser.add_argument("input_dex", default=["national"], nargs='*',
                    help="the pokedex(es) to create teams from")
parser.add_argument("--stat_exclude", default=config_data["stat_exclude"],
                    const=0, nargs='?', type=int,
                    help="exclude pokemon with total base stat value below this number")
parser.add_argument("--rank_types_exclude", default=config_data["rank_types_exclude"],
                    const=0, nargs='?', type=int,
                    help="only evaluate the best this many types")
parser.add_argument("--rank_types", action='store_true', help="just rank types/pokemon")

selected_regions = []
args = parser.parse_args()
if not isinstance(args.input_dex, list):
    args.input_dex = [args.input_dex]
for region_input in args.input_dex:
    while region_input not in region_choices:
        region_input = input(f"{region_input} is invalid, input region from {region_choices}: ")
        if region_input not in region_choices:
            print("incorrect input")
    selected_regions.append(region_input)

dex = set()  # shortlist of pokemon to put in teams and analyze

exclude_regional_names = ['Alola', 'Galar', 'Husui', 'Paldea', 'Blaze Breed',
                          'Combat Breed', 'Aqua Breed']
include_regional_names = []

if args.input_dex == ['national']:
    print('Calculating best teams for full national dex')
    if config_data["exclude_mega_evolutions"]:
        exclude_name_parts = ["Mega ", "Ultra "]
        print("excluding mega evolutions from analysis")
    else:
        exclude_name_parts = []
    for poke in full_dex:
        dex.add(poke)
        for exclude_name_part in exclude_name_parts:
            if exclude_name_part.lower() in poke.name.lower():
                dex.remove(poke)
elif args.input_dex == ['hypothetical']:
    print('Calculating best teams assuming all types are possible, ' +
          'and existing type and ability combinations are possible')
    temp_types = alltypes.copy()
    DUMMY_NUM = 1
    while len(temp_types) > 0:
        atype = temp_types.pop()
        for btype in temp_types:
            dex.add(Pokemon(name=atype+" "+btype, number=DUMMY_NUM, type1=atype, type2=btype,
                            tbstat=args.stat_exclude, ability1="", ability2="", abilityh=""))
            DUMMY_NUM += 1
    ability_poke_typekeys = set()
    for poke in full_dex:
        if len(poke.typekey) > 2 and poke.typekey not in ability_poke_typekeys:
            ability_poke = copy.deepcopy(poke)
            ability_poke.name = f'{poke.type1} {poke.type2} ability:'
            for atype in poke.typekey:
                if len(atype.split("_")) > 1:
                    ability_poke.name = ability_poke.name + " " + atype
            ability_poke.tbstat = args.stat_exclude
            ability_poke_typekeys.add(poke.typekey)
            dex.add(ability_poke)
else:
    print(f'Calculating best teams for {args.input_dex}')
    if config_data["exclude_mega_evolutions"]:
        exclude_name_parts = ["Mega ", "Ultra "]
        print("excluding mega evolutions from analysis")
    else:
        exclude_name_parts = []
    for selected_region in selected_regions:
        if 'alola' in selected_region:
            if 'alola' in exclude_regional_names:
                exclude_regional_names.remove('Alola')
            if 'alola' not in include_regional_names:
                include_regional_names.append('Alola')
        if 'galar' in selected_region:
            if 'Galar' in exclude_regional_names:
                exclude_regional_names.remove('Galar')
            if 'Galar' not in include_regional_names:
                include_regional_names.append('Galar')
        if 'husui' in selected_region:
            if 'Husui' in exclude_regional_names:
                exclude_regional_names.remove('Husui')
            if 'Husui' not in include_regional_names:
                include_regional_names.append('Husui')
        if 'paldea' in selected_region:
            if 'Paldea' in exclude_regional_names:
                exclude_regional_names.remove('Paldea')
            if 'Blaze Breed' in exclude_regional_names:
                exclude_regional_names.remove('Blaze Breed')
            if 'Combat Breed' in exclude_regional_names:
                exclude_regional_names.remove('Combat Breed')
            if 'Aqua Breed' in exclude_regional_names:
                exclude_regional_names.remove('Aqua Breed')
            if 'Paldea' not in include_regional_names:
                include_regional_names.append('Paldea')
            if 'Blaze Breed' not in include_regional_names:
                include_regional_names.append('Blaze Breed')
            if 'Combat Breed' not in include_regional_names:
                include_regional_names.append('Combat Breed')
            if 'Aqua Breed' not in include_regional_names:
                include_regional_names.append('Aqua Breed')
    exclude_name_parts = exclude_name_parts + exclude_regional_names
    regional_nums = set()
    for poke in full_dex:
        for selected_region in selected_regions:
            if poke.number in region_nums[selected_region]:
                dex.add(poke)
                for exclude_name_part in exclude_name_parts:
                    if exclude_name_part.lower() in poke.name.lower():
                        dex.remove(poke)
                for include_name_part in include_regional_names:
                    if include_name_part.lower() in poke.name.lower():
                        regional_nums.add(poke.number)
    for poke in dex.copy():
        if poke.number in regional_nums:
            dex.remove(poke)
        for include_name_part in include_regional_names:
            if include_name_part.lower() in poke.name.lower():
                dex.add(poke)
    print("excluding regional forms not in region from analysis")

# dictionary of type combinations to their Type class variable,
# key is frozen set of types as strings (ex. "FIRE")
# and ability effects as strings (ex. "FIRE_Resist")
dual_types = {}

dex, dual_types = score_dex(dex, dual_types)

# print the best types
if args.rank_types:
    typescore_by_typekey = {}
    for poke in dex:
        typescore_by_typekey[poke.typekey] = dual_types[poke.typekey].score
    sorted_typescore_by_typekey = sorted(typescore_by_typekey.items(), key=lambda x: x[1])
    for entry in sorted_typescore_by_typekey:
        for atype in entry[0]:
            print(atype, end=" ")
        print(f"- Average matchup: {entry[1]/len(dual_types)}")
    print("matchup values:")
    print("\tsuper effective stab move on opponent, resist all opponent stab moves: 4")
    print("\tsuper effective stab move on opponent, opponent has regularly effective stab move: 3")
    print("\tregularly effective stab move on opponent, resist all opponent stab moves: 1")
    print("\topponent resists all stab moves, opponent has regularly effective stab move: -1")
    print("\tregularly effective stab move on opponent, opponent has super effective stab move: -3")
    print("\topponent resists all stab moves, opponent has super effective stab move: -4")
    print("\tneutral matchup: 0")
    exit()

print(f"there are {len(dex)} pokemon initially being evaluated for inclusion in team")

COUNT_ABILTIES = 0
for dtype in dual_types:
    if len(dtype) > 2:
        COUNT_ABILTIES += 1
print(f"\t{str(COUNT_ABILTIES)} of those have abilities that affect type matchups, "
      + "\n\t\tpokemon with multiple possible abilities are duplicated"
      + "\n\t\tone copy with the ability and one without")

NUM_REMOVED = 0
exclude_nums = set()
for num in config_data["exclude_from_team_nums"]:
    exclude_nums.add(int(num))
exclude_names = set()
for name in config_data["exclude_from_team_names"]:
    exclude_names.add(name)
for poke in dex.copy():
    if poke.number in exclude_nums:
        dex.remove(poke.name)
        NUM_REMOVED += 1
    else:
        for exlude_name in exclude_names:
            if exlude_name.lower() in poke.name.lower():
                dex.remove(poke.name)
                NUM_REMOVED += 1
print(f"\t{NUM_REMOVED} type combinations/pokemon removed for being in " +
      "exclude_from_team_names or exclude_from_team_nums")

NUM_REMOVED = 0
if args.stat_exclude != 0:
    weak_poke = set()
    for poke in dex:
        if poke.tbstat < args.stat_exclude:
            weak_poke.add(poke)
    for poke in weak_poke:
        dex.remove(poke)
        NUM_REMOVED += 1
    print(f"\t{NUM_REMOVED} type combinations/pokemon removed for having total" +
          " base stat values less than " + str(args.stat_exclude))

# removes pokemon from dex with lower base stats than a same typed counterpart
best_poke = set()
covered_types = set()
poke_choices = {}  # dictionary of typekey to arrays of pokemon names that have that type
for poke in dex:
    if poke.typekey not in covered_types:
        covered_types.add(poke.typekey)
        best_poke.add(poke)
        poke_choices[poke.typekey] = [poke.name]
    else:
        for bpoke in best_poke.copy():
            if bpoke.typekey == poke.typekey:
                if bpoke.tbstat < poke.tbstat:
                    best_poke.remove(bpoke)
                    best_poke.add(poke)
                poke_choices[poke.typekey].append(poke.name)
NUM_REMOVED = len(dex) - len(best_poke)
dex = best_poke
print(f"\t{NUM_REMOVED} type combinations/pokemon removed for having lower" +
      " base stat values less than a same typed counterpart")

# remove pokemon with super (x4) weaknesses
# Currently, weakness and strength magnitude is not tracked
# EX: it would be a neutral matchup if there is a 4x weakness one side, and a 2x on the other
# there is also the problem of not handling non-stab moves that may have 4X coverage
# by default remove from team as you really can't be certain what something with 4x weakness covers
if config_data["exclude_4x_weak_from_team"]:
    NUM_REMOVED = 0
    for poke in dex.copy():
        super_weakness_types = types[poke.type1].dse.intersection(types[poke.type2].dse)
        if len(poke.typekey) > 2:
            for atype in poke.typekey:
                if len(atype.split("_")) > 1:
                    ability_split = atype.split("_")
                else:
                    continue
                ability_type = ability_split[0]
                ability_effect = ability_split[1]
                if ability_effect in ["Resist", "Immune"]:
                    super_weakness_types.difference_update(ability_type)
        if len(super_weakness_types) > 0:
            dex.remove(poke)
            NUM_REMOVED += 1

print(f"\t{NUM_REMOVED} type combinations/pokemon removed for having 4x weaknesses")
print("\t\tthis is controlled by exclude_4x_weak_from_team setting/parameter")

NUM_REMOVED = 0
for duo in combinations(dex.copy(), 2):
    pokes = []
    for poke in duo:
        pokes.append(poke)
    # don't let abilities effect this.
    if len(pokes[0].typekey) + len(pokes[1].typekey) > 4:
        continue
    ssestabs0 = dual_types[pokes[0].typekey].ssestabs
    ssestabs1 = dual_types[pokes[1].typekey].ssestabs
    restabs0 = dual_types[pokes[0].typekey].restabs
    restabs1 = dual_types[pokes[1].typekey].restabs
    fmatchups0 = ssestabs0.union(restabs0)
    fmatchups1 = ssestabs1.union(restabs1)
    if ssestabs0 == ssestabs1:
        if restabs0.issubset(restabs1):
            dex.discard(pokes[0])
            NUM_REMOVED += 1
        elif restabs1.issubset(restabs0):
            dex.discard(pokes[1])
            NUM_REMOVED += 1
    elif ssestabs0.issubset(ssestabs1):
        if fmatchups0.issubset(fmatchups1):
            dex.discard(pokes[0])
            NUM_REMOVED += 1
    elif ssestabs1.issubset(ssestabs0):
        if fmatchups1.issubset(fmatchups0):
            dex.discard(pokes[1])
            NUM_REMOVED += 1
print(f"\t{NUM_REMOVED} type combinations/pokemon removed for having" +
      " alternatives that cover everything they do and more")

if (args.rank_types_exclude != 0) and (len(dex) > args.rank_types_exclude):
    typescores = []
    for poke in dex:
        typescores.append(dual_types[poke.typekey].score)
    typescores.sort(reverse=True)
    NUM_REMOVED = 0
    for poke in dex.copy():
        if dual_types[poke.typekey].score < typescores[args.rank_types_exclude]:
            dex.remove(poke)
            NUM_REMOVED += 1
    print(f"\t{NUM_REMOVED} type combinations/pokemon removed for having" +
          " too many more bad matchups than good ones")
    print("\t\tthis is controlled by rank_types_exclude setting/parameter")


print(f"there are {str(len(dex))} type combinations/pokemon left out of {str(len(dual_types))}")


@dataclass(order=True, frozen=True)
class Score:
    """Class representing a Score assigned to a team of pokemon"""
    # number of matchups with at least 1 pokemon
    # that super effective stab without the opponent doing the same
    ssestabs_c: int
    # number of matchups with at least a neutral matchup in addition to
    # the ssestab one, avoids wipes.
    fallback_favorable_neutrals_c: int
    # number of matchups with 2 pokemon with favorable matchups
    favorables2x_c: int
    # number of matchups with 2 pokemon with ssestab matchups
    ssestabs2x_c: int
    # number of matchupes with 2 or more neutral or better matchups
    # in addition to the ssestab one
    fallback_favorable_neutrals2x_c: int
    # sum of type scores across team
    tscore: int
    # uniqueness: sum of pokedex number
    unique_breaker: int


def score_team(team, debug, debug2, ssestabs):
    """scores a team"""
    fallback_favorable_neutrals = set()
    favorables2x = set()
    ssestabs2x = set()
    fallback_favorable_neutrals2x = set()
    for score_typekey in dual_types:
        ssestabs_c_part = 0
        restabs_c_part = 0
        neutrals_c_part = 0
        for score_poke in team:
            if score_typekey in dual_types[score_poke.typekey].ssestabs:
                ssestabs_c_part += 1
            elif score_typekey in dual_types[score_poke.typekey].restabs:
                restabs_c_part += 1
            elif score_typekey in dual_types[score_poke.typekey].neutrals:
                neutrals_c_part += 1
        if ssestabs_c_part > 0:
            if restabs_c_part + ssestabs_c_part + neutrals_c_part - 1 > 1:
                fallback_favorable_neutrals2x.add(score_typekey)
                fallback_favorable_neutrals.add(score_typekey)
            elif restabs_c_part + ssestabs_c_part + neutrals_c_part - 1 > 0:
                fallback_favorable_neutrals.add(score_typekey)
            if restabs_c_part + ssestabs_c_part - 1 > 0:
                favorables2x.add(score_typekey)
        if ssestabs_c_part > 1:
            ssestabs2x.add(score_typekey)
    ssestabs_c = len(ssestabs)
    fallback_favorable_neutrals_c = len(fallback_favorable_neutrals)
    favorables2x_c = len(favorables2x)
    ssestabs2x_c = len(ssestabs2x)
    fallback_favorable_neutrals2x_c = len(fallback_favorable_neutrals2x)

    tscore = 0
    unique_breaker = 0
    restabs = set()
    neutrals = set()
    for score_poke in team:
        tscore += dual_types[score_poke.typekey].score
        unique_breaker += score_poke.number
        restabs.update(dual_types[score_poke.typekey].restabs)
        neutrals.update(dual_types[score_poke.typekey].neutrals)

    if debug:
        print(F"{ssestabs_c} {fallback_favorable_neutrals_c} {favorables2x_c} {ssestabs2x_c} " +
              F"{fallback_favorable_neutrals2x_c} {tscore}")
        for debug_poke in sorted(team, key=lambda x: x.name):
            print(f"\t{debug_poke.name}\ttype score:{str(dual_types[debug_poke.typekey].score)}" +
                  f"\tbase stats:{str(debug_poke.tbstat)}\t{debug_poke.type1} {debug_poke.type2}")
            if len(debug_poke.typekey) > 2:
                for debug_type in debug_poke.typekey:
                    if "_" in debug_type:
                        print(f"\t\tAbility effect: {debug_type.split('_')[0]} " +
                              f"{debug_type.split('_')[1]}")
            if len(poke_choices[debug_poke.typekey]) > 1:
                if len(poke_choices[debug_poke.typekey]) > 1:
                    print("\t\tAlternate choices of same type with lower stats: ", end="")
                    for poke_name in [name for name in sorted(poke_choices[debug_poke.typekey])
                                      if name != debug_poke.name]:
                        print(poke_name, end=" ")
                    print(" ")

    if debug2:
        for debug_type in dual_types.keys()-ssestabs.union(restabs).union(neutrals):
            print("\t\t\tbad matchup against: " + str(" ".join(sorted(debug_type))))
        for debug_type in neutrals-ssestabs.union(restabs):
            print("\t\t\tneutral matchup against: " + str(" ".join(sorted(debug_type))))
        for debug_type in restabs-ssestabs:
            print("\t\t\tonly sestab against: " + str(" ".join(sorted(debug_type))))

    return Score(ssestabs_c, fallback_favorable_neutrals_c, favorables2x_c, ssestabs2x_c,
                 fallback_favorable_neutrals2x_c, tscore, unique_breaker)


include_names = set()
for name in config_data["include_in_team_names"]:
    include_names.add(name)
included_pokemon = set()
for include_name in include_names:
    matches_found = set()
    for poke in full_dex:
        if include_name.lower() in poke.name.lower():
            matches_found.add(poke)
    if len(matches_found) == 0:
        print(f"WARNING: no matching pokemon for {include_name} from include_in_team_names" +
              "setting in settings file, no pokemon added to team for it")
    elif len(matches_found) == 1:
        included_pokemon.update(matches_found)
    else:
        EXACT_MATCH = False
        for poke in matches_found:
            if include_name.lower() == poke.name.lower():
                included_pokemon.add(poke)
                EXACT_MATCH = True
        if EXACT_MATCH:
            continue
        print(f"WARNING: multiple matching pokemon for {include_name} from include_in_team_names" +
              "setting in settings file")
        match = matches_found.pop()
        included_pokemon.add(match)
        print(F"\tOnly including first one found: {match.name}")

start_team = set()
for poke in included_pokemon:
    FOUND = False
    for dpoke in dex.copy():
        if poke.name == dpoke.name:
            dex.remove(dpoke)
            start_team.add(dpoke)
            FOUND = True
            break
        elif poke.typekey == dpoke.typekey:
            print(f"including {dpoke.name} in team as a proxy for {poke.name}, " +
                  "it is the same type with better stats")
            dex.remove(dpoke)
            start_team.add(dpoke)
            FOUND = True
            break
    if not FOUND:
        if poke.typekey not in dual_types:
            print(f"WARNING: {poke.name} was found but not included in team, because it's type " +
                  "was not evaluated, it may have been excluded for being a mega evolution or " +
                  "for being from a wrong region?")
        else:
            start_team.add(poke)

# variables to track percent completion along the way
# makes it ~5% slower, but honestly worth
num_combinations = comb(len(dex), 6-len(start_team))
A_PERC = int(num_combinations/10000)
A_PERC = max(A_PERC, 1)
print("there are " + str(num_combinations) + " teams to assess")
PROG = 0

# Keep track of the best teams so we can show progress and output them later
GOOD_TEAMS = {}
MAX_SSESTABS = -1
TOP_SCORE = Score(0, 0, 0, 0, 0, 0, 0)


def score(in_dex, in_ssestabs, in_team, team_size):
    """makes and scores all possible teams of 6 by adding 1 pokemon at a time,
       only continuing on to make full team if adding that pokemon improved the team.
       only fully scoring if the team is near the best team"""
    # pylint: disable=global-statement
    # pylint: disable=global-variable-not-assigned
    # use global variables to track progress and the best teams
    global PROG
    global GOOD_TEAMS
    global TOP_SCORE
    global MAX_SSESTABS
    while len(in_dex) + len(in_team) >= team_size:
        spoke = in_dex.pop()
        out_ssestabs = in_ssestabs | dual_types[spoke.typekey].ssestabs
        if len(out_ssestabs) == len(in_ssestabs):
            PROG += comb(len(in_dex), team_size - (len(in_team) + 1))
            continue
        out_team = in_team.copy()
        out_team.add(spoke)
        if len(out_team) < team_size:
            score(in_dex.copy(), out_ssestabs, out_team, team_size)
        else:
            PROG += 1
            ssestabs_c = len(out_ssestabs)
            if ssestabs_c < (MAX_SSESTABS - 1):
                continue
            team_score = score_team(out_team, False, False, out_ssestabs)
            if TOP_SCORE < team_score:
                TOP_SCORE = team_score
                MAX_SSESTABS = ssestabs_c
            # save teams near to the high score
            GOOD_TEAMS[team_score] = out_team
            # if PROG % A_PERC == 0 and PROG > 0:
            elapsed_time = timeit.default_timer() - start
            estimated_time_left = ((elapsed_time/(PROG/num_combinations)) - elapsed_time)
            print(f"{round(100*PROG/num_combinations, 2):.2f}% of the way" +
                  f"done, current max ssestabs: {MAX_SSESTABS}, time elapsed: " +
                  f"{round(elapsed_time)}, est. time remaining: " +
                  f"{round(estimated_time_left)}\t\t\r", end='')


start_ssestabs = set()
for poke in start_team:
    start_ssestabs.update(dual_types[poke.typekey].ssestabs)
if len(start_team) == 6:
    TEAM_SCORE = score_team(start_team, False, False, start_ssestabs)
    TOP_SCORE = TEAM_SCORE
    MAX_SSESTABS = len(start_ssestabs)
    GOOD_TEAMS[TEAM_SCORE] = start_team
else:
    score(dex.copy(), start_ssestabs, start_team, 6)
print()

# print teams near to the high score
for ascore in sorted(GOOD_TEAMS.keys()):
    if ascore.ssestabs_c > TOP_SCORE.ssestabs_c - 1:
        ateam = GOOD_TEAMS[ascore].copy()
        team_ssestabs = set()
        for poke in ateam:
            team_ssestabs.update(dual_types[poke.typekey].ssestabs)
        score_team(ateam, True, True, team_ssestabs)
        print()

stop = timeit.default_timer()
print("Runtime: ", stop - start)

ateam = GOOD_TEAMS[TOP_SCORE]
while False:
    print("verify team by inputting a pokemon and seeing how each team member matches up")
    in_name = input("Enter pokemon name, or q to quit: ")
    if in_name == "q":
        break
    matches_found = set()
    FOUND_POKE = None
    for poke in full_dex:
        if in_name.lower() in poke.name.lower():
            matches_found.add(poke)
    if len(matches_found) == 0:
        print(f"No matching pokemon for {in_name}")
        continue
    elif len(matches_found) == 1:
        FOUND_POKE = matches_found.pop()
    else:
        EXACT_MATCH = False
        for poke in matches_found:
            if in_name.lower() == poke.name.lower():
                FOUND_POKE = poke
                EXACT_MATCH = True
        if not EXACT_MATCH:
            print(f"WARNING: multiple matching pokemon for {in_name} from include_in_team_names")
            FOUND_POKE = matches_found.pop()
            print(F"\tOnly including first one found: {FOUND_POKE.name}")
    indtype = FOUND_POKE.typekey
    if indtype not in dual_types:
        print("This pokemon was not included in matchups evaluated." +
              "Is it from another region maybe?")
        continue
    print(f"{FOUND_POKE.name}: {FOUND_POKE.type1} {FOUND_POKE.type2}")
    for poke in ateam:
        print(poke.name + "\t" + poke.type1 + " " + poke.type2)
        print("\tmatchup score: " + str(dual_types[poke.typekey].matchups[indtype]))
        if indtype in dual_types[poke.typekey].d_oe:
            print("\t\toffensively regularly effective")
        if indtype in dual_types[poke.typekey].d_ose:
            print("\t\toffensively super effective")
        if indtype in dual_types[poke.typekey].d_one:
            print("\t\toffensively not very effective")
        if indtype in dual_types[poke.typekey].d_de:
            print("\t\tdefensively regularly effective")
        if indtype in dual_types[poke.typekey].d_dse:
            print("\t\tdefensively super effective, as in vulnerable")
        if indtype in dual_types[poke.typekey].d_dne:
            print("\t\tdefensively not very effective, as in resistant")
