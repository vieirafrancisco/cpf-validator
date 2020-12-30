def format(cpf):
    return ''.join(filter(lambda x: x.isdigit(), cpf))

def dot(v1, v2):
    return sum(map(lambda x: int(x[0])*int(x[1]), zip(v1,v2)))

def validate(cpf):
    string = format(str(cpf))
    if len(string) != 11:
        return False
    validators = string[-2:]
    rule_one = 11 - (dot(string[:-2][::-1], range(2,11)) % 11)
    if rule_one != int(validators[0]):
        return False
    rule_two = 11 - (dot(string[:-1][::-1], range(2,12)) % 11)
    if rule_two != int(validators[1]):
        return False
    return True
