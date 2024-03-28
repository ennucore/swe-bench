import json
import os
from apply_patches import extract_patches, extract_rewrite_patch

SWEB_FILENAME = 'swe-bench.json'
sweb = json.load(open(SWEB_FILENAME))


def get_content(filename) -> str:
    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError:
        return ''

def convert_patches(ns: list[int]) -> dict[str, str]:
    #res = [{'instance_id': sweb[n]['instance_id'], 'model_name_or_path': 'clippinator', 'n': n, 'model_patch': '\n'.join(extract_patches(open('logs/' + str(n) + '.txt').read()))} for n in ns if os.path.exists('logs/' + str(n) + '.txt')]
    res = []
    for n in ns:
        paths = [str(n) + '.txt']
        patch, path = next(filter(lambda x: x[0], ((lambda content: (extract_rewrite_patch(content) or '\n'.join(extract_patches(content)), p))(
            get_content(p)) for p in paths)), ('', paths[0]))
        res.append({'instance_id': sweb[n]['instance_id'], 'model_name_or_path': 'clippinator', 'path': path, 'n': n, 'model_patch': patch, 'PASS_TO_PASS': sweb[n]['PASS_TO_PASS'], 'FAIL_TO_PASS': sweb[n]['FAIL_TO_PASS']})
    l1 = len(res)
    for r in res:
        if r['model_patch'].strip() == '':
            content = get_content(r['path'])
            print(f'Empty patch for {r["n"]}, content length: {len(content)}')
    res = list(filter(lambda r: len(r['model_patch'].strip()), res))
    print(f'Filtered {l1 - len(res)} empty patches - {(l1 - len(res)) / l1 * 100:.2f}%')
    print(f'{len(res)} patches')
    return res


if __name__ == '__main__':
    with open('patches-146.json', 'w') as f:
        json.dump(convert_patches(range(100, 146)), f)#range(1373, 1388)), f)

