import unittest
from objects import *

class ReactionTest(unittest.TestCase):
    def setUp(self):
        self.rxn = Reaction({'Glc':1, 'ADP': 2, 'P':2}, {'EtOH': 2, 'CO2': 2, 'ATP': 2})

    def test_no_res(self):
        actual = self.rxn.getMoles([])
        expected = {'Glc':0, 'ADP':0, 'P':0, 'EtOH':0, 'CO2':0, 'ATP':0}
        self.assertEqual(actual, expected)

    def test_one_zero(self):
        actual = self.rxn.getMoles([('Glc',0)])
        expected = {'Glc':0, 'ADP':0, 'P':0, 'EtOH':0, 'CO2':0, 'ATP':0}
        self.assertEqual(actual, expected)

    def test_foreign_res(self):
        actual = self.rxn.getMoles([('N',1)])
        expected = {'Glc':0, 'ADP':0, 'P':0, 'EtOH':0, 'CO2':0, 'ATP':0}
        self.assertEqual(actual, expected)

    def test_all_zero(self):
        actual = self.rxn.getMoles([('Glc',0), ('ADP',0), ('P',0), ('EtOH',0), ('CO2',0), ('ATP',0)])
        expected = {'Glc':0, 'ADP':0, 'P':0, 'EtOH':0, 'CO2':0, 'ATP':0}
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ReactionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)