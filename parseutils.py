import re


gSimplifySpaces = re.compile("  +")
def simplifySpaces(line):
    line = gSimplifySpaces.subn(" ", line)[0]
    line = line.strip()
    return line


gPropertyRe=re.compile("-p *([^ =]+)(?:=(\d+))?")
def parseTaskLine(line):
    """Parse line of form:
    some text -p property1 -p property2=12 some other text
    returns a tuple of ("some text some other text", {property1: None, property2:12})"""
    def fixPropertyValue(value):
        if value != '':
            return int(value)
        else:
            return None

    matches = gPropertyRe.findall(line)
    matches = [(x, fixPropertyValue(y)) for x,y in matches]
    propertyDict = dict(matches)

    line = gPropertyRe.subn("", line)[0]
    line = simplifySpaces(line)
    return line, propertyDict


def createTaskLine(title, propertyDict):
    tokens = []
    for propertyName, value in propertyDict.items():
        tokens.append("-p")
        if value:
            tokens.append(propertyName + "=" + str(value))
        else:
            tokens.append(propertyName)
    tokens.append(title)
    return " ".join(tokens)


def extractYagtdField(line, field):
    textParts = []
    regExp = re.compile(field + "([^ ]+)")
    lst = regExp.findall(line)
    if len(lst) == 1:
        field = lst[0]
    elif len(lst) == 0:
        field = None
    else:
        raise Exception("Multiple '%s' fields found" % field)

    line = regExp.subn("", line)[0]
    line = simplifySpaces(line)
    return line, field
# vi: ts=4 sw=4 et