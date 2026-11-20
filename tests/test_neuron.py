import unittest
from neuron import Neuron


class TestNeuron(unittest.TestCase):
    def test_threshold_one_behaves_like_or(self):
        neuron = Neuron("Y", threshold=1)
        self.assertFalse(neuron.fires(0, False))
        self.assertTrue(neuron.fires(1, False))
        self.assertTrue(neuron.fires(2, False))

    def test_threshold_two_behaves_like_and_for_two_inputs(self):
        neuron = Neuron("Y", threshold=2)
        self.assertFalse(neuron.fires(0, False))
        self.assertFalse(neuron.fires(1, False))
        self.assertTrue(neuron.fires(2, False))

    def test_inhibition_vetoes_excitation(self):
        neuron = Neuron("Y", threshold=1)
        self.assertFalse(neuron.fires(3, True))


if __name__ == "__main__":
    unittest.main()
