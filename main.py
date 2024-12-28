import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.core.window import Window
from kivy.lang import Builder
from kivyandcss import CssParser

class BattleGame(App):
    def build(self):
        # Đặt kích thước màn hình ngang
        Window.size = (800, 600)
        Window.rotation = 0  # Đảm bảo chế độ ngang

        # Tải file CSS
        css_parser = CssParser()
        kv_styles = css_parser.parse_file('style.css')
        Builder.load_string(kv_styles)

        self.layout = FloatLayout(size_hint=(1, 1))
        self.draw_background()

        self.player_health = 100
        self.robot_health = 100
        self.battle_time = 30
        self.timer = None

        self.monster_types = {
            "Dragon": 30,
            "Goblin": 10,
            "Robot": 20,
        }

        self.player_label = Label(text=f"Player Health: {self.player_health}", size_hint=(0.4, 0.1), pos_hint={"x": 0, "top": 1})
        self.robot_label = Label(text=f"Robot Health: {self.robot_health}", size_hint=(0.4, 0.1), pos_hint={"x": 0.6, "top": 1})

        self.code_input = TextInput(size_hint=(0.4, 0.2), pos_hint={"x": 0, "y": 0.3}, multiline=True)

        self.start_button = Button(text="Start Game", size_hint=(0.4, 0.1), pos_hint={"x": 0.6, "y": 0.1})
        self.start_button.bind(on_press=self.start_battle)

        self.result_label = Label(text="", size_hint=(0.4, 0.1), pos_hint={"x": 0.3, "y": 0.8})

        self.layout.add_widget(self.player_label)
        self.layout.add_widget(self.robot_label)
        self.layout.add_widget(self.code_input)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.result_label)

        self.instruction_label = Label(
            text="Nhập lệnh triệu hồi: enemy('tên quái vật')",
            size_hint=(0.4, 0.1),
            pos_hint={"x": 0, "y": 0.5}
        )
        self.layout.add_widget(self.instruction_label)

        self.monster_info_label = Label(
            text="Các quái vật hiện có:\n" + "\n".join(self.monster_types.keys()),
            size_hint=(0.4, 0.3),
            pos_hint={"x": 0, "y": 0.7}
        )
        self.layout.add_widget(self.monster_info_label)

        return self.layout

    def draw_background(self):
        with self.layout.canvas.before:
            # Vẽ bầu trời
            Color(135/255, 206/255, 235/255)  # Màu xanh trời
            Rectangle(pos=(0, 100), size=(800, 500))  # Bầu trời

            # Vẽ mặt đất
            Color(34/255, 139/255, 34/255)  # Màu xanh cỏ
            Rectangle(pos=(0, 0), size=(800, 100))  # Mặt đất

            # Vẽ mặt trời
            Color(1, 1, 0)  # Màu vàng
            Ellipse(pos=(650, 450), size=(100, 100))  # Mặt trời

            # Vẽ đám mây
            Color(1, 1, 1)  # Màu trắng
            for _ in range(5):
                x = random.randint(0, 700)
                y = random.randint(300, 500)
                Ellipse(pos=(x, y), size=(80, 50))  # Đám mây

    def start_battle(self, instance):
        self.timer = Clock.schedule_interval(self.update_timer, 1)
        Clock.schedule_interval(self.robot_attack, 2)
        Clock.schedule_interval(self.player_attack, 3)
        self.summon_monster("Dragon")

    def update_timer(self, dt):
        self.battle_time -= 1
        if self.battle_time <= 0:
            self.end_battle("Hòa!")

    def robot_attack(self, dt):
        if self.robot_health > 0:
            damage_to_robot = random.randint(1, 25)
            self.robot_health -= damage_to_robot
            self.robot_label.text = f"Robot Health: {self.robot_health}"
            print(f"Quái vật tấn công robot! Gây {damage_to_robot} sát thương.")

            if self.robot_health <= 0:
                self.end_battle("Người chơi thắng!")

    def player_attack(self, dt):
        if self.player_health > 0:
            damage_to_player = random.randint(20, 30)
            self.player_health -= damage_to_player
            self.player_label.text = f"Player Health: {self.player_health}"
            print(f"Quái vật tấn công người chơi! Gây {damage_to_player} sát thương.")

            if self.player_health <= 0:
                self.end_battle("Quái vật thắng!")

    def summon_monster(self, monster_name):
        damage_to_robot = self.monster_types[monster_name]
        self.robot_health -= damage_to_robot
        self.robot_label.text = f"Robot Health: {self.robot_health}"

        print(f"Triệu hồi {monster_name}, gây {damage_to_robot} sát thương cho robot!")

        if self.robot_health <= 0:
            self.end_battle("Người chơi thắng!")

    def end_battle(self, result):
        if self.timer:
            self.timer.cancel()
        self.result_label.text = result  # Hiển thị kết quả trên giao diện
        print(result)
        self.player_health = 100
        self.robot_health = 100
        self.player_label.text = f"Player Health: {self.player_health}"
        self.robot_label.text = f"Robot Health: {self.robot_health}"

if __name__ == '__main__':
    BattleGame().run()
