# A generator function means the entire file doesn't need read into memory for analysis
# In initial tests, using generators simplifies the code, reduces memory usage, and eliminates threading without impacting runtimes.
def find_attributes(file_path):
    with open(file_path, 'r', encoding='utf-16-le') as handle:
        ineffective_anchor=0
        for indx, line in enumerate(handle):
            # Clean the line of non UTF-8 characters for comparison using a comprehension
            clean_line=''.join(x for x in line if ord(x) < 128)
            
            # We don't need to read the file several times to find the desired attributes.
            # Given that GPO Reports are computer generated and follow an HTML format,
            # GPO Reports should have GPO elements in a certain order.
            # Each individual GPO should follow the following order:
            #   1. Opening HTML Tag
            #   2. Title Tags (The Name of the GPO)
            #   3. GPO Status
            #   4. GPO Ineffective (If True, the GPO is ineffective)
            #   5. Closing HTML Tag (Closing #1)
            
            # Lines that don't need futher analysis by going through the other elifs
            if clean_line == '' or clean_line.startswith("<!--") or clean_line.endswith("-->\n") or clean_line.startswith("<script ") or clean_line.endswith("</script>\n"):
                pass
            # 1 & 5
            elif (clean_line.startswith("<html ")) or (clean_line.endswith("</html>\n")):
                yield indx
            # 2
            elif ((clean_line.startswith("<title>")) and ("</title>" in clean_line)):
                yield ''.join(x for x in line[7:-9] if x.isalnum() or x==" " or x=="-" or x=="_")
            # 3a
            elif ("<tr><td scope=\"row\">GPO Status</td><td>Enabled</td></tr>" in clean_line):
                yield "enabled"
            # 3b
            elif ("<tr><td scope=\"row\">GPO Status</td><td>All settings disabled</td></tr>" in clean_line):
                yield "disabled"
            # 3c
            elif ("<tr><td scope=\"row\">GPO Status</td><td>User settings disabled</td></tr>" in clean_line):
                yield "computer"
            # 3d
            elif ("<tr><td scope=\"row\">GPO Status</td><td>Computer settings disabled</td></tr>" in clean_line):
                yield "user"
            # 4a
            elif ("<b>The settings in this GPO can only apply to the following groups, users, and computers:</b>" in clean_line):
                ineffective_anchor=indx
            # 4b
            elif ((indx > ineffective_anchor) and (indx < ineffective_anchor + 4)):
                # In all the examples I've seen, the value associated with this tag is always two lines after.
                # However, I decided to use a line range of four in case some variability is introduced.
                # 4ba
                if (("<table" in clean_line) and ("</table>" in clean_line) and ("None" in clean_line)):
                    yield True
                # 4bb
                elif (("<table" in clean_line) and ("</table>" in clean_line)):
                    yield False