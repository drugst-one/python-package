"""Existing calls and result formats must stay valid as optional features are added."""
import importlib
import json
import pickle
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from drugstone import Drug, Gene, new_task, new_tasks, deep_search
from drugstone.task.task import Task
from drugstone.task.tasks import Tasks
from drugstone.scripts.normalize_nodes import normalize_results
from drugstone.scripts.normalize_task_parameter import normalize_task_parameter


def raw_result():
    return {
        'nodeAttributes': {
            'details': {
                'EGFR': {'symbol': ['EGFR'], 'drugstoneId': ['p1'], 'score': 2},
                'GRB2': {'symbol': ['GRB2'], 'drugstoneId': ['p2'], 'score': 1},
                'dr1': {'label': 'Drug A', 'drugstoneId': 'dr1', 'trialLinks': [], 'score': 4}},
            'nodeTypes': {'EGFR': 'protein', 'GRB2': 'protein', 'dr1': 'drug'},
            'isSeed': {'EGFR': True}},
        'targetNodes': ['dr1', 'GRB2'],
        'network': {'nodes': ['EGFR', 'GRB2', 'dr1'],
                    'edges': [{'from': 'EGFR', 'to': 'GRB2'}, {'from': 'EGFR', 'to': 'dr1'}]}}


class CompatibilityTests(unittest.TestCase):
    def test_old_positional_task_constructor_and_token_is_not_exported(self):
        result = {'genes': {'EGFR': {'hasEdgesTo': []}}, 'drugs': {}, 'edges': []}
        raw, info, params = {'network': {}}, {'done': True}, {'taskId': 'degree'}
        task = Task(result, raw, info, params)
        self.assertIsNone(task.get_token())
        token_task = Task(result, raw, info, params, token='secret-token')
        for item in (task, token_task, pickle.loads(pickle.dumps(token_task))):
            self.assertEqual(item.get_result().to_dict(), {'drugs': {}, 'genes': result['genes']})
            self.assertEqual(item.get_result().get_raw_result(), raw)
            self.assertEqual(item.get_info(), info)
            self.assertEqual(item.get_parameters(), params)
            exported = Tasks([item]).get_result().to_dict()
            self.assertNotIn('secret-token', json.dumps(exported))
        self.assertEqual(pickle.loads(pickle.dumps(token_task)).get_token(), 'secret-token')

    def test_pre_token_pickled_task_still_loads(self):
        task = Task(params={'taskId': 'old-task'})
        del task._Task__token  # State written by the original Task class.
        restored = pickle.loads(pickle.dumps(task))
        self.assertIsNone(restored.get_token())
        self.assertEqual(restored.get_parameters(), {'taskId': 'old-task'})
        self.assertEqual(restored.get_result().to_dict(), {'genes': {}, 'drugs': {}})

    def test_default_normalization_and_opt_in_internal_ids(self):
        old_style = normalize_results(raw_result(), 'symbol')
        quiet_style = normalize_results(raw_result(), 'symbol', quiet=True)
        self.assertEqual(old_style, quiet_style)
        kept = normalize_results(raw_result(), 'symbol', quiet=True, drugstone_ids=True)
        for section in ('drugs', 'genes'):
            for name, node in old_style[section].items():
                self.assertNotIn('drugstoneId', node)
                retained = dict(kept[section][name])
                retained.pop('drugstoneId')
                self.assertEqual(retained, node)
        self.assertEqual(old_style['drugs']['Drug A']['score'], 1)
        self.assertEqual(old_style['genes']['GRB2']['score'], 0.5)

    def test_proximity_can_have_drugs_and_genes_as_intermediate_nodes(self):
        raw = raw_result()
        raw['intermediateNodes'] = ['dr1', 'GRB2']
        result = normalize_results(raw, 'symbol', quiet=True)
        self.assertTrue(result['drugs']['Drug A']['isConnector'])
        self.assertTrue(result['genes']['GRB2']['isConnector'])
        self.assertFalse(result['genes']['EGFR']['isConnector'])

    def test_parameter_inputs_not_mutated_and_old_defaults_preserved(self):
        params = {'algorithm': 'degree', 'target': 'drug-target',
                  'custom_edges': [{'from': 'EGFR', 'to': 'GRB2'}]}
        before = deepcopy(params)
        result = normalize_task_parameter(params, ['EGFR'], quiet=True)
        self.assertEqual(params, before)
        self.assertEqual(result['algorithm'], 'degree')
        self.assertEqual(result['target'], 'drug-target')
        self.assertEqual(result['parameters']['resultSize'], 20)
        self.assertEqual(result['parameters']['input_network']['edges'], params['custom_edges'])
        self.assertTrue(result['parameters']['custom_edges'])

    @patch('drugstone.new_task.request_task_result', side_effect=lambda _: raw_result())
    @patch('drugstone.new_task.wait_for_task_to_finish')
    @patch('drugstone.new_task.start_task', return_value='task-token')
    @patch('drugstone.new_task.map_nodes_to_internal_ids')
    def test_existing_dynamic_task_returns_same_shape_and_token(self, mapping, start, wait, fetch):
        mapping.return_value = [{'id': 'EGFR', 'symbol': ['EGFR'], 'drugstoneType': 'protein', 'drugstoneId': ['p1']}]
        wait.return_value = {'done': True, 'algorithm': 'degree',
                             'parameters': {'inputNetwork': {}, 'taskId': 'degree'}}
        params = {'algorithm': 'degree'}
        task = new_task(['EGFR'], params)
        self.assertEqual(params, {'algorithm': 'degree'})
        self.assertEqual(task.get_token(), 'task-token')
        self.assertEqual(set(task.get_result().get_genes()), {'EGFR', 'GRB2'})
        self.assertEqual(set(task.get_result().get_drugs()), {'Drug A'})
        self.assertNotIn('token', task.get_parameters())
        self.assertNotIn('token', task.get_info())

    @patch('drugstone.new_task.wait_for_task_to_finish', return_value={
        'done': False, 'failed': True, 'algorithm': 'degree',
        'parameters': {'inputNetwork': {}, 'taskId': 'degree'}})
    @patch('drugstone.new_task.start_task', return_value='failed-token')
    @patch('drugstone.new_task.map_nodes_to_internal_ids', return_value=[])
    def test_failed_and_empty_tasks_keep_old_empty_results(self, *_):
        task = new_task(['unknown'], {'algorithm': 'degree'}, quiet=True)
        self.assertEqual(task.get_token(), 'failed-token')
        self.assertEqual(task.get_result().to_dict(), {'genes': {}, 'drugs': {}})
        with self.assertWarns(UserWarning):
            empty = new_task([], {}, quiet=True)
        self.assertIsNone(empty.get_token())
        self.assertEqual(empty.get_result().to_dict(), {'genes': {}, 'drugs': {}})

    @patch('drugstone.new_tasks.new_task')
    def test_all_existing_multi_task_call_forms_and_new_option_forwarding(self, start):
        start.side_effect = lambda *a, **kw: Task(params={'taskId': 'test'})
        forms = [{'algorithm': 'degree'}, {'algorithms': ['degree', 'trustrank']},
                 {'algorithm': ['degree', 'degree']}, [{'algorithm': 'degree'}, {'algorithm': 'trustrank'}]]
        for params in forms:
            with self.subTest(params=params):
                before = deepcopy(params)
                result = new_tasks(['EGFR'], params, quiet=True, drugstone_ids=True)
                self.assertEqual(len(result.get_result().get_tasks_list()), 1 if params == forms[0] else 2)
                self.assertEqual(params, before)
                self.assertTrue(start.call_args.kwargs['quiet'])
                self.assertTrue(start.call_args.kwargs['drugstone_ids'])
        self.assertEqual(new_tasks([], {}, True, [Task()]).get_result().get_tasks_list()[0].get_token(), None)

    @patch('drugstone.deep_search.new_task')
    def test_deep_search_both_parameter_forms(self, start):
        first = Task(result={'genes': {'GRB2': {}}, 'drugs': {}})
        second = Task(token='second-token')
        for params in ({'algorithm': ['degree', 'trustrank']},
                       [{'algorithm': 'degree'}, {'algorithm': 'trustrank'}]):
            start.reset_mock()
            start.side_effect = [first, second]
            self.assertIs(deep_search(['EGFR'], params, quiet=True, drugstone_ids=True), second)
            self.assertEqual(set(start.call_args_list[1].args[0]), {'EGFR', 'GRB2'})
            self.assertEqual(start.call_args_list[0].args[1]['target'], 'drug-target')
            self.assertEqual(start.call_args_list[1].args[1]['target'], 'drug')

    @patch('drugstone.new_task.map_nodes_to_internal_ids', return_value=[])
    def test_deprecated_static_call_preserves_existing_return(self, mapping):
        with self.assertWarns(UserWarning):
            self.assertIsNone(new_task([], {}, True, {}, [], [], quiet=True))

    @patch('drugstone.license.requests.get')
    def test_license_helpers_without_accepting_a_real_license(self, get):
        module = importlib.import_module('drugstone.license')
        get.return_value.json.return_value = {'license': 'Test fixture license'}
        with patch.object(module.license, 'printed', False), patch.object(module.license, 'accepted', False):
            module.accept_license()
            self.assertFalse(module.license.accepted)
            module.print_license()
            self.assertTrue(module.license.printed)
            module.accept_license()
            self.assertTrue(module.license.accepted)

    def test_models_aggregation_and_all_result_exports(self):
        gene = Gene('EGFR', 'Receptor', ['GRB2'])
        self.assertIn('EGFR', gene.to_dict())
        self.assertEqual(Drug('Drug A', 'DB1', 'approved').to_dict()['Drug A']['drugId'], 'DB1')
        data = normalize_results(raw_result(), 'symbol', quiet=True)
        task = Task(data, raw_result(), {'done': True}, {'taskId': 'degree'}, token='secret-token')
        tasks = Tasks([task])
        self.assertEqual(tasks.get_union().get_genes(), data['genes'])
        self.assertEqual(tasks.get_intersection().get_drugs(), data['drugs'])
        result = task.get_result()
        self.assertEqual(result.get_edges(), data['edges'])
        self.assertFalse(result.to_pandas_dataframe().empty)
        # Files stay in a fresh temporary directory; no user files are removed.
        directory = Path(tempfile.mkdtemp(prefix='drugstone-exports-'))
        for method, name, extension in [
            ('download_json', 'result', 'json'), ('download_raw_json', 'raw', 'json'),
            ('download_genes_csv', 'genes', 'csv'), ('download_drugs_csv', 'drugs', 'csv'),
            ('download_edges_csv', 'edges', 'csv'), ('download_graph', 'graph', 'html')]:
            with self.subTest(method=method):
                getattr(result, method)(str(directory), name)
                self.assertTrue((directory / (name + '.' + extension)).stat().st_size)
        tasks.get_result().download_json(str(directory), 'tasks')
        self.assertNotIn('secret-token', (directory / 'tasks.json').read_text())
        tasks.get_result().create_upset_plot()  # Existing Python-version warning path.


if __name__ == '__main__':
    unittest.main()
