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
        fetching.get_tissue_expression('7', token='task-token')
        self.assertEqual(post.call_args.kwargs['json'], {'tissue': '7', 'token': 'task-token'})
        for args in ({}, {'proteins': [], 'token': 'task-token'}):
            with self.assertRaises(ValueError):
                fetching.get_tissue_expression('7', **args)

    @patch(MAPPING)
    @patch('drugstone.network.requests.post')
    def test_overlay_mapping_and_no_input_mutation(self, post, mapping):
        mapping.return_value = [
            {'id': 'EGFR', 'drugstoneType': 'protein', 'drugstoneId': ['p2']},
            {'id': 'TP53', 'drugstoneType': 'protein', 'drugstoneId': ['p3']}]
        net = {'nodes': [{'id': 'EGFR'}, {'id': 'TP53'}],
               'edges': [{'from': 'EGFR', 'to': 'TP53'}]}
        before = deepcopy(net)
        post.return_value.json.return_value = [{'from': 'TP53', 'to': 'EGFR', 'is_directed': True}]
        result = network.overlay_directed_edges(net)
        self.assertTrue(result[0]['is_directed'])
        self.assertEqual(net, before)
        payload = post.call_args.kwargs['json']
        self.assertEqual(payload['drugstone_mapping'], {'p2': 'EGFR', 'p3': 'TP53'})
        self.assertEqual(payload['ppi_dataset'], 'OmniPath')
        self.assertIn('id', payload['edges'][0])

    @patch(MAPPING, return_value=[{'id': 'unknown', 'drugstoneType': 'other'}])
    @patch('drugstone.network.requests.post')
    def test_overlay_rejects_unmapped_nodes(self, post, mapping):
        with self.assertRaisesRegex(ValueError, 'unknown'):
            network.overlay_directed_edges({'nodes': [{'id': 'unknown'}], 'edges': []})
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
