from pathlib import Path
import re
from typing import Union, List, Iterable, Tuple
from dataclasses import dataclass
from result import Result, Ok, Err

@dataclass
class Candidate:
    line_no: int
    match: str
    replace: str
    active: bool
    
    def toggle_sel(self):
        self.active = not self.active

    def __repr__(self):
        return f'{self.line_no}: {self.match} <--> {self.replace}'

@dataclass
class File:
    name: str
    path: Path
    text: str
    candidates: List[Candidate]
    active: bool

    def toggle_sel(self):
        for c in self.candidates:
            c.toggle_sel()
        
    def __repr__(self):
        return f'{self.name}:\n' + "\n".join([str(c) for c in self.candidates])

@dataclass
class Folder: 
    name: str
    path: Path
    contents: List[Union[File, 'Folder']] 
    active: bool
        
    def toggle_sel(self):
        for c in self.contents:
            c.toggle_sel()

    def __repr__(self):
        return f'{self.name}: \n' + '\n'.join([str(c) for c in self.contents])

def get_folder_contents(p: Path) -> Iterable:
    return p.glob('**/*')

def filter_folder_contents(cont: Iterable, pattern: str) -> Iterable:
    return filter(lambda x: re.search(pattern, str(x)) is not None, cont)

def sep_file_folder(cont: Iterable) -> Tuple[Iterable, Iterable]:
    ifile = filter(lambda x: x.is_dir() == False, cont)
    ifold = filter(lambda x: x.is_dir() == True, cont)
    return (ifile, ifold)

def process_file(f: Path, search: str, replace: str) -> Result[File, str]:
    try:
        txt = f.open().read()
        lines = txt.split('\n')
        rlines = [re.sub(search, replace, line) for line in lines]
        diff = filter(lambda tup: tup[1] != tup[2], zip(range(1, len(lines) + 1), lines, rlines))
        candidates = [Candidate(d[0], d[1], d[2], False) for d in diff]
        return Ok(File(f.name, f, '', candidates, False))
    except Exception as e:
        return Err(str(e))

def find(root: Path, file_re: str, txt_re: str, replace_re: str) -> Folder:
    f = Folder(root.name, root, [], True)
    cont = filter_folder_contents(get_folder_contents(root), file_re)
    files, folders = sep_file_folder(cont)
    files = map(lambda f: f.ok(), 
                filter(lambda f: (f.is_ok()) and (f.ok().candidates != []),
                   map(lambda x: process_file(x, txt_re, replace_re), files) ) )
    f.contents = list(files) # + list(folders)
    return f

