import os
import sys
import subprocess

def extract_patches(file_content):
    patches = []
    current_patch = []
    in_patch = False
    print(len(file_content))

    for line in file_content.split('\n'):
        if line.startswith('diff --git'):
            if current_patch:
                patches.append('\n'.join(current_patch))
                current_patch = []
            in_patch = True
        elif in_patch and (line.startswith('CondaError:') or line.startswith('no change  ')):
            if current_patch:
                patches.append('\n'.join(current_patch))
            break

        if in_patch:
            current_patch.append(line)

    if current_patch:
        patches.append('\n'.join(current_patch))

    return patches


def extract_rewrite_patch(file_content: str) -> str:
    if '</write_files>' not in file_content:
        return ''
    block = file_content.split('</write_files>')[-2].split('<write_files>')[-1]
    return 'REWRITE\n' + block


def apply_patches(patches, django_dir):
    for patch in patches:
        with open('temp.patch', 'w') as f:
            f.write(patch)

        try:
            subprocess.run(['git', 'apply', 'temp.patch'], cwd=django_dir, check=True)
            print(f"Applied patch {patch.split()[2]} cleanly.")
        except subprocess.CalledProcessError:
            print(f"Failed to apply patch {patch.split()[2]}.")

        os.remove('temp.patch')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <n>")
        sys.exit(1)

    n = sys.argv[1]
    file_path = f"/mnt/{n}.txt"

    with open(file_path, 'r') as f:
        file_content = f.read()

    patches = extract_patches(file_content)
    django_dir = '/django'

    apply_patches(patches, django_dir)