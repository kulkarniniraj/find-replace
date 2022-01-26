import urwid
from pathlib import Path
import easydict as ed

import findlib

STATE = ed.EasyDict()

def eprint(*args):
    with open('log.txt', 'a') as f:
        for arg in args:
            f.write(f'{str(arg)}\n')

class MyEdit(urwid.Edit):
    def keypress(self, size, key):
        if key == 'esc':
             raise urwid.ExitMainLoop()
        return super().keypress(size, key)


class InitialScreen:
    class MyListBox(urwid.ListBox):
        def keypress(self, size, key):
            eprint('got key', key)
            if key == 'enter':
                r = findlib.find(Path('.'), '', 'import', 'export')
                STATE.loop.widget = ResultScreen(r).build()
            return super().keypress(size, key)

    def build(self):
        root_edit = MyEdit("Enter root folder: ")
        file_search_edit = MyEdit("File search patterns(regex): ")
        text_search_edit = MyEdit("Text search pattern(regex): ")
        text_replace_edit = MyEdit("Text search pattern(regex): ")
        lst = self.MyListBox([
            urwid.Text(''), root_edit, 
            urwid.Text(''), file_search_edit,
            urwid.Text(''), text_search_edit, 
            urwid.Text(''), text_replace_edit])

        frm = lst
        frm = urwid.LineBox(frm)
        frm = urwid.Padding(frm, urwid.CENTER, ('relative', 70)) 
        frm = urwid.Filler(frm, height = 15) 
        frm = urwid.LineBox(frm)
        return frm

class ResultScreen:
    class MyListBox(urwid.ListBox):
        def keypress(self, size, key):
            eprint('got key', key)
            if key == 'esc':
                STATE.loop.widget = InitialScreen().build()
                # raise urwid.ExitMainLoop()
            return super().keypress(size, key)

    def __init__(self, fol: findlib.Folder):
        self.folder = fol

    def build_row(self, candidate: findlib.Candidate)->urwid.Widget:
        return urwid.Columns([
            ('weight', 1, urwid.Text('*')),
            ('weight', 1, urwid.Text('1.')),
            ('weight', 10, urwid.Text(('orig', candidate.match) ) ),
            ('weight', 10, urwid.Text([('diff', candidate.replace)] ) )
        ]) 

    def build_file(self, fil: findlib.File) -> urwid.Widget:
        w1 = urwid.Text(f'{fil.path}')
        w1 = urwid.AttrMap(w1, 'header')
        _w2 = [self.build_row(cand) for cand in fil.candidates]
        w2 = urwid.Pile(_w2)
        return urwid.Pile([w1, w2])

    def build(self):
        palette = [
                ('orig', 'dark red', 'default'),
                ('diff', 'dark green', 'default'),
                ('active', 'black', 'light gray'),
                ('header', 'default', 'dark magenta')
                ]

        STATE.loop.screen.register_palette(palette)
        # w2 = urwid.AttrMap(w2, 'active')
        return self.MyListBox([self.build_file(fil) for fil in self.folder.contents])
        # return urwid.Pile([self.build_file(fil) for fil in self.folder.contents])

def main():
    loop = urwid.MainLoop(InitialScreen().build())
    STATE.loop = loop
    STATE.cols, STATE.rows = loop.screen.get_cols_rows()
    eprint('state', STATE)
    loop.run()


if __name__ == '__main__':
    f = findlib.find(Path('.'), 'py$', 'urwid', 'mywid')
    # print(f)
    main()
