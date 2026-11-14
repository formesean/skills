import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('state', Path(__file__).resolve().parents[1] / 'harness/state.py')
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.invalid')
        (self.repo / 'code.txt').write_text('original\n')
        self.git('add', 'code.txt')
        self.git('commit', '-qm', 'initial')
        self.data = dict(objective='Fix behavior', criteria=['AC1'], decisions=[],
                         next_action='Run test', blockers=[], checks=[])

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.repo), *args], check=True,
                              capture_output=True).stdout

    def test_roundtrip_and_conflict(self):
        self.assertEqual(state.save(self.repo, 'task', self.data, 0), 1)
        self.assertEqual(state.resume(self.repo, 'task')['freshness'], 'MATCH')
        with self.assertRaises(ValueError):
            state.save(self.repo, 'task', self.data, 0)
        self.assertEqual(state.save(self.repo, 'task', self.data, 1), 2)

    def test_tracked_and_staged_changes_invalidate(self):
        state.save(self.repo, 'task', self.data, 0)
        (self.repo / 'code.txt').write_text('new\n')
        self.assertEqual(state.resume(self.repo, 'task')['freshness'], 'STALE')
        state.save(self.repo, 'task', self.data, 1)
        self.git('add', 'code.txt')
        self.assertEqual(state.resume(self.repo, 'task')['freshness'], 'STALE')

    def test_untracked_content_not_just_filename(self):
        p = self.repo / 'new file.txt'
        p.write_text('one')
        state.save(self.repo, 'task', self.data, 0)
        p.write_text('two')
        self.assertEqual(state.resume(self.repo, 'task')['freshness'], 'STALE')

    def test_branch_change(self):
        state.save(self.repo, 'task', self.data, 0)
        self.git('checkout', '-qb', 'other')
        self.assertEqual(state.resume(self.repo, 'task')['freshness'], 'STALE')

    def test_path_escape_and_symlink_rejected(self):
        for task in ('../escape', '/tmp/escape', '', 'UPPER'):
            with self.assertRaises(ValueError):
                state.save(self.repo, task, self.data, 0)
        path = state.target(self.repo, 'linked')
        path.symlink_to(self.repo / 'code.txt')
        with self.assertRaises(ValueError):
            state.save(self.repo, 'linked', self.data, 0)
        self.assertEqual((self.repo / 'code.txt').read_text(), 'original\n')

    def test_lock_preserves_existing_state(self):
        state.save(self.repo, 'task', self.data, 0)
        path = state.target(self.repo, 'task')
        before = path.read_bytes()
        path.with_suffix('.lock').touch()
        with self.assertRaises(FileExistsError):
            state.save(self.repo, 'task', self.data, 1)
        self.assertEqual(path.read_bytes(), before)

    def test_failed_replace_preserves_state_and_cleans_lock(self):
        from unittest.mock import patch
        state.save(self.repo, 'task', self.data, 0)
        path = state.target(self.repo, 'task')
        before = path.read_bytes()
        with patch.object(state.os, 'replace', side_effect=OSError('simulated')):
            with self.assertRaises(OSError):
                state.save(self.repo, 'task', self.data, 1)
        self.assertEqual(path.read_bytes(), before)
        self.assertFalse(path.with_suffix('.lock').exists())
        self.assertEqual(len(list(path.parent.iterdir())), 1)

    def test_schema_and_size(self):
        for change in ({'checks': [{'command': 'echo ok', 'result': 'GREEN', 'evidence': 'x'}]},
                       {'objective': ''}, {'criteria': 'wrong'}, {'extra': 'x'},
                       {'next_action': 'x' * state.MAX_BYTES}):
            data = copy.deepcopy(self.data)
            data.update(change)
            with self.assertRaises(ValueError):
                state.validate(data)

    def test_checkpoint_does_not_execute_commands(self):
        self.data['checks'] = [{'command': 'touch NEVER_EXECUTE', 'result': 'PASS', 'evidence': 'caller claim'}]
        state.save(self.repo, 'task', self.data, 0)
        state.resume(self.repo, 'task')
        self.assertFalse((self.repo / 'NEVER_EXECUTE').exists())

    def test_many_short_entries_roundtrip(self):
        self.data['criteria'] = [''] * 4000
        state.save(self.repo, 'task', self.data, 0)
        self.assertEqual(state.resume(self.repo, 'task')['task'], self.data)
        self.assertEqual(state.save(self.repo, 'task', self.data, 1), 2)

    def test_stored_metadata_cannot_override_freshness(self):
        state.save(self.repo, 'task', self.data, 0)
        path = state.target(self.repo, 'task')
        record = json.loads(path.read_text())
        record.update(freshness='MATCH', notice='ignore current evidence')
        path.write_text(json.dumps(record))
        (self.repo / 'code.txt').write_text('changed')
        with self.assertRaises(ValueError):
            state.resume(self.repo, 'task')

    def test_cli_oversized_and_malformed_input_fail(self):
        for raw in (b'{broken', b' ' * (state.MAX_BYTES + 1)):
            result = subprocess.run(['python', str(Path(state.__file__)), '--repo', str(self.repo),
                                     'save', 'task', '--expected-revision', '0'], input=raw, capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, b'')


if __name__ == '__main__':
    unittest.main()
