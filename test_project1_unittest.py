import unittest
import tempfile
import csv
from Project1 import csv_open, avg_weight, percent_over_weight


class TestPenguinCalculations(unittest.TestCase):
    def make_temp_csv(self, rows, fieldnames):
        tmp = tempfile.NamedTemporaryFile(mode='w+', newline='', delete=False, suffix='.csv')
        writer = csv.DictWriter(tmp, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
        tmp.flush()
        return tmp.name
    
    def test_avg_weight_standard(self):
        fieldnames = ['id', 'species', 'sex', 'body_mass_g']
        rows = [
            {'id': '1', 'species': 'Adelie', 'sex': 'Male', 'body_mass_g': '3600'},
            {'id': '2', 'species': 'Adelie', 'sex': 'Female', 'body_mass_g': '3400'},
            {'id': '3', 'species': 'Gentoo', 'sex': 'Male', 'body_mass_g': '5000'},
            {'id': '4', 'species': 'Gentoo', 'sex': 'Female', 'body_mass_g': '4700'}
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = avg_weight(data)
        self.assertAlmostEqual(result[('Adelie', 'Male')], 3600.0, 1)
        self.assertAlmostEqual(result[('Gentoo', 'Female')], 4700.0, 1)

    def test_avg_weight_with_invalid_values(self):
        fieldnames = ['id', 'species', 'sex', 'body_mass_g']
        rows = [
            {'id': '1', 'species': 'Adelie', 'sex': 'Male', 'body_mass_g': 'bad'},
            {'id': '2', 'species': 'Adelie', 'sex': 'Male', 'body_mass_g': '4000'},
            {'id': '3', 'species': 'Adelie', 'sex': 'Female', 'body_mass_g': '4100'}
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = avg_weight(data)
        self.assertEqual(result[('Adelie', 'Male')], 4000.0)
        self.assertEqual(result[('Adelie', 'Female')], 4100.0)

    def test_avg_weight_empty_dataset(self):
        fieldnames = ['id', 'species', 'sex', 'body_mass_g']
        rows = []
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = avg_weight(data)
        self.assertEqual(result, {})

    def test_avg_weight_all_invalid(self):
        fieldnames = ['id', 'species', 'sex', 'body_mass_g']
        rows = [
            {'id': '1', 'species': 'Adelie', 'sex': 'Male', 'body_mass_g': 'NaN'},
            {'id': '2', 'species': 'Adelie', 'sex': 'Female', 'body_mass_g': 'missing'}
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = avg_weight(data)
        self.assertEqual(result, {})
    
    def test_percent_over_weight_standard(self):
        fieldnames = ['id', 'species', 'body_mass_g']
        rows = [
            {'id': '1', 'species': 'Adelie', 'body_mass_g': '3500'},
            {'id': '2', 'species': 'Adelie', 'body_mass_g': '3800'},
            {'id': '3', 'species': 'Gentoo', 'body_mass_g': '5000'},
            {'id': '4', 'species': 'Gentoo', 'body_mass_g': '5200'}
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = percent_over_weight(data)
        self.assertEqual(result['Adelie'], '0.0%')
        self.assertEqual(result['Gentoo'], '100.0%')
    
    def test_percent_over_weight_invalid_values(self):
        """Standard: gracefully skips invalid weights."""
        fieldnames = ['id', 'species', 'body_mass_g']
        rows = [
            {'id': '1', 'species': 'Adelie', 'body_mass_g': 'bad'},
            {'id': '2', 'species': 'Adelie', 'body_mass_g': '3700'},
            {'id': '3', 'species': 'Chinstrap', 'body_mass_g': '4000'}
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = percent_over_weight(data)
        # Average = (3700+4000)/2=3850 → Adelie below avg (0%), Chinstrap above avg (100%)
        self.assertEqual(result['Adelie'], '0.0%')
        self.assertEqual(result['Chinstrap'], '100.0%')
    
    def test_percent_over_weight_empty(self):
        """Edge: empty dataset returns empty dict."""
        fieldnames = ['id', 'species', 'body_mass_g']
        rows = []
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = percent_over_weight(data)
        self.assertEqual(result, {})

    def test_percent_over_weight_all_equal(self):
        """Edge: all equal weights -> 0% above average."""
        fieldnames = ['id', 'species', 'body_mass_g']
        rows = [
            {'id': '1', 'species': 'Adelie', 'body_mass_g': '4000'},
            {'id': '2', 'species': 'Adelie', 'body_mass_g': '4000'},
            {'id': '3', 'species': 'Gentoo', 'body_mass_g': '4000'}
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = percent_over_weight(data)
        self.assertTrue(all(v == '0.0%' for v in result.values()))
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
