# Pokemon Type Optimizer
This program will identify an optimal team of 6 pokemon based solely on type matchups. Each unique type combination that may be faced by the team is considered a single matchup. The primary metric that is used to measure the team is the number of matchups that have "safe super effective stabs". If a pokemon in the team of six has a super effective move that has same type attack bonus and the opposing pokemon does not have the same, this is a "safe super effective stab" .

Considerations:
- Double / x4 weaknesses are not differentiated from x2 weaknesses in the assessments. For this reason by default these pokemon are not considered for inclusion in the team. If you accept that your "safe super effectvie stab" may not be all that safe because they could have a coverage move that is x4 effective (more than your likely x3 with STAB considered), you can override this and include those pokemon anyway.
- Abilities that effect type effectiveness are accounted for by default if they are not hidden abilities. Hidden ability assessment can be enabled.
- Mega evolutions are not included in assesments by default. If this is overriden, they are accounted for as if they are separate pokemon. 
- Terastallization is not accounted for.
- In order to make runtime of the program reasonable, only the top 50 pokemon types are assessed as part of the team by default.
- non-STAB moves are not accounted for, nor is move power.

## Example Output / Just Tell Me the Best Teams 
Read more sections to know more about what the numbers actually mean.

National dex
```text
194 194 158 135 192 425
        Chi-Yu  type score:50   base stats:570  DARK FIRE
                Alternate choices of same type with lower stats: Houndoom Incineroar
        Groudon type score:57   base stats:670  GROUND NONE
                Alternate choices of same type with lower stats: Donphan Hippowdon Mudsdale Sandaconda Sandslash
        Ogerpon - Cornerstone Mask      type score:36   base stats:550  GRASS ROCK
                Alternate choices of same type with lower stats: Cradily
        Tapu Fini       type score:89   base stats:570  WATER FAIRY
                Alternate choices of same type with lower stats: Primarina
        Thundurus - Therian Forme - Volt Absorb type score:107  base stats:580  ELECTRIC FLYING
                Ability effect: ELECTRIC Immune
        Zamazenta - Crowned Shield      type score:86   base stats:700  FIGHTING STEEL
                Alternate choices of same type with lower stats: Cobalion Lucario
```
Paldea Dex (with all DLC)
```text
162 162 126 108 161 322
        Chi-Yu  type score:28   base stats:570  DARK FIRE
                Alternate choices of same type with lower stats: Houndoom Incineroar
        Corviknight     type score:99   base stats:495  FLYING STEEL
                Alternate choices of same type with lower stats: Skarmory
        Gallade type score:57   base stats:518  PSYCHIC FIGHTING
        Hippowdon       type score:48   base stats:525  GROUND NONE
                Alternate choices of same type with lower stats: Donphan Mudsdale Sandaconda Sandslash
        Ogerpon - Cornerstone Mask      type score:27   base stats:550  GRASS ROCK
        Primarina       type score:63   base stats:530  WATER FAIRY
```
Hypothetical dex (all possible type combinations, abilities included only for pokemon that do already exist)
```text
204 204 168 145 202 477
        DARK FIRE       type score:54   base stats:450  DARK FIRE
        ELECTRIC FLYING ability: ELECTRIC_Immune        type score:101  base stats:450  ELECTRIC FLYING
                Ability effect: ELECTRIC Immune
        FAIRY WATER     type score:105  base stats:450  FAIRY WATER
                Alternate choices of same type with lower stats: WATER FAIRY ability: FIRE_Resist ICE_Resist
        GROUND NONE     type score:66   base stats:450  GROUND NONE
        ROCK GRASS      type score:44   base stats:450  ROCK GRASS
        STEEL FIGHTING  type score:107  base stats:450  STEEL FIGHTING
```
## Requirements
Python 3.12 with standard libraries

If you would like to re-run the web scraper used to collect pokemon data (there should really not be a reason to do this unless you forked and made changes), you will need the selenium and webdriver manager python packages as well as chrome.

## Usage
```bash
python main.py [-h] [--stat_exclude [STAT_EXCLUDE]] [--rank_types_exclude [RANK_TYPES_EXCLUDE]] [--rank_types] [input_dex] [input_dex2] ...
```
- STAT_EXCLUDE: pokemon with total base stats less than this number will be considered as matchups, but not considered for inclusion in the team. Default: 450
- RANK_TYPES_EXCLUDE: The top this many pokemon based on how many good matchups they have will be considered with inclusion in the team. Default: 50
- --rank_types: If used, shows the ranking of types that will be used for RANK_TYPES_EXCLUDE without calculating teams.
- input_dex: The pokedex used. This will align with the name of the datafile in the datafolder, or national to include the entire pokedex. pass multiple to combine multiple inputs. Special cases: national (all), hypothetical (assess all type combinations even if no pokemon exists with that type), cant combine special cases with other pokedexes. Default: national 

## Settings
Copy the default_settings.toml to settings.toml and change things there if you would like to change settings.
- include pokemon with 4x weaknesses in teams
- Assess mega evolutions as separate pokemon
- include or exclude specific pokemon from your team
- include or exclude more pokemon from your team based on total base stats
- include or exclude more pokemon from your team based on how many good matchups they have.

## Data Files
### pokedex.csv
The list of pokemon that exist
```csv
name, national dex number, type 1, type 2, base stat total, ability 1, ability 2, hidden ability
```
### [name]_national_dex_numbers.txt
For a region [name], the list of national pokedex numbers to include in that regional pokedex.

## Team Assessment Metric Details
The following metrics are used to rank the pokemon teams, with the next metric only used to break ties for all previous metrics.
- Number of "safe super effective stab" matchups
- Number of matchups with at least a neutral matchup in addition to the "safe super effective stab" one, avoids wipes.
- number of matchups with 2 pokemon with favorable matchups
- number of matchups with 2 pokemon with "safe super effective stab" matchups
- number of matchupes with 2 or more neutral or better matchups
- sum of type scores across team

### Type Scores
A pokemon's type score is the sum of all the values given to each matchup possible.

Each matchup is given a value:
- defensively weak offensively neutral matchup is worth -3
- defensively weak offensively strong matchup is worth 0
- defensively neutral offensively weak matchup is worth -1
- defensively neutral offensively neutral matchup is worth 0
- defensively neutral offensively strong matchup is worth 3
- defensively strong offensively weak matchup is worth 0
- defensively strong offensively neutral matchup is worth 1
- defensively strong offensively strong matchup is worth 4

#### What are the best types?
Assuming Hypothetical pokedex (all types combinations are possible)
Type  | Average Matchup Score
----- | -----
FAIRY STEEL  | 0.7990196078431373
DARK POISON  | 0.7303921568627451
FLYING STEEL  | 0.6715686274509803
GHOST FAIRY  | 0.6225490196078431
GROUND STEEL  | 0.6127450980392157
FAIRY GROUND  | 0.6127450980392157
DRAGON STEEL  | 0.5735294117647058
WATER_Immune FIRE WATER  | 0.5441176470588235
ELECTRIC FAIRY  | 0.5392156862745098
FIGHTING STEEL  | 0.5245098039215687
WATER FAIRY  | 0.5147058823529411
FIRE WATER  | 0.5049019607843137
WATER ELECTRIC ELECTRIC_Immune  | 0.5049019607843137
ELECTRIC FLYING ELECTRIC_Immune  | 0.4950980392156863
ICE GROUND  | 0.47549019607843135
GROUND_Immune WATER ELECTRIC  | 0.45098039215686275
WATER ELECTRIC  | 0.45098039215686275
ELECTRIC FLYING  | 0.44607843137254904
WATER STEEL  | 0.4411764705882353
FIRE GRASS  | 0.4362745098039216
FIRE FAIRY  | 0.4264705882352941
DARK FAIRY  | 0.39705882352941174
ROCK BUG  | 0.3872549019607843
DRAGON WATER  | 0.38235294117647056
GHOST STEEL  | 0.38235294117647056
GHOST NORMAL  | 0.36764705882352944
DRAGON FIRE  | 0.35784313725490197
GROUND BUG  | 0.3431372549019608
FIGHTING GHOST  | 0.3382352941176471
PSYCHIC FIGHTING  | 0.3284313725490196
POISON GROUND  | 0.3235294117647059
NONE GROUND  | 0.3235294117647059
GROUND_Immune ELECTRIC BUG  | 0.31862745098039214
ELECTRIC BUG  | 0.29411764705882354
DARK GHOST  | 0.28921568627450983
ELECTRIC GROUND  | 0.28431372549019607
GHOST GROUND  | 0.27941176470588236
WATER POISON  | 0.2647058823529412
DARK FIRE  | 0.2647058823529412
WATER BUG  | 0.25980392156862747
FIRE FIGHTING  | 0.24509803921568626
GROUND_Immune ELECTRIC GHOST  | 0.22058823529411764
ELECTRIC GHOST  | 0.22058823529411764
ELECTRIC FIGHTING  | 0.22058823529411764
ROCK GRASS  | 0.21568627450980393
WATER GHOST  | 0.17647058823529413
FIRE_Immune FAIRY NONE  | 0.1715686274509804
GROUND_Immune ELECTRIC NONE  | 0.16666666666666666
ELECTRIC NONE  | 0.16666666666666666
ICE WATER FIRE_Resist ICE_Resist  | 0.15196078431372548
FAIRY NONE  | 0.14215686274509803
GROUND_Immune NONE STEEL  | 0.14215686274509803
NONE STEEL  | 0.14215686274509803
ICE WATER  | 0.1323529411764706
FIRE GHOST  | 0.12745098039215685
FIRE NONE  | 0.09803921568627451
FIRE_Resist FAIRY NORMAL ICE_Resist  | 0.09313725490196079
WATER NONE  | 0.09313725490196079
STEEL_Stab GHOST GRASS  | 0.08823529411764706
GROUND_Immune GHOST NONE  | 0.08823529411764706
GROUND_Immune POISON FAIRY  | 0.06862745098039216
POISON FAIRY  | 0.06862745098039216
PSYCHIC GROUND_Immune STEEL  | 0.06862745098039216
PSYCHIC STEEL  | 0.06862745098039216
GHOST NONE  | 0.06372549019607843
GROUND_Immune ELECTRIC ICE  | 0.05392156862745098
ICE ELECTRIC  | 0.05392156862745098
DARK FLYING  | 0.0392156862745098
FAIRY NORMAL  | 0.03431372549019608
PSYCHIC FAIRY  | 0.0196078431372549
DARK GROUND  | 0.0196078431372549
FIGHTING FIRE_Resist ICE_Resist NONE  | 0.0196078431372549
NORMAL GROUND  | -0.0196078431372549
FIGHTING NONE  | -0.029411764705882353
FIGHTING FLYING  | -0.029411764705882353
ICE GHOST  | -0.049019607843137254
PSYCHIC FIRE  | -0.049019607843137254
FLYING ROCK  | -0.058823529411764705
WATER GRASS  | -0.06862745098039216
DARK ELECTRIC  | -0.0784313725490196
PSYCHIC POISON  | -0.08333333333333333
GROUND_Immune POISON GHOST  | -0.08823529411764706
POISON GHOST  | -0.08823529411764706
ICE FIGHTING  | -0.09803921568627451
GHOST ROCK  | -0.11274509803921569
POISON NONE  | -0.12745098039215685
GROUND_Immune POISON NONE  | -0.12745098039215685
FIGHTING FAIRY  | -0.12745098039215685
DARK WATER  | -0.12745098039215685
WATER FIGHTING  | -0.13725490196078433
ELECTRIC NORMAL  | -0.14705882352941177
WATER NORMAL  | -0.1715686274509804
FLYING GHOST  | -0.17647058823529413
PSYCHIC NORMAL  | -0.18627450980392157
FIRE NORMAL  | -0.19607843137254902
PSYCHIC GROUND_Immune GROUND  | -0.20588235294117646
FLYING NONE  | -0.21568627450980393
GROUND_Immune ICE NONE  | -0.22058823529411764
DARK NONE  | -0.22058823529411764
ICE NONE  | -0.23039215686274508
FIGHTING ROCK  | -0.23529411764705882
FIGHTING GROUND  | -0.23529411764705882
PSYCHIC GROUND  | -0.24019607843137256
PSYCHIC WATER  | -0.24019607843137256
NONE FIRE_Resist ICE_Resist NORMAL  | -0.25
PSYCHIC ELECTRIC  | -0.2549019607843137
NONE BUG  | -0.2647058823529412
NORMAL NONE  | -0.27450980392156865
DRAGON FAIRY  | -0.29901960784313725
GROUND_Immune DRAGON GHOST  | -0.29901960784313725
DRAGON ELECTRIC  | -0.3088235294117647
GHOST GRASS  | -0.3235294117647059
ICE POISON  | -0.3284313725490196
GHOST BUG  | -0.3284313725490196
PSYCHIC FIRE_Resist ICE_Resist NONE  | -0.3333333333333333
DRAGON GHOST  | -0.3431372549019608
FLYING FAIRY  | -0.3431372549019608
PSYCHIC GROUND_Immune NONE  | -0.3480392156862745
POISON GRASS  | -0.35784313725490197
FIGHTING NORMAL  | -0.35784313725490197
PSYCHIC NONE  | -0.36764705882352944
DRAGON POISON  | -0.38235294117647056
FLYING NORMAL  | -0.38235294117647056
POISON NORMAL  | -0.3872549019607843
NONE ROCK  | -0.39215686274509803
POISON FLYING  | -0.4215686274509804
FAIRY BUG  | -0.4264705882352941
DRAGON ROCK  | -0.4411764705882353
GROUND_Immune ELECTRIC GRASS  | -0.4411764705882353
PSYCHIC ICE  | -0.44607843137254904
NORMAL BUG  | -0.45588235294117646
ELECTRIC GRASS  | -0.46568627450980393
DARK BUG  | -0.4803921568627451
PSYCHIC GROUND_Immune ROCK  | -0.4852941176470588
PSYCHIC ROCK  | -0.4852941176470588
POISON BUG  | -0.5049019607843137
ICE DRAGON  | -0.5147058823529411
DRAGON NONE  | -0.5294117647058824
PSYCHIC BUG  | -0.5490196078431373
PSYCHIC FLYING  | -0.5686274509803921
DRAGON BUG  | -0.6617647058823529
NONE GRASS  | -0.7745098039215687
PSYCHIC GROUND_Immune DRAGON  | -0.7843137254901961
PSYCHIC DRAGON  | -0.8235294117647058
DRAGON NORMAL  | -0.8382352941176471
NORMAL GRASS  | -1.0784313725490196
