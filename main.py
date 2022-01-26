import urwid
from pathlib import Path
import easydict as ed
from typing import List

import findlib
import utils
from utils import eprint
from ui import ContentFile, ContentText, MyEdit, MyListBox

STATE = ed.EasyDict()

class InitialScreen:
    class MyListBox(urwid.ListBox):
        def keypress(self, size, key):
            # eprint('got key', key)
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
    def __init__(self, fol: findlib.Folder):
        self.folder = fol

    def build_row(self, candidate: findlib.Candidate)->urwid.Widget:
        # return CAttrMap(ContentText(candidate), 'def')
        return ContentText(candidate, 'def')

    def build_file(self, fil: findlib.File) -> List[urwid.Widget]:
        lst = [
            ContentFile(fil, 'def'),
            *[self.build_row(cand) for cand in fil.candidates]
            ]

        # eprint('build file lst', lst)
        return lst

    def build(self):
        widgets = []
        for fil in self.folder.contents:
            widgets.extend(ContentFile(fil, 'def', children=fil.candidates)
                    .get_widgets())
        lst = MyListBox(widgets)
        # w = ContentFile(fil, 'def')
        # lst = MyListBox(

        frm = lst
        frm = urwid.LineBox(frm)
        return frm

def main():
    loop = urwid.MainLoop(InitialScreen().build(), palette=[
        ('def', 'default', 'default'),
        ('orig', 'dark red', 'default'),
        ('orig_f', 'dark red', 'dark gray'),
        ('repl', 'light green', 'default'),
        ('repl_f', 'light green', 'dark gray'),
        ('hl', 'default', 'dark gray'),
        ('file', 'default', 'light blue'),
        ('file_f', 'default', 'dark blue'),
        ])
    STATE.loop = loop
    loop.run()

if __name__ == '__main__':
    main()
