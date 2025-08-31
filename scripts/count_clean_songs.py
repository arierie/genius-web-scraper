
import re
import sys

def count_clean_songs(input_path):
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
        clean_songs.append(title)
        seen_titles.add(title)
    print(f"Total clean songs found: {len(clean_songs)}")
    return clean_songs

if __name__ == '__main__':
    if len(sys.argv) > 1:
        count_clean_songs(sys.argv[1])
    else:
        print('Usage: python count_clean_songs.py <input_file>')
