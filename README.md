# Pokemon Type Optimizer
This program will identify an optimal team of 6 pokemon based solely on type matchups. Each unique type combination that may be faced by the team is considered a single matchup. The primary metric that is used to measure the team is the number of matchups that have "safe super effective stabs". If a pokemon in the team of six has a super effective move that has same type attack bonus and the opposing pokemon does not have the same, this is a "safe super effective stab" .

Considerations:
- Double / x4 weaknesses are not differentiated from x2 weaknesses in the assessments. For this reason by default these pokemon are not considered for inclusion in the team. If you accept that your "safe super effectvie stab" may not be all that safe because they could have a coverage move that is x4 effective (more than your likely x3 with STAB considered), you can override this and include those pokemon anyway.
- Abilities that effect type effectiveness are accounted for by default if they are not hidden abilities. Hidden ability assessment can be enabled.
- Mega evolutions are not included in assesments by default. If this is overriden, they are accounted for as if they are separate pokemon. 
- Terastallization is not accounted for.
- In order to make runtime of the program reasonable, only the top 50 pokemon types are assessed as part of the team by default.
- non-STAB moves are not accounted for, nor is move power.


## Requirements
Python 3.12 with standard libraries

If you would like to re-run the web scraper used to collect pokemon data (there should really not be a reason to do this unless you forked and made changes), you will need the selenium and webdriver manager python packages as well as chrome.

## Usage
```bash
python main.py [-h] [--stat_exclude [STAT_EXCLUDE]] [--rank_types_exclude [RANK_TYPES_EXCLUDE]] [--rank_types] [input_dex]
```
- STAT_EXCLUDE: pokemon with total base stats less than this number will be considered as matchups, but not considered for inclusion in the team. Default: 450
- RANK_TYPES_EXCLUDE: The top this many pokemon based on how many good matchups they have will be considered with inclusion in the team. Default: 50
- --rank_types: If used, shows the ranking of types that will be used for RANK_TYPES_EXCLUDE without calculating teams.
- input_dex: The pokedex used. This will align with the name of the datafile in the datafolder, or national to include the entire pokedex. Default: national

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
