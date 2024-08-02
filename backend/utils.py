def convert_string(d, s):
    """
    Replace placeholders in a string with corresponding values from a dictionary.

    :param d: Dictionary containing the values to be inserted into the string.
    :type d: dict
    :param s: String with placeholders that match the keys in the dictionary.
    :type s: str
    :return: A string with the placeholders replaced by dictionary values.
    :rtype: str
    """
    for key, value in d.items():
        s = s.replace(f"{{{key}}}", value)
    return s