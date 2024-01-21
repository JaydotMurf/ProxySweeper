def write_proxies_to_file(proxies, file_path):
    """
    Writes a list of proxy IP addresses to a specified file.

    Args:
        proxies (str): String containing proxy IP addresses, each separated by a newline.
        file_path (str): The path to the file where the proxy IPs will be written.
    """
    assert proxies, "No proxies provided to write to file"
    assert file_path, "No file path provided"

    with open(file_path, "w") as file:
        file.write(proxies)
