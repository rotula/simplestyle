"""
A parser for simplified CSS
"""

class CSSError(Exception): pass

class CSSUnexpectedEOFError(CSSError): pass

class CSSMissingSemicolonError(CSSError): pass

class CSSMissingColonError(CSSError): pass

class CSSIllegalCharacterError(CSSError): pass

class CSSEmptyDocumentError(CSSError): pass

class EOF(Exception): pass

class SimpleCSSParser(object):

    """
    CSS parser (simplified)

    Simplified CSS-Grammar:

    css := declaration (";" declaration)* ';'?
    declaration := property ":" expr
    property := [a-zA-Z -]+
    expr := (string | [^;"']+)
    string := string1 | string2
    string1 := "'" [^'\n\r\f] "'"
    string2 := '"' [^"\n\r\f] '"'
    """

    css = ""  # the CSS to parse
    declarations = None  # the list of declarations parsed
    pos = 0  # pointer into CSS (for scanning)
    maxpos = 0  # utmost pointer position
    eof = False

    def __init__(self, css):
        """Initialize with CSS string"""
        if len(css.strip()) == 0:
            raise CSSEmptyDocumentError("No CSS content given.")
        self.css = css
        self.declarations = []
        self.maxpos = len(self.css) - 1

    def parse(self):
        """Parse CSS and fill list of declarations"""
        try:
            self.parse_declaration()
            while 1:
                try:
                    self.skip_whites()
                except EOF:
                    break
                if self.get_next() != ";":
                    raise CSSMissingSemicolonError(
                            "Expected ';' at pos {}".format(self.pos))
                try:
                    self.parse_declaration()
                except EOF:
                    break
        except EOF:
            raise CSSUnexpectedEOFError()
        return self.declarations

    def parse_declaration(self):
        self.skip_whites()
        prop = self.parse_property()
        self.skip_whites()
        if self.get_next() != ":":
            raise CSSMissingColonError(
                    "Expected ':' at pos {}".format(self.pos))
        self.skip_whites()
        expr = self.parse_expr()
        self.declarations.append((prop, expr))

    def parse_expr(self):
        ret = ""
        end_space_count = 0
        try:
            while 1:
                c = self.get_next()
                if c == "'":
                    ret += self.parse_string1()
                    # self.skip_whites()
                    end_space_count = 0
                elif c == "\"":
                    ret += self.parse_string2()
                    end_space_count = 0
                elif c == ";":
                    self.push_back()
                    break
                elif c.isspace():
                    if end_space_count:
                        continue
                    else:
                        ret += " "
                        end_space_count = 1
                    # return ret
                else:
                    ret += c
                    end_space_count = 0
        except EOF:
            if ret == "":
                raise CSSUnexpectedEOFError("Unexpected end of file")
        if end_space_count:
            if ret[-1].isspace():
                ret = ret[0:-1]
        return ret

    def parse_string1(self):
        ret = ""
        try:
            c = self.get_next()
            while c != "'":
                ret += c
                c = self.get_next()
        except EOF:
            raise CSSUnexpectedEOFError("Unexpected end of file")
        return ret

    def parse_string2(self):
        ret = ""
        try:
            c = self.get_next()
            while c != "\"":
                ret += c
                c = self.get_next()
        except EOF:
            raise CSSUnexpectedEOFError("Unexpected end of file")
        return ret


    def parse_property(self):
        ret = ""
        try:
            c = self.get_next()
            while self.is_nmchar(c):
                ret += c
                c = self.get_next()
        except EOF:
            raise CSSUnexpectedEOFError("Unexpected end of file")
        if c == ":":
            self.push_back()
            return ret
        if c.isspace():
            return ret
        raise CSSIllegalCharacterError(u"Illegal character '{}' at pos {}."\
                .format(c, self.pos))

    def is_nmchar(self, c):
        if c >= "a" and c <= "z":
            return True
        if c >= "A" and c <= "Z":
            return True
        if c == "-":
            return True
        return False

    def get_next(self):
        """Get next token"""
        if self.pos > self.maxpos:
            raise EOF()
        c = self.css[self.pos]
        self.pos += 1
        return c

    def push_back(self):
        """Set scanner one step back"""
        if self.pos == 0:
            raise CSSError("Called pushback on pos 0.")
        self.pos -= 1

    def skip_whites(self):
        """Advance pointer until the first non whitespace character"""
        while self.get_next().isspace():
            pass
        self.push_back()

