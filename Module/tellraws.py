


class Part:
    def __init__(self,txt,color = "white", bold = False, italic = False, underlined = False, strikethrough = False, obfuscated = False):
        self.txt = txt
        self.color = color
        self.bold = bold
        self.italic = italic
        self.underlined = underlined
        self.strikethrough = strikethrough
        self.obfuscated = obfuscated

    def get(self):
        return f'{{"text":"{self.txt}","bold":"{self.bold}","italic":"{self.italic}","strikethrough":"{self.strikethrough}","underlined":"{self.underlined}","obfuscated":"{self.obfuscated}","color":"{self.color}"}}'

class Tellraw:
    def __init__(self,player,*parts):
        self.player = player
        self.start = f'tellraw {self.player} ["",'
        self.end = ']'
        self.parts = parts
        self.cmd = self.generate()

    def generate(self):
        cmd = self.start
        for n,i in enumerate(self.parts):
            cmd += i.get()
            if n < len(self.parts) -1:
                cmd+=","
        cmd += self.end
        return cmd

    def __repr__(self):
        return f'{self.cmd}'