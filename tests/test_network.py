import unittest
from network import Network
from neuron import Neuron
from synapse import Synapse, SynapseType


class TestNetwork(unittest.TestCase):
    def test_one_step_delay(self):
        net = Network()
        net.add_neuron(Neuron("Y", 1))
        net.add_synapse(Synapse("A", "Y", delay=1))
        first = net.step({"A": True})
        second = net.step({"A": False})
        self.assertFalse(first["Y"])
        self.assertTrue(second["Y"])

    def test_and_gate(self):
        net = Network()
        net.add_neuron(Neuron("Y", 2))
        net.add_synapse(Synapse("A", "Y"))
        net.add_synapse(Synapse("B", "Y"))
        net.step({"A": True, "B": True})
        result = net.step({})
        self.assertTrue(result["Y"])

    def test_inhibitory_veto(self):
        net = Network()
        net.add_neuron(Neuron("Y", 1))
        net.add_synapse(Synapse("A", "Y", SynapseType.EXCITATORY))
        net.add_synapse(Synapse("B", "Y", SynapseType.INHIBITORY))
        net.step({"A": True, "B": True})
        result = net.step({})
        self.assertFalse(result["Y"])


if __name__ == "__main__":
    unittest.main()
