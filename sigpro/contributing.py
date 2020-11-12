"""Tools to contribute a primitive."""


def run_primitive(primitive, **kwargs):
    """Run a given `primitive` with the specified hyperparameters against demo data.

    Given a primitive and it's tunable hyperparameters and fixed hyperparameters, perform the
    following steps in order to validate the correct execution of the primitive:

        * Load the demo data as timeseries segments.
        * If the primitive is a frequency or frequency_time aggregation, it applies an
          ``fft`` or ``stft`` transformation on the demo data.
        * Call the primitive for each row in the data using the given hyperparameter values.
        * Return a list of tuples with the output that the primitive generated

    Args:
        primitive (str):
            Path or name of the primitive to be used.
        hyperparameters (optional):
            Additional hyperparameters or tunable hyperparameters arguments.
        context (additional):
            Additional context arguments required to run the primitive.

    Returns:
        tuple:
            A tuple with the produced values from the primitive for each row of the demo data
            corresponding to the type and subtype of this.
    """
