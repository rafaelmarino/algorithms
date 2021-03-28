# python3


class Bracket:
    def __init__(self, bracket_type, position):
        self.bracket_type = bracket_type
        self.position = position

    def match(self, c):
        if self.bracket_type == '[' and c == ']':
            return True
        if self.bracket_type == '{' and c == '}':
            return True
        if self.bracket_type == '(' and c == ')':
            return True
        return False


def main():
    stack = []  # stack to hold a Bracket object for each iteration

    for i, symbol in enumerate(text):
        if symbol == '(' or symbol == '[' or symbol == '{':
            a = Bracket(symbol, i)
            stack.append(a)
        # checking if closing brackets match
        if symbol == ')' or symbol == ']' or symbol == '}':
            if not stack:  # if the stack IS empty
                return i + 1  # return the position of the unmatching closing bracket
            top = stack.pop()  # key + position (OBI)

            if not top.match(symbol):
                return i + 1
        # checking if any bracket is unmatched
        # after the for loop the stack should be empty if the string is balanced
    return 'Success' if not stack else stack.pop().position + 1

if __name__ == "__main__":
    text = input()  # originally sys.stdin.read()
    print(main())
