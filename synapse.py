"""Synapses connecting source units to target neurons."""
from dataclasses import dataclass
from enum import Enum


class SynapseType(str, Enum):
    EXCITATORY = "excitatory"
    INHIBITORY = "inhibitory"


@dataclass(frozen=True)
class Synapse:
    source: str
    target: str
    kind: SynapseType = SynapseType.EXCITATORY
    delay: int = 1

    def __post_init__(self) -> None:
        if not self.source or not self.target:
            raise ValueError("Synapse source and target must be non-empty.")
        if self.delay < 1:
            raise ValueError("Synaptic delay must be at least one time step.")
        if isinstance(self.kind, str):
            object.__setattr__(self, "kind", SynapseType(self.kind))
