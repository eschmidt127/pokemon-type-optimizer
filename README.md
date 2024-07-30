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
FIRE GROUND | 1.191176471
FLYING GROUND | 1.093137255
WATER GROUND | 1.06372549
STEEL BUG | 0.818627451
STEEL FAIRY | 0.799019608
DARK POISON | 0.730392157
WATER FLYING | 0.705882353
STEEL FLYING | 0.671568627
DARK STEEL | 0.62745098
FAIRY GHOST | 0.62254902
FIRE STEEL FIRE_Immune | 0.617647059
STEEL GROUND | 0.612745098
FAIRY GROUND | 0.612745098
ROCK STEEL | 0.607843137
DARK FIGHTING | 0.578431373
STEEL ICE | 0.578431373
STEEL DRAGON | 0.573529412
FIRE STEEL | 0.553921569
FIRE WATER_Immune WATER | 0.544117647
FAIRY ELECTRIC | 0.539215686
STEEL FIGHTING | 0.524509804
STEEL GRASS | 0.519607843
WATER FAIRY | 0.514705882
WATER ELECTRIC ELECTRIC_Immune | 0.504901961
WATER FIRE | 0.504901961
GROUND_Immune GROUND DRAGON | 0.5
FLYING ELECTRIC ELECTRIC_Immune | 0.495098039
GROUND DRAGON | 0.475490196
ICE GROUND | 0.475490196
STEEL ELECTRIC | 0.470588235
FIRE ELECTRIC | 0.465686275
FIRE GROUND_Immune ELECTRIC | 0.465686275
WATER ELECTRIC | 0.450980392
WATER GROUND_Immune ELECTRIC | 0.450980392
FLYING ELECTRIC | 0.446078431
WATER STEEL | 0.441176471
FIRE GRASS | 0.43627451
ROCK FAIRY | 0.426470588
FIRE FAIRY | 0.426470588
PSYCHIC GHOST | 0.416666667
STEEL POISON | 0.406862745
ROCK FIRE | 0.406862745
DARK FAIRY | 0.397058824
ROCK BUG | 0.387254902
STEEL GHOST | 0.382352941
WATER DRAGON | 0.382352941
DARK PSYCHIC | 0.37254902
GHOST NORMAL | 0.367647059
FIRE DRAGON | 0.357843137
BUG GROUND | 0.343137255
FIGHTING GHOST | 0.338235294
FIGHTING PSYCHIC | 0.328431373
FIRE FIRE_Immune BUG | 0.328431373
POISON GROUND | 0.323529412
NONE GROUND | 0.323529412
GROUND_Immune BUG ELECTRIC | 0.318627451
BUG ELECTRIC | 0.294117647
DARK GHOST | 0.289215686
ROCK GROUND | 0.289215686
ELECTRIC GROUND | 0.284313725
FIRE BUG | 0.284313725
GHOST GROUND | 0.279411765
FIGHTING POISON | 0.269607843
WATER POISON | 0.264705882
DARK FIRE | 0.264705882
FIRE ICE | 0.259803922
WATER BUG | 0.259803922
FIRE FLYING | 0.25
FIRE FIGHTING | 0.245098039
ELECTRIC POISON | 0.245098039
WATER ROCK | 0.235294118
FIGHTING ELECTRIC | 0.220588235
GHOST ELECTRIC | 0.220588235
GROUND_Immune GHOST ELECTRIC | 0.220588235
ROCK GRASS | 0.215686275
WATER GHOST | 0.176470588
FAIRY NONE FIRE_Immune | 0.171568627
NONE ELECTRIC | 0.166666667
GROUND_Immune NONE ELECTRIC | 0.166666667
WATER ICE_Resist ICE FIRE_Resist | 0.151960784
STEEL GROUND_Immune NONE | 0.142156863
STEEL NONE | 0.142156863
FAIRY NONE | 0.142156863
WATER ICE | 0.132352941
FIRE GHOST | 0.12745098
STEEL NORMAL | 0.107843137
FIRE NONE | 0.098039216
WATER NONE | 0.093137255
FAIRY FIRE_Resist NORMAL ICE_Resist | 0.093137255
GROUND_Immune GHOST NONE | 0.088235294
GHOST GRASS STEEL_Stab | 0.088235294
STEEL PSYCHIC | 0.068627451
STEEL PSYCHIC GROUND_Immune | 0.068627451
FAIRY POISON | 0.068627451
FAIRY GROUND_Immune POISON | 0.068627451
GHOST NONE | 0.06372549
ICE ELECTRIC GROUND_Immune | 0.053921569
ICE ELECTRIC | 0.053921569
GRASS GROUND | 0.049019608
DARK FLYING | 0.039215686
FAIRY NORMAL | 0.034313725
FIGHTING NONE FIRE_Resist ICE_Resist | 0.019607843
DARK GROUND | 0.019607843
PSYCHIC FAIRY | 0.019607843
ROCK POISON | 0.004901961
FAIRY ICE | -0.009803922
FIRE POISON | -0.009803922
NORMAL GROUND | -0.019607843
FIGHTING NONE | -0.029411765
FIGHTING FLYING | -0.029411765
ROCK ICE | -0.039215686
ROCK ELECTRIC | -0.039215686
FLYING ICE | -0.049019608
ICE GHOST | -0.049019608
FIRE PSYCHIC | -0.049019608
ROCK FLYING | -0.058823529
WATER GRASS | -0.068627451
DARK ELECTRIC | -0.078431373
PSYCHIC POISON | -0.083333333
GHOST POISON | -0.088235294
GROUND_Immune GHOST POISON | -0.088235294
ICE BUG | -0.098039216
FIGHTING ICE | -0.098039216
ROCK GHOST | -0.112745098
WATER DARK | -0.12745098
FIGHTING FAIRY | -0.12745098
GROUND_Immune NONE POISON | -0.12745098
NONE POISON | -0.12745098
WATER FIGHTING | -0.137254902
NORMAL ELECTRIC | -0.147058824
WATER NORMAL | -0.171568627
FIGHTING BUG | -0.171568627
FLYING GHOST | -0.176470588
PSYCHIC NORMAL | -0.18627451
FIRE NORMAL | -0.196078431
FLYING DRAGON | -0.200980392
PSYCHIC GROUND_Immune GROUND | -0.205882353
FLYING NONE | -0.215686275
DARK NONE | -0.220588235
ICE NONE GROUND_Immune | -0.220588235
ICE NONE | -0.230392157
ROCK FIGHTING | -0.235294118
FIGHTING GROUND | -0.235294118
PSYCHIC GROUND | -0.240196078
WATER PSYCHIC | -0.240196078
ICE_Resist FIRE_Resist NORMAL NONE | -0.25
DARK NORMAL | -0.25
PSYCHIC ELECTRIC | -0.254901961
FLYING GRASS | -0.259803922
FIGHTING DRAGON | -0.259803922
NONE BUG | -0.264705882
NONE NORMAL | -0.274509804
FAIRY GRASS | -0.289215686
FAIRY DRAGON | -0.299019608
GROUND_Immune GHOST DRAGON | -0.299019608
DARK ICE | -0.299019608
ELECTRIC DRAGON | -0.308823529
GHOST GRASS | -0.323529412
GHOST BUG | -0.328431373
ICE POISON | -0.328431373
ICE NORMAL | -0.333333333
PSYCHIC NONE FIRE_Resist ICE_Resist | -0.333333333
GHOST DRAGON | -0.343137255
FLYING FAIRY | -0.343137255
PSYCHIC GROUND_Immune NONE | -0.348039216
DARK ROCK | -0.352941176
GRASS POISON | -0.357843137
FIGHTING NORMAL | -0.357843137
PSYCHIC NONE | -0.367647059
POISON DRAGON | -0.382352941
FLYING NORMAL | -0.382352941
NORMAL POISON | -0.387254902
ROCK NONE | -0.392156863
FLYING POISON | -0.421568627
FAIRY BUG | -0.426470588
DARK GROUND_Immune DRAGON | -0.431372549
GROUND_Immune GRASS ELECTRIC | -0.441176471
ROCK DRAGON | -0.441176471
FLYING BUG | -0.441176471
PSYCHIC ICE | -0.446078431
BUG NORMAL | -0.455882353
ROCK NORMAL | -0.460784314
GRASS ELECTRIC | -0.465686275
DARK DRAGON | -0.475490196
DARK BUG | -0.480392157
ROCK PSYCHIC GROUND_Immune | -0.485294118
ROCK PSYCHIC | -0.485294118
BUG POISON | -0.504901961
ICE DRAGON | -0.514705882
NONE DRAGON | -0.529411765
PSYCHIC BUG | -0.549019608
FLYING PSYCHIC | -0.568627451
ICE GRASS | -0.598039216
FIGHTING GRASS | -0.637254902
BUG DRAGON | -0.661764706
DARK GRASS | -0.725490196
NONE GRASS | -0.774509804
PSYCHIC GROUND_Immune DRAGON | -0.784313725
BUG GRASS | -0.808823529
PSYCHIC DRAGON | -0.823529412
GRASS DRAGON | -0.833333333
NORMAL DRAGON | -0.838235294
PSYCHIC GRASS | -0.857843137
GRASS NORMAL | -1.078431373

