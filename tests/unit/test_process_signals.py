# -*- coding: utf-8 -*-

"""Unit tests for the sigpro.process_signals module."""


def test_process_signals_target_column():
    """Test the function ``process_signals``, if a target column is passed.

    Ensure that the primitives are being applied to the specified target column.

    Input:
        - data (pd.DataFrame).
        - primitives (list).
        - target_column (str).
    Output:
        - The featurized dataframe using the selected column.
    """
    pass


def test_process_signals_multiple_first_level_primitives():
    """Test the function ``process_signals`` with more than one first level primitive.

    Process signals is expected to call each one of the first level primitives with
    the original ``target_column``.

    Input:
        - data (pd.DataFrame).
        - primitives (list).
        - target_column (str).
    Output:
        - The featurized dataframe using more than one first level primitive.
    Mock:
        - Primitives
    """
    pass


def test_process_signals_multiple_second_level_primitives():
    """Test the function ``process_signals`` with more than one second level primitives.

    Process signals is expected to call each of the second level primitives (the ones specified
    for each first level primitive) with the output of it's parent primitive output.

    Input:
        - data (pd.DataFrame).
        - primitives (list).
        - target_column (str).
    Output:
        - The featurized dataframe using more than one second level primitives.
    """
    pass


def test_process_signals_multiple_transformations():
    """Test the function ``process_signals`` that can apply more than one transformation.

    After a transformation to the ``target_column`` has been applied, there could be another
    transformation and/or aggregation to be applied afterwards. Ensure that a transformation
    can be applied and it's primitives.

    Input:
        - data (pd.DataFrame).
        - primitives (list).
        - target_column (str).
    Output:
        - The featurized dataframe using multiple transformations.
    """
    pass


def test_process_signals_nomenclature():
    """Test the function ``process_signals`` that the names specified are as expected.

    When a new feature is generated this comes with a name which comes specified by the
    name of the previous level primitive and the following primitive name usually it's
    ``transformation_name_aggregation_name``.

    Input:
        - data (pd.DataFrame).
        - primitives (list).
        - target_column (str).
    Output:
        - The featurized dataframe with the expected column names.
    """
    pass


def test_process_signals_first_level_hyperparameters():
    """Test the function ``process_signals`` that uses the specified hyperparameters.

    Ensure that the specified hyperparameters are used for the first level primitives.

    Input:
        - data (pd.DataFrame).
        - primitives (list).
        - target_column (str).
    Output:
        - The featurized dataframe.
    """
    pass


def test_process_signals_second_level_hyperparameters():
    """Test the function ``process_signals`` that uses the specified hyperparameters.

    Ensure that the specified hyperparameters are used for the second level primitives.

    Input:
        - data (pd.DataFrame).
        - primitives (list).
        - target_column (str).
    Output:
        - The featurized dataframe.
    """
    pass
