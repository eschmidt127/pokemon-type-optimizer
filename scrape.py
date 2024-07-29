'''scrapes each individual pokemons pokemondb page for info'''
import os
import re
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.headless = True
options.add_argument("--log-level=3")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))


def get_variation_data(panel, name, region_nums, region_dexnames):
    '''get data for one variation/tab in page of the pokemon'''
    number = 0
    type1 = "NONE"
    type2 = "NONE"
    tbstat = 0
    ability1 = ""
    ability2 = ""
    abilityh = ""
    xpath = ".//h2[text()='Pokédex data']/following::table[@class='vitals-table']"
    pokedex_data = panel.find_element(By.XPATH, xpath)
    for line in pokedex_data.text.splitlines():
        sline = line.split()
        # print(" ".join(sline))
        if "National" == sline[0]:
            number = sline[2]
        if "Type" == sline[0]:
            type1 = sline[1]
            if len(sline) == 3:
                type2 = sline[2]
        if "Abilities" == sline[0]:
            ability1 = " ".join(sline[2:])
        if "2." == sline[0]:
            ability2 = " ".join(sline[1:])
        if "ability)" == sline[-1]:
            abilityh = " ".join(sline[:-2])
    xpath = ".//h2[text()='Base stats']/following::table[@class='vitals-table']"
    base_stats = panel.find_element(By.XPATH, xpath)
    for line in base_stats.text.splitlines():
        sline = line.split()
        # print(" ".join(sline))
        if sline[0] == "Total":
            tbstat = int(sline[1])
    pokedata = f"{name},{int(number)},{type1},{type2},{tbstat},{ability1},{ability2},{abilityh}"
    print(pokedata)
    POKEDEX_FILE.write(pokedata+"\n")
    dexes = pokedex_data.text.split("Local № ", 1)[1].splitlines()
    dexes_regex = re.compile("(\\d+ \\()(.+)(\\))")
    for dex in dexes:
        match = re.match(dexes_regex, dex)
        if not match:
            sys.exit(f"\nERR: {dex} not able to be parsed into a region name")
        elif match.group(2) not in region_dexnames:
            sys.exit(f"\nERR: {match.group(2)} not recognized as a region name")
        else:
            region_nums[region_dexnames[match.group(2)]].add(int(number))


def get_pokemon_data(page, region_nums, region_dexnames):
    '''get data for one pokemon'''
    h1 = page.find_element(By.TAG_NAME, "h1")
    name = h1.text
    base_name = name
    pdata_header_xpath = "//h2[text()='Pokédex data']"
    if len(driver.find_elements(By.XPATH, pdata_header_xpath)) < 1:
        print(f"No pokemon found on page {page}")
    elif len(driver.find_elements(By.XPATH, pdata_header_xpath)) == 1:
        single_tab_xpath = (pdata_header_xpath +
                            "/ancestor-or-self::" +
                            "div[@class='tabset-basics sv-tabs-wrapper sv-tabs-onetab']")
        single_tab = page.find_element(By.XPATH, single_tab_xpath)
        get_variation_data(single_tab, name, region_nums, region_dexnames)
    else:
        active_tab_xpath = (pdata_header_xpath +
                            "/ancestor-or-self::" +
                            "div[@class='sv-tabs-panel active']")
        tab_select_xpath = (pdata_header_xpath +
                            "/ancestor-or-self::" +
                            "div[@class='tabset-basics sv-tabs-wrapper ']" +
                            "/div[@class='sv-tabs-tab-list']/a")
        for atab in page.find_elements(By.XPATH, tab_select_xpath):
            if base_name not in atab.text:
                name = base_name + " - " + atab.text
            else:
                name = atab.text
            atab.click()
            apanel = page.find_element(By.XPATH, active_tab_xpath)
            get_variation_data(apanel, name, region_nums, region_dexnames)


NEXT_BUTTON_XPATH = "//a[@class='entity-nav-next']"
REGION_NUMS = {"gen1_kanto": set(),
               "gen2_johto": set(),
               "gen3_hoenn": set(),
               "gen3_kanto": set(),
               "gen4_sinnoh": set(),
               "gen4_sinnoh2": set(),
               "gen4_johto": set(),
               "gen5_unova": set(),
               "gen5_unova2": set(),
               "gen6_kalos": set(),
               "gen6_hoenn": set(),
               "gen7_alola": set(),
               "gen7_alola2": set(),
               "gen7_kanto": set(),
               "gen8_galar": set(),
               "gen8_galar2": set(),
               "gen8_galar3": set(),
               "gen8_sinnoh": set(),
               "gen8_hisui": set(),
               "gen9_paldea": set(),
               "gen9_paldea2": set(),
               "gen9_paldea3": set(),
               }
REGION_DEXNAMES = {"Red/Blue/Yellow": "gen1_kanto",
                   "Yellow/Red/Blue": "gen1_kanto",
                   "Gold/Silver/Crystal": "gen2_johto",
                   "Crystal/Gold/Silver": "gen2_johto",
                   "Ruby/Sapphire/Emerald": "gen3_hoenn",
                   "FireRed/LeafGreen": "gen3_kanto",
                   "Diamond/Pearl": "gen4_sinnoh",
                   "Platinum": "gen4_sinnoh2",
                   "HeartGold/SoulSilver": "gen4_johto",
                   "Black/White": "gen5_unova",
                   "Black 2/White 2": "gen5_unova2",
                   "X/Y — Central Kalos": "gen6_kalos",
                   "X/Y — Coastal Kalos": "gen6_kalos",
                   "X/Y — Mountain Kalos": "gen6_kalos",
                   "Omega Ruby/Alpha Sapphire": "gen6_hoenn",
                   "Sun/Moon — Alola dex": "gen7_alola",
                   "U.Sun/U.Moon — Alola dex": "gen7_alola2",
                   "Let's Go Pikachu/Let's Go Eevee": "gen7_kanto",
                   "Sword/Shield": "gen8_galar",
                   "The Isle of Armor": "gen8_galar2",
                   "The Crown Tundra": "gen8_galar3",
                   "Brilliant Diamond/Shining Pearl": "gen8_sinnoh",
                   "Legends: Arceus": "gen8_hisui",
                   "Scarlet/Violet": "gen9_paldea",
                   "The Teal Mask": "gen9_paldea2",
                   "The Indigo Disk": "gen9_paldea3",
                   }
data_path = os.path.join(os.path.dirname(__file__), "data")
if not os.path.isdir(data_path):
    os.mkdir(data_path)
if os.path.isfile(os.path.join(data_path, "pokedex.csv")):
    iny = input("pokedex.csv already exists, do you really want to run again and replace data? " +
                "Be kind to pokemondb's bandwidth. Enter y to continue, anything else to exit:")
    if iny != 'y':
        exit()

POKEDEX_FILE = open(os.path.join(data_path, "pokedex.csv"), "w", encoding="utf-8")
driver.get("https://pokemondb.net/pokedex/bulbasaur")
while len(driver.find_elements(By.XPATH, NEXT_BUTTON_XPATH)) > 0:
    get_pokemon_data(driver, REGION_NUMS, REGION_DEXNAMES)
    driver.find_element(By.XPATH, NEXT_BUTTON_XPATH).click()
# when new things are happening, pages may be missing the next button to get to the latest.
missing_poke_addresses = []
for address in missing_poke_addresses:
    driver.get(address)
    get_pokemon_data(driver, REGION_NUMS, REGION_DEXNAMES)
POKEDEX_FILE.close()
for dexname, dexnums in REGION_NUMS.items():
    nums_file = open(os.path.join(data_path, dexname + "_national_dex_numbers.txt"),
                     "w", encoding="utf-8")
    for poke_number in dexnums:
        nums_file.write(str(poke_number)+"\n")
    nums_file.close()
    print(f"{len(dexnums)} pokemon in pokedex for {dexname}")

driver.quit()
