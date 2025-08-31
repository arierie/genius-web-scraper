import re

def clean_lyrics_further(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile:
        content = infile.read()
    songs = [s.strip() for s in content.split('-----')]
    cleaned_songs = []
    for song in songs:
        lines = [line.rstrip() for line in song.splitlines()]
        # Remove leading/trailing blank lines
        while lines and lines[0].strip() == '':
            lines = lines[1:]
        while lines and lines[-1].strip() == '':
            lines = lines[:-1]
        if not lines:
            continue
        # Remove blank lines after title
        title = lines[0]
        rest = lines[1:]
        while rest and rest[0].strip() == '':
            rest = rest[1:]
        # Remove fully parenthetical/bracketed lines
        filtered = [title]
        for line in rest:
            l = line.strip()
            if re.fullmatch(r'\([^(]*\)', l) or re.fullmatch(r'\[[^\[]*\]', l):
                continue
            filtered.append(line)
        # Remove trailing blank lines
        while filtered and filtered[-1].strip() == '':
            filtered.pop()
        cleaned_songs.append('\n'.join(filtered))
    # Write with a blank line before each separator, but not after
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for idx, song in enumerate(cleaned_songs):
            if idx > 0:
                outfile.write('\n\n-----\n')
            outfile.write(song)
    print(f"Further cleaned lyrics written to {output_path}")
    print(f"Further cleaned lyrics written to {output_path}")

if __name__ == '__main__':
    clean_lyrics_further('../beatles_lyrics.txt', '../beatles_lyrics.txt')
