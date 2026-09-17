import json
import re
from pathlib import Path
def web_color_value(value):
    """Convert Android #AARRGGBB token colors to CSS #RRGGBBAA."""
    if isinstance(value, str) and re.fullmatch(r"#[0-9A-Fa-f]{8}", value):
        return f"#{value[3:]}{value[1:3]}".upper()
    return value

def generate_platforms():
    root_dir = Path(__file__).resolve().parent.parent
    tokens_file = root_dir / "tokens" / "tokens.json"
    
    if not tokens_file.exists():
        print("tokens.json not found!")
        return

    with open(tokens_file, "r", encoding="utf-8") as f:
        tokens = json.load(f)

    web_dir = root_dir / "platforms" / "web"
    ios_dir = root_dir / "platforms" / "ios"
    android_dir = root_dir / "platforms" / "android"

    web_dir.mkdir(parents=True, exist_ok=True)
    ios_dir.mkdir(parents=True, exist_ok=True)
    android_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate Web CSS Colors
    for theme_name, theme_data in tokens.get("themes", {}).items():
        css_lines = [f"/* Theme: {theme_name} */", f":root[data-theme='{theme_name}'] {{"]
        for name, value in theme_data.get("colors", {}).items():
            css_lines.append(f"  --xnet-{name}: {web_color_value(value)};")
        css_lines.append("}\n")
        (web_dir / f"xnet-theme.{theme_name}.css").write_text("\n".join(css_lines), encoding="utf-8")

    # 2. Generate Web CSS Dimensions
    css_dim_lines = ["/* Xnet Base Dimensions */", ":root {"]
    for comp_name, comp_data in tokens.get("components", {}).get("drawable-dimensions", {}).items():
        for prop, val in comp_data.items():
            css_val = str(val).replace("dp", "px").replace("sp", "px")
            css_dim_lines.append(f"  --xnet-{comp_name}-{prop}: {css_val};")
            
    for layout_name, layout_data in tokens.get("components", {}).get("layout-dimensions", {}).items():
        for view_id, view_data in layout_data.items():
            for prop, val in view_data.items():
                css_val = str(val).replace("dp", "px").replace("sp", "px")
                css_dim_lines.append(f"  --xnet-layout-{layout_name}-{view_id}-{prop}: {css_val};")
                
    for font_name, font_data in tokens.get("base", {}).get("typography", {}).get("metadata", {}).items():
        for weight, weight_data in font_data.items():
            css_dim_lines.append(f"  --xnet-font-{font_name}-{weight}: {weight};")
            
    css_dim_lines.append("}\n")
    (web_dir / "xnet-dimensions.css").write_text("\n".join(css_dim_lines), encoding="utf-8")

    # 3. Generate iOS Swift Dimensions
    swift_dim_lines = ["import SwiftUI", "", "public struct XnetDimensions {"]
    for comp_name, comp_data in tokens.get("components", {}).get("drawable-dimensions", {}).items():
        for prop, val in comp_data.items():
            swift_val = str(val).replace("dp", "").replace("sp", "")
            cam_name = re.sub(r"-([a-z0-9])", lambda m: m.group(1).upper(), f"{comp_name}-{prop}")
            swift_dim_lines.append(f"    public static let {cam_name}: CGFloat = {swift_val}")
            
    for layout_name, layout_data in tokens.get("components", {}).get("layout-dimensions", {}).items():
        for view_id, view_data in layout_data.items():
            for prop, val in view_data.items():
                swift_val = str(val).replace("dp", "").replace("sp", "")
                if "match_parent" in swift_val or "wrap_content" in swift_val or "?" in swift_val:
                    continue
                cam_name = re.sub(r"-([a-z0-9])", lambda m: m.group(1).upper(), f"layout-{layout_name}-{view_id}-{prop}")
                cam_name = cam_name.replace("_", "")
                swift_dim_lines.append(f"    public static let {cam_name}: CGFloat = {swift_val}")
                
    swift_dim_lines.append("}\n")
    (ios_dir / "XnetDimensions.swift").write_text("\n".join(swift_dim_lines), encoding="utf-8")

    # 4. Generate iOS Swift Typography
    swift_font_lines = ["import SwiftUI", "", "public struct XnetTypography {"]
    for font_name, font_data in tokens.get("base", {}).get("typography", {}).get("metadata", {}).items():
        for weight, weight_data in font_data.items():
            swift_font_lines.append(f"    public static let {font_name}Weight{weight} = Font.Weight.init({weight})")
    swift_font_lines.append("}\n")
    (ios_dir / "XnetTypography.swift").write_text("\n".join(swift_font_lines), encoding="utf-8")

    # 5. Generate iOS Swift Colors
    for theme_name, theme_data in tokens.get("themes", {}).items():
        struct_name = "Xnet" + "".join(word.capitalize() for word in theme_name.split("-")) + "Colors"
        swift_lines = ["import SwiftUI", "", f"public struct {struct_name} {{"]
        for name, value in theme_data.get("colors", {}).items():
            cam_name = re.sub(r"-([a-z0-9])", lambda m: m.group(1).upper(), name)
            swift_lines.append(f'    public static let {cam_name} = Color(hex: "{value}")')
        swift_lines.append("}\n")
        (ios_dir / f"{struct_name}.swift").write_text("\n".join(swift_lines), encoding="utf-8")

    # 6. Generate Android XML Colors
    for theme_name, theme_data in tokens.get("themes", {}).items():
        xml_name = theme_name.replace("-", "_")
        xml_lines = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>"]
        for name, value in theme_data.get("colors", {}).items():
            color_name = f"xnet_color_{xml_name}_{name.replace('-', '_')}"
            xml_lines.append(f'    <color name="{color_name}">{value}</color>')
        xml_lines.append("</resources>\n")
        (android_dir / f"colors_{xml_name}.xml").write_text("\n".join(xml_lines), encoding="utf-8")

    # 7. Generate Android XML Dimensions
    android_dim_lines = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>"]
    
    def process_val(dim_name, val):
        s_val = str(val).strip()
        if s_val in ["match_parent", "wrap_content"] or "?" in s_val:
            return
            
        if s_val.endswith("dp") or s_val.endswith("sp") or s_val.endswith("px"):
            android_dim_lines.append(f'    <dimen name="{dim_name}">{s_val}</dimen>')
        elif s_val.startswith("#") or s_val.startswith("rgba"):
            android_dim_lines.append(f'    <string name="{dim_name}">{s_val}</string>')
        elif s_val.isalpha():
            android_dim_lines.append(f'    <string name="{dim_name}">{s_val}</string>')
        elif s_val.isdigit() or (s_val.startswith("-") and s_val[1:].isdigit()):
            android_dim_lines.append(f'    <integer name="{dim_name}">{s_val}</integer>')
        else:
            try:
                float(s_val)
                if "alpha" in dim_name.lower() or "weight" in dim_name.lower():
                    android_dim_lines.append(f'    <item name="{dim_name}" type="dimen" format="float">{s_val}</item>')
                else:
                    android_dim_lines.append(f'    <dimen name="{dim_name}">{s_val}dp</dimen>')
            except ValueError:
                android_dim_lines.append(f'    <string name="{dim_name}">{s_val}</string>')

    for comp_name, comp_data in tokens.get("components", {}).get("drawable-dimensions", {}).items():
        for prop, val in comp_data.items():
            dim_name = f"xnet_{comp_name}_{prop}".replace("-", "_")
            process_val(dim_name, val)
            
    for layout_name, layout_data in tokens.get("components", {}).get("layout-dimensions", {}).items():
        for view_id, view_data in layout_data.items():
            for prop, val in view_data.items():
                dim_name = f"xnet_layout_{layout_name}_{view_id}_{prop}".replace("-", "_")
                process_val(dim_name, val)
                
    android_dim_lines.append("</resources>\n")
    (android_dir / "dimens.xml").write_text("\n".join(android_dim_lines), encoding="utf-8")
    
    print("Successfully generated all platforms from tokens.json")

if __name__ == '__main__':
    generate_platforms()

