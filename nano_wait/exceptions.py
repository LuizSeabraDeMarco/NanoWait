class VisionTimeout(Exception):
    """Raised when a visual condition is not detected within the timeout."""


class WaitTimeoutError(Exception):
    """Raised when a callable condition does not become True within timeout."""
