"""Module constants for test markers."""

# Marker name
MARKER_NAME = "depends"

# Keyword arguments for the marker
MARKER_KWARGS = {
    "names": "Custom names for the tests",
    "depends_on": "Tests to depend on"
}

# Default value for the marker keyword arguments
MARKER_KWARG_DEFAULTS = {
    MARKER_KWARGS["names"]: None,
    MARKER_KWARGS["depends_on"]: None
}
