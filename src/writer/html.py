HEADER="""
<html>
<body>
"""

FOOTER="""
</body>
</html>
"""


def write(writer, blocks):
    writer.write(HEADER)
    for block in blocks:
        if block.is_header():
            level = block.header_level
            title = block.header_title
            writer.write("<h%s>%s</h%s>\n" % (level, title, level))
        elif block.is_text():
            writer.write("<p>")
            writer.write(block.text)
            writer.write("</p>")
        elif block.is_quote():
            writer.write("<pre>")
            for line in block.lines:
                writer.write(line)
            writer.write("</pre>")


    writer.write(FOOTER)
