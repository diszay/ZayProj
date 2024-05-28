This is the readme for the Networking GUI 


############################### Overview ###################################

This application is a GUI tool for configuring network switches using SSH. It is built with Python, Kivy, and KivyMD, and is designed to help network administrators manage their network devices more easily.



################################ Features ##################################

1. **Login Screen**: Allows users to connect to a network switch via SSH.
2. **Main Window**: Provides access to various network configuration commands.
3. **Command Window**: Contains buttons for common network configuration tasks.
4. **Show Commands Window**: Allows users to view various network status and configuration details.

################################ Prerequisites ###############################
- Python 3.x
- Kivy
- KivyMD
- Paramiko

################################  Installation ################################ 
1. Clone the repository to your local machine: "git clone https://github.com/"yourusername"/your-repo-name.git
2. Navigate to the project directory "cd"
3. Install required Python packages 'pip install kivy kivymd paramiko'
4. Run the application using the following command: 'python MY_KIVYMD2024.py'

################################ Using Application ##############################

				Login Screen
 **Username**: Enter your SSH username.
 **Password**: Enter your SSH password.
 **IP Address**: Enter the IP address of the network switch.
 **Login Button**: Click to connect to the switch.
 **Toggle Dark Mode Button**: Switch between light and dark themes.
 **Exit Button**: Close the application.

				Main Window
 **Open Configuration Window Button**: Opens the Command Window for network configuration   tasks.
			        Command window
This window contains buttons for common network configuration tasks, arranged in a grid for easy access. The buttons are:

 **Add Poe**: Configure Power over Ethernet (PoE) on a port.
 **No Poe**: Remove PoE configuration from a port.
 **Shut/Noshut**: Shut and then no shut a port.
 **Default**: Reset a port to its default configuration.
 **Vlan**: Configure VLAN on a port.
 **Voice 156**: Configure voice VLAN 156 on a port.
 **Voice 220**: Configure voice VLAN 220 on a port.
 **Multiple Vlan**: Configure multiple VLANs on ports.
 **Multi Voip Vlan**: Configure multiple VoIP VLANs on ports.
 **SHOW Commands**: Navigate to the Show Commands Window.

				SHOW Commands Window
This window allows you to view various network status and configuration details. The buttons available are:

 **CDP Neighbors**: Show CDP neighbors.
 **Environment**: Show environmental details of the switch.
 **Show Process**: Show running processes.
 **Show Hardware**: Show hardware details.
 **Show Trunkport**: Show trunk port details.
 **Show Run**: Show running configuration.
 **Show Version**: Show software version.
 **Show Vlan Brief**: Show VLAN brief.
 **Show MAC Address Table**: Show MAC address table.
 **Show Logs**: Show system logs.
 **Config-if Commands**: Navigate back to the Command Window.


################################ Error Handling ################################## 
If login fails, an error message will be displayed. Try re-entering your credentials and IP address.

################################ Troubleshooting ################################
- Ensure your device is connected to the network.
- Verify the IP address, username, and password.
- Check SSH access on the network switch.

################################ License ##########################################
This project is licensed under the MIT License.

################################## Acknowledgements ################################
- Kivy and KivyMD for the GUI framework.
- Paramiko for SSH connectivity.


