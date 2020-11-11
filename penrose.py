import math, cmath, cairo, random, re

# User input
try: divisions = int(input("Enter the desired number of tiling layers/subdivisions (ex. '7'): "))
except ValueError:
    msg = ["Why did you think that is a valid number of divisions?", "Helpful Suggestion: try an integer"]
    print("\n" + random.choice(msg))
    raise SystemExit(0)

try: zoom = input("\nWould you like the image zoomed in our out (ex. 'in'): ")
except ValueError:
    print("\nI don't know how you manged to mess this one up...")
    raise SystemExit(0)

try: scale = {
        "in": 1,
        "out": 2
    } [zoom]
except KeyError:
    print("\nThe only valid options are 'in' and 'out'")
    raise SystemExit(0)

try: r1, r2 = [int(r) for r in tuple(input("\nEnter the desired image resolution, separated by a space (ex: '1080 1080'): ").split())]
except ValueError:
    print("\nI get that this one is a bit trickier; the format should be: ['integer' 'integer']")
    raise SystemExit(0)

try: c1, c2, c3 = tuple(input("\nEnter the desired colors, separated by spaces (ex: 'red blue grey'): ").split())
except ValueError:
    msg = ["The format should be: ['color' 'color' 'color']", "Really? You got the last one formatted right."]
    print("\n" + random.choice(msg))
    raise SystemExit(0)

try: filename = input("\nEnter the desired filename to output the image to (ex. 'example.png') (don't accidentally overwrite anything...): ")
except ValueError:
    print("\nInvalid input on the very last one? Back to the top!")
    raise SystemExit(0)
if re.compile('\.png$').search(filename) is None:
    print("\nYou've got to include the .png at the end!")
    raise SystemExit(0)

colors = []
for c in c1, c2, c3:
    try: colors.append({
        "random": [random.randint(0, 256) / 256, random.randint(0, 256) / 256, random.randint(0, 256) / 256],
        "red": [0.8, 0.3, 0.3],
        "orange": [0.9, 0.6, 0.3],
        "yellow": [0.6, 0.9, 0.3],
        "green": [0.3, 0.9, 0.6],
        "blue": [0.3, 0.6, 0.9],
        "purple": [0.8, 0.3, 0.6],
        "grey": [0.2, 0.2, 0.2],
        "brown": [0.6, 0.3, 0.1],
        "black": [0, 0, 0],
        "white": [1, 1, 1]
    } [c])
    except KeyError:
        color = [int(x, 16) / 256 for x in re.compile('[0-9a-fA-F]{2}').findall(c)]
        
        if len(color) != 3:
            print("\nColor not supported")
            raise SystemExit(0)
        
        colors.append(color)

base = 5 # Eventuall, more bases will be supported (meaning instead of based on five, based on 7 or something)
            
# Canvas setup
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, r1, r2)
ctx = cairo.Context(surface)
ctx.scale(max(r1,r2) / scale, max(r1,r2) / scale)
ctx.translate(0.5 * scale, 0.5 * scale) # Center the drawing

# Create first layer of triangles
triangles = []
for i in range(base * 2):
    v2 = cmath.rect(1, (2*i - 1) * math.pi / (base * 2))
    v3 = cmath.rect(1, (2*i + 1) * math.pi / (base * 2))
    
    if i % 2 == 0:
        v2, v3 = v3, v2  # Mirror every other triangle
    
    triangles.append(("thin", 0, v2, v3))

phi = (5 ** 0.5 + 1) / 2 # Golden ratio

for i in range(divisions):
    new_triangles = []

    for shape, v1, v2, v3 in triangles:
        if shape == "thin":
            # Divide thin rhombus
            p1 = v1 + (v2 - v1) / phi
            p4 = 
            new_triangles += [("thin", v3, p1, v2), ("thicc", p1, v3, v1)]
        else:
            # Divide thicc rhombus
            p2 = v2 + (v1 - v2) / phi
            p3 = v2 + (v3 - v2) / phi
            new_triangles += [("thicc", p3, v3, v1), ("thicc", p2, p3, v2), ("thin", p3, p2, v1)]
        
        triangles = new_triangles

# Draw thin rhombi
for shape, v1, v2, v3 in triangles:
    if shape == "thin":
        ctx.move_to(v1.real, v1.imag)
        ctx.line_to(v2.real, v2.imag)
        ctx.line_to(v3.real, v3.imag)
        ctx.close_path()
ctx.set_source_rgb(colors[0][0], colors[0][1], colors[0][2])
ctx.fill()    

# Draw thicc rhombi
for shape, v1, v2, v3 in triangles:
    if shape == "thicc":
        ctx.move_to(v1.real, v1.imag)
        ctx.line_to(v2.real, v2.imag)
        ctx.line_to(v3.real, v3.imag)
        ctx.close_path()
ctx.set_source_rgb(colors[1][0], colors[1][1], colors[1][2])
ctx.fill()

# Determine line width
shape, v1, v2, v3 = triangles[0]
ctx.set_line_width(abs(v2 - v1) / (base * 2))
ctx.set_line_join(cairo.LINE_JOIN_ROUND)

# Draw outlines
for shape, v1, v2, v3 in triangles:
    ctx.move_to(v2.real, v2.imag)
    ctx.line_to(v1.real, v1.imag)
    ctx.line_to(v3.real, v3.imag)

ctx.set_source_rgb(colors[2][0], colors[2][1], colors[2][2]) 
ctx.set_line_width(divisions ** -3) if divisions > 3 else ctx.set_line_width(divisions ** -5)
ctx.stroke()

surface.write_to_png(filename)