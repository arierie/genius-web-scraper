import re

def clean_lyrics(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = [line.rstrip('\n') for line in infile]

    output_lines = []
    song_started = False
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Remove multi-line section headers: skip from [ to ]
        if line.startswith('['):
            while i < len(lines):
                if lines[i].strip().endswith(']'):
                    i += 1
                    break
                i += 1
            continue
        # Title line
        if line.startswith('<') and line.endswith('>'):
            while output_lines and output_lines[-1] == '':
                output_lines.pop()
            if song_started:
                if output_lines and output_lines[-1] != '':
                    output_lines.append('')
                output_lines.append('-----')
            output_lines.append(line[1:-1].strip())
            song_started = True
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line == '' or (next_line.startswith('[') and next_line.endswith(']')):
                    i += 1
                else:
                    break
            continue
        # Section header (single line)
        if line.startswith('[') and line.endswith(']'):
            if output_lines and output_lines[-1] not in ('', '-----'):
                output_lines.append('')
            i += 1
            continue
        # Blank line
        if line == '':
            if output_lines and output_lines[-1] not in ('', '-----'):
                output_lines.append('')
            i += 1
            continue
        # Bracket merge: ( ... )
        if line.endswith('(') and i+2 < len(lines):
            mid = lines[i+1].strip()
            end = lines[i+2].strip()
            if end == ')':
                merged = line + mid + end
                merged = re.sub(r'\(\s*([^)]*?)\s*\)', r'(\1)', merged)
                output_lines.append(merged)
                i += 3
                continue
        fixed_line = re.sub(r'\(\s*([^)]*?)\s*\)', r'(\1)', lines[i])
        output_lines.append(fixed_line)
        i += 1

    # Remove trailing blank lines at the end of the file
    while output_lines and output_lines[-1] == '':
        output_lines.pop()

    # Write to output file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for idx, line in enumerate(output_lines):
            if line == '-----' or idx == 0:
                outfile.write(line + '\n')
            else:
                # Write blank line as a single newline
                if line == '':
                    outfile.write('\n')
                else:
                    outfile.write(line + '\n')

if __name__ == '__main__':
    clean_lyrics('../beatles_lyrics.txt', '../beatles_lyrics.txt')
