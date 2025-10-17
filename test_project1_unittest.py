import unittest
import tempfile
import csv
import sys 
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Project1 import csv_open, island_percentage, bill_size, avg_weight, percent_over_weight, flipper_corr_strength , species_flipper_length_range



class TestPenguinCalculations(unittest.TestCase):
    def make_temp_csv(self, rows, fieldnames):
        tmp = tempfile.NamedTemporaryFile(mode='w+', newline='', delete=False, suffix='.csv')
        writer = csv.DictWriter(tmp, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
        tmp.flush()
        return tmp.name
    
    # Now testing the island_percentage() function - Calculation #1

    def test_island_percentage_standard(self):
        fieldnames = ['id', 'species', 'island']
        rows = [
            {'id': '1', 'species': 'Adelie', 'island': 'Torgersen'},
            {'id': '2', 'species': 'Gentoo', 'island': 'Biscoe'},
            {'id': '3', 'species': 'Adelie', 'island': 'Torgersen'},
            {'id': '4', 'species': 'Chinstrap', 'island': 'Dream'},
            {'id': '5', 'species': 'Gentoo', 'island': 'Biscoe'}
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = island_percentage(data)
        self.assertEqual(result['Torgersen'], '40.0%')
        self.assertEqual(result['Biscoe'], '40.0%')
        self.assertEqual(result['Dream'], '20.0%')

    def test_island_percentage_empty(self):
        fieldnames = ['id', 'species', 'island']
        rows = []
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = island_percentage(data)
        self.assertEqual(result, {})

    def test_island_percentage_all_same_island(self):
        fieldnames = ['id', 'species', 'island']
        rows = [
            {'id': '1', 'species': 'Adelie', 'island': 'Biscoe'},
            {'id': '2', 'species': 'Gentoo', 'island': 'Biscoe'},
            {'id': '3', 'species': 'Chinstrap', 'island': 'Biscoe'}
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = island_percentage(data)
        self.assertEqual(result['Biscoe'], '100.0%')
        self.assertEqual(len(result), 1)

    def test_island_percentage_invalid_entries(self):
        fieldnames = ['id', 'species', 'island']
        rows = [
            {'id': '1', 'species': 'Adelie', 'island': 'Torgersen'},
            {'id': '2', 'species': 'Gentoo', 'island': ''},
            {'id': '3', 'species': 'Adelie', 'island': 'Torgersen'}
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = island_percentage(data)
        self.assertEqual(result['Torgersen'], '66.67%')
        self.assertEqual(result[''], '33.33%')
        self.assertEqual(len(result), 2)

    # Now testing the bill_size() function - Calculation #2

    def test_bill_size_standard(self):
        """Standard: computes average bill area per species correctly."""
        fieldnames = ['id', 'species', 'bill_length_mm', 'bill_depth_mm']
        rows = [
            {'id': '1', 'species': 'Adelie', 'bill_length_mm': '40.0', 'bill_depth_mm': '18.0'},  
            {'id': '2', 'species': 'Adelie', 'bill_length_mm': '42.0', 'bill_depth_mm': '20.0'},  
            {'id': '3', 'species': 'Gentoo', 'bill_length_mm': '50.0', 'bill_depth_mm': '16.0'}   
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = bill_size(data)
        self.assertAlmostEqual(result['Adelie'], 780.0, 1)
        self.assertAlmostEqual(result['Gentoo'], 800.0, 1)

    def test_bill_size_with_invalid_values(self):
        """Standard: ignores non-numeric bill measurements gracefully."""
        fieldnames = ['id', 'species', 'bill_length_mm', 'bill_depth_mm']
        rows = [
            {'id': '1', 'species': 'Adelie', 'bill_length_mm': '40.0', 'bill_depth_mm': '18.0'},  
            {'id': '2', 'species': 'Adelie', 'bill_length_mm': 'bad', 'bill_depth_mm': '20.0'},  
            {'id': '3', 'species': 'Gentoo', 'bill_length_mm': '50.0', 'bill_depth_mm': '15.0'}   
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = bill_size(data)
        self.assertTrue('Adelie' in result)
        self.assertTrue('Gentoo' in result)
        self.assertAlmostEqual(result['Adelie'], 720.0, 1)

    def test_bill_size_empty(self):
        """Edge: empty dataset returns empty dictionary."""
        fieldnames = ['id', 'species', 'bill_length_mm', 'bill_depth_mm']
        rows = []
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = bill_size(data)
        self.assertEqual(result, {})

    def test_bill_size_all_invalid(self):
        """Edge: all invalid numeric values -> return empty dict."""
        fieldnames = ['id', 'species', 'bill_length_mm', 'bill_depth_mm']
        rows = [
            {'id': '1', 'species': 'Adelie', 'bill_length_mm': 'bad', 'bill_depth_mm': 'nope'},
            {'id': '2', 'species': 'Gentoo', 'bill_length_mm': '', 'bill_depth_mm': 'NaN'}
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = bill_size(data)
        self.assertEqual(result, {})

    # Now testing the avg_weight() function - Calculation #3

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

    # Now testing the percent_over_weight() function - Calculation #4    
    
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

    # Now testing the flipper_corr_strength() function - Calculation #5

    def test_flipper_corr_strength_positive_linear(self):
        fieldnames = ['id', 'species', 'flipper_length_mm', 'body_mass_g']
        rows = [
            {'id': '1', 'species': 'Adelie', 'flipper_length_mm': '180', 'body_mass_g': '360'},
            {'id': '2', 'species': 'Adelie', 'flipper_length_mm': '190', 'body_mass_g': '380'},
            {'id': '3', 'species': 'Gentoo', 'flipper_length_mm': '200', 'body_mass_g': '400'},
        ]
        path = self.make_temp_csv(rows, fieldnames); data = csv_open(path)
        result = flipper_corr_strength(data)
        self.assertEqual(result['correlation'], 1.0)
        self.assertEqual(
            result['interpretation'],
            'strong positive correlation between flipper length and penguin weight'
        )

    def test_flipper_corr_strength_negative_linear(self):
        fieldnames = ['id', 'species', 'flipper_length_mm', 'body_mass_g']
        rows = [
            {'id': '1', 'species': 'Adelie', 'flipper_length_mm': '180', 'body_mass_g': '400'},
            {'id': '2', 'species': 'Adelie', 'flipper_length_mm': '190', 'body_mass_g': '380'},
            {'id': '3', 'species': 'Gentoo', 'flipper_length_mm': '200', 'body_mass_g': '360'},
        ]
        path = self.make_temp_csv(rows, fieldnames); data = csv_open(path)
        result = flipper_corr_strength(data)
        self.assertEqual(result['correlation'], -1.0)
        self.assertEqual(
            result['interpretation'],
            'strong negative correlation between flipper length and penguin weight'
        )

    def test_flipper_corr_strength_skips_na_and_null(self):
        fieldnames = ['id', 'species', 'flipper_length_mm', 'body_mass_g']
        rows = [
            {'id': '1', 'species': 'Adelie', 'flipper_length_mm': 'NA',   'body_mass_g': '360'},   
            {'id': '2', 'species': 'Adelie', 'flipper_length_mm': '',     'body_mass_g': '380'},   
            {'id': '3', 'species': 'Gentoo', 'flipper_length_mm': '200',  'body_mass_g': 'null'},  
            {'id': '4', 'species': 'Gentoo', 'flipper_length_mm': '210',  'body_mass_g': '420'},   
            {'id': '5', 'species': 'Adelie', 'flipper_length_mm': '180',  'body_mass_g': '360'},   
        ]
        path = self.make_temp_csv(rows, fieldnames); data = csv_open(path)
        result = flipper_corr_strength(data)
        self.assertEqual(result['correlation'], 1.0)
        self.assertEqual(
            result['interpretation'],
            'strong positive correlation between flipper length and penguin weight'
        )

    def test_flipper_corr_strength_insufficient_after_cleaning(self):
        fieldnames = ['id', 'species', 'flipper_length_mm', 'body_mass_g']
        rows = [
            {'id': '1', 'species': 'Adelie', 'flipper_length_mm': 'NA',  'body_mass_g': '360'},
            {'id': '2', 'species': 'Adelie', 'flipper_length_mm': '190', 'body_mass_g': ''}, 
            {'id': '3', 'species': 'Gentoo', 'flipper_length_mm': '210', 'body_mass_g': '420'},  
        ]
        path = self.make_temp_csv(rows, fieldnames); data = csv_open(path)
        result = flipper_corr_strength(data)
        self.assertEqual(result['correlation'], None)
        self.assertEqual(result['interpretation'], 'Not enough data to find correlation.')

    # Now testing the species_flipper_length_range() function - Calculation #6

    def test_species_flipper_length_range_standard(self):
        """Standard: correctly computes min, max, and range for each species using flipper length."""
        fieldnames = ['id', 'species', 'flipper_length_mm']
        rows = [
            {'id': '1', 'species': 'Adelie', 'flipper_length_mm': '180'},
            {'id': '2', 'species': 'Adelie', 'flipper_length_mm': '190'},
            {'id': '3', 'species': 'Gentoo', 'flipper_length_mm': '210'},
            {'id': '4', 'species': 'Gentoo', 'flipper_length_mm': '215'}
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = species_flipper_length_range(data)

        self.assertEqual(result['Adelie']['min'], 180.0)
        self.assertEqual(result['Adelie']['max'], 190)       
        self.assertEqual(result['Adelie']['range'], 10.0)
        self.assertEqual(result['Gentoo']['min'], 210.0)
        self.assertEqual(result['Gentoo']['max'], 215)
        self.assertEqual(result['Gentoo']['range'], 5.0)

    def test_species_flipper_length_range_with_invalid_values(self):
        """Handles non-numeric or missing flipper lengths gracefully."""
        fieldnames = ['id', 'species', 'flipper_length_mm']
        rows = [
            {'id': '1', 'species': 'Adelie', 'flipper_length_mm': 'bad'},
            {'id': '2', 'species': 'Adelie', 'flipper_length_mm': '188'},
            {'id': '3', 'species': 'Gentoo', 'flipper_length_mm': 'N/A'},
            {'id': '4', 'species': 'Gentoo', 'flipper_length_mm': '205'}
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = species_flipper_length_range(data)

        self.assertEqual(result['Adelie']['min'], 188.0)
        self.assertEqual(result['Adelie']['max'], 188)
        self.assertEqual(result['Adelie']['range'], 0.0)
        self.assertEqual(result['Gentoo']['min'], 205.0)
        self.assertEqual(result['Gentoo']['max'], 205)
        self.assertEqual(result['Gentoo']['range'], 0.0)

    def test_species_flipper_length_range_empty_dataset(self):
        """Edge: returns empty dictionary for empty CSV."""
        fieldnames = ['id', 'species', 'flipper_length_mm']
        rows = []
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = species_flipper_length_range(data)
        self.assertEqual(result, {})

    def test_species_flipper_length_range_all_invalid(self):
        """Edge: all invalid rows result in empty dict."""
        fieldnames = ['id', 'species', 'flipper_length_mm']
        rows = [
            {'id': '1', 'species': 'Adelie', 'flipper_length_mm': ''},
            {'id': '2', 'species': 'Gentoo', 'flipper_length_mm': 'N/A'},
            {'id': '3', 'species': 'Chinstrap', 'flipper_length_mm': ''},
        ]
        path = self.make_temp_csv(rows, fieldnames)
        data = csv_open(path)
        result = species_flipper_length_range(data)
        self.assertEqual(result, {})


    
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
