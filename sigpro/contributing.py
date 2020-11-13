"""Tools to contribute a primitive."""


def run_primitive(primitive, primitive_type=None,, primitive_subtype=None,
                  amplitude_values=None, sampling_frequency=None, frequency_values=None,
                  time_values=None, dataframe=None, **kwargs):
    """Run a given `primitive` with the specified configuration.

    Given a primitive and it's hyperparameters, attempt to run this against either the data
    provided by the user or against the demo data. If there is no data provided, the type
    and subtype of the primitive must be passed as arguments if those are not specified inside
    the metadata. If the data it's passed for the primitive there is no requirement of the type
    and subtype.

    In order to validate the primitive this function will run the following steps:

        * Create an instance of the primitive.
        * Call the primitive for each row in the data, the provided one or the demo one,
          using the given hyperparameter values.
        * Return a list of tuples with the output that the primitive generated

    Args:
        primitive (str):
            Path or name of the primitive to be used.
        primitive_type (str):
            Type to which the primitive belongs to.
        primitive_subtype (str):
            Subtype to which the primitive belongs to.
        amplitude_values (numpy.ndarray or None):
            Array of floats representing signal values or ``None``.
        sampling_frequency (float, int or None):
            Sampling frequency value passed in Hz or ``None``.
        frequency_values (numpy.ndarray or None):
            Array of floats representing frequency values for the given amplitude values
            or ``None``.
        time_values (numpy.ndarray or None):
            Array of floats representing time values or ``None``.
        dataframe (pandas.DataFrame or None):
            A ``pandas.DataFrame`` used as data for frequency time primitives or ``None``.
        context (optional):
            Additional context arguments required to run the primitive.
        hyperparameters (optional):
            Additional hyperparameters or tunable hyperparameters arguments.

    Returns:
        tuple:
            A tuple with the produced values from the primitive for each row of the demo data
            corresponding to the type and subtype of this.
    """
