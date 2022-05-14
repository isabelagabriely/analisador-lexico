class Lexer:
    """ Analisador Léxico
    """

    def __init__(self):
        with open('input.txt', 'r') as source:
            source_code = source.read()
            self.code = repr(source_code).strip("'")
        
        self.rules = self.__txt_to_dict('patterns/rules.txt')
        self.unit_symbols = self.__txt_to_dict('patterns/unit_symbols.txt')
        self.lexems = []
        self.tokens = []

    def __txt_to_dict(self, file: str):
        with open(file, 'r') as f:
            dic = {}
            for line in f.readlines():
                pattern, token = line.split()
                dic[pattern] = token
        return dic

    def __split_into_lexems(self):
        input_string = self.code
        char = input_string[0]
        lexem = ''
        next_index = 1

        while next_index <= len(input_string):
            while (
                next_index < len(input_string) and 
                char != ' ' and 
                char not in self.unit_symbols.keys()
            ):
                lexem += char
                char = input_string[next_index]
                next_index += 1

            if char in self.unit_symbols.keys():
                if lexem != '':
                    next_index -= 1
                else:
                    lexem = char

            if lexem != '':
                self.lexems.append(lexem)
            
            if next_index < len(input_string):
                char = input_string[next_index]
            
            next_index += 1
            lexem = ''
                

if __name__ == '__main__':
    x = Lexer()
    print(x._Lexer__split_into_lexems())
    print(x.lexems)
