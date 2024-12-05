import os

def get_data_path(relative_path: str) -> str:
    """
    Get the absolute path to a file in the `dataset` directory.

    Args:
        relative_path: The path to the file relative to the `dataset` directory including the file name.

    Returns:
        The full path to the file in the `dataset` directory.

    Examples:
        >>> get_data_path("assignment1/boston_listings.csv")
        'C:/Users/username/assignments/dataset/assignment1/boston_listings.csv'
    """
    joined_path = os.path.join(os.path.dirname(__file__), "../../dataset", relative_path)
    return os.path.abspath(joined_path)
