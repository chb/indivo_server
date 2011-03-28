"""
Link Expansion in Messages

this is an extension to the markdown parser
"""

import markdown, re


REGEXP = "\{([a-zA-Z\_]+)\}"

class LinkExpanderPreprocessor(markdown.preprocessors.Preprocessor):
    def __init__(self, variables):
        self.variables = variables

    def process_string(self, s):
        new_s = s

        # match the regexp
        while True:
            m = re.search(REGEXP, new_s)
            if not m:
                break
            new_s = "%s%s%s" % (new_s[:m.span()[0]], self.variables.get(m.group(1),""), new_s[m.span()[1]:])
        return new_s

    def run(self, lines):
        new_lines = []
        for line in lines:
            new_lines.append(self.process_string(line))
        return new_lines
            

class MessageLinkExpanderExtension(markdown.Extension):
    def __init__(self, variables):
        self.variables = variables

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('linkexpander', LinkExpanderPreprocessor(self.variables), '_begin') 
