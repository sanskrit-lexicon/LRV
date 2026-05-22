import os
import re
from indic_transliteration import sanscript

def main():
    # Resolve paths relative to the script directory
    dir_path = os.path.dirname(os.path.abspath(__file__))
    log1_file = os.path.join(dir_path, 'log1.tsv')
    log2_file = os.path.join(dir_path, 'log2.tsv')
    vaidya_file = os.path.join(dir_path, '..', '..', 'glacier', 'LR_Vaidya_Main_proofed_20220920.txt')
    temp0_file = os.path.join(dir_path, 'temp_lrv_0.txt')
    temp1_file = os.path.join(dir_path, 'temp_lrv_1.txt')

    if not os.path.exists(log1_file):
        print(f"Error: {log1_file} does not exist. Please run step1.py first.")
        return

    if not os.path.exists(log2_file):
        print(f"Error: {log2_file} does not exist. Please run step2.py first.")
        return

    if not os.path.exists(vaidya_file):
        print(f"Error: {vaidya_file} does not exist.")
        return

    if not os.path.exists(temp0_file):
        print(f"Error: {temp0_file} does not exist.")
        return

    # 1. Read log1.tsv
    print(f"Reading {log1_file}...")
    log1_entries = {}
    with open(log1_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 3:
                l_num, prefix, headword = parts
                log1_entries[l_num] = (prefix, headword)

    print(f"Loaded {len(log1_entries)} parent mappings from log1.tsv.")

    # 2. Read existing log2.tsv
    print(f"Reading existing {log2_file}...")
    log2_entries = {}
    with open(log2_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                l_num, val = parts
                log2_entries[l_num] = val

    print(f"Loaded {len(log2_entries)} entries from existing log2.tsv.")

    # 3. Find missing L numbers
    missing_l = sorted([l for l in log1_entries if l not in log2_entries])
    print(f"Found {len(missing_l)} parent entries missing from log2.tsv.")

    # 4. Read Vaidya database
    print(f"Reading Vaidya database {vaidya_file}...")
    vaidya_map = {}
    with open(vaidya_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if parts:
                vaidya_map[parts[0]] = parts

    # 5. Extract and supply ring-symbol (˚) suffix entries
    supplied_count = 0
    for l_num in missing_l:
        parts = vaidya_map.get(l_num)
        if not parts:
            continue
        
        # Check for suffix column starting with ˚
        suffix_str = None
        for part in parts[1:]:
            part_stripped = part.strip()
            clean_part = re.sub(r'<[^>]+>', '', part_stripped).strip()
            if clean_part.startswith('˚'):
                suffix_str = clean_part
                break
        
        if suffix_str:
            # Transliterate suffix from Devanagari to SLP1
            slp1_suffix = sanscript.transliterate(suffix_str, sanscript.DEVANAGARI, sanscript.SLP1)
            
            # Find ring-prefix from parent headword
            prefix, parent_headword = log1_entries[l_num]
            if '˚' in parent_headword:
                ring_prefix = parent_headword.split('˚')[0].strip()
                new_val = slp1_suffix.replace('˚', ring_prefix + '˚', 1)
                log2_entries[l_num] = new_val
                supplied_count += 1
            else:
                # Fallback to hyphen prefix
                if '-' in parent_headword:
                    hyphen_prefix = parent_headword.split('-')[0].strip()
                    new_val = slp1_suffix.replace('˚', hyphen_prefix + '˚', 1)
                    log2_entries[l_num] = new_val
                    supplied_count += 1

    print(f"Successfully supplied {supplied_count} missing entries.")

    # 6. Overwrite log2.tsv with all 1,908 unified entries
    print(f"Writing all unified entries to {log2_file}...")
    with open(log2_file, 'w', encoding='utf-8') as f:
        for l_num in sorted(log2_entries.keys()):
            f.write(f"{l_num}\t{log2_entries[l_num]}\n")
    
    print(f"Total entries in unified log2.tsv: {len(log2_entries)}")

    # 7. Apply updates from log2.tsv to temp_lrv_0.txt and save to temp_lrv_1.txt
    print(f"Applying all unified updates from log2.tsv to {temp0_file}...")
    with open(temp0_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

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
            if l_number and l_number in log2_entries:
                new_val = log2_entries[l_number]
                old_headword = new_val.split(',')[0].strip()
                old_target = f"{{#{old_headword}#}}¦"
                new_target = f"{{#{new_val}#}}¦"

                content_line_idx = None
                for c_idx in current_entry_lines:
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
                        # Fallback regex replacement
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

            current_entry_lines = []
            header_idx = None
            l_number = None
        else:
            if header_idx is not None:
                current_entry_lines.append(idx)

    print(f"Successfully applied {updated_count} updates in temp_lrv_1.txt.")
    if warning_count > 0:
        print(f"Warning: {warning_count} updates could not be applied.")

    # Write the complete result to temp_lrv_1.txt
    print(f"Writing output to {temp1_file}...")
    with open(temp1_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("step4.py completed successfully.")

if __name__ == '__main__':
    main()
