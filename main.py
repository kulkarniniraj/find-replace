import urwid
from pathlib import Path
import easydict as ed
from typing import List
import time

import findlib
import utils
from utils import eprint
from ui import ContentFile, ContentText, MyEdit, MyListBox

STATE = ed.EasyDict()

class InitialScreen:
    class MyListBox(urwid.ListBox):
        def keypress(self, size, key):
            eprint('got key', key)
            if key == 'enter':
                # r = findlib.find(Path('.'), '', 'import', 'export')
                eprint('body', self.body)
                r = findlib.find(
                        Path(self.body[1].edit_text),
                        self.body[3].edit_text,
                        self.body[5].edit_text,
                        self.body[7].edit_text,
                        # self.body[3].get_text()[0],
                        # '.*.py',
                        # 'import',
                        # 'export'
                        )
                STATE.loop.widget = ResultScreen(r).build()
            elif key == 'tab':
                return super().keypress(size, 'down')
            else:
                return super().keypress(size, key)

    def build(self):
        self.root_edit = MyEdit("Enter root folder: ")
        self.file_search_edit = MyEdit("File search patterns(regex): ")
        self.text_search_edit = MyEdit("Text search pattern(regex): ")
        self.text_replace_edit = MyEdit("Text search pattern(regex): ")
        lst = self.MyListBox([
            urwid.Text(''), self.root_edit, 
            urwid.Text(''), self.file_search_edit,
            urwid.Text(''), self.text_search_edit, 
            urwid.Text(''), self.text_replace_edit])

        frm = lst
        frm = urwid.LineBox(frm)
        frm = urwid.Padding(frm, urwid.CENTER, ('relative', 70)) 
        frm = urwid.Filler(frm, height = 15) 
        frm = urwid.LineBox(frm)
        return frm

class ResultScreen:
    class MyXListBox(MyListBox):
        def __init__(self, on_enter_func, *args):
            self.enter = on_enter_func
            super().__init__(*args)

        def keypress(self, size, key):
            if key == 'enter':
                self.enter()
            else:
                return super().keypress(size, key)

    def __init__(self, fol: findlib.Folder):
        self.folder = fol

    def apply_change(self, _):
        pass

    def discard_change(self, _):
        STATE.loop.widget = self.bg

    def apply_overlay(self):
        STATE.loop.widget = urwid.Overlay(self.overlay, 
                self.bg, 'center', 50, 'middle', 7)

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
        t1 = time.time()
        widgets = []
        for fil in self.folder.contents:
            widgets.extend(ContentFile(fil, 'def', children=fil.candidates)
                    .get_widgets())
        t2 = time.time()
        lst = self.MyXListBox(self.apply_overlay, widgets)
        t3 = time.time()

        frm = lst
        frm = urwid.LineBox(frm)
        self.bg = frm
        t4 = time.time()
        # eprint('build time', t2-t1, t3-t1, t4-t1)

        over_frm = urwid.Text("Are you sure about applying changes?")
        over_frm = urwid.ListBox([
            urwid.Text("Are you sure about applying changes?"),
            urwid.Text(""),
            urwid.Columns([
                urwid.Button('Apply Changes', self.apply_change),
                urwid.Button('Cancel', self.discard_change),

                ], dividechars=3)
            ])
        over_frm = urwid.LineBox(over_frm)
        over_frm = urwid.BoxAdapter(over_frm, 6)
        over_frm = urwid.AttrMap(over_frm, 'confirm')
        over_frm = urwid.Padding(over_frm, 'center', width=50)
        over_frm = urwid.Filler(over_frm, 'middle', height='pack')
        self.overlay = over_frm
        # frm = urwid.Overlay(over_frm, frm, 'center', 120, 'middle', 100)
        return frm

class ConfirmScreen:
    def __init__(self):
        pass

    def build(self):
        pass

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
        ('confirm', 'white', 'dark blue'),
        ])
    STATE.loop = loop
    loop.run()

if __name__ == '__main__':
    main()
