import re


class Lexer:
    """ Analisador Léxico
    """
    def __init__(self):
        with open('input.txt', 'r') as source:
            source_code = source.read()
            self.code = repr(source_code).strip("'")
    
    @classmethod
    def patterns(self):
        rules = {
            'MAIN': r'main',                      # main
            'PRINT': r'print',                    # printf
            'SCAN': r'scan',                      # scanf
            'VOID': r'void',                      # void
            'INT': r'int',                        # int
            'FLOAT': r'float',                    # float
            'IF': r'if',                          # if
            'ELSE': r'else',                      # else
            'LBRACKET': r'\(',                    # (
            'RBRACKET': r'\)',                    # )
            'LBRACE': r'\{',                      # {
            'RBRACE': r'\}',                      # }
            'COMMA': r',',                        # ,
            'SEMCOL': r';',                       # ;
            'EQ': r'==',                          # ==
            'NE': r'!=',                          # !=
            'LE': r'<=',                          # <=
            'GE': r'>=',                          # >=
            'OR': r'\|\|',                        # ||
            'AND': r'&&',                         # &&
            'ATTR': r'\=',                        # =
            'LT': r'\<',                          # <
            'GT': r'\>',                          # >
            'PLUS': r'\+',                        # +
            'MINUS': r'-',                        # -
            'MULT': r'\*',                        # *
            'DIV': r'\/',                         # /
            'PERCENT': r'%',                      # %
            'ID': r'[a-zA-Z]\w*',                 # IDENTIFIERS
            'INTEGER_CONST': r'\d\d*',            # INT
            'FLOAT_CONST': r'\d\d*\.\d\d*',       # FLOAT
            'STRING': r'\"[^"]*\"',               # STRING
            'NEWLINE': r'\\n',                    # NEW LINE
            'MISMATCH': r'.'                      # ANOTHER CHARACTER
        }
        return rules

    @classmethod
    def split_symbols(self, text):
        symbols_list = { 
            '(',
            ')',
            '{',
            '}',
            ',',
            ';',
            '|',
            '&',
            '=',
            '!',
            '<',
            '>',
            '+',
            '-',
            '*',
            '/',
            '%'
        }

        new_text = ''
        temp = ' '

        for index, l in enumerate(text):
            if l == ' ':
                new_text += temp + ' '
                temp = ' '

            elif l in symbols_list:
                if (
                    index+1 < len(text) and
                    ((l == '=' or l == '<' or l == '>' or l == '!') and text[index+1] == '=') or
                    (l == '&' and text[index+1] == '&') or 
                    (l == '|' and text[index+1] == '|')
                ):
                    new_text += temp + ' ' + l + text[index+1] + ' '

                elif (
                    ((text[index-1] == '=' or text[index-1] == '<' or text[index-1] == '>' or text[index-1] == '!') and l == '=') or
                    (text[index-1] == '&' and l == '&') or
                    (text[index-1] == '|' and l == '|') 
                ):
                    pass

                else:
                    new_text += temp + ' ' + l + ' '
                    
                temp = ' '

            elif (
                not (index+1 < len(text) and l == '\\' and text[index+1] == 'n') and
                not (l == '"') and
                re.match(r'\W', l)
            ):
                new_text += temp + ' ' + l + ' '
                temp = ' '

            else:
                temp += l

        if temp:
            new_text += temp

        return new_text

    @property
    def lexems(self):
        code = self.split_symbols(self.code)
        return code.split()

    @property
    def tokens(self):
        tokens_found = []

        for lexem in self.lexems:
            for token, pattern in self.patterns().items():
                if re.fullmatch(pattern, lexem):
                    tokens_found.append(token)
                    break
        
        return tokens_found

    def tokenize(self):  
        message = 'Ocorreu um erro ao realizar a análise léxica'

        try:
            symbols_table = list(zip(self.tokens, self.lexems))

            if 'MISMATCH' in self.tokens:
                mismatch_token_index = self.tokens.index('MISMATCH')
                mismatch_lexem = self.lexems[mismatch_token_index]
                line_num = self.tokens[:mismatch_token_index].count('NEWLINE')
                message = f'{mismatch_lexem} inesperado na linha {line_num+1}'
                raise RuntimeError

        except BaseException as e:
            print(message)
            exit()

        return symbols_table


if __name__ == '__main__':
    lexicalAnalyzer = Lexer()
    symbols_table = lexicalAnalyzer.tokenize()
    print(symbols_table)
