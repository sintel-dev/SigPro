# -*- coding: utf-8 -*-


def process_signals(data, primitives, target_column='values'):
    """Process Signals.

    The Process Signals is responsible for applying a collection of primitives specified by the
    user in order to create features for the given data.

    Args:
        data (pandas.DataFrame):
            Dataframe with the signal value.
        primitives (list):
            A list of python dictionaries with the following keys:

                * ``Name``:
                    Name of the transformation / aggregation.
                * ``primitive``:
                    Name of the primitive to apply.
                * ``hyperparameters``:
                    Dictionary containing the hyperparameters of the primitive.
                * ``primitives``:
                    List with dictionaries describing the primitives to use for the output of this
                    primitive. (Allows the same nomenclature as this one).

        target_column (str):
            The column which contains the signal. Defaults to ``values``.

    Returns:
        pandas.DataFrame:
            A dataframe with new feature columns by applying the previous primitives.
    """
    pass
