import os
import subprocess
import threading
import time
import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernCMD(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Modern Terminal")
        self.geometry("1000x650") 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Unified UI Font Size
        self.terminal_font = ("VCR OSD Mono", 16)

        # Command History Tracking
        self.command_history = []
        self.history_index = -1

        # 1. Base Tkinter Text Box (Allows embedded widget windows)
        self.terminal_output = tk.Text(
            self,
            font=self.terminal_font,
            bg="#1A1B26",
            fg="#A9B1D6",
            insertbackground="#FFFFFF",
            relief="flat",
            bd=0,
            padx=15,
            pady=15,
            wrap="none"
        )
        self.terminal_output.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="nsew")
        
        # Welcome Message
        self.terminal_output.insert("end", "Modern Python Terminal Initialized.\nStart your command with \"copypop-{command}\" to copy output.\n\n")
        self.terminal_output.configure(state="disabled")

        # 2. Command Input Box
        self.command_input = ctk.CTkEntry(
            self,
            placeholder_text="Type a command...",
            font=self.terminal_font,
            fg_color="#24283B",
            text_color="#FFFFFF",
            border_width=0,
            corner_radius=12
        )
        self.command_input.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="ew")
        
        # Action Key Bindings
        self.command_input.bind("<Return>", self.process_command)
        self.command_input.bind("<Up>", self.scroll_history_up)
        self.command_input.bind("<Down>", self.scroll_history_down)

    def play_sound(self, filename):
        """Plays an MP3 natively with a comfortable, lowered volume level."""
        if os.path.exists(filename):
            abs_path = os.path.abspath(filename)
            
            # We add a 'setaudio' command to cap the volume at 300 out of 1000
            ps_command = (
                f"$open = '[DllImport(\"winmm.dll\")] public static extern int mciSendString(string lpstrCommand, System.Text.StringBuilder lpstrReturnString, int uReturnLength, int hwndCallback);';"
                f"$type = Add-Type -MemberDefinition $open -Name WinMM -Namespace WinMMPInvoke -PassThru;"
                f"[WinMMPInvoke.WinMM]::mciSendString('open \"{abs_path}\" type mpegvideo alias bgmusic', $null, 0, 0);"
                f"[WinMMPInvoke.WinMM]::mciSendString('setaudio bgmusic volume to 125', $null, 0, 0);"
                f"[WinMMPInvoke.WinMM]::mciSendString('play bgmusic wait', $null, 0, 0);"
                f"[WinMMPInvoke.WinMM]::mciSendString('close bgmusic', $null, 0, 0);"
            )
            
            def run_audio():
                subprocess.run(
                    ["powershell", "-Command", ps_command],
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
            threading.Thread(target=run_audio, daemon=True).start()
        else:
            self.append_output(f"\n[AUDIO ERROR]: Cannot find file '{filename}' in this directory.\n")

    def process_command(self, event):
        raw_command = self.command_input.get().strip()
        if not raw_command:
            return

        # Track history logs cleanly
        if not self.command_history or self.command_history[-1] != raw_command:
            self.command_history.append(raw_command)
        self.history_index = len(self.command_history)

        self.command_input.delete(0, "end")
        self.append_output(f"\n> {raw_command}\n")

        # Easter Egg Code Trigger
        if raw_command.lower() == "amiafailure":
            self.append_output("Yes. Don't ask again.\n")
            self.play_sound("nope.mp3")
            return

        # Clean Window Exit Commands
        if raw_command.lower() in ["exit", "quit"]:
            self.destroy()
            return

        should_copy = False
        command = raw_command
        if raw_command.startswith("copypop-"):
            should_copy = True
            command = raw_command[8:].strip()

        if command.lower() == "testbar":
            threading.Thread(target=self.run_embedded_progress_bar, daemon=True).start()
            return
        elif command.startswith("cd "):
            try:
                path = command[3:].strip()
                os.chdir(path)
                self.append_output(f"Changed directory to: {os.getcwd()}\n")
            except Exception as e:
                self.append_output(f"Error: {str(e)}\n")
            return
        elif command.lower() in ["clear", "cls"]:
            self.terminal_output.configure(state="normal")
            self.terminal_output.delete("1.0", "end")
            self.terminal_output.configure(state="disabled")
            return

        # --- MULTI-FILE COMMAND EXTENSIONS ---
        elif command.lower() in ["ls", "dir"]:
            try:
                import file_ops
                result = file_ops.list_directory()
                self.append_output(result)
            except ModuleNotFoundError:
                self.append_output("Extension missing: Create 'file_ops.py' and 'utils.py' to use this command.\n")
            return

        elif command.startswith("touch "):
            try:
                import file_ops
                filename = command[6:].strip()
                result = file_ops.make_file(filename)
                self.append_output(result)
            except ModuleNotFoundError:
                self.append_output("Extension missing: Create 'file_ops.py' to use this command.\n")
            return

        elif command.startswith("cat ") or command.startswith("view "):
            try:
                import file_viewer
                filename = command[4:].strip()
                result = file_viewer.read_file_content(filename)
                self.append_output(result)
            except ModuleNotFoundError:
                self.append_output("Extension missing: Create 'file_viewer.py' to use this command.\n")
            return
        # -------------------------------------

        threading.Thread(target=self.execute_system_command, args=(command, should_copy), daemon=True).start()

    def scroll_history_up(self, event):
        if not self.command_history:
            return "break"
        if self.history_index > 0:
            self.history_index -= 1
            self.command_input.delete(0, "end")
            self.command_input.insert(0, self.command_history[self.history_index])
        return "break"

    def scroll_history_down(self, event):
        if not self.command_history:
            return "break"
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_input.delete(0, "end")
            self.command_input.insert(0, self.command_history[self.history_index])
        else:
            self.history_index = len(self.command_history)
            self.command_input.delete(0, "end")
        return "break"

    def run_embedded_progress_bar(self):
        self.after(0, self._create_bar_ui)

    def _create_bar_ui(self):
        self.terminal_output.configure(state="normal")
        self.terminal_output.insert("end", "Downloading Package Assets... ")
        
        self.p_bar = ctk.CTkProgressBar(
            self.terminal_output,
            width=400,
            height=8,
            corner_radius=4,          
            progress_color="#569CD6", 
            fg_color="#2D2D2D"
        )
        self.p_bar.set(0)
        
        self.terminal_output.window_create("end", window=self.p_bar)
        self.terminal_output.insert("end", "   0%", "progress_pct")
        self._conditional_scroll()
        self.terminal_output.configure(state="disabled")

        threading.Thread(target=self._animate_bar, daemon=True).start()

    def _animate_bar(self):
        total_steps = 100
        for i in range(total_steps + 1):
            time.sleep(0.02)
            val = i / total_steps
            self.after(0, self.p_bar.set, val)
            self.after(0, self._update_percentage_label, i)

        self.after(0, self._finish_bar_ui)

    def _update_percentage_label(self, percent):
        self.terminal_output.configure(state="normal")
        formatted = f" {percent:>3}%"
        
        try:
            start_idx = self.terminal_output.index("progress_pct.first")
            end_idx = self.terminal_output.index("progress_pct.last")
            self.terminal_output.delete(start_idx, end_idx)
            self.terminal_output.insert(start_idx, formatted, "progress_pct")
        except tk.TclError:
            self.terminal_output.insert("end", formatted, "progress_pct")
            
        self._conditional_scroll()
        self.terminal_output.configure(state="disabled")

    def _finish_bar_ui(self):
        self.terminal_output.configure(state="normal")
        self.terminal_output.tag_delete("progress_pct")
        self.terminal_output.insert("end", "\nFinished successfully!\n")
        self._conditional_scroll()
        self.terminal_output.configure(state="disabled")
        # Play completion tone
        self.play_sound("jingle.mp3")

    def execute_system_command(self, command, should_copy):
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            full_output = []
            for line in iter(process.stdout.readline, ''):
                self.after(0, self.append_output, line)
                if should_copy: 
                    full_output.append(line)
                
            stderr = process.communicate()[1]
            if stderr: 
                self.after(0, self.append_output, stderr)

            if should_copy and full_output: 
                self.after(0, self.clipboard_append, "".join(full_output))

        except Exception as e:
            self.after(0, self.append_output, f"Execution Error: {str(e)}\n")

    def append_output(self, text):
        self.terminal_output.configure(state="normal")
        self.terminal_output.insert("end", text)
        self._conditional_scroll()
        self.terminal_output.configure(state="disabled")

    def _conditional_scroll(self):
        current_yview = self.terminal_output.yview()
        if current_yview[1] >= 0.98:
            self.terminal_output.see("end")

if __name__ == "__main__":
    app = ModernCMD()
    app.mainloop()