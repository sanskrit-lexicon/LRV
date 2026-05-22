import os
import re

def main():
    # Resolve paths relative to the script directory
    dir_path = os.path.dirname(os.path.abspath(__file__))
    log2_file = os.path.join(dir_path, 'log2.tsv')
    input_file = os.path.join(dir_path, 'temp_lrv_0.txt')
    output_file = os.path.join(dir_path, 'temp_lrv_1.txt')

    if not os.path.exists(log2_file):
        print(f"Error: {log2_file} does not exist. Please run step2.py first.")
        return

    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist.")
        return

    # Read log2.tsv
    print(f"Reading {log2_file}...")
    new_vals_map = {}
    with open(log2_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) == 2:
                l_num, new_val = parts
                new_vals_map[l_num] = new_val

    print(f"Loaded {len(new_vals_map)} updates from log2.tsv.")

    # Read temp_lrv_0.txt
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parse and update entries in place
    # We will locate each entry block and check if its L number needs to be updated.
    current_entry_lines = []
    header_idx = None
    l_number = None

    updated_count = 0
    warning_count = 0

    for idx, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        if line_stripped.startswith('<L>'):
            header_idx = idx
            m = re.search(r'<L>([^<]+)<pc>', line)
            if m:
                l_number = m.group(1).strip()
            else:
                l_number = None
            current_entry_lines = [idx]
        
        elif line_stripped == '<LEND>':
            if l_number and l_number in new_vals_map:
                new_val = new_vals_map[l_number]
                old_headword = new_val.split(',')[0].strip()
                old_target = f"{{#{old_headword}#}}¦"
                new_target = f"{{#{new_val}#}}¦"

                # Find the content line of this entry block
                content_line_idx = None
                for c_idx in current_entry_lines:
                    # Skip the header line itself
                    if c_idx == header_idx:
                        continue
                    if '¦' in lines[c_idx]:
                        content_line_idx = c_idx
                        break
                
                if content_line_idx is not None:
                    orig_line = lines[content_line_idx]
                    if old_target in orig_line:
                        lines[content_line_idx] = orig_line.replace(old_target, new_target, 1)
                        updated_count += 1
                    else:
                        # Fallback: if old_target is not in the line, try a regex replacement of anything inside {#...#} before ¦
                        # E.g. replacing whatever is before ¦
                        content_parts = orig_line.split('¦')
                        before_bar = content_parts[0]
                        if before_bar.startswith('{#') and before_bar.endswith('#}'):
                            new_before_bar = f"{{#{new_val}#}}"
                            content_parts[0] = new_before_bar
                            lines[content_line_idx] = '¦'.join(content_parts)
                            updated_count += 1
                        else:
                            print(f"Warning: Could not replace headword for L={l_number}. Content line: {orig_line.strip()}")
                            warning_count += 1
                else:
                    print(f"Warning: Content line with ¦ not found for L={l_number}")
                    warning_count += 1

            # Reset state for next entry
            current_entry_lines = []
            header_idx = None
            l_number = None
        
        else:
            if header_idx is not None:
                current_entry_lines.append(idx)

    print(f"Successfully updated {updated_count} entries.")
    if warning_count > 0:
        print(f"Warning: {warning_count} updates could not be applied.")

    # Write temp_lrv_1.txt
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("step3.py completed successfully.")

if __name__ == '__main__':
    main()
