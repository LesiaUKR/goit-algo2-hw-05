from colorama import Fore, Style, init
import time
from datasketch import HyperLogLog
import re

# Initialize colorama
init()


def load_data(file_path: str) -> list:
    """
    Loads IP addresses from a log file, ignoring invalid lines.

    Args:
        file_path (str): Path to the log file.

    Returns:
        list: A list of valid IP addresses.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or contains no valid IP
        addresses.
    """
    ip_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
    ip_addresses = []

    try:
        # Open the file with UTF-8 encoding
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                match = ip_pattern.search(line.strip())
                if match:
                    ip_addresses.append(match.group())
    except FileNotFoundError:
        print(
            Fore.RED + f"Error: File '{file_path}' not found."
            + Style.RESET_ALL
        )
        raise
    except UnicodeDecodeError:
        print(
            Fore.RED
            + f"Error: The file '{file_path}' contains invalid characters."
              f" Please ensure it is encoded in UTF-8."
            + Style.RESET_ALL
        )
        raise
    except Exception as e:
        print(Fore.RED + f"Error reading file: {e}" + Style.RESET_ALL)
        raise

    if not ip_addresses:
        print(
            Fore.YELLOW
            + "Warning: The file does not contain any valid IP addresses."
            + Style.RESET_ALL
        )
        raise ValueError("The file does not contain valid IP addresses.")

    return ip_addresses


def exact_count_unique_ips(ip_addresses: list) -> int:
    """
    Counts the exact number of unique IP addresses using a set.

    Args:
        ip_addresses (list): A list of IP addresses.

    Returns:
        int: The exact count of unique IP addresses.
    """
    return len(set(ip_addresses))


def hyperloglog_count_unique_ips(ip_addresses: list, p: int = 10) -> int:
    """
    Estimates the number of unique IP addresses using HyperLogLog.

    Args:
        ip_addresses (list): A list of IP addresses.
        p (int): The precision parameter for HyperLogLog (default is 10).

    Returns:
        int: The estimated count of unique IP addresses.
    """
    hll = HyperLogLog(p=p)  # Use 'p' instead of 'error_rate'
    for ip in ip_addresses:
        hll.update(ip.encode("utf-8"))
    return int(hll.count())


def compare_methods(ip_addresses: list):
    """
    Compares the performance of exact counting and HyperLogLog.

    Args:
        ip_addresses (list): A list of IP addresses.
    """
    # Exact counting
    start_time = time.time()
    exact_count = exact_count_unique_ips(ip_addresses)
    exact_time = time.time() - start_time

    # HyperLogLog counting
    start_time = time.time()
    hll_count = hyperloglog_count_unique_ips(ip_addresses)
    hll_time = time.time() - start_time

    # Print results
    print(Fore.CYAN + "Comparison Results:" + Style.RESET_ALL)
    print(
        Fore.YELLOW
        + "{:>25} {:>15} {:>15}"
        .format("", "Exact Count", "HyperLogLog")
        + Style.RESET_ALL
    )
    print(
        Fore.GREEN
        + "{:>25} {:>15.1f} {:>15.1f}"
        .format("Unique Elements", exact_count, hll_count)
        + Style.RESET_ALL
    )
    print(
        Fore.GREEN
        + "{:>25} {:>15.4f} {:>15.4f}".format(
            "Execution Time (sec)", exact_time, hll_time
        )
        + Style.RESET_ALL
    )


if __name__ == "__main__":
    # Path to the log file
    file_path = "lms-stage-access.log"

    try:
        # Load data
        ip_addresses = load_data(file_path)

        # Compare methods
        compare_methods(ip_addresses)
    except Exception as e:
        print(
            Fore.RED + f"Program terminated with an error: {e}" +
            Style.RESET_ALL
        )
