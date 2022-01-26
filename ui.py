import urwid
from typing import List

import findlib
import utils
from utils import eprint

class MyEdit(urwid.Edit):
    def keypress(self, size, key):
        if key == 'esc':
             raise urwid.ExitMainLoop()
        return super().keypress(size, key)

class ContentFile(urwid.AttrMap):
    def __init__(self, file: findlib.File, *args, 
            children: List[findlib.Candidate] = []):
        self.w = _ContentFile(file, children)
        super().__init__(self.w, *args)

    def render(self, size, focus):
        # eprint('attrmap', focus)
        if focus:
             self.set_attr_map({None: 'file_f'})                                  
        else:
             self.set_attr_map({None: 'file'})                                  
        return super().render(size, focus)

    def get_widgets(self) -> List[urwid.Widget]:
        return [self, *self.w.children]

class _ContentFile(urwid.Columns):
    def __init__(self, file: findlib.File, children: List[findlib.Candidate]):
        from urwid import Text
        self.file = file
        # eprint('file active', file.active)
        self.sel_txt = Text(utils.get_select_text(file.active))
        self.fpath = Text(str(file.path))
        self.children = [ContentText(cand, 'def') for cand in children]
        super().__init__([
            ('weight', 1, self.sel_txt), 
            ('weight', 25, self.fpath)] )
        self._selectable = True

    def rows(self, size, focus):
        if focus:
            self.fpath.set_wrap_mode('space')
        else:
            self.fpath.set_wrap_mode('ellipsis')

        return super().rows(size, focus)

    def refresh(self):
        self.sel_txt.set_text(utils.get_select_text(self.file.active))
        for w in self.children:
            w.refresh()

    def keypress(self, size, key):
        # eprint('column', key)
        if key == ' ':
            # self.sel_txt.set_text(f'[{"*" if self.sel else " "}]')
            # eprint('file active before toggle', self.file.active)
            self.file.toggle_sel()
            # eprint('file active after toggle', self.file.active)
            self.refresh()
        else:
            return key

class ContentText(urwid.AttrMap):
    def __init__(self, cand: findlib.Candidate, *args):
        # eprint('ctxtext args', cand, *args)
        self.w = _ContentText(cand)
        super().__init__(self.w, *args)

    def render(self, size, focus):
        if focus:
             self.set_attr_map({None: 'hl'})                                  
        else:
             self.set_attr_map({None: 'def'})                                  

        return super().render(size, focus)

    def refresh(self):
        self.w.refresh()

class _ContentText(urwid.Columns):
    def __init__(self, cand: findlib.Candidate):
        from urwid import Text
        self.cand = cand
        self.sel_txt = Text(utils.get_select_text(cand.active) )
        self.line = Text(str(cand.line_no) )
        self.orig = urwid.AttrMap(Text(cand.match), 'orig')
        self.repl = urwid.AttrMap(Text(cand.replace), 'repl')
        super().__init__([
            ('weight', 1, self.sel_txt), 
            ('weight', 1, self.line), 
            ('weight', 8, self.orig), 
            ('weight', 8, self.repl)])
        self._selectable = True

    def rows(self, size, focus):
        if focus:
            self.orig.set_attr_map({None: 'orig_f'})
            self.orig.original_widget.set_wrap_mode('space')

            self.repl.set_attr_map({None: 'repl_f'})
            self.repl.original_widget.set_wrap_mode('space')
        else:
            self.orig.set_attr_map({None: 'orig'})
            self.orig.original_widget.set_wrap_mode('ellipsis')

            self.repl.set_attr_map({None: 'repl'})
            self.repl.original_widget.set_wrap_mode('ellipsis')
        return super().rows(size, focus)

    def refresh(self):
        self.sel_txt.set_text(utils.get_select_text(self.cand.active) )

    def keypress(self, size, key):
        # eprint('column', key)
        if key == ' ':
            self.cand.toggle_sel()
            self.refresh()
        else:
            return key

class MyListBox(urwid.ListBox):
    def keypress(self, size, key):
        # import pudb; pu.db
        # eprint('listbox', key)
        # eprint(self.get_focus())
        if key == 'esc':
            raise urwid.ExitMainLoop()
        return super().keypress(size, key)

