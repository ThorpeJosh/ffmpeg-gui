""" FFMPEG wrapper
"""
import os
import subprocess
try:
    from Tkinter import messagebox
except ImportError:
    from tkinter import messagebox


class FFMPEG:
    """ FFMPEG wrapper object
    """
    def __init__(self):
        self._command = ['ffmpeg']
        self.error_message = 'FFMPEG failed\n' \
                             'This may be due to this tool being in the pre-release stage,\n' \
                             'or because the filename and extensions are incorrect.\n' \
                             'Please see terminal for details'

    def convert(self, input_file, output_file):
        """ffmpeg -i input -vn output  """
        self._command.append('-y')
        self._command.append('-i')
        self._command.append(input_file)
        self._command.append('-vn')
        self._command.append(output_file)
        fail = subprocess.call(self._command)
        if fail:
            messagebox.showerror('Error', self.error_message)
        else:
            messagebox.showinfo('Finished', f'Job successful, please find output at\n{output_file}')
        self.__init__()

    def stitch(self, input_files_list, output_file):
        """ffmpeg -f concat -safe 0 -i tmplist.txt -c copy output  """
        with open('tmplist.txt', 'w', encoding='utf-8') as file:
            for in_file in input_files_list:
                # pylint: disable=(consider-using-f-string)
                file.write('file {}\n'.format(in_file.replace(' ', r'\ ')))
        self._command.append('-y')
        self._command.append('-f')
        self._command.append('concat')
        self._command.append('-safe')
        self._command.append('0')
        self._command.append('-i')
        self._command.append('tmplist.txt')
        self._command.append('-c')
        self._command.append('copy')
        self._command.append(output_file)

        fail = subprocess.call(self._command)
        if fail:
            messagebox.showerror('Error', self.error_message)
        else:
            messagebox.showinfo('Finished', f'Job successful, please find output at\n{output_file}')
        self.__init__()
        os.remove('tmplist.txt')

    def video_from_audio_picture(self, audio_file, image_file, output_file):
        """fffmpeg -loop 1 -i image_file -i audio_file -tune stillimage -shortest output """
        self._command.append('-y')
        self._command.append('-loop')
        self._command.append('1')
        self._command.append('-i')
        self._command.append(image_file)
        self._command.append('-i')
        self._command.append(audio_file)
        self._command.append('-tune')
        self._command.append('stillimage')
        self._command.append('-shortest')
        self._command.append(output_file)

        fail = subprocess.call(self._command)
        if fail:
            messagebox.showerror('Error', self.error_message)
        else:
            messagebox.showinfo('Finished', f'Job successful, please find output at\n{output_file}')
        self.__init__()
