from collections import defaultdict
from bs4 import BeautifulSoup
import re

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

# I understand that defaultdict requires a function as paramenter
# it is not to raise an error, as is peculiar of the workings
# of a default dictionary as opposed to a simple dicitionary.
# What I don't understand is the need for the recursive
# default dictionary.


# Would there be a difference between declaring utf-8
# enconding on the opening of the file and declaring it
# when BeautifulSoup is called?



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
  

#################################################################
######### Annotations for extract_sessions(file_path) ###########
#################################################################

# extract_sections(file_path) seems to be doing the following:
# Taking in a path to a file.
# In the case of the advent files, it is taking a file containing
# the propers for each day of one entire week of the advent.

# It is opening the file and setting it up for parsing with Beautiful
# Soup.

# It is initializing three variables: 
#   was_h3 = False; 
#   current_mass = ''
#   masses_raw_text = {}
          
# It is going over each element in soup.body.find_all(),
# and checking that element with two conditional flows.
          
# 1 - Checking if element's text is a non-break space

# 2.1 - Checking if element.name == 'h3'
#  if was_h3 == False, set current_mass = ''
#  Effectively reset current_mass variable
#  set was_h3 = True
#  set current_mass += ' ' + element.get_text()
# 2.1 - If element is not a space and h3
#  if was_h3 == False, a "new mass day" is commencing
#     so current_mass ought to be reset
#  set was_h3 == True, indicating that future elements
#     are from the same mass day
#  add a space and the element's text to current_mass var

# 2.2 - Checking if element.name == 'p'
# if was_h3 == True, 
#    remove leading and trailing characters
#      from current_mass and replace new line characters with
#      simple spaces, ' '
#    set current_mass as key within masses_raw_text hash (?)
#       for an array (list (?))
# if current_mass != ''
#     append (add to end) element's text to 
#       masses_raw_text[current_mass]
#     reset was_h3 back to False
# 2.2 - If element is not a space and p
#  if was_h3 == True, indicating nearest p
#                     to initial h3.
#  Meaning: current_mass will hold ' ' + h3 text contents,
#           e.g. ' I Semana do Advento Domingo'
#          == '' + ' ' + 'I Semana do Advento' 
#                + ' ' + 'Domingo'
#     set key for day's mass
#  if current_mass != ''
#     add element's text to array of mass day
#  Note: considering that the first element is the
#        nearest p element after the initial h3 elements.
#        That is why, for instance, the first element for
#        masses_raw_text['I Semana do Advento Domingo'] is
#        'ANTÝFONA DE ENTRADA - Salmo\n24, 1-3' and not
#        something like 'I Semana do Advento'. 
#         
#  reset was_h3 back to false

# return masses_raw_text, a dictionary (?) with each mass
# day as a key and an array of its' respective text content
# as a list (?), set as a value to that key. 


# Output considerations:
# Note that sunday will have one initial page with propers
# and three other pages, depending on the liturgical cycle
# (A, B, C) with the respective readings.

# print(repr(extract_sections("./_old/AdvSem01.htm")['I Semana do Advento Domingo']))


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

#################################################################
# Annotations for get_mass_by_sections(mass_raw_text, sections) #
#################################################################

# Taking in soup for one mass and possible sections

# Initiate mass_by_section to empty dictionary (?)
# Initiate current_section to ''
# For each element of mass_raw_text, meaning each element
#   composing the "daily mass" prayers and titles list (?)
#   Replace new line breaks with spaces
#   Initiate var is_section_title to False
#   For each section in sections list (see possible sections list)
#     Check if section is in, matches element of "daily mass' list"
#       is_section_title set to True
#       current_section set to element of "daily mass' list"
#       Set current_section as a key to mass_by_section dictionary
#         with a empty list as its initial value
#   If is_section_title == False && current_section not empty
#     Append element of "daily mass' list" to 
#       mass_by_section[current_section]
# Return mass_by_section dictionary with keys defined by section

# Output test:

possible_sections = [
    "ANTÍFONA DE ENTRADA",
    "ORAÇÃO COLECTA",
    "ANTÍFONA DA COMUNHÃO",
    "ORAÇÃO SOBRE AS OBLATAS",
    "ORAÇÃO DEPOIS DA COMUNHÃO",
    "LEITURA I ",
    "SALMO RESPONSORIAL",
    "ALELUIA",
    "LEITURA II",
    "EVANGELHO"
]

masses_raw_text = extract_sections("_old/AdvSem01.htm")

masses_raw_text_init_key = list(masses_raw_text.keys())[1:][0]

mass_raw_text = masses_raw_text[masses_raw_text_init_key]

print(repr(get_mass_by_sections(mass_raw_text, possible_sections).keys()))
print(repr(get_mass_by_sections(mass_raw_text, possible_sections)['EVANGELHO - Mt 24, 37-44']))


def create_json_mass_readings(reading_idxs, mass_by_section):

  readings = {}

  sections = list(mass_by_section.keys()) 
  # Couldn't this also be passed in as an argument?

  readings_present = []
  for idx in reading_idxs:

    data_from_title = sections[idx].split(' - ')
    name = data_from_title[0].title() # Correct words' casing
    if name.split(' ')[0] == 'Leitura':
      name = name.split(' ')[0].title() + ' ' + name.split(' ')[1].upper() 
      # Couldn't this be done more efficiently?
    reference = ' - '.join(data_from_title[1:])
    # In case data_from_title contains more than one ' - ' substring?

    if reference == '':
      reference = None

    section_content = mass_by_section[sections[idx]]

    reading_data = {}
    reading_type = None

    if 'Leitura' in name:
      reading_type = 'reading-' + name.split(' ')[-1]
      if reading_type in readings_present:
        readings_present.append('alt-' + reading_type)
        reading_type = f"alt-{reading_type}--{reading_type.count('alt-' + reading_type) + 1}"
        # Shouldn't it be ....{reading_present.count('alt-' + reading_type)}....
        # Will this count also readings signalled as, e.g., alt-reading I-1 ?
      else:
        readings_present.append(reading_type)
      reading_data["reference"] = reference
      base_idx = 0
      if section_content[0][0] == '«':
        reading_data['snippet'] = section_content[base_idx]
      else:
        base_idx = -1   # What is the need of this base_idx being set to -1?
      reading_data["announcement"] = section_content[base_idx + 1]
      reading_data['text'] = re.sub(r'(Palavra do Senhor\.)$', '', section_content[base_idx + 2])
      # Why the parenthesis surrounding Palavra do Senhor\. ?
      # ChatGPT:
      # The purpose of the parentheses in the regular expression is to create a capturing group. In this specific case, it captures the entire string "Palavra do Senhor." at the end of the input string ($ asserts the position at the end of the string). This capturing group is not used in the replacement (since the replacement is an empty string), but it could be used if you wanted to refer to the captured text in the replacement string or elsewhere in your code.

      # How does section_content[0 + 2] // section_content[-1 + 2] target p{Palavra do Senhor.} ?
      # It doesn't. It pressuposes, 'Palavra do Senhor.' is included in the text section.
      # Is this a logic that is most of the times applicable? For Terça, Quarta, Quinta Primeira
      # Semana do Advento it is not applicable.

    if 'Evangelho' in name:
      reading_type = 'gospel'
      reading_data['reference'] = reference
      if section_content[0][0] == '«':
        reading_data['snippet'] = section_content[base_idx]
      else:
        base_idx = -1
        # Is there a need for this conditional new assignemnt of base_idx?
      reading_data['snippet'] = section_content[0]
      reading_data['announcement'] = section_content[1]
      reading_data['text'] = re.sub(r"(Palavra da salvação\.)$", "", section_content[2])
      # Again is this substitution required? For Primeira Semana Advento Domingo Ano A 
      # e Quinta-Feira it was not.

    
    if reading_type != None:
      readings[reading_type] = reading_data
    else:
      print('Reading type not recognized')

  return readings
    







####################################################
####################################################
# Scripts for Parsing Files to JSON

possible_sections = [
    "ANTÍFONA DE ENTRADA",
    "ORAÇÃO COLECTA",
    "ANTÍFONA DA COMUNHÃO",
    "ORAÇÃO SOBRE AS OBLATAS",
    "ORAÇÃO DEPOIS DA COMUNHÃO",
    "LEITURA I ",
    "SALMO RESPONSORIAL",
    "ALELUIA",
    "LEITURA II",
    "EVANGELHO"
]

# Creating advent dictionary
advent_readings = defaultdict(recursive_defaultdict)

# # Weeks 1-3
file_paths = [
    "../_old/AdvSem01.htm",
    "../_old/AdvSem02.htm",
    "../_old/AdvSem03.htm",
]

weekdays = ["1", "1", "1", "2", "3", "4", "5", "6", "7"]
cycles = ["A", "B", "C"]


# for i, file_path in enumerate(file_paths):
#   masses_raw_text = extract_sections(file_path)

#   for i, key in enumerate(list(masses_raw_text.keys())[1:]):
#     # [1:] == Exclusion of first key in masses_raw_text as the 
#     #   first key refers to the first sunday section with its
#     #   propers.
#     mass_by_section = get_mass_by_sections(masses_raw_text[key], possible_sections)
#     sections = list(mass_by_section.keys())

#     keywords = ["EVANGELHO", "LEITURA", "ALELUIA", "SALMO"]
#     reading_idxs = [i for i, element in enumerate(sections) if any(word in element for word in keywords)]
#     # CHATGPT: reading_idxs will contain the indices of elements in the sections list where any of the keywords are found.
#     # Is a dictionary an **ordered** collection of key-value pairs, as opposed to a unorderd collection of key-value pairs?

#     readings = create_json_mass_readings(reading_idxs, mass_by_section)