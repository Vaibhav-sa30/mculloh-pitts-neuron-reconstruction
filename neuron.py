"""Binary McCulloch–Pitts-style neuron.

This implementation uses `threshold` to mean the MINIMUM number of active
excitatory synapses required to fire. The 1943 paper describes excitation as
exceeding a threshold; this minimum-count convention is the equivalent
integer representation (minimum_count = paper_threshold + 1).

Any active inhibitory synapse vetoes firing at that time.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Neuron:
    name: str
    threshold: int = 1

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Neuron name cannot be empty.")
        if self.threshold < 1:
            raise ValueError("threshold must be at least 1.")

    def fires(self, active_excitatory_count: int, inhibitory_active: bool) -> bool:
        if inhibitory_active:
            return False
        return active_excitatory_count >= self.threshold
