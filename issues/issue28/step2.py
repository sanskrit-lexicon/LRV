import os
import re
from indic_transliteration import sanscript

def main():
    # Resolve paths relative to the script directory
    dir_path = os.path.dirname(os.path.abspath(__file__))
    log1_file = os.path.join(dir_path, 'log1.tsv')
    vaidya_file = os.path.join(dir_path, '..', '..', 'glacier', 'LR_Vaidya_Main_proofed_20220920.txt')
    output_file = os.path.join(dir_path, 'log2.tsv')

    if not os.path.exists(log1_file):
        print(f"Error: {log1_file} does not exist. Please run step1.py first.")
        return

    if not os.path.exists(vaidya_file):
        print(f"Error: {vaidya_file} does not exist.")
        return

    # Read log1.tsv
    print(f"Reading {log1_file}...")
    parent_map = {}
    with open(log1_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) == 3:
                l_num, prefix, full_headword = parts
                parent_map[l_num] = (prefix, full_headword)

    print(f"Loaded {len(parent_map)} parent entries mapping from log1.tsv.")

    # Read Vaidya file and match L numbers
    print(f"Processing {vaidya_file}...")
    log2_records = []
    
    with open(vaidya_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if not parts:
                continue
            
            vaidya_l = parts[0].strip()
            if vaidya_l in parent_map:
                prefix, full_headword = parent_map[vaidya_l]
                
                # Search for suffix column
                suffix_str = None
                for part in parts[1:]:
                    part_stripped = part.strip()
                    # Strip any HTML tags (e.g. <b>, </b>)
                    clean_part = re.sub(r'<[^>]+>', '', part_stripped).strip()
                    if clean_part.startswith('-'):
                        suffix_str = clean_part
                        break
                
                if suffix_str:
                    # Transliterate from Devanagari to SLP1
                    slp1_suffix = sanscript.transliterate(suffix_str, sanscript.DEVANAGARI, sanscript.SLP1)
                    
                    # Substitute the first hyphen with the prefix
                    new_val = slp1_suffix.replace('-', prefix + '-', 1)
                    log2_records.append((vaidya_l, new_val))
                else:
                    print(f"Warning: Suffix column not found in Vaidya file for L={vaidya_l}")

    print(f"Generated {len(log2_records)} suffix records.")

    # Write log2.tsv
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for l_num, val in log2_records:
            f.write(f"{l_num}\t{val}\n")

    print("step2.py completed successfully.")

if __name__ == '__main__':
    main()
