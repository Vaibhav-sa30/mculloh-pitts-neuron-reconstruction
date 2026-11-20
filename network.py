"""Discrete-time network simulator for binary neurons."""
from collections import defaultdict
from typing import Mapping

from neuron import Neuron
from synapse import Synapse, SynapseType


class Network:
    """A synchronous network with positive integer synaptic delays.

    External afferents are source names that do not correspond to an internal
    Neuron. At time t, a synapse with delay d reads its source at time t-d.
    All internal neuron states at a time step are calculated from earlier
    history, so updates are synchronous and independent of insertion order.
    """

    def __init__(self) -> None:
        self.neurons: dict[str, Neuron] = {}
        self.synapses: list[Synapse] = []
        self.history: dict[str, list[bool]] = defaultdict(list)
        self.time = 0

    def add_neuron(self, neuron: Neuron) -> None:
        if neuron.name in self.neurons:
            raise ValueError(f"Neuron {neuron.name!r} already exists.")
        self.neurons[neuron.name] = neuron
        self.history.setdefault(neuron.name, [])

    def add_synapse(self, synapse: Synapse) -> None:
        if synapse.target not in self.neurons:
            raise ValueError(f"Unknown target neuron: {synapse.target!r}")
        if synapse.source == synapse.target:
            # Self-loops are allowed; the positive delay makes them well-defined.
            pass
        self.synapses.append(synapse)
        self.history.setdefault(synapse.source, [])

    @property
    def external_sources(self) -> set[str]:
        return {
            s.source for s in self.synapses
            if s.source not in self.neurons
        }

    def reset(self) -> None:
        self.history = defaultdict(list)
        for name in self.neurons:
            self.history[name] = []
        for synapse in self.synapses:
            self.history.setdefault(synapse.source, [])
        self.time = 0

    def _was_active(self, source: str, time_index: int) -> bool:
        if time_index < 0:
            return False
        values = self.history.get(source, [])
        return time_index < len(values) and bool(values[time_index])

    def step(self, external_activity: Mapping[str, bool] | None = None) -> dict[str, bool]:
        external_activity = dict(external_activity or {})
        unknown = set(external_activity) - self.external_sources
        if unknown:
            raise ValueError(f"Unknown external source(s): {sorted(unknown)}")

        current: dict[str, bool] = {
            source: bool(external_activity.get(source, False))
            for source in self.external_sources
        }

        incoming: dict[str, list[Synapse]] = defaultdict(list)
        for synapse in self.synapses:
            incoming[synapse.target].append(synapse)

        for name, neuron in self.neurons.items():
            excitatory_count = 0
            inhibitory_active = False

            for synapse in incoming[name]:
                source_time = self.time - synapse.delay
                active = self._was_active(synapse.source, source_time)
                if synapse.kind is SynapseType.INHIBITORY:
                    inhibitory_active = inhibitory_active or active
                elif active:
                    excitatory_count += 1

            current[name] = neuron.fires(excitatory_count, inhibitory_active)

        # Commit all states together after every neuron has been evaluated.
        for source in self.external_sources:
            self.history[source].append(current[source])
        for name in self.neurons:
            self.history[name].append(current[name])

        self.time += 1
        return current

    def run(self, steps: int, input_schedule=None) -> list[dict[str, bool]]:
        if steps < 0:
            raise ValueError("steps cannot be negative.")
        schedule = input_schedule or {}
        outputs = []
        for t in range(steps):
            outputs.append(self.step(schedule.get(t, {})))
        return outputs
