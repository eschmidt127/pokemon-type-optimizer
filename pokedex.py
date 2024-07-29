"""initializes Type and Pokemon classes, creates full set of pokemon,
   determines pokemon in each region,
   provides function for filling in type effectiveness given a set of pokemon"""
import os
import sys
from dataclasses import dataclass, field
import copy
import re
import tomllib


@dataclass
class Type:
    """Class representing a Pokemon Type combination"""
    # pylint: disable=too-many-instance-attributes

    # sets of types as a string (ex. "FIRE")
    oe: set = field(default_factory=set)  # offensively (regularly) effective
    ose: set = field(default_factory=set)  # offensively super effective against
    one: set = field(default_factory=set)  # offensively not very effective against
    de: set = field(default_factory=set)  # defensively (regularly) effective
    dse: set = field(default_factory=set)  # defensively super effective, as in vulnerable
    dne: set = field(default_factory=set)  # defensively not very effective, as in resistant

    # sets of dual types as frozenset of 2 types as strings, where no second type is "NONE"
    d_oe: set = field(default_factory=set)  # offensively (regularly) effective
    d_ose: set = field(default_factory=set)  # offensively super effective against
    d_one: set = field(default_factory=set)  # offensively not very effective against
    d_de: set = field(default_factory=set)  # defensively (regularly) effective
    d_dse: set = field(default_factory=set)  # defensively super effective, as in vulnerable
    d_dne: set = field(default_factory=set)  # defensively not very effective, as in resistant

    # members are d[w|n|s]_o[w|n|s] defensively weak, neutral, strong _
    # offensively weak, neutral, strong
    dw_ow: set = field(default_factory=set)
    dw_on: set = field(default_factory=set)
    dw_os: set = field(default_factory=set)
    dn_ow: set = field(default_factory=set)
    dn_on: set = field(default_factory=set)
    dn_os: set = field(default_factory=set)
    ds_ow: set = field(default_factory=set)
    ds_on: set = field(default_factory=set)
    ds_os: set = field(default_factory=set)

    # safe super effective stabs - highest priority metric
    ssestabs: set = field(default_factory=set)
    # resist, effective stabs - second priority metric
    restabs: set = field(default_factory=set)
    neutrals: set = field(default_factory=set)

    # dictionary of matchup values a type faces, values explained later
    matchups: dict = field(default_factory=dict)
    score: int = 0  # sum of above dictionary entries, values explained later


@dataclass
class Pokemon:
    """Class representing a Pokemon"""
    # pylint: disable=too-many-instance-attributes
    name: str
    number: int
    type1: str  # all caps string of type name
    type2: str
    typekey: frozenset = field(init=False)
    tbstat: int  # total base stats
    ability1: str
    ability2: str
    abilityh: str

    def __post_init__(self):
        self.typekey = frozenset({self.type1, self.type2})

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


def add_ability(name, in_dex, include_hidden, effect1, effect2=""):
    '''adds new pokemon to dex, or updates in place, for effects of abilities'''
    for poke in in_dex.copy():
        make_new = ((poke.ability1 == name and poke.ability2 != "") or
                    (poke.ability2 == name) or
                    (include_hidden and poke.abilityh == name) or
                    (include_hidden and poke.ability1 == name and poke.abilityh != ""))
        if make_new:
            new_ability_poke = copy.deepcopy(poke)
            new_ability_poke.name = poke.name + " - " + name
            if effect2 != "":
                new_ability_poke.typekey = frozenset({poke.type1, poke.type2, effect1, effect2})
            else:
                new_ability_poke.typekey = frozenset({poke.type1, poke.type2, effect1})
            in_dex.add(copy.deepcopy(new_ability_poke))
        elif poke.ability1 == name:
            poke.name = poke.name + " - " + name
            if effect2 != "":
                poke.typekey = frozenset({poke.type1, poke.type2, effect1, effect2})
            else:
                poke.typekey = frozenset({poke.type1, poke.type2, effect1})


# dictionary of type names as strings to their Type class variable
types = {
    "NORMAL": Type(),
    "FIRE": Type(),
    "WATER": Type(),
    "ELECTRIC": Type(),
    "GRASS": Type(),
    "ICE": Type(),
    "FIGHTING": Type(),
    "POISON": Type(),
    "GROUND": Type(),
    "FLYING": Type(),
    "PSYCHIC": Type(),
    "BUG": Type(),
    "ROCK": Type(),
    "GHOST": Type(),
    "DRAGON": Type(),
    "DARK": Type(),
    "STEEL": Type(),
    "FAIRY": Type(),
    "NONE": Type()
}


def is_se(otype, *detypes):  # otype is offensize type
    """fills Type variables with their OSE and DSE taking a type,
       then each type that it is super effective against"""
    for detype in detypes:  # detype are defending types
        types[otype].ose.add(detype)
        types[detype].dse.add(otype)


def is_ne(otype, *detypes):
    """fills Type variables with their ONE and DNE taking a type,
       then each type that it is not effective against"""
    for detype in detypes:
        types[otype].one.add(detype)
        types[detype].dne.add(otype)


def score_dex(dex, dual_types):
    """uses set of pokemen dex to fill type effectiveness for each type
       in dual_types dictionary of typekey to type class object"""
    # fill in set of single type effectivenesses for each pokemon
    # oe,one,ose,de,dne,dse
    for poke in dex:
        if poke.typekey not in dual_types:
            # offensively super effective against a type if either type is
            ose = types[poke.type1].ose.union(types[poke.type2].ose)
            # offensively not effective against a type if both types are
            one = types[poke.type1].one.intersection(types[poke.type2].one)
            # defensively super effective against a type if either type is,
            # and the other does not resist it
            dse = types[poke.type1].dse.union(types[poke.type2].dse)
            dse.difference_update(types[poke.type1].dne)
            dse.difference_update(types[poke.type2].dne)
            # defensively not effective against a type if either type is,
            # and the other is not weak to it
            dne = types[poke.type1].dne.union(types[poke.type2].dne)
            dne.difference_update(types[poke.type1].dse)
            dne.difference_update(types[poke.type2].dse)
            # immunities take precedent
            if poke.type1 == "GHOST" or poke.type2 == "GHOST":
                dne.add("NORMAL")
                dne.add("FIGHTING")
            if poke.type1 == "GROUND" or poke.type2 == "GROUND":
                dne.add("ELECTRIC")
            if poke.type1 == "FLYING" or poke.type2 == "FLYING":
                dne.add("GROUND")
            if poke.type1 == "DARK" or poke.type2 == "DARK":
                dne.add("PSYCHIC")
            if poke.type1 == "STEEL" or poke.type2 == "STEEL":
                dne.add("POISON")
            if poke.type1 == "FAIRY" or poke.type2 == "FAIRY":
                dne.add("DRAGON")
            if len(poke.typekey) > 2:
                for abtype in poke.typekey:
                    if len(abtype.split("_")) > 1:
                        ability_split = abtype.split("_")
                    else:
                        continue
                    ability_type = ability_split[0]
                    ability_effect = ability_split[1]
                    if ability_effect == "Resist":
                        if ability_type in dse:
                            dse.difference_update(ability_type)
                        else:
                            dne.add(ability_type)
                    if ability_effect == "Immune":
                        dse.difference_update(ability_type)
                        dne.add(ability_type)
                    if ability_effect == "Stab":
                        one.difference_update(types[ability_type].ose)
                        ose.update(types[ability_type].ose)
            dual_types[poke.typekey] = Type(ose=ose, one=one, dse=dse, dne=dne)

    for btype in dual_types.values():
        btype.oe = alltypes - btype.ose - btype.one
        btype.de = alltypes - btype.dse - btype.dne

    # updates pokemon that were included because of their ability,
    # but their ability does not change anything
    remove_from_dual_types = set()
    for poke in dex.copy():
        if len(poke.typekey) > 2:
            typekey_no_ability = frozenset({poke.type1, poke.type2})
            ability_type_effectiveness = [dual_types[poke.typekey].oe,
                                          dual_types[poke.typekey].one,
                                          dual_types[poke.typekey].ose,
                                          dual_types[poke.typekey].de,
                                          dual_types[poke.typekey].dne,
                                          dual_types[poke.typekey].dse]
            base_type_effectiveness = [dual_types[typekey_no_ability].oe,
                                       dual_types[typekey_no_ability].one,
                                       dual_types[typekey_no_ability].ose,
                                       dual_types[typekey_no_ability].de,
                                       dual_types[typekey_no_ability].dne,
                                       dual_types[typekey_no_ability].dse]
            if ability_type_effectiveness == base_type_effectiveness:
                remove_from_dual_types.add(poke.typekey.copy())
                # remove it if this pokemon has two mutliple abilities, and this version was a copy
                # added due to the ability that had no positive effect
                removed = False
                for inner_poke in dex.copy():
                    if (poke.number == inner_poke.number and
                            inner_poke.typekey == typekey_no_ability):
                        dex.remove(poke)
                        removed = True
                # if this pokemon's only ability had no effect, revert the typekey to not have the
                # ability anymore - later on will combine all same types pokemon.
                if not removed:
                    poke.typekey = typekey_no_ability.copy()
    for typekey in remove_from_dual_types:
        del dual_types[typekey]
    # fill dual_types with more advanced info (type effectivenesses against every dual type)
    # d_oe,d_one,d_ose,d_de,d_dne,d_dse
    for poke in dex:
        for dtypekey, dtype in dual_types.items():
            if "NONE" in dtypekey and len(dtypekey) < 3:
                for adtype in dtypekey:
                    if adtype != "NONE":
                        if adtype in dual_types[poke.typekey].ose:
                            dual_types[poke.typekey].d_ose.add(dtypekey)
                        if adtype in dual_types[poke.typekey].one:
                            dual_types[poke.typekey].d_one.add(dtypekey)
                        if adtype in dual_types[poke.typekey].oe:
                            dual_types[poke.typekey].d_oe.add(dtypekey)
                        if adtype in dual_types[poke.typekey].dse:
                            dual_types[poke.typekey].d_dse.add(dtypekey)
                        if adtype in dual_types[poke.typekey].dne:
                            dual_types[poke.typekey].d_dne.add(dtypekey)
                        if adtype in dual_types[poke.typekey].de:
                            dual_types[poke.typekey].d_de.add(dtypekey)
            else:
                dtypes = []
                for adtype in dtypekey:
                    if "_" not in adtype:
                        dtypes.append(adtype)
                dtype1 = dtypes[0]
                dtype2 = dtypes[1]
                ptype = dual_types[poke.typekey]
                # offensively super effective against a type
                # if either of our types are in it's weak list
                if poke.type1 in dtype.dse or poke.type2 in dtype.dse:
                    ptype.d_ose.add(dtypekey)
                # offensively not effective against a type
                # if both of our types are in it's resist list
                if poke.type1 in dtype.dne and poke.type2 in dtype.dne:
                    ptype.d_one.add(dtypekey)
                # defensively super effective against a type
                # if either of the other type's types are in our weak list
                if dtype1 in ptype.dse or dtype2 in ptype.dse:
                    ptype.d_dse.add(dtypekey)
                # defensively not effective against a type
                # if both of the other type's types are in our resist list
                if dtype1 in ptype.dne and dtype2 in ptype.dne:
                    ptype.d_dne.add(dtypekey)
                if len(poke.typekey) > 2:
                    for aptype in poke.typekey:
                        if len(aptype.split("_")) > 1:
                            ability_split = aptype.split("_")
                        else:
                            continue
                        ability_type = ability_split[0]
                        ability_effect = ability_split[1]
                        if ability_effect == "Resist":
                            if (dtype1 in ptype.dse and
                                    dtype2 in ptype.dse):
                                continue
                            if ability_type in ptype.d_dse:
                                ptype.d_dse.difference_update(ability_type)
                            else:
                                ptype.d_dne.add(ability_type)
                        elif ability_effect == "Immune":
                            ptype.d_dse.difference_update(ability_type)
                            ptype.d_dne.add(ability_type)
                        elif ability_effect == "Stab":
                            if ability_type in dtype.dse:
                                ptype.d_one.difference_update(dtypekey)
                                ptype.d_ose.add(dtypekey)
                            elif ability_type in dtype.de:
                                ptype.d_one.difference_update(dtypekey)
    for poke in dex:
        dual_types[poke.typekey].d_oe = (dual_types.keys() - dual_types[poke.typekey].d_ose
                                         - dual_types[poke.typekey].d_one)
        dual_types[poke.typekey].d_de = (dual_types.keys() - dual_types[poke.typekey].d_dse
                                         - dual_types[poke.typekey].d_dne)

    # fill the xx_xx variables, they hold a list of matchups a pokemon/Type combination faces.
    for poke in dex:
        for dtype in dual_types:
            # value based on
            # dw_ow_matchup is worth -4
            # dw_on_matchup is worth -3
            # dw_os_matchup is worth 0
            # dn_ow_matchup is worth -1
            # dn_on_matchup is worth 0
            # dn_os_matchup is worth 3
            # ds_ow_matchup is worth 0
            # ds_on_matchup is worth 1
            # ds_os_matchup is worth 4

            # if defensively neutral (+ 0)
            if dtype in dual_types[poke.typekey].d_de:
                # if offensively neutral (+ 0)
                if dtype in dual_types[poke.typekey].d_oe:
                    dual_types[poke.typekey].dn_on.add(dtype)
                    dual_types[poke.typekey].matchups[dtype] = 0
                    dual_types[poke.typekey].neutrals.add(dtype)
                # if offensively weak (-1)
                elif dtype in dual_types[poke.typekey].d_one:
                    dual_types[poke.typekey].dn_ow.add(dtype)
                    dual_types[poke.typekey].matchups[dtype] = -1
                # if offensively strong (+3)
                elif dtype in dual_types[poke.typekey].d_ose:
                    dual_types[poke.typekey].dn_os.add(dtype)
                    dual_types[poke.typekey].matchups[dtype] = 3
                    dual_types[poke.typekey].ssestabs.add(dtype)
            # if defensively weak (-3)
            elif dtype in dual_types[poke.typekey].d_dse:
                # if offensively neutral (+ 0)
                if dtype in dual_types[poke.typekey].d_oe:
                    dual_types[poke.typekey].dw_on.add(dtype)
                    dual_types[poke.typekey].matchups[dtype] = -3
                # if offensively weak (-1)
                elif dtype in dual_types[poke.typekey].d_one:
                    dual_types[poke.typekey].dw_ow.add(dtype)
                    dual_types[poke.typekey].matchups[dtype] = -4
                # if offensively strong (+3)
                elif dtype in dual_types[poke.typekey].d_ose:
                    dual_types[poke.typekey].dw_os.add(dtype)
                    dual_types[poke.typekey].matchups[dtype] = 0
                    dual_types[poke.typekey].neutrals.add(dtype)
            # if defensively strong (+1)
            elif dtype in dual_types[poke.typekey].d_dne:
                # if offensively neutral (+ 0)
                if dtype in dual_types[poke.typekey].d_oe:
                    dual_types[poke.typekey].ds_on.add(dtype)
                    dual_types[poke.typekey].matchups[dtype] = 1
                    dual_types[poke.typekey].restabs.add(dtype)
                # if offensively weak (-1)
                elif dtype in dual_types[poke.typekey].d_one:
                    dual_types[poke.typekey].ds_ow.add(dtype)
                    dual_types[poke.typekey].matchups[dtype] = 0
                    dual_types[poke.typekey].neutrals.add(dtype)
                # if offensively strong (+3)
                elif dtype in dual_types[poke.typekey].d_ose:
                    dual_types[poke.typekey].ds_os.add(dtype)
                    dual_types[poke.typekey].matchups[dtype] = 4
                    dual_types[poke.typekey].ssestabs.add(dtype)

    for mtype in dual_types:
        for amatchup in dual_types[mtype].matchups:
            dual_types[mtype].score += dual_types[mtype].matchups[amatchup]

    return dex, dual_types


default_settings_path = os.path.join(os.path.dirname(__file__), "default_settings.toml")
with open(default_settings_path, "rb") as f:
    config_data = tomllib.load(f)
settings_path = os.path.join(os.path.dirname(__file__), "settings.toml")
if os.path.isfile(settings_path):
    with open(settings_path, "rb") as f:
        custom_config_data = tomllib.load(f)
    config_data.update(custom_config_data)

full_dex = set()
data_path = os.path.join(os.path.dirname(__file__), "data")
if not os.path.isfile(os.path.join(data_path, "pokedex.csv")):
    sys.exit(f"pokedex.csv does not exist in {os.mkdir(data_path)}," +
             "try running scrape.py to generate data")
with open(os.path.join(data_path, "pokedex.csv"), "r", encoding="utf-8") as f:
    for pokecsv in f:
        s = pokecsv.split(",")
        full_dex.add(Pokemon(name=s[0], number=int(s[1]), type1=s[2].upper(), type2=s[3].upper(),
                             tbstat=int(s[4]), ability1=s[4], ability2=s[5], abilityh=s[6]))
region_nums = {}
region_num_regex = re.compile("(.+)(_national_dex_numbers\\.txt)")
for path in os.listdir(data_path):
    match = re.match(region_num_regex, path)
    if match:
        region_nums[match.group(1)] = set()
        with open(os.path.join(data_path, match.group(0)), encoding="utf-8") as f:
            for num in f:
                region_nums[match.group(1)].add(int(num))

is_se("BUG", "PSYCHIC", "DARK", "GRASS")
is_ne("BUG", "FIRE", "FIGHTING", "POISON", "FLYING", "GHOST", "STEEL", "FAIRY")
is_se("DARK", "PSYCHIC", "GHOST")
is_ne("DARK", "FIGHTING", "DARK", "FAIRY")
is_se("DRAGON", "DRAGON")
is_ne("DRAGON", "STEEL", "FAIRY")
is_se("ELECTRIC", "WATER", "FLYING")
is_ne("ELECTRIC", "ELECTRIC", "GRASS", "DRAGON", "GROUND")
is_se("FAIRY", "FIGHTING", "DRAGON", "DARK")
is_ne("FAIRY", "FIRE", "POISON", "STEEL")
is_se("FIGHTING", "NORMAL", "ICE", "ROCK", "DARK", "STEEL")
is_ne("FIGHTING", "POISON", "FLYING", "PSYCHIC", "BUG", "FAIRY", "GHOST")
is_se("FIRE", "GRASS", "ICE", "BUG", "STEEL")
is_ne("FIRE", "FIRE", "WATER", "ROCK", "DRAGON")
is_se("FLYING", "GRASS", "FIGHTING", "BUG")
is_ne("FLYING", "ELECTRIC", "ROCK", "STEEL")
is_se("GHOST", "PSYCHIC", "GHOST")
is_ne("GHOST", "DARK", "NORMAL")
is_se("GRASS", "WATER", "GROUND", "ROCK")
is_ne("GRASS", "FIRE", "GRASS", "POISON", "FLYING", "BUG", "DRAGON", "STEEL")
is_se("GROUND", "FIRE", "ELECTRIC", "POISON", "ROCK", "STEEL")
is_ne("GROUND", "GRASS", "BUG", "FLYING")
is_se("ICE", "GRASS", "GROUND", "FLYING", "DRAGON")
is_ne("ICE", "FIRE", "WATER", "ICE", "STEEL")
# is_se("NORMAL",)
is_ne("NORMAL", "ROCK", "STEEL", "GHOST")
is_se("POISON", "GRASS", "FAIRY")
is_ne("POISON", "POISON", "GROUND", "ROCK", "GHOST", "STEEL")
is_se("PSYCHIC", "FIGHTING", "POISON")
is_ne("PSYCHIC", "PSYCHIC", "STEEL", "DARK")
is_se("ROCK", "FIRE", "ICE", "FLYING", "BUG")
is_ne("ROCK", "FIGHTING", "GROUND", "STEEL")
is_se("STEEL", "ICE", "ROCK", "FAIRY")
is_ne("STEEL", "FIRE", "WATER", "ELECTRIC", "STEEL")
is_se("WATER", "FIRE", "GROUND", "ROCK")
is_ne("WATER", "GRASS", "WATER", "DRAGON")

if config_data["assess_abilities"]:
    add_ability("Sap Sipper", full_dex, config_data["assess_hidden_abilities"], "GRASS_Immune")
    add_ability("Storm Drain", full_dex, config_data["assess_hidden_abilities"], "WATER_Immune")
    add_ability("Water Absorb", full_dex, config_data["assess_hidden_abilities"], "WATER_Immune")
    add_ability("Motor Drive", full_dex, config_data["assess_hidden_abilities"], "ELECTRIC_Immune")
    add_ability("Volt Absorb", full_dex, config_data["assess_hidden_abilities"], "ELECTRIC_Immune")
    add_ability("Thick Fat", full_dex, config_data["assess_hidden_abilities"],
                "FIRE_Resist", "ICE_Resist")
    add_ability("Levitate", full_dex, config_data["assess_hidden_abilities"], "GROUND_Immune")
    add_ability("Earth Eater", full_dex, config_data["assess_hidden_abilities"], "GROUND_Immune")
    add_ability("Flash Fire", full_dex, config_data["assess_hidden_abilities"], "FIRE_Immune")
    add_ability("Well-Baked Body", full_dex, config_data["assess_hidden_abilities"], "FIRE_Immune")
    add_ability("Water-Bubble", full_dex, config_data["assess_hidden_abilities"], "FIRE_Resist")
    add_ability("Heatproof", full_dex, config_data["assess_hidden_abilities"], "FIRE_Resist")
    add_ability("Steelworker", full_dex, config_data["assess_hidden_abilities"], "STEEL_Stab")

alltypes = set()
for atype in types:
    alltypes.add(atype)

for atypekey, atype in types.items():
    atype.oe = alltypes - atype.ose - atype.one
    atype.de = alltypes - atype.dse - atype.dne
