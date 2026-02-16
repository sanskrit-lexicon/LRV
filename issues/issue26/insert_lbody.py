import re
import sys
import codecs

import re

def process_lbody_final(text):
    # Split text into blocks based on <LEND>
    blocks = text.strip().split("<LEND>")
    processed_blocks = []
    
    parent_registry = {}
    report = {
        "already_tagged": [],
        "replacements": [],
        "mismatches": [],
        "orphans": []
    }

    # --- Pass 1: Build the Registry ---
    for block in blocks:
        if not block.strip(): continue
        
        # Extract ID from <L>ID<pc>
        id_match = re.search(r'<L>([^<]+)', block)
        if not id_match: continue
        full_id = id_match.group(1).strip()
        
        # Check for existing Lbody
        if "{{Lbody=" in block:
            report["already_tagged"].append(full_id)
            continue
            
        # Register parents (IDs without a dot)
        if "." not in full_id:
            if "¦" in block:
                # Content is everything after the broken bar
                content_after = block.split("¦", 1)[1].strip()
                # Normalize whitespace for reliable matching
                parent_registry[full_id] = " ".join(content_after.split())

    # --- Pass 2: Process and Replace ---
    for block in blocks:
        if not block.strip(): continue
        
        id_match = re.search(r'<L>([^<]+)', block)
        full_id = id_match.group(1).strip()
        
        # Skip parents and already tagged entries
        if "." not in full_id or full_id in report["already_tagged"]:
            processed_blocks.append(block.strip())
            continue
            
        # Process Children
        base_id = full_id.split('.')[0]
        if "¦" in block:
            child_content = " ".join(block.split("¦", 1)[1].strip().split())
            
            if base_id in parent_registry:
                if child_content == parent_registry[base_id]:
                    # PERFORM REPLACEMENT
                    # Keep the header (first line), add Lbody tag
                    lines = block.strip().split('\n')
                    header = lines[0]
                    new_block = f"{header}\n{{{{Lbody={base_id}}}}}"
                    processed_blocks.append(new_block)
                    report["replacements"].append(f"{full_id} -> {base_id}")
                else:
                    report["mismatches"].append(full_id)
                    processed_blocks.append(block.strip())
            else:
                report["orphans"].append(full_id)
                processed_blocks.append(block.strip())
        else:
            processed_blocks.append(block.strip())

    # Reconstruct the text
    final_text = "\n<LEND>\n".join(processed_blocks) + "\n<LEND>\n"
    
    # --- PRINT REPORT ---
    print("--- VALIDATION REPORT ---")
    print(f"Already Tagged:    {len(report['already_tagged'])}")
    for item in report['already_tagged']: print(f"  [-] {item}")
    
    print(f"\nReplacements:      {len(report['replacements'])}")
    for item in report['replacements']: print(f"  [✓] {item}")
    
    print(f"\nMismatches:        {len(report['mismatches'])}")
    for item in report['mismatches']: print(f"  [!] {item} (Content differs from parent)")
    
    print(f"\nOrphans:           {len(report['orphans'])}")
    for item in report['orphans']: print(f"  [?] {item} (Parent not found)")
    print("-" * 25)

    return final_text

if __name__=="__main__":
    filein = sys.argv[1]
    fileout = sys.argv[2]
    with codecs.open(filein, 'r', 'utf-8') as fin:
        data = fin.read()
    processed_output = process_lbody_final(data)
    with codecs.open(fileout, 'w', 'utf-8') as fout:
        fout.write(processed_output)
