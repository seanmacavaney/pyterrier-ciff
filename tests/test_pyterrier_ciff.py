import unittest
import pyterrier_ciff
import pandas as pd

from pyterrier_ciff import MyAwesomeTransformer


class TestPyterrier_ciff(unittest.TestCase):
    def test_something(self):
        # Arrange
        transformer = MyAwesomeTransformer()
        inp = pd.DataFrame()

        # Act
        res = transformer(inp)

        # Assert
        pd.testing.assert_frame_equal(inp, res)
