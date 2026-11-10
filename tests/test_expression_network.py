import json
import unittest
from copy import deepcopy
from unittest.mock import patch

from drugstone import fetching, network

MAPPING = 'drugstone.external_scripts.map_nodes_to_internal_ids.map_nodes_to_internal_ids'


class ExpressionNetworkTests(unittest.TestCase):
    @patch(MAPPING)
    @patch('drugstone.fetching.requests.post')
    def test_expression_retains_multiple_proteins_and_ignores_unmapped(self, post, mapping):
        mapping.return_value = [
            {'id': 'EGFR', 'drugstoneType': 'protein', 'drugstoneId': ['p2', 'p3']},
            {'id': 'missing', 'drugstoneType': 'other'},
            {'id': 'alias', 'drugstoneType': 'protein', 'drugstoneId': ['p2']}]
        post.return_value.json.return_value = {'p2': 3.0, 'p3': None}
        self.assertEqual(fetching.get_tissue_expression('7', ['EGFR', 'missing', 'alias']),
                         {'p2': 3.0, 'p3': None})
        payload = post.call_args.kwargs['json']
        self.assertEqual(json.loads(payload['proteins']), ['2', '3'])
        self.assertEqual(payload['tissue'], '7')
        post.return_value.raise_for_status.assert_called_once()

    @patch(MAPPING)
    @patch('drugstone.fetching.requests.post')
    def test_no_mapped_proteins_does_not_query_all_proteins(self, post, mapping):
        mapping.return_value = []
        self.assertEqual(fetching.get_tissue_expression('7', []), {})
        post.assert_not_called()

    @patch('drugstone.fetching.requests.post')
    def test_token_and_exclusive_arguments(self, post):
        # The proteins of the task result are sent, whatever identifier the task used.
        result = {'nodeAttributes': {'nodeTypes': {'EGFR': 'protein', 'dr1': 'drug'},
                                     'details': {'EGFR': {'drugstoneId': ['p2', 'p5']},
                                                 'dr1': {'drugstoneId': 'dr1'}}}}
        with patch('drugstone.fetching.request_task_result', return_value=result) as fetch:
            fetching.get_tissue_expression('7', token='task-token')
        fetch.assert_called_once_with('task-token')
        self.assertEqual(post.call_args.kwargs['json'], {'tissue': '7', 'proteins': json.dumps(['2', '5'])})
        for args in ({}, {'proteins': [], 'token': 'task-token'}):
            with self.assertRaises(ValueError):
                fetching.get_tissue_expression('7', **args)

    @patch(MAPPING)
    @patch('drugstone.network.requests.post')
    def test_overlay_mapping_and_no_input_mutation(self, post, mapping):
        mapping.return_value = [
            {'id': 'EGFR', 'drugstoneType': 'protein', 'drugstoneId': ['p2', 'p4']},
            {'id': 'TP53', 'drugstoneType': 'protein', 'drugstoneId': ['p3']}]
        net = {'nodes': [{'id': 'EGFR'}, {'id': 'TP53'}],
               'edges': [{'from': 'EGFR', 'to': 'TP53', 'id': 7}]}
        before = deepcopy(net)
        post.return_value.json.return_value = [
            {'from': 'EGFR', 'to': 'TP53', 'id': '7', 'isDirected': True},
            {'from': 'TP53', 'to': 'EGFR', 'id': '7_rev', 'isDirected': True}]
        result = network.overlay_directed_edges(net)
        # integer ids are restored; the reverse direction keeps the backend's "_rev" id
        self.assertEqual([e['id'] for e in result], [7, '7_rev'])
        self.assertEqual(net, before)
        payload = post.call_args.kwargs['json']
        self.assertEqual(payload['ppi_dataset'], 'OmniPath')
        self.assertEqual(payload['edges'], [{'from': 'EGFR', 'to': 'TP53', 'id': '7'}])
        self.assertEqual(payload['drugstone_mapping'], {'p2': 'EGFR', 'p3': 'TP53'})

    @patch(MAPPING, return_value=[{'id': 'TP53', 'drugstoneType': 'protein', 'drugstoneId': ['p3']},
                                  {'id': 'Imatinib', 'drugstoneType': 'drug'}])
    @patch('drugstone.network.requests.post')
    def test_overlay_keeps_edges_to_non_protein_nodes(self, post, mapping):
        net = {'nodes': [{'id': 'TP53'}, {'id': 'Imatinib'}],
               'edges': [{'from': 'TP53', 'to': 'Imatinib'}]}
        self.assertEqual(network.overlay_directed_edges(net), [{'from': 'TP53', 'to': 'Imatinib', 'id': 0}])
        post.assert_not_called()

    @patch('drugstone.network.requests.post')
    def test_custom_statistics_config_is_forwarded_without_mutation(self, post):
        config = {'identifier': 'symbol', 'custom_edges': True,
                  'exclude_drugstone_ppi_edges': True, 'calculateProperties': False}
        before = deepcopy(config)
        net = {'nodes': [{'id': 'EGFR', 'symbol': ['EGFR']}], 'edges': []}
        network.recalculate_statistics(net, config)
        payload = post.call_args.kwargs['json']
        self.assertTrue(payload['config']['calculateProperties'])
        self.assertTrue(payload['config']['exclude_drugstone_ppi_edges'])
        self.assertEqual(payload['network'], net)
        self.assertEqual(config, before)
        post.return_value.raise_for_status.assert_called_once()


if __name__ == '__main__':
    unittest.main()
