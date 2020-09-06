#! /usr/bin/python3
from __future__ import annotations


def get_names(path: str) -> List[str]:
    names = list()
    with open(path, 'r') as f:
        for l in f.readlines():
            n = l.strip()
            if n:
                names.append(n)
    print("Found %i names in %s" % (len(names), path))
    return names


def load_template(svg_file: str) -> str:
    assert svg_file.endswith(".svg")
    as_string : str
    with open(svg_file, 'r') as f:
        as_string = f.read()
    return as_string

def _chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    # https://stackoverflow.com/a/312464/3442125
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def create_laser_files(names: List[str], template: str, placeholder: str, file_prefix: str = 'new_template_'):
    object_cnt = template.count(placeholder) 
    
    for i, l in enumerate(_chunks(names, object_cnt)):
        new_template = template
        
        truncated = len(l) < object_cnt
        if truncated:
            l += ["XXXXXXXXXXXXX"] * (object_cnt-len(l))       # replace placeholder in unused spots with test that's easy to spot
            new_path = "%s%i_truncated.svg" % (file_prefix, i) # change filename to make the file easier to recognize
        else:
            new_path = "%s%i.svg" % (file_prefix, i)

        for name in l:
            # only replace first occurence, not really efficient, but readable
            new_template = new_template.replace(placeholder, name, 1) 
        
        with open(new_path, 'w') as f:
            f.write(new_template)
        
    print("Created %i files" % (i+1))


if __name__ == "__main__":
    names = get_names("names.txt")
    placeholder = "GUEST"
    template = load_template("birthday_template.svg")
    create_laser_files(names, template, placeholder)
    