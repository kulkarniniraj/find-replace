def get_select_text(active: bool) -> str:
    if active:
        return '[*]'
    return '[ ]'

def eprint(*args):
    with open('log.txt', 'a') as f:
        for arg in args:
            f.write(f'{arg}, ')
        f.write('\n')
