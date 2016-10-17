# Authors: Julia Samol, Bartosz Przybylski
from datetime import datetime
import os
import sys
import re
import codecs

def generate_date_pattern():
    #separators which can be used in date
    separators = [r"-", r"\.", r"/"]
    #year_pattern accepts all years from 1000 to 2016 (yyyy)
    year_pattern = r"(1[0-9]{3}|20[01][0-6]|200[7-9])"
    date_pattern = r"\b("
    for separator in separators:
        #case: 31 days January, March, May, July, August, October, December
        date_pattern += ("(%s%s%s%s%s)|") % (r"([0-2][0-9]|3[01])", separator, r"(0[13578]|1[02])", separator, year_pattern)
        date_pattern += ("(%s%s%s%s%s)|") % (year_pattern, separator, r"([0-2][0-9]|3[01])", separator, r"(0[13578]|1[02])")
        #case: 30 days: April, June, September
        date_pattern += ("(%s%s%s%s%s)|") % (r"([0-2][0-9]|30)", separator, r"(0[469]|11)", separator, year_pattern)
        date_pattern += ("(%s%s%s%s%s)|") % (year_pattern, separator, r"([0-2][0-9]|30)", separator, r"(0[469]|11)")
        #case: 29 days: February
        date_pattern += ("(%s%s%s%s%s)|") % (r"([0-2][0-9])", separator, r"(02)", separator, year_pattern)
        date_pattern += ("(%s%s%s%s%s)|") % (year_pattern, separator, r"([0-2][0-9])", separator, r"(02)")

    #date_pattern must be returned without the last char (which is "|")
    return (date_pattern[:len(date_pattern) - 1] + r")\b")

#function for looking for specific metatag
def from_meta_regexp(_meta_name):
    return re.compile('<META NAME="' + _meta_name + '" CONTENT="(.+?)">')


def get_date_format(item):
    if re.match(r"[0-9]{2}-.", item):
        return "%d-%m-%Y"
    elif re.match(r"[0-9]{2}\..", item):
        return "%d.%m.%Y"
    elif re.match(r"[0-9]{2}/.", item):
        return "%d/%m/%Y"
    elif re.match(r"[0-9]{4}-.", item):
        return "%Y-%d-%m"
    elif re.match(r"[0-9]{4}\..", item):
        return "%Y.%d.%m"
    elif re.match(r"[0-9]{4}/.", item):
        return "%Y/%d/%m"

#function counts unique elements
def get_unique_data_number(_list, _type):
    unique_list = []
    if _type == "float":
        for item in _list:
            if float(item[0]) not in unique_list:
                unique_list.append(float(item[0]))
    elif _type == "date":
        for item in _list:
            _format = get_date_format(item[0])
            if datetime.strptime(item[0], _format) not in unique_list:
                unique_list.append(datetime.strptime(item[0], _format))
    else:
        for item in _list:
            if item[0] not in unique_list:
                unique_list.append(item[0])
    return len(unique_list)

# ---patterns used in program---
sentence_pattern = r"(\w|\s)*\w+(\.|(!|\?)+)"
shortcut_pattern = r"((^|(?<=\s)|<.+>)(([a-zA-Z]|[\u0104-\u017c]){1,3}\.)($|(?=\s)|<.+>))"
int_pattern = r"((\b|^)((-)?((?(2)([1-9]|3276[0-8])|([0-9]|3276[0-7]))|[1-9][0-9]{,4}|327[0-5][0-9]|32[0-6][0-9][0-9]|3[0-1][0-9][0-9][0-9]))\b)"
float_pattern = r"(-?([0-9]*\.[0-9]+[eE][+-][0-9]+|[0-9]*\.[0-9]+|[0-9]+\.[0-9]*))"
date_pattern = generate_date_pattern()
email_pattern = r"\b(\w+@\w+(\.\w+)*\.\w+)\b"
text_pattern = r'<P[\s\S]*<META NAME='
meta_text_pattern = r'^<META NAME.+$'
# ---end of patterns---

#processing single file
def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')
    content = fp.read()

    SOME_TEXT_TO_PROCESS = '\n'.join(re.compile(text_pattern, re.MULTILINE).findall(content))
    META_TEXT_TO_PROCESS = '\n'.join(re.compile(meta_text_pattern, re.MULTILINE).findall(content))

    fp.close()
    print("nazwa pliku:", filepath)
    print("autor:", ', '.join(from_meta_regexp('AUTOR').findall(META_TEXT_TO_PROCESS)))
    print("dzial:", ', '.join(from_meta_regexp('DZIAL').findall(META_TEXT_TO_PROCESS)))
    print("slowa kluczowe:", ', '.join(from_meta_regexp(r'KLUCZOWE_\d').findall(META_TEXT_TO_PROCESS)))
    print("liczba zdan:", len(re.findall(sentence_pattern, \
                                re.sub(date_pattern, "date", \
                                re.sub(email_pattern, "email", \
                                re.sub(float_pattern, "float", \
                                re.sub(shortcut_pattern, "shortcut", SOME_TEXT_TO_PROCESS, re.UNICODE)))), re.UNICODE)))
    print("liczba skrotow:", get_unique_data_number(re.findall(shortcut_pattern, SOME_TEXT_TO_PROCESS, re.UNICODE), "shortcut"))
    print("liczba liczb calkowitych z zakresu int:", get_unique_data_number(re.findall(int_pattern, SOME_TEXT_TO_PROCESS), "int"))
    print("liczba liczb zmiennoprzecinkowych:", get_unique_data_number(re.findall(float_pattern, SOME_TEXT_TO_PROCESS), "float"))
    print("liczba dat:", get_unique_data_number(re.findall(date_pattern, SOME_TEXT_TO_PROCESS), "date"))
    print("liczba adresow email:", get_unique_data_number(re.findall(email_pattern, SOME_TEXT_TO_PROCESS), "email"))
    print("\n")

#main from template
try:
    path = sys.argv[1]
except IndexError:
    print("Brak podanej nazwy katalogu")
    sys.exit(0)


tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)
