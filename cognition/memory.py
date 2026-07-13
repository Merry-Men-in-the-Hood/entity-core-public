"""
Memory - STUB for public repository

Memory schema and retrieval logic are in the private repository.

The functions below match the import surface used by entity_v0.py
so the orchestrator can be parsed and statically inspected from
the public repository, even though running it requires the private
implementation.
"""


def get_seen_registry():
    """Return the seen-threats registry."""
    raise NotImplementedError(
        "cognition.memory implementation is in the private repository."
    )


def get_posted_archive():
    """Return the posted-threats archive."""
    raise NotImplementedError(
        "cognition.memory implementation is in the private repository."
    )


def threat_hash(threat) -> str:
    """Compute a stable identifier for a threat record."""
    raise NotImplementedError(
        "cognition.memory implementation is in the private repository."
    )


class Memory:
    def store(self, item):
        raise NotImplementedError(
            "cognition.memory implementation is in the private repository."
        )

    def retrieve(self, query):
        raise NotImplementedError(
            "cognition.memory implementation is in the private repository."
        )
