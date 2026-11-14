#!/usr/bin/env python3
"""Validate this repository's deliberately restricted skill/agent format, not all YAML."""
import json
from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
NAMES = {'answer', 'debug', 'frame', 'implement', 'pin', 'plan', 'review', 'ship', 'verify', 'which'}


def frontmatter(path):
    text = path.read_text()
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ValueError(f'{path}: missing frontmatter')
    header, body = text[4:].split('\n---\n', 1)
    fields = {}
    for line in header.splitlines():
        key, separator, value = line.partition(': ')
        if not separator or key in fields or not value.strip():
            raise ValueError(f'{path}: invalid single-line metadata')
        # This repository uses unquoted YAML plain scalars only.
        if ': ' in value or ' #' in value or value[0] in "[{'\"&*!|>@`%":
            raise ValueError(f'{path}: use a simple YAML scalar')
        fields[key] = value
    return fields, body


def validate(root=ROOT):
    paths = sorted((root / 'skills').glob('*/SKILL.md'))
    assert {p.parent.name for p in paths} == NAMES, 'skill inventory drift'
    sizes = {}
    for path in paths:
        fields, body = frontmatter(path)
        assert set(fields) == {'name', 'description'}, f'{path}: metadata fields'
        assert fields['name'] == path.parent.name, f'{path}: name mismatch'
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', fields['name'])
        assert len(fields['name']) <= 64 and len(fields['description']) <= 1024
        assert len(path.read_text().splitlines()) <= 150, f'{path}: local line budget'
        assert len(path.read_text().encode()) <= 4500, f'{path}: local byte budget'
        for title in ('Rules', 'Method', 'Output'):
            assert f'## {title}\n' in body, f'{path}: missing {title}'
        sizes[path.parent.name] = {'bytes': path.stat().st_size,
                                   'description_chars': len(fields['description'])}
    manifests = [json.loads((root / p).read_text()) for p in
                 ('.claude-plugin/plugin.json', '.codex-plugin/plugin.json')]
    assert manifests[0]['version'] == manifests[1]['version'], 'version drift'
    for manifest in manifests:
        assert manifest['skills'] == './skills/'
    marketplace = json.loads((root / '.claude-plugin/marketplace.json').read_text())
    assert marketplace['plugins'][0]['name'] == manifests[0]['name']
    assert marketplace['plugins'][0]['source'] == './'
    assert (root / 'AGENTS.md').read_bytes() == (root / 'CLAUDE.md').read_bytes(), 'guide drift'
    assert (root / 'LICENSE').is_file(), 'license missing'
    for name in ('explorer', 'reviewer', 'verifier'):
        fields, body = frontmatter(root / f'agents/{name}.md')
        cfg = tomllib.loads((root / f'.codex/agents/{name}.toml').read_text())
        assert fields['name'] == cfg['name'] == name
        assert fields['description'] == cfg['description']
        assert body.strip() == cfg['developer_instructions'].strip(), 'role drift'
        if name != 'verifier':
            assert fields['tools'] == 'Read, Grep, Glob'
    print(json.dumps({'status': 'PASS', 'skills': sizes, 'total_skill_bytes': sum(x['bytes'] for x in sizes.values())}, indent=2))


if __name__ == '__main__':
    try:
        validate()
    except (AssertionError, ValueError, OSError, KeyError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
