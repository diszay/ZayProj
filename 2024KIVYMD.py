import socket
import threading
import paramiko
import time
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp

KV = '''
ScreenManager:
    LoginWindow:
    MainWindow:
    CommandWindow:
    ShowCommandsWindow:

<LoginWindow@Screen>:
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        padding: [50, 20, 50, 20]
        spacing: 20

        MDLabel:
            text: 'Username'
            theme_text_color: 'Secondary'

        MDTextField:
            id: username_entry
            multiline: False
            hint_text: 'Enter your username'
            on_text_validate: app.on_enter_pressed(self)
            focus: True

        MDLabel:
            text: 'Password'
            theme_text_color: 'Secondary'

        MDTextField:
            id: password_entry
            multiline: False
            password: True
            hint_text: 'Enter your password'
            on_text_validate: app.on_enter_pressed(self)
            focus: True

        MDLabel:
            text: 'IP Address'
            theme_text_color: 'Secondary'

        MDTextField:
            id: ip_entry
            multiline: False
            hint_text: 'Enter IP address'
            on_text_validate: app.on_enter_pressed(self)
            focus: True

        BoxLayout:
            orientation: 'horizontal'
            spacing: 20
            size_hint_y: None
            height: self.minimum_height

            MDRaisedButton:
                text: 'Login'
                size_hint: None, None
                on_press: app.login()

            Widget:
                size_hint_x: 1

            MDRaisedButton:
                text: 'Toggle Dark Mode'
                size_hint: None, None
                on_press: app.toggle_dark_mode()

            MDFlatButton:
                text: 'Exit'
                size_hint: None, None
                on_press: app.stop()

        Widget:
            size_hint_y: 0.1

        MDLabel:
            text: '© 2023 Intellinet. All rights reserved'
            theme_text_color: 'Secondary'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]

<MainWindow@Screen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        padding: [50, 20, 50, 20]
        spacing: 20

        MDLabel:
            text: 'Welcome to IntelliNet'
            theme_text_color: 'Primary'
            font_style: 'H5'
            halign: 'center'
            valign: 'top'
            size_hint_y: None
            height: self.texture_size[1]

        Widget:
            size_hint_y: 1

        MDRaisedButton:
            text: 'Open Configuration Window'
            size_hint: None, None
            size: 200, 100
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_press: root.manager.current = 'command'

<CommandWindow@Screen>:
    name: 'command'
    BoxLayout:
        orientation: 'vertical'
        padding: [50, 20, 50, 20]
        spacing: 20

        MDLabel:
            text: 'Config-if Buttons'
            theme_text_color: 'Primary'
            font_style: 'H5'
            halign: 'center'
            valign: 'top'
            size_hint_y: None
            height: self.texture_size[1]

        FloatLayout:
            GridLayout:
                cols: 4
                spacing: [20, 20]
                size_hint: None, None
                size: self.minimum_size
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                row_default_height: 100
                row_force_default: True

                MDRaisedButton:
                    text: 'Add Poe'
                    on_press: app.poe(self)

                MDRaisedButton:
                    text: 'Default'
                    on_press: app.default(self)

                MDRaisedButton:
                    text: 'Exit'
                    on_press: app.stop()

                MDRaisedButton:
                    text: 'No Poe'
                    on_press: app.nopoe(self)

                MDRaisedButton:
                    text: 'Shut/Noshut'
                    on_press: app.shut_noshut(self)

                MDRaisedButton:
                    text: 'Vlan'
                    on_press: app.vlan_script(self)

                MDRaisedButton:
                    text: 'Voice 156'
                    on_press: app.voip(self)

                MDRaisedButton:
                    text: 'Voice 220'
                    on_press: app.voip220(self)

                MDRaisedButton:
                    text: 'Multiple Vlan'
                    on_press: app.multiplevlan_script(self)

                MDRaisedButton:
                    text: 'Multi Voip Vlan'
                    on_press: app.multiplevoip(self)

                MDRaisedButton:
                    text: 'SHOW Commands'
                    on_press: root.manager.current = 'show_commands'

<ShowCommandsWindow@Screen>:
    name: 'show_commands'
    BoxLayout:
        orientation: 'vertical'
        padding: [50, 20, 50, 20]
        spacing: 20

        MDLabel:
            text: 'Show Commands'
            theme_text_color: 'Primary'
            font_style: 'H5'
            halign: 'center'
            valign: 'top'
            size_hint_y: None
            height: self.texture_size[1]

        FloatLayout:
            GridLayout:
                cols: 4
                spacing: [20, 20]
                size_hint: None, None
                size: self.minimum_size
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                row_default_height: 100
                row_force_default: True

                MDRaisedButton:
                    text: 'CDP Neighbors'
                    on_press: app.cdp(self)

                MDRaisedButton:
                    text: 'Environment'
                    on_press: app.switchenv(self)

                MDRaisedButton:
                    text: 'Show Process'
                    on_press: app.show_process(self)

                MDRaisedButton:
                    text: 'Show Hardware'
                    on_press: app.show_hardware(self)

                MDRaisedButton:
                    text: 'Show Trunkport'
                    on_press: app.show_trunk(self)

                MDRaisedButton:
                    text: 'Show Run'
                    on_press: app.show_run_log(self)

                MDRaisedButton:
                    text: 'Show Version'
                    on_press: app.show_version(self)

                MDRaisedButton:
                    text: 'Show VLAN Brief'
                    on_press: app.show_vlan_brief(self)

                MDRaisedButton:
                    text: 'Show MAC Address Table'
                    on_press: app.show_mac_address_table(self)

                MDRaisedButton:
                    text: 'Show Logs'
                    on_press: app.show_logs(self)

                MDRaisedButton:
                    text: 'Exit'
                    on_press: app.stop()

                MDRaisedButton:
                    text: 'Config-if Commands'
                    on_press: root.manager.current = 'command'

'''


class NetworkGUIApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Gray"
        return Builder.load_string(KV)

    def on_focus_next(self, instance):
        def focus_next(dt):
            next_widget = instance.get_focus_next()
            if next_widget:
                next_widget.focus = True

        Clock.schedule_once(focus_next, 0.2)

    def on_enter_pressed(self, instance):
        if instance == self.root.get_screen('login').ids.ip_entry:
            self.login()
        else:
            instance.focus = False

    def login(self):
        global ssh
        ip_address = self.root.get_screen('login').ids.ip_entry.text
        username = self.root.get_screen('login').ids.username_entry.text
        password = self.root.get_screen('login').ids.password_entry.text
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ip_address, username=username, password=password)
            chan = ssh.invoke_shell()
            self.chan = chan
            self.root.current = 'main'
        except (paramiko.AuthenticationException, paramiko.SSHException, socket.error):
            self.display_error_message()

    def display_error_message(self):
        error_label = self.root.get_screen('login').ids.error_message
        error_label.text = 'Login Failed, Try Again'

        def clear_error_message():
            error_label.text = ''

        timer = threading.Timer(15, clear_error_message)
        timer.start()

    def toggle_dark_mode(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    def vlan_script(self, *args):
        popup = Popup(title="Interface and Vlan entry")

        vlan_label = Label(text='Enter vlan number')
        self.vlan_entry = TextInput(hint_text='Enter vlan number')

        interface_label = Label(text='Enter Interface with corresponding bit port')
        self.interface_entry = TextInput(hint_text='Ex. gi, twogi, FastEthernet, etc.')

        description_label = Label(text='Enter description of port')
        self.description_entry = TextInput(hint_text='Enter the description you want 15 character limit')

        self.vlan_entry.bind(on_text_validate=lambda x: self.interface_entry.focus())
        self.interface_entry.bind(on_text_validate=lambda x: self.description_entry.focus())
        self.description_entry.bind(on_text_validate=lambda x: self.submit_vlan(popup))

        submit_button = Button(text='Submit Change')
        submit_button.bind(on_press=lambda x: self.submit_vlan(popup))

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(vlan_label)
        layout.add_widget(self.vlan_entry)
        layout.add_widget(interface_label)
        layout.add_widget(self.interface_entry)
        layout.add_widget(description_label)
        layout.add_widget(self.description_entry)
        layout.add_widget(submit_button)

        popup.content = layout
        popup.open()

    def submit_vlan(self, popup, *args):
        interface = self.interface_entry.text
        vlan = self.vlan_entry.text
        description = self.description_entry.text
        self.chan.send("configure terminal\n")
        self.chan.send(f'interface {interface}\n')
        self.chan.send("switchport mode access\n")
        self.chan.send(f"switchport access vlan {vlan}\n")
        self.chan.send(f'description {description}\n')
        self.chan.send('end\n')
        self.chan.send('wr\n')
        time.sleep(1)
        self.chan.send(f'show int {interface} status\n')
        output = self.chan.recv(65535).decode('utf-8')
        self.vlan_entry.text = ''
        self.interface_entry.text = ''
        self.description_entry.text = ''

        confirm_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        confirm_label = Label(text="VLAN Configuration Updated!")
        confirm_layout.add_widget(confirm_label)

        output_label = Label(text=output, size_hint_y=None, height=50)
        confirm_layout.add_widget(output_label)

        confirm_popup = Popup(title="Confirmation", content=confirm_layout, size_hint=(None, None), size=(400, 300))

        confirm_button = Button(text="OK", on_press=lambda x: confirm_popup.dismiss())
        confirm_layout.add_widget(confirm_button)

        def open_confirm_popup(dt):
            confirm_popup.open()
            popup.dismiss()

        Clock.schedule_once(open_confirm_popup, 0.1)

    def shut_noshut(self, *args):
        def show_confirmation_popup():
            confirm_window = Popup(title="Confirmation", size_hint=(0.5, 0.5), auto_dismiss=True)
            confirm_label = Label(text="Port has been shut and no shut!")
            confirm_button = Button(text="OK", size_hint=(None, None), size=(100, 50))
            confirm_button.bind(on_press=confirm_window.dismiss)

            confirm_layout = BoxLayout(orientation='vertical')
            confirm_layout.add_widget(confirm_label)
            confirm_layout.add_widget(confirm_button)

            confirm_window.content = confirm_layout
            confirm_window.open()

        def submit_shut():
            interface = self.interface_entry.text
            self.chan.send("configure terminal\n")
            self.chan.send(f'interface {interface}\n')
            self.chan.send('shut\n')
            self.chan.send('no shut\n')
            self.chan.send('exit\n')

            time.sleep(1)
            self.interface_entry.text = ''

            show_confirmation_popup()

        popup = Popup(title="Interface entry")

        interface_label = Label(text='Enter corresponding bit port')
        self.interface_entry = TextInput()

        self.interface_entry.bind(on_text_validate=lambda x: submit_shut())

        submit_button = Button(text='Submit Change')
        submit_button.bind(on_press=lambda x: submit_shut())

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(interface_label)
        layout.add_widget(self.interface_entry)
        layout.add_widget(submit_button)

        popup.content = layout
        popup.open()

    def voip(self, instance):
        self.open_voip_popup('156')

    def voip220(self, instance):
        self.open_voip_popup('220')

    def open_voip_popup(self, vlan):
        popup = Popup(title=f"VoIP Configuration for VLAN {vlan}", size_hint=(0.5, 0.5))
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        interface_label = Label(text='Enter corresponding bit port')
        interface_entry = TextInput(hint_text='Ex. gi, twogi, FastEthernet, etc.')
        popup_layout.add_widget(interface_label)
        popup_layout.add_widget(interface_entry)

        submit_button = Button(text='Submit Change')
        submit_button.bind(on_press=lambda instance: self.submit_voip(interface_entry, vlan, popup))
        popup_layout.add_widget(submit_button)

        popup.content = popup_layout
        popup.open()

    def submit_voip(self, interface_entry, vlan, popup):
        interface = interface_entry.text
        self.chan.send("configure terminal\n")
        self.chan.send(f'interface {interface}\n')
        self.chan.send("switchport mode access\n")
        self.chan.send(f'switchport access vlan {vlan}\n')
        self.chan.send(f"switchport voice vlan {vlan}\n")
        self.chan.send("switchport port-security maximum 3\n")
        self.chan.send("switchport port-security violation restrict\n")
        self.chan.send("switchport port-security aging time 2\n")
        self.chan.send("switchport aging time type inactivity\n")
        self.chan.send("switchport port-security\n")
        self.chan.send("trust device cisco-phone\n")
        self.chan.send("auto qos voip cisco-phone\n")
        self.chan.send("macro description cisco-phone\n")
        self.chan.send("spanning-tree portfast\n")
        self.chan.send("spanning-tree bpduguard enable\n")
        self.chan.send("service-policy input AutoQos-4.0-CiscoPhone-Input-Policy\n")
        self.chan.send("service-policy output AutoQos-4.0-Output-Policy\n")
        self.chan.send("end\n")
        self.chan.send("wr\n")
        time.sleep(1)
        self.chan.send(f'show int {interface} status\n')
        output = self.chan.recv(65535).decode('utf-8')
        interface_entry.text = ''

        text = TextInput(text=output, readonly=True, font_size=14, size_hint_y=None)
        text.bind(minimum_height=text.setter('height'))

        scrollview = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scrollview.add_widget(text)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        ok_button.bind(on_press=popup.dismiss)

        layout = BoxLayout(orientation='vertical', padding=(10))
        layout.add_widget(scrollview)
        layout.add_widget(ok_button)

        popup.title = "VoIP VLAN Configuration Updated!"
        popup.content = layout
        popup.size_hint = (0.8, 0.8)
        popup.open()

    def default(self, instance):
        popup = Popup(title="Default Port Interface", size_hint=(0.5, 0.5))
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        interface_label = Label(text='Enter corresponding bit port')
        interface_entry = TextInput(hint_text='Ex. gi, twogi, FastEthernet, etc.')
        popup_layout.add_widget(interface_label)
        popup_layout.add_widget(interface_entry)

        submit_button = Button(text='Submit Change')
        submit_button.bind(on_press=lambda instance: self.submit_default(interface_entry, popup))
        popup_layout.add_widget(submit_button)

        popup.content = popup_layout
        popup.open()

    def submit_default(self, interface_entry, popup):
        interface = interface_entry.text
        self.chan.send("configure terminal\n")
        self.chan.send(f'default interface {interface}\n')
        self.chan.send(f'interface {interface}\n')
        self.chan.send("description this port has been defaulted\n")
        self.chan.send('end\n')
        self.chan.send('wr\n')
        time.sleep(1)
        self.chan.send(f'show int {interface} status\n')
        output = self.chan.recv(65535).decode('utf-8')

        confirm_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        confirm_label = Label(text="Port has been defaulted!", font_size=20, color=[0.13, 0.13, 0.13, 1])
        confirm_layout.add_widget(confirm_label)

        output_label = Label(text=output, size_hint_y=None, height=150)
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(output_label)
        confirm_layout.add_widget(scroll_view)

        confirm_button = Button(text="OK", font_size=20, size_hint=(None, None), width=100)
        confirm_button.bind(on_press=lambda x: confirm_popup.dismiss())
        confirm_layout.add_widget(confirm_button)

        confirm_popup = Popup(title="Confirmation", content=confirm_layout, size_hint=(None, None), size=(400, 400))
        popup.dismiss()
        confirm_popup.open()

    def cdp(self, instance):
        self.chan.send("show cdp neighbors\n")
        time.sleep(1)
        output = self.chan.recv(65535).decode('utf-8')

        text = TextInput(text=output, readonly=True, font_size=14, size_hint_y=None)
        text.bind(minimum_height=text.setter('height'))

        scrollview = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scrollview.add_widget(text)

        confirm_button = Button(text="OK", size_hint=(1, 0.2))
        confirm_button.bind(on_press=lambda x: popup.dismiss())

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(scrollview)
        layout.add_widget(confirm_button)

        popup = Popup(title="CDP Neighbors Interface", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def poe(self, instance):
        popup = Popup(title="POE Interface", size_hint=(0.5, 0.5))
        layout = BoxLayout(orientation="vertical", padding=10)

        interface_label = Label(text='Enter corresponding bit port')
        interface_entry = TextInput(hint_text='Ex. gi, twogi, FastEthernet, etc.')
        layout.add_widget(interface_label)
        layout.add_widget(interface_entry)

        submit_button = Button(text='Submit Change')
        submit_button.bind(on_press=lambda instance: self.submit_poe(interface_entry, popup))
        layout.add_widget(submit_button)

        popup.content = layout
        popup.open()

    def submit_poe(self, interface_entry, popup):
        interface = interface_entry.text
        self.chan.send('configure terminal\n')
        self.chan.send(f'interface {interface}\n')
        self.chan.send("power inline auto\n")
        self.chan.send('end\n')
        self.chan.send('wr\n')
        time.sleep(1)
        self.chan.send(f'show int {interface} status\n')
        output = self.chan.recv(65535).decode('utf-8')
        interface_entry.text = ''

        confirm_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        confirm_label = Label(text="POE Configuration Updated!")
        confirm_layout.add_widget(confirm_label)

        output_label = Label(text=output, size_hint_y=None, height=50)
        confirm_layout.add_widget(output_label)

        confirm_button = Button(text="OK", on_press=popup.dismiss)
        confirm_layout.add_widget(confirm_button)

        confirm_popup = Popup(title="Confirmation", content=confirm_layout, size_hint=(0.8, 0.8))
        confirm_popup.open()

    def nopoe(self, instance):
        popup = Popup(title="Remove POE Interface", size_hint=(0.5, 0.5))
        layout = BoxLayout(orientation="vertical", padding=10)

        interface_label = Label(text='Enter corresponding bit port')
        interface_entry = TextInput(hint_text='Ex. gi, twogi, FastEthernet, etc.')
        layout.add_widget(interface_label)
        layout.add_widget(interface_entry)

        submit_button = Button(text='Submit Change')
        submit_button.bind(on_press=lambda instance: self.submit_nopoe(interface_entry, popup))
        layout.add_widget(submit_button)

        popup.content = layout
        popup.open()

    def submit_nopoe(self, interface_entry, popup):
        interface = interface_entry.text
        self.chan.send('configure terminal\n')
        self.chan.send(f'interface {interface}\n')
        self.chan.send("power inline never\n")
        self.chan.send('end\n')
        self.chan.send('wr\n')
        time.sleep(1)
        self.chan.send(f'show int {interface} status\n')
        output = self.chan.recv(65535).decode('utf-8')
        interface_entry.text = ''

        confirm_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        confirm_label = Label(text="POE Configuration Removed!")
        confirm_layout.add_widget(confirm_label)

        output_label = Label(text=output, size_hint_y=None, height=50)
        confirm_layout.add_widget(output_label)

        confirm_button = Button(text="OK", on_press=popup.dismiss)
        confirm_layout.add_widget(confirm_button)

        confirm_popup = Popup(title="Confirmation", content=confirm_layout, size_hint=(0.8, 0.8))
        confirm_popup.open()

    def switchenv(self, instance):
        self.chan.send("sh env all\n")
        time.sleep(1)
        output = self.chan.recv(65535).decode('utf-8')

        text = TextInput(text=output, readonly=True, font_size=14, size_hint_y=None)
        text.bind(minimum_height=text.setter('height'))

        scrollview = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scrollview.add_widget(text)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        ok_button.bind(on_press=lambda x: popup.dismiss())

        layout = BoxLayout(orientation='vertical', padding=(10))
        layout.add_widget(scrollview)
        layout.add_widget(ok_button)

        popup = Popup(title="Switch's Environment", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def show_run_log(self, instance):
        self.chan.send("sh run\n")
        time.sleep(3)  # increase sleep time to ensure complete output
        output = self.chan.recv(65535).decode('utf-8')

        text = TextInput(text=output, readonly=True, font_size=14, size_hint_y=None)
        text.bind(minimum_height=text.setter('height'))

        scrollview = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scrollview.add_widget(text)

        confirm_button = Button(text="OK", size_hint=(1, 0.2))
        confirm_button.bind(on_press=lambda x: popup.dismiss())

        layout = BoxLayout(orientation='vertical', padding=(10))
        layout.add_widget(scrollview)
        layout.add_widget(confirm_button)

        popup = Popup(title="Switch's Show Run Log", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def multiplevlan_script(self, *args):
        popup = Popup(title="Interface and Vlan entry")

        vlan_label = Label(text='Enter vlan number')
        self.vlan_entry = TextInput(hint_text='Enter vlan number')

        interface_label = Label(text='Enter Interfaces with corresponding bit port')
        self.interface_entry = TextInput(hint_text='Ex. gi, twogi, FastEthernet 1/0/1-3')

        description_label = Label(text='Enter description of port')
        self.description_entry = TextInput(hint_text='Enter the description you want 15 character limit')

        self.vlan_entry.bind(on_text_validate=lambda x: self.interface_entry.focus())
        self.interface_entry.bind(on_text_validate=lambda x: self.description_entry.focus())
        self.description_entry.bind(on_text_validate=lambda x: self.submit_multiplevlan(popup))

        submit_button = Button(text='Submit Change')
        submit_button.bind(on_press=lambda x: self.submit_multiplevlan(popup))

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(vlan_label)
        layout.add_widget(self.vlan_entry)
        layout.add_widget(interface_label)
        layout.add_widget(self.interface_entry)
        layout.add_widget(description_label)
        layout.add_widget(self.description_entry)
        layout.add_widget(submit_button)

        popup.content = layout
        popup.open()

    def submit_multiplevlan(self, popup, *args):
        interface = self.interface_entry.text
        vlan = self.vlan_entry.text
        description = self.description_entry.text
        self.chan.send("configure terminal\n")
        self.chan.send(f'interface range {interface}\n')
        self.chan.send("switchport mode access\n")
        self.chan.send(f"switchport access vlan {vlan}\n")
        self.chan.send(f'description {description}\n')
        self.chan.send('end\n')
        self.chan.send('wr\n')
        time.sleep(1)
        self.chan.send(f'show int {interface} status\n')
        output = self.chan.recv(65535).decode('utf-8')
        self.vlan_entry.text = ''
        self.interface_entry.text = ''
        self.description_entry.text = ''

        confirm_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        confirm_label = Label(text="Multiple VLAN Configuration Updated!")
        confirm_layout.add_widget(confirm_label)

        output_label = Label(text=output, size_hint_y=None, height=50)
        confirm_layout.add_widget(output_label)

        confirm_popup = Popup(title="Confirmation", content=confirm_layout, size_hint=(None, None), size=(400, 300))

        confirm_button = Button(text="OK", on_press=lambda x: confirm_popup.dismiss())
        confirm_layout.add_widget(confirm_button)

        def open_confirm_popup(dt):
            confirm_popup.open()
            popup.dismiss()

        Clock.schedule_once(open_confirm_popup, 0.1)

    def multiplevoip(self, instance):
        popup = Popup(title="VoIP Configuration", size_hint=(0.5, 0.5))
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        vlan_label = Label(text='Enter VLAN ID')
        popup_layout.add_widget(vlan_label)

        vlan_entry = TextInput(hint_text='Enter vlan number')
        popup_layout.add_widget(vlan_entry)

        interface_label = Label(text='Enter corresponding bit ports')
        popup_layout.add_widget(interface_label)

        interface_entry = TextInput(hint_text='Ex. gi, twogi, FastEthernet, etc. gi 1/0/1-3')
        popup_layout.add_widget(interface_entry)

        submit_button = Button(text='Submit Change')
        submit_button.bind(on_press=lambda instance: self.submit_multivoip(vlan_entry, interface_entry, popup))
        popup_layout.add_widget(submit_button)

        popup.content = popup_layout
        popup.open()

    def submit_multivoip(self, vlan_entry, interface_entry, popup):
        vlan = vlan_entry.text
        interface = interface_entry.text
        self.chan.send("configure terminal\n")
        self.chan.send(f'interface range {interface}\n')
        self.chan.send("switchport mode access\n")
        self.chan.send(f'switchport access vlan {vlan}\n')
        self.chan.send(f"switchport voice vlan {vlan}\n")
        self.chan.send("switchport port-security maximum 3\n")
        self.chan.send("switchport port-security violation restrict\n")
        self.chan.send("switchport port-security aging time 2\n")
        self.chan.send("switchport aging time type inactivity\n")
        self.chan.send("switchport port-security\n")
        self.chan.send("trust device cisco-phone\n")
        self.chan.send("auto qos voip cisco-phone\n")
        self.chan.send("macro description cisco-phone\n")
        self.chan.send("spanning-tree portfast\n")
        self.chan.send("spanning-tree bpduguard enable\n")
        self.chan.send("service-policy input AutoQos-4.0-CiscoPhone-Input-Policy\n")
        self.chan.send("service-policy output AutoQos-4.0-Output-Policy\n")
        self.chan.send("end\n")
        self.chan.send("wr\n")
        time.sleep(1)
        self.chan.send(f'show int {interface} status\n')
        output = self.chan.recv(65535).decode('utf-8')
        vlan_entry.text = ''
        interface_entry.text = ''

        text = TextInput(text=output, readonly=True, font_size=14, size_hint_y=None)
        text.bind(minimum_height=text.setter('height'))

        scrollview = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scrollview.add_widget(text)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        ok_button.bind(on_press=popup.dismiss)

        layout = BoxLayout(orientation='vertical', padding=(10))
        layout.add_widget(scrollview)
        layout.add_widget(ok_button)

        popup.title = "VoIP VLAN Configuration Updated!"
        popup.content = layout
        popup.size_hint = (0.8, 0.8)
        popup.open()

    def show_process(self, instance):
        self.chan.send("sh process\n")
        time.sleep(1)
        output = self.chan.recv(65535).decode('utf-8')

        text = TextInput(text=output, readonly=True, font_size=14, size_hint_y=None)
        text.bind(minimum_height=text.setter('height'))

        scrollview = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scrollview.add_widget(text)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        ok_button.bind(on_press=lambda x: popup.dismiss())

        layout = BoxLayout(orientation='vertical', padding=(10))
        layout.add_widget(scrollview)
        layout.add_widget(ok_button)

        popup = Popup(title="Switch's Process", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def show_hardware(self, instance):
        self.chan.send("sh hardware\n")
        self.chan.send(" " * 2 + "\n")
        time.sleep(1)
        output = self.chan.recv(65535).decode('utf-8')

        text = TextInput(text=output, readonly=True, font_size=14, size_hint_y=None)
        text.bind(minimum_height=text.setter('height'))

        scrollview = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scrollview.add_widget(text)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        ok_button.bind(on_press=lambda x: popup.dismiss())

        layout = BoxLayout(orientation='vertical', padding=(10))
        layout.add_widget(scrollview)
        layout.add_widget(ok_button)

        popup = Popup(title="Switch's Hardware", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def show_version(self, instance):
        self.chan.send("sh version\n")
        self.chan.send(" " * 2 + "\n")
        time.sleep(1)
        output = self.chan.recv(65535).decode('utf-8')

        text = TextInput(text=output, readonly=True, font_size=14, size_hint_y=None)
        text.bind(minimum_height=text.setter('height'))

        scrollview = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scrollview.add_widget(text)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        ok_button.bind(on_press=lambda x: popup.dismiss())

        layout = BoxLayout(orientation='vertical', padding=(10))
        layout.add_widget(scrollview)
        layout.add_widget(ok_button)

        popup = Popup(title="Switch's Version", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def show_trunk(self, instance):
        self.chan.send("show interface trunk\n")
        time.sleep(1)
        output = self.chan.recv(65535).decode('utf-8')

        text = TextInput(text=output, readonly=True, font_size=14, size_hint_y=None)
        text.bind(minimum_height=text.setter('height'))

        scrollview = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scrollview.add_widget(text)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        ok_button.bind(on_press=lambda x: popup.dismiss())

        layout = BoxLayout(orientation='vertical', padding=(10))
        layout.add_widget(scrollview)
        layout.add_widget(ok_button)

        popup = Popup(title="Switch's Trunk Port", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def show_vlan_brief(self, instance):
        self.chan.send("show vlan brief\n")
        time.sleep(1)
        output = self.chan.recv(65535).decode('utf-8')

        text = TextInput(text=output, readonly=True, font_size=14, size_hint_y=None)
        text.bind(minimum_height=text.setter('height'))

        scrollview = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scrollview.add_widget(text)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        ok_button.bind(on_press=lambda x: popup.dismiss())

        layout = BoxLayout(orientation='vertical', padding=(10))
        layout.add_widget(scrollview)
        layout.add_widget(ok_button)

        popup = Popup(title="Switch's VLAN Brief", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def show_mac_address_table(self, instance):
        self.chan.send("show mac address-table\n")
        time.sleep(1)
        output = self.chan.recv(65535).decode('utf-8')

        text = TextInput(text=output, readonly=True, font_size=14, size_hint_y=None)
        text.bind(minimum_height=text.setter('height'))

        scrollview = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scrollview.add_widget(text)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        ok_button.bind(on_press=lambda x: popup.dismiss())

        layout = BoxLayout(orientation='vertical', padding=(10))
        layout.add_widget(scrollview)
        layout.add_widget(ok_button)

        popup = Popup(title="Switch's MAC Address Table", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def show_logs(self, instance):
        self.chan.send("show logging\n")
        time.sleep(1)
        output = self.chan.recv(65535).decode('utf-8')

        text = TextInput(text=output, readonly=True, font_size=14, size_hint_y=None)
        text.bind(minimum_height=text.setter('height'))

        scrollview = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scrollview.add_widget(text)

        ok_button = Button(text="OK", size_hint=(1, 0.2))
        ok_button.bind(on_press=lambda x: popup.dismiss())

        layout = BoxLayout(orientation='vertical', padding=(10))
        layout.add_widget(scrollview)
        layout.add_widget(ok_button)

        popup = Popup(title="Switch's Logs", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def exit(self, instance):
        ssh.close()
        MDApp.get_running_app().stop()

    def on_stop(self):
        ssh.close()


if __name__ == '__main__':
    NetworkGUIApp().run()


