import re

class CssParser:
    def __init__(self):
        self.styles = {}
        self.kivy_filename = 'style.kv'
        self.color_names = {
            'red': '255, 0, 0',
            'green': '0, 255, 0',
            'blue': '0, 0, 255',
            'black': '0, 0, 0',
            'white': '255, 255, 255',
            'yellow': '255, 255, 0',
            'cyan': '0, 255, 255',
            'magenta': '255, 0, 255',
        }

    def set_kivy_filename(self, filename):
        self.kivy_filename = filename

    def parse_file(self, css_filename):
        try:
            with open(css_filename, 'r') as file:
                css_content = file.read()
            print("Successfully read content from", css_filename)
            self.parse_css(css_content)
            kv_styles = self.get_kivy_styles()
            return kv_styles
        except Exception as e:
            print(f"Failed to read CSS file: {e}")
            return ""

    def parse_css(self, css_content):
        pattern = r'(?P<selector>\.[\w-]+)\s*\{\s*(?P<properties>[^}]+)\s*\}'
        matches = re.finditer(pattern, css_content)
        
        for match in matches:
            selector = match.group('selector')
            properties = match.group('properties')
            prop_dict = {}
            for prop in properties.split(';'):
                if ':' in prop:
                    key, value = prop.split(':', 1)
                    prop_dict[key.strip()] = value.strip()
            self.styles[selector] = prop_dict

        print("Successfully parsed CSS content")

    def convert_color(self, color):
        def rgb_to_kivy_color(r, g, b):
            return [r / 255.0, g / 255.0, b / 255.0, 1]

        if 'rgba' in color:
            rgba = color.strip('rgba()').split(',')
            rgba = [int(c) for c in rgba]
            return rgb_to_kivy_color(*rgba[:3]) + [rgba[3] / 255.0]
        elif 'rgb' in color:
            rgb = color.strip('rgb()').split(',')
            rgb = [int(c) for c in rgb]
            return rgb_to_kivy_color(*rgb)
        elif color in self.color_names:
            rgb = [int(c) for c in self.color_names[color].split(',')]
            return rgb_to_kivy_color(*rgb)
        return color

    def px_to_dp(self, value):
        match = re.match(r'(\d+)(px)?', value)
        if match:
            num = int(match.group(1))
            return f'{num}'  # Giá trị đơn vị dp
        return value

    def convert_to_kivy_selector(self, selector):
        if selector.startswith('.'):
            return selector[1:]
        return selector

    def convert_property(self, prop_name, value):
        kivy_properties = {
            'color': 'color',
            'background-color': 'background_color',
            'font-size': 'font_size',
            'font-family': 'font_name',
            'font-weight': 'bold',
            'text-align': 'halign',
            'vertical-align': 'valign',
            'text-decoration': 'text_size',
            'line-height': 'line_height',
            'opacity': 'opacity',
            'width': 'size_hint_x',
            'height': 'size_hint_y',
            'margin': None,
            'padding': 'padding',
            'border': None,
            'display': None,
            'position': None,
            'transform': None,
            'justify-content': 'justify_content',
            'align-items': 'valign',
            'text': 'text'
        }
        kivy_prop_name = kivy_properties.get(prop_name, prop_name)
        if kivy_prop_name is None:
            return None
        if kivy_prop_name == 'color' or kivy_prop_name == 'background_color':
            value = self.convert_color(value)
        if kivy_prop_name in ['font_size', 'size_hint_x', 'size_hint_y']:
            value = self.px_to_dp(value)
        if kivy_prop_name in ['halign', 'valign']:
            value = f"'{value}'"
        return f'{kivy_prop_name}: {value}' if value is not None else None


    def get_kivy_styles(self):
        kv_styles = ""
        for selector, style in self.styles.items():
            kivy_selector = self.convert_to_kivy_selector(selector)
            kv_styles += f'<{kivy_selector}>:\n'
            for prop, value in style.items():
                kv_property = self.convert_property(prop, value)
                if kv_property:
                    kv_styles += f'    {kv_property}\n'
            kv_styles += '\n'
        return kv_styles
