# TODO: check if no tabs
import os
import sys
import re
import codecs

#pattern generators
def generate_date_pattern():
    separators = ["-", ".", "/"]
    #year_pattern accepts all years from 1 to 2016
    year_pattern = "([1-9][0-9]{,2}|1[0-9]{,3}|20(0|1)[0-6])"
    date_pattern = r"("
    #probably can be done more compressed
    for separator in separators:
        #case: January, March, May, July, August, October, December
        date_pattern += ("(%s%s%s%s%s)|") % ("([0-2][0-9]|3(0|1))", separator, "(0[13578]|1(0|2))", separator, year_pattern)
        #case: April, June, September
        date_pattern += ("(%s%s%s%s%s)|") % ("([0-2][0-9]|30)", separator, "(0[469]|11)", separator, year_pattern)
        #case: February
        date_pattern += ("(%s%s%s%s%s)|") % ("[0-2][0-9]", separator, "02", separator, year_pattern)

    #date_pattern must be returned without the last char (which is "|")
    return (date_pattern[:len(date_pattern) - 1] + ")")


#patterns
sentence_pattern = r"([^.!?]+\s?)*(\w|\))+(\.|(!|\?)+)"
shortcut_pattern = r"\b[a-zA-Z]{1,3}\."
int_pattern = r"(^|(?<=\s))(-)?(?(2)([1-9]|[1-9][0-9]{,3}|3276[0-8]|327[0-5][0-9]|32[0-6][0-9][0-9]|3[0-1][0-9][0-9][0-9])|([0-9]|[1-9][0-9]{,3}|3276[0-7]|327[0-5][0-9]|32[0-6][0-9][0-9]|3[0-1][0-9][0-9][0-9]))($|(?=\s))"
float_pattern = r"(^|(?<=\s))-?([0-9])*(\.(?(2)[0-9]*|[0-9]+)|(\.)?(?(4)[0-9]+)e[+-][0-9]+)($|(?=\s))"
date_pattern = generate_date_pattern()
email_pattern = r"\b\w+@\w+(\.\w+)*\.\w+\b" # TODO: (optional) non-alfanumeric signs before an '@'

def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()

    # TODO: process file, SOME_TEXT_TO_PROCESS

    fp.close()
    print("nazwa pliku:", filepath)
    print("autor:")
    print("dzial:")
    print("slowa kluczowe:")
    print("liczba zdan:", len(re.findall(sentence_pattern, re.sub(date_pattern, "date", re.sub(email_pattern, "email", re.sub(float_pattern, "float", re.sub(shortcut_pattern, "shortcut", to_process)))))))
    print("liczba skrotow:", len(re.findall(shortcut_pattern, SOME_TEXT_TO_PROCESS)))
    print("liczba liczb calkowitych z zakresu int:", len(re.findall(int_pattern, SOME_TEXT_TO_PROCESS)))
    print("liczba liczb zmiennoprzecinkowych:", len(re.findall(float_pattern, SOME_TEXT_TO_PROCESS))
    print("liczba dat:", len(re.findall(date_pattern, SOME_TEXT_TO_PROCESS)))
    print("liczba adresow email:", len(re.findall(email_pattern, SOME_TEXT_TO_PROCESS)))
    print("\n")



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
