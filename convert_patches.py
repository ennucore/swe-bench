import json
import os
from apply_patches import extract_patches, extract_rewrite_patch

SWEB_FILENAME = 'swe-bench.json'
sweb = json.load(open(SWEB_FILENAME))

def convert_patches(ns: list[int]) -> dict[str, str]:
    #res = [{'instance_id': sweb[n]['instance_id'], 'model_name_or_path': 'clippinator', 'n': n, 'model_patch': '\n'.join(extract_patches(open('logs/' + str(n) + '.txt').read()))} for n in ns if os.path.exists('logs/' + str(n) + '.txt')]
    res = []
    for n in ns:
        path = 'logs/' + str(n) + '.txt'
        if not os.path.exists(path):
            if os.path.exists(str(n) + '.txt'):
                path = str(n) + '.txt'
            else:
                continue
        with open(path) as f:
            content = f.read()
        if not content:
            if os.path.exists(str(n) + '.txt'):
                with open(str(n) + '.txt') as f:
                    content = f.read()
                    path = str(n) + '.txt'
                if not content:
                    continue
            else:
                continue
        patch = extract_rewrite_patch(content) or '\n'.join(extract_patches(content))
        res.append({'instance_id': sweb[n]['instance_id'], 'model_name_or_path': 'clippinator', 'path': path, 'n': n, 'model_patch': patch})
    l1 = len(res)
    for r in res:
        if r['model_patch'].strip() == '':
            with open(r['path']) as f:
                content = f.read()
            print(f'Empty patch for {r["n"]}, content length: {len(content)}')
    res = list(filter(lambda r: len(r['model_patch'].strip()), res))
    print(f'Filtered {l1 - len(res)} empty patches - {(l1 - len(res)) / l1 * 100:.2f}%')
    print(f'{len(res)} patches')
    return res


if __name__ == '__main__':
    with open('patches-alot.json', 'w') as f:
        json.dump(convert_patches(range(95, 1400)), f)#range(1373, 1388)), f)

