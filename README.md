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

National dex (With Mega evolutions)
```text
195 195 160 135 193 463
        Clodsire - Water Absorb type score:93   ajusted base stats:385  POISON GROUND
                Ability effect: WATER Immune
        Mega Houndoom   type score:46   ajusted base stats:510  DARK FIRE
                Alternate choices of same type with lower stats: Houndoom - Flash Fire(410) Incineroar(450) Houndoom(410) Chi-Yu(490)
        Mega Mewtwo X   type score:77   ajusted base stats:626  PSYCHIC FIGHTING
                Alternate choices of same type with lower stats: Gallade(453) Mega Gallade(553) Mega Medicham(430)
        Mega Skarmory   type score:138  ajusted base stats:525  STEEL FLYING
                Alternate choices of same type with lower stats: Skarmory(425) Celesteela(469) Corviknight(442)
        Ogerpon - Cornerstone Mask      type score:29   ajusted base stats:490  GRASS ROCK
                Alternate choices of same type with lower stats: Cradily(414)
        Tapu Fini       type score:80   ajusted base stats:495  WATER FAIRY
                Alternate choices of same type with lower stats: Primarina(456)
  neutral matchup against: ELECTRIC GROUND_Immune NONE
```
National dex (Without Mega evolutions)
```text
192 192 157 132 190 451
        Celesteela      type score:129  ajusted base stats:469  STEEL FLYING
                Alternate choices of same type with lower stats: Corviknight(442) Skarmory(425)
        Chi-Yu  type score:44   ajusted base stats:490  DARK FIRE
                Alternate choices of same type with lower stats: Houndoom(410) Incineroar(450) Houndoom - Flash Fire(410)
        Clodsire - Water Absorb type score:93   ajusted base stats:385  POISON GROUND
                Ability effect: WATER Immune
        Gallade type score:78   ajusted base stats:453  PSYCHIC FIGHTING
        Ogerpon - Cornerstone Mask      type score:29   ajusted base stats:490  GRASS ROCK
                Alternate choices of same type with lower stats: Cradily(414)
        Tapu Fini       type score:78   ajusted base stats:495  WATER FAIRY
                Alternate choices of same type with lower stats: Primarina(456)
  neutral matchup against: ELECTRIC GROUND_Immune NONE
```
Paldea Dex (with no DLC)
```text
127 127 102 87 124 336
        Chi-Yu  type score:38   ajusted base stats:490  DARK FIRE
                Alternate choices of same type with lower stats: Houndoom - Flash Fire(410) Houndoom(410)
        Clodsire - Water Absorb type score:72   ajusted base stats:385  POISON GROUND
                Ability effect: WATER Immune
        Froslass        type score:9    ajusted base stats:400  ICE GHOST
        Scovillain      type score:44   ajusted base stats:378  GRASS FIRE
        Tinkaton        type score:88   ajusted base stats:436  FAIRY STEEL
                Alternate choices of same type with lower stats: Klefki(390)
        Wash Rotom - Levitate   type score:85   ajusted base stats:455  ELECTRIC WATER
                Ability effect: GROUND Immune
  only defensive advantage against: NONE NORMAL
  neutral matchup against: ELECTRIC GROUND_Immune NONE
```
Paldea Dex (with all DLC)
```text
161 161 131 108 159 372
        Chi-Yu  type score:17   ajusted base stats:490  DARK FIRE
                Alternate choices of same type with lower stats: Incineroar(450) Houndoom(410) Houndoom - Flash Fire(410)
        Clodsire - Water Absorb type score:94   ajusted base stats:385  POISON GROUND
                Ability effect: WATER Immune
        Corviknight     type score:110  ajusted base stats:442  FLYING STEEL
                Alternate choices of same type with lower stats: Skarmory(425)
        Gallade type score:63   ajusted base stats:453  PSYCHIC FIGHTING
        Ogerpon - Cornerstone Mask      type score:26   ajusted base stats:490  GRASS ROCK
        Primarina       type score:62   ajusted base stats:456  WATER FAIRY
  neutral matchup against: ELECTRIC GROUND_Immune NONE
```
Legends Z-A Dex (No DLC)
```text
79 79 65 57 77 131
        Heliolisk       type score:-7   ajusted base stats:426  ELECTRIC NORMAL
        Hippowdon       type score:44   ajusted base stats:457  GROUND NONE
        Mega Froslass   type score:2    ajusted base stats:500  ICE GHOST
                Alternate choices of same type with lower stats: Froslass(400)
        Mega Houndoom   type score:-2   ajusted base stats:510  DARK FIRE
                Alternate choices of same type with lower stats: Houndoom(410)
        Mega Mawile     type score:77   ajusted base stats:425  STEEL FAIRY
                Alternate choices of same type with lower stats: Klefki(390)
        Mega Mewtwo X   type score:17   ajusted base stats:626  PSYCHIC FIGHTING
                Alternate choices of same type with lower stats: Mega Medicham(430) Mega Gallade(553) Gallade(453)
```
Legends Z-A Dex (with DLC)
```text
108 108 90 70 105 173
        Krookodile      type score:10   ajusted base stats:454  GROUND DARK
        Mega Altaria    type score:-4   ajusted base stats:480  DRAGON FAIRY
        Mega Hawlucha   type score:-5   ajusted base stats:526  FIGHTING FLYING
                Alternate choices of same type with lower stats: Mega Staraptor(525) Flamigo(425) Hawlucha(426)
        Mega Scovillain type score:19   ajusted base stats:448  GRASS FIRE
                Alternate choices of same type with lower stats: Scovillain(378)
        Mega Steelix    type score:82   ajusted base stats:555  STEEL GROUND
                Alternate choices of same type with lower stats: Steelix(455) Excadrill(458) Mega Excadrill(543)
        Wash Rotom      type score:71   ajusted base stats:455  ELECTRIC WATER
  neutral matchup against: ELECTRIC FLYINGG
```
Hypothetical dex (all possible type combinations, abilities included only for pokemon that do already exist)
```text
209 209 174 149 207 524
        DARK FIRE       type score:52   ajusted base stats:375  DARK FIRE
        FIGHTING PSYCHIC        type score:79   ajusted base stats:375  FIGHTING PSYCHIC
        GRASS ROCK      type score:43   ajusted base stats:375  GRASS ROCK
        POISON GROUND ability: WATER_Immune     type score:108  ajusted base stats:375  POISON GROUND
                Ability effect: WATER Immune
        STEEL FLYING    type score:145  ajusted base stats:375  STEEL FLYING
        WATER FAIRY     type score:97   ajusted base stats:375  WATER FAIRY
  neutral matchup against: ELECTRIC GROUND_Immune NONE
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
