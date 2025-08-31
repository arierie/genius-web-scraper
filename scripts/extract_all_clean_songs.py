import re

def extract_all_clean_songs(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile:
        content = infile.read()
    songs = [s.strip() for s in content.split('-----')]
    clean_songs = []
    seen_titles = set()
    for song in songs:
        lines = [line.strip() for line in song.splitlines() if line.strip()]
        if not lines:
            continue
        title = lines[0]
        if len(title) < 3 or not re.match(r'^[A-Za-z0-9!?.\'’\- ]+$', title):
            continue
        if title in seen_titles:
            continue
        if len(lines) < 5:
            continue
        bracket_lines = sum(1 for l in lines if l.startswith('[') or l.startswith('('))
        if bracket_lines > len(lines) // 2:
            continue
        clean_songs.append(song.strip())
        seen_titles.add(title)
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write('\n\n-----\n\n'.join(clean_songs))
    print(f"Extracted {len(clean_songs)} clean songs to {output_path}")

if __name__ == '__main__':
    extract_all_clean_songs('../beatles_lyrics.txt', '../beatles_lyrics.txt')
