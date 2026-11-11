import unittest
from copy import deepcopy
from unittest.mock import patch

from drugstone import fetching, network, new_task
from drugstone.scripts.normalize_task_parameter import normalize_task_parameter


class ExtendedWorkflowTests(unittest.TestCase):
    @patch('drugstone.fetching.requests.put')
    @patch('drugstone.fetching.request_task_result')
    def test_pathway_requires_actual_table_pair_and_summary_keeps_statistics(self, fetch, put):
        row = {'geneset': 'reactome', 'pathway': 'Signal & repair', 'genes': ['EGFR'], 'adjPvalue': 0.01}
        raw = {'tableView': [row], 'geneset': 'reactome', 'pathway': row['pathway'],
               'geneInteractionDataset': {'name': 'NeDRex'}, 'network': {'nodes': [], 'edges': []},
               'nodeAttributes': {'isSeed': {'EGFR': True}}}
        fetch.return_value = raw
        put.return_value.ok, put.return_value.text = True, '"worked!"'
        result = fetching.get_pathway_network('token', 'reactome', row['pathway'], summary=True)
        fetch.assert_called_once_with('token')
        self.assertEqual(result['statistics']['adjPvalue'], 0.01)
        self.assertNotIn('genes', result['statistics'])
        self.assertEqual(result['isSeed'], {'EGFR': True})
        self.assertEqual(put.call_args.kwargs['params']['pathway'], row['pathway'])
        put.return_value.ok = False
        with self.assertRaisesRegex(ValueError, 'not in the task result'):
            fetching.get_pathway_network('token', 'kegg', row['pathway'])
        fetch.return_value = {}
        with self.assertRaises(ValueError):
            fetching.get_pathway_network('token', 'reactome', row['pathway'])

    def test_new_algorithm_parameters_and_sources(self):
        for algorithm, target in [('harmonic', 'drug'), ('first-neighbor', 'drug-target'),
                                  ('connect', 'drug-target'), ('connectSelected', 'drug-target'),
                                  ('quick', 'drug'), ('super', 'drug'),
                                  ('louvain-clustering', 'clustering'), ('leiden-clustering', 'clustering'),
                                  ('pathway-enrichment', 'gene'), ('adjacentDisorders', 'drug')]:
            with self.subTest(algorithm=algorithm):
                result = normalize_task_parameter({'algorithm': algorithm, 'target': target}, ['EGFR'], quiet=True)
                self.assertEqual(result['algorithm'], algorithm)
                self.assertEqual(result['target'], target)
        result = normalize_task_parameter({'algorithm': 'pathway-enrichment', 'reactome': True, 'kegg': False}, [], quiet=True)
        self.assertTrue(result['parameters']['reactome'])
        self.assertFalse(result['parameters']['kegg'])
        self.assertFalse(result['parameters']['wiki'])

    @patch('drugstone.new_task.request_task_result', return_value={'network': {'nodes': ['EGFR'], 'edges': []}})
    @patch('drugstone.new_task.wait_for_task_to_finish')
    @patch('drugstone.new_task.start_task', return_value='token')
    @patch('drugstone.new_task.map_nodes_to_internal_ids')
    @patch('drugstone.new_task.fetch_edges', return_value=[{'proteinA': 'p1', 'proteinB': 'p2'}])
    def test_clustering_autofill_and_raw_result(self, edges, mapping, start, wait, fetch):
        mapping.side_effect = lambda *a, **kw: deepcopy([
            {'id': 'EGFR', 'symbol': ['EGFR'], 'drugstoneType': 'protein', 'drugstoneId': ['p1']},
            {'id': 'GRB2', 'symbol': ['GRB2'], 'drugstoneType': 'protein', 'drugstoneId': ['p2']}])
        wait.return_value = {'done': True, 'algorithm': 'louvain-clustering',
                             'parameters': {'inputNetwork': {}, 'taskId': 'louvain-clustering'}}
        task = new_task(['EGFR', 'GRB2'], {'algorithm': 'louvain-clustering', 'target': 'clustering'}, quiet=True)
        sent = start.call_args.args[0]['parameters']['input_network']
        self.assertEqual(sent['nodes'], [{'id': 'EGFR'}, {'id': 'GRB2'}])
        self.assertEqual(sent['edges'], [{'from': 'EGFR', 'to': 'GRB2'}])
        self.assertEqual(task.get_result().get_genes(), {})
        self.assertEqual(task.get_result().get_raw_result()['network']['nodes'], ['EGFR'])
        self.assertEqual(task.get_token(), 'token')

    @patch('drugstone.new_task.start_task')
    @patch('drugstone.new_task.fetch_edges', return_value=[])
    @patch('drugstone.new_task.map_nodes_to_internal_ids')
    def test_clustering_rejects_edgeless_self_loop_and_outside_input_networks(self, mapping, edges, start):
        mapping.side_effect = lambda *a, **kw: deepcopy([
            {'id': name, 'symbol': [name], 'drugstoneType': 'protein', 'drugstoneId': ['p' + str(i)]}
            for i, name in enumerate(['EGFR', 'GRB2', 'TP53']) if name in a[0]])
        for algorithm in ('louvain-clustering', 'leiden-clustering'):
            for custom in (None, [{'from': 'EGFR', 'to': 'EGFR'}],
                           [{'from': 'EGFR', 'to': 'TP53'}]):
                with self.subTest(algorithm=algorithm, custom=custom):
                    params = {'algorithm': algorithm, 'target': 'clustering'}
                    if custom is not None:
                        params['custom_edges'] = custom
                    with self.assertRaisesRegex(ValueError, 'interaction between two input proteins'):
                        new_task(['EGFR', 'GRB2'], params, quiet=True)
        start.assert_not_called()

    @patch('drugstone.new_task.wait_for_task_to_finish', return_value={'done': False, 'algorithm': 'trustrank',
                                                                      'parameters': {'inputNetwork': {}}})
    @patch('drugstone.new_task.start_task', return_value='token')
    @patch('drugstone.new_task.map_nodes_to_internal_ids')
    def test_compact_custom_edges_map_nodes_and_drop_unmapped(self, mapping, start, wait):
        mapping.side_effect = lambda ids, *a, **kw: [
            {'id': name, 'symbol': [name.lower()], 'drugstoneType': 'protein', 'drugstoneId': ['p' + name]}
            for name in ids if name != 'UNKNOWN']
        custom = {'nodes': ['EGFR', 'UNKNOWN', 'GRB2', 'TP53'], 'edges': [[0, 2], [0, 1], [2, 3]]}
        with self.assertWarnsRegex(UserWarning, 'Skipped 1 custom edges'):
            new_task(['EGFR'], {'algorithm': 'trustrank', 'custom_edges': custom}, quiet=True)
        sent = start.call_args.args[0]['parameters']
        self.assertTrue(sent['custom_edges'])
        self.assertEqual(sent['input_network']['edges'],
                         {'nodes': ['egfr', 'grb2', 'tp53'], 'edges': [[0, 1], [1, 2]]})
        self.assertEqual(custom['nodes'][1], 'UNKNOWN')  # the caller's parameters are not modified

    @patch('drugstone.new_task.start_task')
    @patch('drugstone.new_task.map_nodes_to_internal_ids')
    def test_clustering_accepts_compact_custom_edges(self, mapping, start):
        mapping.side_effect = lambda ids, *a, **kw: [
            {'id': name, 'symbol': [name], 'drugstoneType': 'protein', 'drugstoneId': ['p' + name]} for name in ids]
        start.side_effect = RuntimeError('started')
        custom = {'nodes': ['EGFR', 'GRB2'], 'edges': [[0, 1]]}
        with self.assertRaisesRegex(RuntimeError, 'started'):
            new_task(['EGFR', 'GRB2'], {'algorithm': 'louvain-clustering', 'target': 'clustering',
                                        'custom_edges': custom}, quiet=True)
        self.assertEqual(start.call_args.args[0]['parameters']['input_network']['edges'],
                         [{'from': 'EGFR', 'to': 'GRB2'}])

    def test_distribution_empty_missing_boolean_and_identical_values(self):
        result = network.get_pruning_distribution([
            {'properties': {'x': 2}}, {'properties': {'x': 2}}, {'properties': {'x': True}},
            {'properties': {'x': float('nan')}}, {}, {'properties': None}], 'x')
        self.assertEqual(result['count'], 2)
        self.assertEqual(result['missing'], 4)
        self.assertEqual(sum(b['count'] for b in result['bins']), 2)
        self.assertEqual(network.get_pruning_distribution([], 'x')['bins'], [])

    @patch('drugstone.fetching.requests.post')
    def test_disorder_prefixes_and_optional_dataset(self, post):
        fetching.get_adjacent_disorders_of_drugs(['dr12', '34', 56], dataset='NeDRex')
        self.assertEqual(post.call_args.kwargs['json'], {'drugs': ['12', '34', 56], 'licenced': False, 'dataset': 'NeDRex'})


if __name__ == '__main__':
    unittest.main()


class MappingWarningTests(unittest.TestCase):
    @patch('drugstone.external_scripts.map_nodes_to_internal_ids.requests.post')
    def test_quiet_summarizes_unmapped_nodes(self, post):
        from drugstone.external_scripts.map_nodes_to_internal_ids import map_nodes_to_internal_ids
        post.return_value.json.return_value = [{'id': 'EGFR', 'drugstoneId': ['p1']}] + [
            {'id': f'X{i}'} for i in range(7)]
        with self.assertLogs(level='WARNING') as logs:
            map_nodes_to_internal_ids(['EGFR'], {'identifier': 'symbol'}, quiet=True)
        self.assertEqual(logs.output, ['WARNING:root:Could not map 7 nodes, e.g. "X0", "X1", "X2", "X3", "X4".'])
        with self.assertLogs(level='WARNING') as logs:
            map_nodes_to_internal_ids(['EGFR'], {'identifier': 'symbol'})
        self.assertEqual(len(logs.output), 7)


class EmptyCompactEdgesTests(unittest.TestCase):
    @patch('drugstone.new_task.wait_for_task_to_finish', return_value={'done': False, 'algorithm': 'trustrank',
                                                                      'parameters': {'inputNetwork': {}}})
    @patch('drugstone.new_task.start_task', return_value='token')
    @patch('drugstone.new_task.map_nodes_to_internal_ids', return_value=[
        {'id': 'EGFR', 'symbol': ['EGFR'], 'drugstoneType': 'protein', 'drugstoneId': ['p1']}])
    def test_empty_compact_custom_edges(self, mapping, start, wait):
        new_task(['EGFR'], {'algorithm': 'trustrank', 'custom_edges': {'nodes': [], 'edges': []}}, quiet=True)
        self.assertEqual(start.call_args.args[0]['parameters']['input_network']['edges'], {'nodes': [], 'edges': []})
