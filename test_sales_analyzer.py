import unittest
import pandas as pd
import os
from sales_analyzer import SalesAnalyzer

class TestSalesAnalyzer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests."""
        # Create a sample test data file
        cls.test_data = {
            'date': ['2023-01-15', '2023-01-20', '2023-02-10', '2023-02-25', '2023-03-05'],
            'branch_id': ['BR001', 'BR002', 'BR001', 'BR002', 'BR001'],
            'product_name': ['Apple', 'Banana', 'Apple', 'Orange', 'Banana'],
            'category': ['Fruits', 'Fruits', 'Fruits', 'Fruits', 'Fruits'],
            'price': [1.50, 0.80, 1.60, 2.00, 0.85],
            'quantity': [10, 15, 8, 12, 20],
            'total_amount': [15.00, 12.00, 12.80, 24.00, 17.00]
        }
        
        cls.test_df = pd.DataFrame(cls.test_data)
        cls.test_file = 'test_sales_data.csv'
        cls.test_df.to_csv(cls.test_file, index=False)
        
        # Initialize the analyzer
        cls.analyzer = SalesAnalyzer(cls.test_file)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)
    
    def test_load_data(self):
        """Test data loading and preprocessing."""
        self.assertIsInstance(self.analyzer.df, pd.DataFrame)
        self.assertIn('month', self.analyzer.df.columns)
        self.assertIn('year', self.analyzer.df.columns)
        self.assertIn('week', self.analyzer.df.columns)
        self.assertEqual(len(self.analyzer.df), 5)
    
    def test_monthly_sales_analysis(self):
        """Test monthly sales analysis."""
        result = self.analyzer.monthly_sales_analysis()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('total_amount', result.columns)
        self.assertIn('branch_id', result.columns)
        self.assertGreater(len(result), 0)
    
    def test_monthly_sales_analysis_with_filters(self):
        """Test monthly sales analysis with filters."""
        result = self.analyzer.monthly_sales_analysis(branch_id='BR001', year=2023)
        self.assertIsInstance(result, pd.DataFrame)
        # Should only contain BR001 data
        if not result.empty:
            self.assertTrue(all(result['branch_id'] == 'BR001'))
    
    def test_price_analysis_by_product(self):
        """Test price analysis by product."""
        result = self.analyzer.price_analysis_by_product()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('product_name', result.columns)
        self.assertIn('mean', result.columns)
        self.assertIn('min', result.columns)
        self.assertIn('max', result.columns)
        self.assertGreater(len(result), 0)
    
    def test_weekly_sales_analysis(self):
        """Test weekly sales analysis."""
        result = self.analyzer.weekly_sales_analysis()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('total_amount', result.columns)
        self.assertIn('week', result.columns)
        self.assertIn('year', result.columns)
        self.assertGreater(len(result), 0)
    
    def test_product_preference_analysis(self):
        """Test product preference analysis."""
        result = self.analyzer.product_preference_analysis()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('product_name', result.columns)
        self.assertIn('quantity', result.columns)
        self.assertGreater(len(result), 0)
        # Check if results are sorted by quantity in descending order
        if len(result) > 1:
            self.assertGreaterEqual(result.iloc[0]['quantity'], result.iloc[1]['quantity'])
    
    def test_total_sales_distribution_analysis(self):
        """Test total sales distribution analysis."""
        result = self.analyzer.total_sales_distribution_analysis()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('category', result.columns)
        self.assertIn('total_amount', result.columns)
        self.assertGreater(len(result), 0)
        # Check if results are sorted by total_amount in descending order
        if len(result) > 1:
            self.assertGreaterEqual(result.iloc[0]['total_amount'], result.iloc[1]['total_amount'])
    
    def test_apply_filters(self):
        """Test the _apply_filters method."""
        # Test with branch filter
        filtered_df = self.analyzer._apply_filters(self.analyzer.df, branch_id='BR001')
        self.assertTrue(all(filtered_df['branch_id'] == 'BR001'))
        
        # Test with year filter
        filtered_df = self.analyzer._apply_filters(self.analyzer.df, year=2023)
        self.assertTrue(all(filtered_df['year'] == 2023))
        
        # Test with month filter
        filtered_df = self.analyzer._apply_filters(self.analyzer.df, month=1)
        self.assertTrue(all(filtered_df['month'] == 1))
    
    def test_empty_results(self):
        """Test handling of filters that return no results."""
        # Test with non-existent branch
        result = self.analyzer.monthly_sales_analysis(branch_id='BR999')
        self.assertTrue(result.empty)
        
        # Test with non-existent year
        result = self.analyzer.price_analysis_by_product(year=2025)
        self.assertTrue(result.empty)

if __name__ == '__main__':
    unittest.main()

