
def GetValidWords(filepath: str) -> {str}:
    """
    Get valid words from dictionary.txt
    Ideally, this would be saved in a database

    :return: set of valid words from dictionary
    """
    with open(filepath, 'r') as f:
        content = f.readlines()
    return set([line.strip().upper() for line in content])
