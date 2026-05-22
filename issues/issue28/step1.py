import os
import re

def main():
    # Resolve paths relative to the script directory
    dir_path = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(dir_path, 'temp_lrv_0.txt')
    output_file = os.path.join(dir_path, 'log1.tsv')

    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parse entries
    entries = []
    current_entry_lines = []
    for idx, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        current_entry_lines.append((idx, line))
        if line_stripped == '<LEND>':
            entries.append(current_entry_lines)
            current_entry_lines = []

    print(f"Parsed {len(entries)} entries.")

    # Create a map of L-number to entry
    l_map = {}
    for entry in entries:
        header_line = entry[0][1]
        m = re.search(r'<L>([^<]+)<pc>', header_line)
        if m:
            l_num = m.group(1).strip()
            l_map[l_num] = entry

    # Identify places with Lbody component
    log_records = []
    seen_parents = set()

    for entry in entries:
        # Check if this entry has an Lbody tag
        entry_text = "".join([line for _, line in entry])
        m = re.search(r'\{\{Lbody=([^}]+)\}\}', entry_text)
        if m:
            parent_l = m.group(1).strip()
            if parent_l in seen_parents:
                continue

            # Look up parent entry
            parent_entry = l_map.get(parent_l)
            if not parent_entry:
                print(f"Warning: Parent L={parent_l} not found for entry L={re.search(r'<L>([^<]+)', entry[0][1]).group(1)}")
                continue

            # Extract parent headword
            # The content line of the parent is usually the second line of the parent entry
            # Let's search all lines of the parent entry for the one containing '¦'
            content_line = None
            for idx, line in parent_entry:
                if '¦' in line:
                    content_line = line
                    break

            if content_line:
                before_bar = content_line.split('¦')[0].strip()
                clean_word = before_bar.replace('{#', '').replace('#}', '').strip()
                if '-' in clean_word:
                    prefix = clean_word.split('-')[0].strip()
                    log_records.append((parent_l, prefix, clean_word))
                    seen_parents.add(parent_l)
            else:
                # No content line with '¦' found (could be another sub-entry itself, or empty)
                pass

    print(f"Found {len(log_records)} unique parent entries with hyphens.")

    # Write log1.tsv
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for rec in log_records:
            f.write(f"{rec[0]}\t{rec[1]}\t{rec[2]}\n")

    print("step1.py completed successfully.")

if __name__ == '__main__':
    main()
