"""GUI module
"""
import sys
import subprocess
import tkinter as tk
from ffmpeg_gui.ffmpeg_wrapper import FFMPEG

try:
    from Tkinter import ttk
    from Tkinter import messagebox
    from Tkinter import filedialog
except ImportError:
    from tkinter import ttk
    from tkinter import messagebox
    from tkinter import filedialog


class GUI(tk.Tk):
    """ TK GUI Object
    """
    # pylint: disable=(too-many-instance-attributes)
    # pylint: disable=(attribute-defined-outside-init)
    # pylint does not play well with tkinter, often thinking variables are declared
    # outside __init__ when they aren't.
    # Also picks up on Widgets defined in their respective draw method

    ffmpeg_task = ''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("FFMPEG GUI tool")
        # self.geometry('800x500')
        self.init_vars()
        self.input_textbox1_var.trace("w", self.enable_start_button)
        self.input_textbox2_var.trace("w", self.enable_start_button)
        self.output_textbox_var.trace("w", self.enable_start_button)
        self.tool = FFMPEG()
        self.options = [('Convert Audio', self.draw_convert_audio, 'Convert and audo file from one format to another'),
                        ('Stitch audio files', self.draw_stitch_audio,
                         'Stitch multiple audio files together into one file'),
                        ('Merge audio and image into video', self.draw_merge_audio_picture,
                         'Create a video with an audio track and static picture'),
                        ('Quit', self._quit, 'Stop having fun')]

    def init_vars(self):
        """ Initialize GUI vars
        """
        self.output_file = str()

        self.input_textbox1_var = tk.StringVar()
        self.input_textbox2_var = tk.StringVar()
        self.output_textbox_var = tk.StringVar()

        self.textbox_width = 80

    def check_if_ffmpeg_installed(self):
        """ Ensure FFMPEG is installed and if not display an error
        """
        try:
            subprocess.call(['ffmpeg'])
        except FileNotFoundError:
            messagebox.showerror('Error', "FFMPEG is not installed\n"
                                          "Macos: 'brew install ffmpeg'\n"
                                          "Linux: 'apt-get install ffmpeg'\n"
                                          "Windows: You're on your own")
            self._quit()

    def draw_main(self):
        """ Draw the main window
        """
        for widget in self.winfo_children():
            widget.destroy()
        # Main GUI has 2 columns
        cols = 2

        # First row
        description_label = ttk.Label(self, text='FFMPEG GUI  -  Maintained by Joshua Thorpe')
        description_label.grid(column=0, row=0, columnspan=cols, pady=40)

        # options is a list of tuples (option_title, option_function, option_description)
        row_buttons = 1
        for row, option in enumerate(self.options):
            op_title, op_func, op_desc = option
            ttk.Button(self, text=op_title, command=op_func).grid(column=0, row=row + row_buttons, sticky='W')
            ttk.Label(self, text=op_desc).grid(column=1, row=row + row_buttons, sticky='W')

    def draw_convert_audio(self):
        """ Draw the window for audio conversion
        """
        for widget in self.winfo_children():
            widget.destroy()

        # number of columns is 3
        col = 3
        op_title, __, op_desc = self.options[0]
        title_label = ttk.Label(self, text=op_title)
        title_label.grid(column=0, row=0, columnspan=col, pady=40)

        description_label = ttk.Label(self, text=op_desc)
        description_label.grid(column=0, row=1, columnspan=col, pady=10)

        # Input File widgets
        ttk.Label(self, text="Input file").grid(column=0, row=2, sticky='W')
        self.input_textbox1 = ttk.Entry(self, textvariable=self.input_textbox1_var, width=self.textbox_width)
        self.input_textbox1.grid(column=1, row=2, padx=5)
        ttk.Button(self, text='Browse', command=lambda: self.get_file(self.input_textbox1_var)).grid(column=2, row=2)

        # Output File Widgets
        ttk.Label(self, text="Output file").grid(column=0, row=3, sticky='W')
        self.output_textbox = ttk.Entry(self, textvariable=self.output_textbox_var, width=self.textbox_width)
        self.output_textbox.grid(column=1, row=3, padx=5)
        ttk.Button(self, text='Browse', command=self.save_file).grid(column=2, row=3)

        # Back button
        ttk.Button(self, text='Back', command=self.draw_main).grid(column=2, row=4, pady=10)

        # Start button
        self.start_button = ttk.Button(self, text='Start')
        self.enable_start_button()
        self.start_button.grid(column=1, row=4)
        self.start_button.config(command=lambda: self.process_start_button_change(self.process_convert_audio))

    def draw_stitch_audio(self):
        """ Draw the window for stitching audio together
        """
        for widget in self.winfo_children():
            widget.destroy()

        # number of columns is 3
        cols = 3
        op_title, __, op_desc = self.options[1]
        title_label = ttk.Label(self, text=op_title)
        title_label.grid(column=0, row=0, columnspan=cols, pady=40)

        description_label = ttk.Label(self, text=op_desc)
        description_label.grid(column=0, row=1, columnspan=cols, pady=10)

        # Audio File 1 widgets
        ttk.Label(self, text="Audio file 1").grid(column=0, row=2, sticky='W')
        self.input_textbox1 = ttk.Entry(self, textvariable=self.input_textbox1_var, width=self.textbox_width)
        self.input_textbox1.grid(column=1, row=2, padx=5)
        ttk.Button(self, text='Browse', command=lambda: self.get_file(self.input_textbox1_var)).grid(column=2, row=2)

        # Audio File 2 Widgets
        ttk.Label(self, text="Audio file 2").grid(column=0, row=3, sticky='W')
        self.input_textbox2 = ttk.Entry(self, textvariable=self.input_textbox2_var, width=self.textbox_width)
        self.input_textbox2.grid(column=1, row=3, padx=5)
        ttk.Button(self, text='Browse', command=lambda: self.get_file(self.input_textbox2_var)).grid(column=2, row=3)

        # Output File Widgets
        ttk.Label(self, text="Output audio file").grid(column=0, row=4, sticky='W')
        self.output_textbox = ttk.Entry(self, textvariable=self.output_textbox_var, width=self.textbox_width)
        self.output_textbox.grid(column=1, row=4, padx=5)
        ttk.Button(self, text='Browse', command=self.save_file).grid(column=2, row=4)

        # Back button
        ttk.Button(self, text='Back', command=self.draw_main).grid(column=2, row=5, pady=10)

        # Start button
        self.start_button = ttk.Button(self, text='Start')
        self.enable_start_button()
        self.start_button.grid(column=1, row=5)
        self.start_button.config(command=lambda: self.process_start_button_change(self.process_stitch_audio))

    def draw_merge_audio_picture(self):
        """ Draw the window for merging audio and picture into a video
        """
        for widget in self.winfo_children():
            widget.destroy()

        # number of columns is 3
        cols = 3
        op_title, __, op_desc = self.options[2]
        title_label = ttk.Label(self, text=op_title)
        title_label.grid(column=0, row=0, columnspan=cols, pady=40)

        description_label = ttk.Label(self, text=op_desc)
        description_label.grid(column=0, row=1, columnspan=cols, pady=10)

        # Audio File widgets
        ttk.Label(self, text="Audio file").grid(column=0, row=2, sticky='W')
        self.input_textbox1 = ttk.Entry(self, textvariable=self.input_textbox1_var, width=self.textbox_width)
        self.input_textbox1.grid(column=1, row=2, padx=5)
        ttk.Button(self, text='Browse', command=lambda: self.get_file(self.input_textbox1_var)).grid(column=2, row=2)

        # Image File Widgets
        ttk.Label(self, text="Image file").grid(column=0, row=3, sticky='W')
        self.input_textbox2 = ttk.Entry(self, textvariable=self.input_textbox2_var, width=self.textbox_width)
        self.input_textbox2.grid(column=1, row=3, padx=5)
        ttk.Button(self, text='Browse', command=lambda: self.get_file(self.input_textbox2_var)).grid(column=2, row=3)

        # Output File Widgets
        ttk.Label(self, text="Output Video file").grid(column=0, row=4, sticky='W')
        self.output_textbox = ttk.Entry(self, textvariable=self.output_textbox_var, width=self.textbox_width)
        self.output_textbox.grid(column=1, row=4, padx=5)
        ttk.Button(self, text='Browse', command=self.save_file).grid(column=2, row=4)

        # Back button
        ttk.Button(self, text='Back', command=self.draw_main).grid(column=2, row=5, pady=10)

        # Start button
        self.start_button = ttk.Button(self, text='Start')
        self.enable_start_button()
        self.start_button.grid(column=1, row=5)
        self.start_button.config(command=lambda: self.process_start_button_change(self.process_merge_audio_picture))

    def process_start_button_change(self, tool):
        """ Change the start button state when processing a job
        """
        self.start_button.config(text='Processing', state='disabled')
        self.after(100, tool)

    def process_convert_audio(self):
        """ Perform the audio conversion and reset start button
        """
        self.tool.convert(self.input_textbox1_var.get(), self.output_textbox_var.get())
        self.start_button.config(text='Start')
        self.init_vars()

    def process_stitch_audio(self):
        """ Perform the audio stitching and reset the start button
        """
        self.tool.stitch([self.input_textbox1_var.get(),
                          self.input_textbox2_var.get()], self.output_textbox_var.get())
        self.start_button.config(text='Start')
        self.init_vars()

    def process_merge_audio_picture(self):
        """ Perform the audio picture merge and reset the start button
        """
        self.tool.video_from_audio_picture(self.input_textbox1_var.get(),
                                           self.input_textbox2_var.get(), self.output_textbox_var.get())
        self.start_button.config(text='Start')
        self.init_vars()

    def _quit(self):
        """ Quit the program
        """
        self.quit()
        self.destroy()
        sys.exit()

    @staticmethod
    def get_file(tk_var_to_change):
        """ Prompt for an input file
        """
        input_file = filedialog.askopenfilename(title="Select a file")
        # If user cancelled, filedialog doesn't return a string
        if isinstance(input_file, str):
            tk_var_to_change.set(input_file)
        else:
            raise ValueError('No file provided')

    def save_file(self):
        """ Prompt for an output file
        """
        output_file = filedialog.asksaveasfilename(title="Select file", filetypes=(("audio files", ["*.mp3", "*.wav"])))
        if isinstance(output_file, str):
            self.output_textbox_var.set(output_file)
        else:
            raise ValueError('No file provided')

    def enable_start_button(self):
        """Callback for a trace on the input_files and output_file variables.
        Enables the start button if both variables contain valid filenames
        """
        in_text = self.input_textbox1_var.get()
        out_text = self.output_textbox_var.get()

        # Offset to account for non-uniform letter spacing
        offset = 0

        if len(in_text) > self.textbox_width + offset or len(out_text) > self.textbox_width + offset:
            self.input_textbox1.config(width=max(len(in_text), len(out_text)))
            try:
                self.input_textbox2.config(width=max(len(in_text), len(out_text)))
            # pylint: disable=(broad-except)
            except Exception as error:
                print(error)
            self.output_textbox.config(width=max(len(in_text), len(out_text)))

        if in_text and out_text:
            self.start_button.config(state='normal')
        else:
            self.start_button.config(state='disabled')
