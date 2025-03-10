def filter_datasets(datasets, filter_3d=None):
    """
    Filters the datasets based on whether they are 2D, 3D, or both.
    :param datasets: List of dataset classes to filter.
    :param filter_3d: If True, filters only 3D datasets. If False, filters only 2D datasets. If None, includes all datasets.
    :return: Filtered list of dataset classes.
    """
    if filter_3d is None:
        return datasets
    return [dataset_cls for dataset_cls in datasets if dataset_cls().is_3d == filter_3d]
