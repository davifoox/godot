"""
Generates black-background / white-outline Godot launcher icons for all Android densities.
Run once: python generate_icons.py
"""

import skia
from PIL import Image
import io
import os

BASE = os.path.dirname(__file__)

# --------------------------------------------------------------------------
# SVG path data extracted from misc/dist/macos/GodotLG.icon/Assets/
# --------------------------------------------------------------------------

# Outer diamond/frame shape (layer_0)
FRAME_PATH = (
    "M104.743,673.152C104.728,673.152 104.714,673.152 104.699,673.152"
    "L104.699,427.387C86.329,404.634 66.493,375.457 48,346.429"
    "C71.531,306.384 100.337,270.598 131.144,237.443"
    "C159.724,251.825 187.468,268.117 213.68,285.455"
    "C226.801,272.417 241.599,261.753 256.089,250.605"
    "C270.35,239.154 286.397,230.758 301.665,220.976"
    "C297.116,187.188 294.872,153.925 293.973,119.208"
    "C333.289,99.419 375.223,86.299 417.615,76.875"
    "C434.573,105.334 450.05,136.154 463.528,166.283"
    "C479.525,163.611 495.581,162.62 511.698,162.429"
    "L511.698,162.404C511.798,162.404 511.902,162.429 512.002,162.429"
    "C512.098,162.429 512.202,162.404 512.314,162.404"
    "L512.314,162.429C528.403,162.62 544.47,163.611 560.463,166.283"
    "C573.95,136.154 589.435,105.334 606.368,76.875"
    "C648.781,86.299 690.711,99.419 730.031,119.208"
    "C729.128,153.925 726.884,187.188 722.347,220.976"
    "C737.586,230.758 753.654,239.154 767.911,250.605"
    "C782.422,261.753 797.195,272.417 810.311,285.455"
    "C836.523,268.117 864.276,251.825 892.848,237.443"
    "C923.655,270.598 952.477,306.384 976,346.429"
    "C960.608,371.216 940.518,400.678 919.301,427.387"
    "L919.301,653.521L919.239,653.542L919.239,673.14"
    "C919.24,673.148 919.241,673.152 919.241,673.152"
    "L919.449,705.662L919.39,705.672L919.502,705.661"
    "C919.435,720.23 919.24,736.115 919.24,739.349"
    "C919.24,882.434 737.792,951.209 512.278,952"
    "L511.724,952C286.211,951.209 104.7,882.434 104.7,739.349"
    "C104.7,736.173 104.513,720.222 104.45,705.661"
    "L104.497,705.665L104.701,673.16"
    "C104.715,673.16 104.729,673.158 104.743,673.152Z"
)

# Robot body — multiple sub-paths (body, eyes, nose, lower collar) from layer_1
ROBOT_PATH = (
    "M784.071,718.723L919.502,705.661"
    "C919.435,720.23 919.24,736.115 919.24,739.349"
    "C919.24,882.434 737.792,951.209 512.278,952"
    "L511.724,952C286.211,951.209 104.7,882.434 104.7,739.349"
    "C104.7,736.173 104.513,720.222 104.45,705.661"
    "L239.931,718.723L244.597,785.587"
    "C245.159,793.646 251.569,800.061 259.628,800.639"
    "L420.118,812.09C428.576,812.711 436.085,806.671 437.322,798.271"
    "L446.525,735.856L577.477,735.856L586.68,798.271"
    "C587.858,806.279 594.739,812.132 602.715,812.132"
    "C603.102,812.132 603.493,812.12 603.884,812.09"
    "L764.374,800.639C772.433,800.061 778.843,793.646 779.405,785.587"
    "L784.071,718.723Z"
    "M104.699,427.387C86.329,404.634 66.493,375.457 48,346.429"
    "C71.531,306.384 100.337,270.598 131.144,237.443"
    "C159.724,251.825 187.468,268.117 213.68,285.455"
    "C226.801,272.417 241.599,261.753 256.089,250.605"
    "C270.35,239.154 286.397,230.758 301.665,220.976"
    "C297.116,187.188 294.872,153.925 293.973,119.208"
    "C333.289,99.419 375.223,86.299 417.615,76.875"
    "C434.573,105.334 450.05,136.154 463.528,166.283"
    "C479.525,163.611 495.581,162.62 511.698,162.429"
    "L511.698,162.404C511.798,162.404 511.902,162.429 512.002,162.429"
    "C512.098,162.429 512.202,162.404 512.314,162.404"
    "L512.314,162.429C528.403,162.62 544.47,163.611 560.463,166.283"
    "C573.95,136.154 589.435,105.334 606.368,76.875"
    "C648.781,86.299 690.711,99.419 730.031,119.208"
    "C729.128,153.925 726.884,187.188 722.347,220.976"
    "C737.586,230.758 753.654,239.154 767.911,250.605"
    "C782.422,261.753 797.195,272.417 810.311,285.455"
    "C836.523,268.117 864.276,251.825 892.848,237.443"
    "C923.655,270.598 952.477,306.384 976,346.429"
    "C960.608,371.216 940.518,400.678 919.301,427.387"
    "L919.301,653.521L919.239,653.542L919.239,673.152"
    "C918.789,673.156 918.344,673.173 917.898,673.214"
    "L767.287,687.742C759.394,688.508 753.213,694.856 752.659,702.765"
    "L748.018,769.275L616.584,778.653L607.53,717.267"
    "C606.356,709.308 599.529,703.41 591.483,703.41"
    "L432.521,703.41C424.471,703.41 417.644,709.308 416.47,717.267"
    "L407.416,778.653L275.986,769.275L271.341,702.765"
    "C270.791,694.856 264.606,688.504 256.713,687.742"
    "L106.043,673.214C105.598,673.173 105.148,673.156 104.699,673.152"
    "L104.699,427.387Z"
    "M511.993,626.22C528.136,626.22 541.248,614.323 541.248,599.658"
    "L541.248,516.069C541.248,501.416 528.136,489.507 511.993,489.507"
    "C495.851,489.507 482.768,501.416 482.768,516.069"
    "L482.768,599.658C482.768,614.323 495.851,626.22 511.993,626.22Z"
    "M389.215,527.151C389.215,477.017 348.567,436.398 298.416,436.398"
    "C248.29,436.398 207.629,477.017 207.629,527.151"
    "C207.629,577.319 248.29,617.959 298.416,617.959"
    "C348.567,617.959 389.215,577.319 389.215,527.151Z"
    "M634.787,527.151C634.787,577.319 675.435,617.959 725.594,617.959"
    "C775.716,617.959 816.373,577.319 816.373,527.151"
    "C816.373,477.017 775.716,436.398 725.594,436.398"
    "C675.435,436.398 634.787,477.017 634.787,527.151Z"
)

STROKE_W = 14  # stroke-width in SVG units (canvas = 1024x1024)

COMMON_ATTRS = f'fill="none" stroke="#ffffff" stroke-width="{STROKE_W}" stroke-linejoin="round" stroke-linecap="round"'

def svg_foreground():
    """White outlines on transparent background — used as adaptive foreground/monochrome layer."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <path {COMMON_ATTRS} d="{FRAME_PATH}"/>
  <path {COMMON_ATTRS} d="{ROBOT_PATH}"/>
</svg>"""

def svg_background():
    """Solid black — used as adaptive background layer."""
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><rect width="1024" height="1024" fill="#000000"/></svg>'

def svg_legacy():
    """Black background + white outlines — used as the flat legacy icon."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <rect width="1024" height="1024" fill="#000000"/>
  <path {COMMON_ATTRS} d="{FRAME_PATH}"/>
  <path {COMMON_ATTRS} d="{ROBOT_PATH}"/>
</svg>"""

def svg_to_webp(svg_str: str, width: int, height: int) -> bytes:
    surface = skia.Surface(width, height)
    stream = skia.DynamicMemoryWStream()
    stream.write(svg_str.encode("utf-8"))
    svg_dom = skia.SVGDOM.MakeFromStream(skia.MemoryStream(svg_str.encode("utf-8")))

    with surface as canvas:
        canvas.clear(skia.ColorTRANSPARENT)
        if svg_dom:
            svg_dom.setContainerSize(skia.Size(width, height))
            svg_dom.render(canvas)

    image = surface.makeImageSnapshot()
    png_bytes = image.encodeToData().bytes()
    img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    buf = io.BytesIO()
    img.save(buf, format="WEBP", lossless=True, quality=100)
    return buf.getvalue()

def write(path: str, data: bytes):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    print(f"  wrote {os.path.relpath(path, BASE)}")

# density → (legacy_px, adaptive_px)
DENSITIES = {
    "mipmap-mdpi":    (48,  108),
    "mipmap-hdpi":    (72,  162),
    "mipmap-xhdpi":   (96,  216),
    "mipmap-xxhdpi":  (144, 324),
    "mipmap-xxxhdpi": (192, 432),
}
# mipmap (no suffix): legacy 192, adaptive 108
MIPMAP_PLAIN = (192, 108)

fg_svg  = svg_foreground()
bg_svg  = svg_background()
leg_svg = svg_legacy()

print("Generating icons...")

for density, (leg_px, adp_px) in DENSITIES.items():
    d = os.path.join(BASE, density)
    write(os.path.join(d, "icon.webp"),            svg_to_webp(leg_svg, leg_px, leg_px))
    write(os.path.join(d, "icon_background.webp"), svg_to_webp(bg_svg,  adp_px, adp_px))
    write(os.path.join(d, "icon_foreground.webp"), svg_to_webp(fg_svg,  adp_px, adp_px))
    write(os.path.join(d, "icon_monochrome.webp"), svg_to_webp(fg_svg,  adp_px, adp_px))

# mipmap plain
d = os.path.join(BASE, "mipmap")
write(os.path.join(d, "icon.webp"),            svg_to_webp(leg_svg, MIPMAP_PLAIN[0], MIPMAP_PLAIN[0]))
write(os.path.join(d, "icon_background.webp"), svg_to_webp(bg_svg,  MIPMAP_PLAIN[1], MIPMAP_PLAIN[1]))
write(os.path.join(d, "icon_foreground.webp"), svg_to_webp(fg_svg,  MIPMAP_PLAIN[1], MIPMAP_PLAIN[1]))
write(os.path.join(d, "icon_monochrome.webp"), svg_to_webp(fg_svg,  MIPMAP_PLAIN[1], MIPMAP_PLAIN[1]))

print("Done.")
