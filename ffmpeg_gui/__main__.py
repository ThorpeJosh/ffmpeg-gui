""" Entrypoint
"""
from ffmpeg_gui.gui import GUI


def run():
    """ Main loop
    """
    root = GUI()
    root.draw_main()
    root.check_if_ffmpeg_installed()
    root.mainloop()


if __name__ == '__main__':
    run()
