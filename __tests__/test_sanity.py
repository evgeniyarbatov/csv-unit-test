import unittest
import sys

import pandas as pd
import numpy as np

# Make output less verbose
sys.tracebacklimit = -1

class SanityTest(unittest.TestCase):
    def setUp(self):
      self.df = pd.read_csv(
         'data/gpx-route.csv',
          names=[
              'latitude',
              'longitude',
              'distance',
              'cuttoff_time',
              'address',
              'total_hours',
              'planned_time'
          ]
      )

    def get_sample_row(self, df):
        idx = np.random.randint(0, len(df))
        row = df.iloc[idx]
        return ','.join(row.astype(str))

    def test_address(self):
        is_alphabetic = self.df['address'].str.contains('[a-zA-Z]')
        self.assertTrue(
            is_alphabetic.all(), 
            f"Addresses are not alphabetic: {self.get_sample_row(self.df[~is_alphabetic])}",
        )

    def test_increasing_colums(self):
        for column_name in ['distance', 'total_hours']:
            previous = self.df[column_name].shift(1)
            is_increasing = self.df[column_name] > previous
            self.assertTrue(
                is_increasing[1:].all(), 
                f"Values in {column_name} are not increasing: {
                    self.get_sample_row(self.df[~is_increasing])
                }",
            )
