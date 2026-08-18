import unittest
import os
import json
from src.models import Ticket
from src.analyzer import TicketAnalyzer

class TestTicketAnalyzer(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tickets.json')
        self.analyzer = TicketAnalyzer.load_from_file(self.data_path)

    def test_overview_metrics(self):
        ov = self.analyzer.get_overview()
        self.assertEqual(ov['total_tickets'], 50)
        self.assertEqual(ov['resolved_count'], 42)
        self.assertEqual(ov['unresolved_count'], 8)
        self.assertEqual(ov['resolved_rate'], 84.0)
        self.assertEqual(ov['avg_satisfaction'], 2.36)
        self.assertEqual(ov['avg_resolution_time_hours'], 19.69)
        self.assertEqual(ov['high_priority_count'], 31)

    def test_category_aggregation(self):
        cats = self.analyzer.analyze_categories()
        self.assertEqual(len(cats), 6)
        cat_map = {c['category']: c for c in cats}
        self.assertEqual(cat_map['支付问题']['count'], 16)
        self.assertEqual(cat_map['退款退货']['count'], 13)
        self.assertEqual(cat_map['退款退货']['unresolved_count'], 5)
        self.assertEqual(cat_map['退款退货']['unresolved_rate'], 38.46)
        self.assertEqual(cat_map['退款退货']['max_resolution_time_hours'], 120.0)

    def test_anomaly_detection_dynamic(self):
        anomalies = self.analyzer.detect_anomalies()
        self.assertEqual(len(anomalies), 5)
        a_map = {a['id']: a for a in anomalies}
        
        self.assertIn("ANOMALY-01", a_map)
        self.assertEqual(a_map['ANOMALY-01']['level'], "CRITICAL (P0)")
        
        facts_01_text = " ".join(a_map['ANOMALY-01']['objective_facts'])
        self.assertIn("1.9", facts_01_text)
        self.assertIn("2.25", facts_01_text)

        self.assertIn("ANOMALY-02", a_map)
        facts_02_text = " ".join(a_map['ANOMALY-02']['objective_facts'])
        self.assertIn("38.5%", facts_02_text)
        self.assertIn("45.2", facts_02_text)
        self.assertIn("120", facts_02_text)

        self.assertIn("ANOMALY-05", a_map)
        facts_05_text = " ".join(a_map['ANOMALY-05']['objective_facts'])
        self.assertIn("06-08(1.4)", facts_05_text)
        self.assertIn("87.5%", facts_05_text)

    def test_dynamic_behavior_on_subset(self):
        inquiry_tickets = [t for t in self.analyzer.tickets if t.category == '商品咨询']
        inquiry_analyzer = TicketAnalyzer(inquiry_tickets)
        anomalies = inquiry_analyzer.detect_anomalies()
        self.assertEqual(len(anomalies), 0)

        empty_analyzer = TicketAnalyzer([])
        self.assertEqual(empty_analyzer.get_overview()['total_tickets'], 0)
        self.assertEqual(len(empty_analyzer.detect_anomalies()), 0)

    def test_sub_issue_clusters(self):
        clusters = self.analyzer.cluster_sub_issues()
        self.assertIn("重复扣款与金额多扣", clusters)
        self.assertIn("退货垫付运费报销严重滞后", clusters)
        self.assertIn("智能客服死循环与人工排队过长", clusters)
        self.assertEqual(clusters["重复扣款与金额多扣"]["count"], 5)
        self.assertEqual(clusters["退货垫付运费报销严重滞后"]["unresolved_count"], 2)

    def test_executive_attention_matrix(self):
        matrix = self.analyzer.calculate_executive_attention_matrix()
        self.assertTrue(len(matrix) > 0)
        top_item = matrix[0]
        self.assertTrue(top_item['attention_index'] >= matrix[-1]['attention_index'])
        self.assertIn("target_department", top_item)
        self.assertIn("recommended_directive", top_item)

if __name__ == '__main__':
    unittest.main()
