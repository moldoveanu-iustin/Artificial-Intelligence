class CalculatorException(Exception):
    """Exceptie pentru erorile calculatorului"""
    pass

class Calculator(object):
    def read(self):
        '''read input from stdin'''
        return input('> ')

    def eval(self, string):
        '''Evaluates an infix arithmetic expression '''
        try:
            tokens = self._tokenize(string)
            postfix = self._infix_to_postfix(tokens)
            return self._evaluate_postfix(postfix)
        except Exception:
            raise CalculatorException("Invalid expression")

    def _tokenize(self, string):
        import re
        return re.findall(r'\d+\.?\d*|[+*/()-]', string)

    def _infix_to_postfix(self, tokens):
        precedenta = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operatori = []
        for token in tokens:
            if token.isdigit() or '.' in token:
                output.append(token)
            elif token in precedenta:
                while operatori and operatori[-1] != '(' and precedenta[operatori[-1]] >= precedenta[token]:
                    output.append(operatori.pop())
                operatori.append(token)
            elif token == '(':
                operatori.append(token)
            elif token == ')':
                while operatori and operatori[-1] != '(':
                    output.append(operatori.pop())
                operatori.pop()
        while operatori:
            output.append(operatori.pop())
        return output

    def _evaluate_postfix(self, tokens):
        stack = []
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif '.' in token:
                stack.append(float(token))
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    rezultat = a + b
                elif token == '-':
                    rezultat = a - b
                elif token == '*':
                    rezultat = a * b
                elif token == '/':
                    if b == 0:
                        raise CalculatorException("Impartire la 0!")
                    rezultat = a / b

                if isinstance(rezultat, float) and rezultat.is_integer():
                    rezultat = int(rezultat)

                stack.append(rezultat)

        rezultat = stack[0]
        return int(rezultat) if isinstance(rezultat, float) and rezultat.is_integer() else rezultat

    def loop(self):
        """Read a line of input, evaluate and print it
        repeat the above until the user types 'quit'."""
        while True:
            line = self.read()
            if line.lower() == 'quit':
                break
            try:
                rezultat = self.eval(line)
                print(int(rezultat) if isinstance(rezultat, float) and rezultat.is_integer() else rezultat)
            except CalculatorException as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    calc = Calculator()
    calc.loop()