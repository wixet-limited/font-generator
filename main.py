import fontforge
import os
import subprocess

print("@################@")
print("@ FONT GENERATOR @")
print("@################@")

# Env vars to control some behaviour
FONT_NAME = os.environ.get("FONT_NAME", "foo")
SRC_DIR = os.environ.get("SRC_DIR", "/src")
UNI_START = os.environ.get("FONT_START", 0xf000)
NEGATE = bool(os.environ.get("NEGATE", 0))
SVG_DIR = "/svg"

# Imagemagick probably accepts more but these are the most common
accepted_extensions = ["png", "jpeg", "jpg"]

# create an empty font with the provided name
font = fontforge.font()
font.familyname = FONT_NAME
font.fullname = FONT_NAME
font.fontname = FONT_NAME

# Information to generate the final CSS for the icons
css_icons = []
css_index = UNI_START

# Add the glyph to the font from an svg
def add_glyph(svg_file_path, uni_index):
    filename = svg_file_path.split("/")[-1].lower()
    print("Adding", filename)
    glyph = font.createChar(uni_index)
    glyph.importOutlines(svg_file_path)
    return ".icon-{name}:before{{content:'\{uni_val}';}}".format(name=filename.split(".")[0], uni_val=hex(uni_index)[2:])

# Scan for any image
for i in os.listdir(SRC_DIR):
    name, extension = i.split(".", 1)
    if extension.lower() in accepted_extensions:
        svg_path = os.path.join(SVG_DIR,name + ".svg")
        bitmap_path = "/tmp/" + name + ".ppm"
        print("Procesing", i);
        params = [os.path.join(SRC_DIR, i), '-alpha', 'remove', bitmap_path]
        if NEGATE:
            params = ['-negate'] + params
        
        subprocess.call(['convert'] + params)
        subprocess.call(['potrace', '--svg', '-o', svg_path, bitmap_path])
        css_icons.append(add_glyph(svg_path, css_index))
        css_index += 1
        
    elif i.lower().endswith(".svg"):
        css_icons.append(add_glyph(os.path.join(SRC_DIR, i), css_index))
        css_index += 1
    else:
        print("Ignoring", name)
        
    

font.generate(os.path.join(SRC_DIR, FONT_NAME + '.ttf'))
print("Created", FONT_NAME + '.ttf')

font.generate(os.path.join(SRC_DIR, FONT_NAME + '.eot'))
print("Created", FONT_NAME + '.eot')

font.generate(os.path.join(SRC_DIR, FONT_NAME + '.woff'))
print("Created", FONT_NAME + '.woff')

font.generate(os.path.join(SRC_DIR, FONT_NAME + '.svg'))
print("Created", FONT_NAME + '.svg')


template = """@font-face {{
  font-family: '{fontname}';
  src: url('/assets/fonts/{fontname}.eot');
  src: url('/assets/fonts/{fontname}.eot?#iefix') format('embedded-opentype'),
       url('/assets/fonts/{fontname}.woff') format('woff'),
       url('/assets/fonts{fontname}.ttf') format('truetype'),
       url('/assets/fonts/{fontname}.svg#/{fontname}') format('svg');
  font-weight: normal;
  font-style: normal;
}}
[class*='icon-']:before{{
display: inline-block;
 font-family: '{fontname}';
 font-style: normal;
 font-weight: normal;
 line-height: 1;
 -webkit-font-smoothing: antialiased;
 -moz-osx-font-smoothing: grayscale
}}
"""


css_content = template.format(fontname=FONT_NAME) + "\n".join(css_icons) + "\n"

with open(os.path.join(SRC_DIR, FONT_NAME + '.css'), 'w') as f:
    f.write(css_content)
    print("Created", FONT_NAME + '.css')

