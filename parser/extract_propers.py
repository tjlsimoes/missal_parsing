from collections import defaultdict
from bs4 import BeautifulSoup
import json

def recursive_defaultdict():
  return defaultdict(recursive_defaultdict)

def defaultdict_to_dict(d):
  if isinstance(d, defaultdict):
    # Convert the defaultdict itself to a dict
    d = dict(d)
    # Recursively apply this conversion
    for key, value in d.items():
      d[key] = defaultdict_to_dict(value)
  return d

def extract_sections(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

    was_h3 = False
    current_mass = ''

    masses_raw_text = {}
    for element in soup.body.find_all():
      if element.get_text() == '\xa0': # Matches a " " chr [code 160])
        continue                       # no-break space

      if element.name == 'h3':
        if was_h3 == False:
          current_mass = ''
        was_h3 = True
        current_mass += ' ' + element.get_text()
      elif element.name == 'p':
        if was_h3 == True:
          current_mass = current_mass.strip().replace('\n', ' ')
          # print(repr(current_mass))
          masses_raw_text[current_mass] = []
        if current_mass != '':
          masses_raw_text[current_mass].append(element.get_text())
          # if len(masses_raw_text[current_mass]) == 1 :
            # print(repr(masses_raw_text[current_mass]))
        was_h3 = False
  
  return masses_raw_text


def get_mass_by_sections(mass_raw_text, sections):
  mass_by_section = {}
  current_section = ''
  for text in mass_raw_text:
    text = text.replace('\n', ' ')
    is_section_title = False
    for section in sections:
      if section in text:
        is_section_title = True
        current_section = text
        mass_by_section[current_section] = []
    if not is_section_title and current_section != '':
      mass_by_section[current_section].append(text)

  return mass_by_section


def create_json_mass_propers(propers_idxs, mass_by_section):

  propers = {}

  sections = list(mass_by_section.keys())

  propers_present = []    # Not used?
  for idx in propers_idxs:
    data_from_title = sections[idx].split(' - ')
    name = data_from_title[0].title()
    reference = ' - '.join(data_from_title[1:])

    if reference == '':
      reference = None

    section_content = mass_by_section[sections[idx]]
    proper_data = {}
    proper_type = None

    if 'Entrada' in name:
      proper_type = 'entrance'
    
    if 'Colecta' in name:
      proper_type = 'collect'

    if 'Oblatas' in name:
      proper_type = 'offerings'

    if 'Antífona' in name and 'Comunhão' in name:
      proper_type = 'communion'
    # Why not 'Antífona Da Comunhão' in name?
    # in operator is case-sensitive.
    # title('hello to my world') #=> 'Hello To My World'
      
    if 'Depois' in name:
      proper_type = 'post_communion'
    
    proper_data['reference'] = reference
    proper_data['text'] = section_content[0]

    if proper_type != None:
      propers[proper_type] = proper_data
    else:
      print('Proper type not recognized')

  return propers


possible_sections = [
    "ANTÍFONA DE ENTRADA",
    "ORAÇÃO COLECTA",
    "ORAÇÃO SOBRE AS OBLATAS",
    "ANTÍFONA DA COMUNHÃO",
    "ORAÇÃO DEPOIS DA COMUNHÃO",
    "LEITURA I ",
    "SALMO RESPONSORIAL",
    "ALELUIA",
    "LEITURA II",
    "EVANGELHO"
]

weekdays = ["1", "1","1","1", "2", "3", "4", "5", "6", "7"]
cycles = ["A", "B", "C"]

advent_propers = defaultdict(recursive_defaultdict)

# Weeks 1-3
# Sundays included!

file_paths = [
  '../_old/AdvSem01.htm',
  '../_old/AdvSem02.htm',
  '../_old/AdvSem03.htm'
]

for i, file_path in enumerate(file_paths):
  masses_raw_text = extract_sections(file_path)
  # print(f'{i}, {file_path}')
  for i, key in enumerate(list(masses_raw_text.keys())[0:]):
    # Why is this [0:] necessary?
    # print(f'{i}, {key}')
    if i in [1, 2, 3]:
      # print('Does not go through.')
      continue
    # What i is exactly being refered to here?
    # idx that would match the different cycle sunday readings'
    #   pages?
  
    mass_by_section = get_mass_by_sections(masses_raw_text[key], possible_sections)
    sections = list(mass_by_section.keys())

    keywords = ["EVANGELHO", "LEITURA", "ALELUIA", "SALMO"]
    propers_idxs = [i for i, element in enumerate(sections) if not any(word in element for word in keywords)]
    # Seemingly: every section index that is not a reading.
    # To what extent wouldn't this step be avoidable with a refactoring
    #   possible_sections list to only include propers' sections?

    propers = create_json_mass_propers(propers_idxs, mass_by_section)

    advent_propers[f'week-{file_path[-6:-4]}'][weekdays[i]] = propers


# print(repr(advent_propers.keys()))
# print(repr(advent_propers['week-01'].keys()))
# print(repr(advent_propers['week-01']['1']))
    


# Week 4 (Sundays' propers)

file_paths = [
  '../_old/AdvSem04.htm'
]

for i, file_path in enumerate(file_paths):
  masses_raw_text = extract_sections(file_path)
  for i, key in enumerate(list(masses_raw_text.keys())[:1]): # Up to index 1.
    # if i in [1, 2, 3]:
    #   continue
    # Conditional flow unneccessary, right?
    mass_by_section = get_mass_by_sections(masses_raw_text[key], possible_sections)
    sections = list(mass_by_section.keys())

    keywords = ['EVANGELHO', 'LEITURA', 'ALELUIA', 'SALMO']
    propers_idxs = [i for i, element in enumerate(sections) if not any(word in element for word in keywords)]

    propers = create_json_mass_propers(propers_idxs, mass_by_section)

    advent_propers[f'week-{file_path[-6:-4]}'][weekdays[i]] = propers



# print(repr(advent_propers.keys()))

# print('advent_propers[\'week-03\'].keys()')
# print(repr(advent_propers['week-03'].keys()))

# print('advent_propers[\'week-04\'].keys()')
# print(repr(advent_propers['week-04'].keys()))

# print('advent_propers[\'week-04\'][\'1\']')
# print(repr(advent_propers['week-04']['1']))


# Week 4 (Specific days)

season = 'advent'
month = 'december'

file_paths = [
  '../_old/AdvSem04.htm'
]

days = [str(i) for i in range(17, 25)]

for i, file_path in enumerate(file_paths):
  masses_raw_text = extract_sections(file_path)
  for i, key in enumerate(list(masses_raw_text.keys())[4:]):
    mass_by_section = get_mass_by_sections(masses_raw_text[key], possible_sections)
    sections = list(mass_by_section.keys())

    keywords = ['EVANGELHO', 'LEITURA', 'ALELUIA', 'SALMO']
    propers_idxs = [i for i, element in enumerate(sections) if not any(word in element for word in keywords)]

    propers = create_json_mass_propers(propers_idxs, mass_by_section)

    advent_propers[month][days[i]] = propers


# print(repr(advent_propers.keys()))
# print(repr(advent_propers['december'].keys()))
# print(repr(advent_propers['december']['17']))

file_path = '../_new/pt/advent.json'

# Open the file and load its content as a Pyhton dictionary
with open(file_path, 'r', encoding='utf-8') as file:
  advent_readings = json.load(file)['readings']

advent_readings = defaultdict_to_dict(advent_readings)
advent = {
  'propers': advent_propers,
  'readings': advent_readings
}

output_file_path = f'../_new/pt/advent.json'
with open(output_file_path, 'w', encoding='utf-8') as file:
  json.dump(advent, file, ensure_ascii=False, indent = 4)
