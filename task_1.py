from colorama import Fore, Style, init
import mmh3
from bitarray import bitarray

# Initialize colorama
init()


class BloomFilter:
    """
    A Bloom Filter is a space-efficient probabilistic data structure
    that is used to test whether an element is a member of a set.
    It allows for false positives but guarantees no false negatives.

    Attributes:
        size (int): The size of the Bloom filter bit array.
        num_hashes (int): The number of hash functions to use.
        bit_array (bitarray): The bit array representing the Bloom filter.
    """

    def __init__(self, size: int, num_hashes: int):
        """
        Initializes the BloomFilter with a given size and number of hash
        functions.

        Args:
            size (int): The size of the Bloom filter bit array.
            num_hashes (int): The number of hash functions to use.
        """
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)  # Initialize all bits to 0

    def add(self, item: str):
        """
        Adds an item to the Bloom filter.

        Args:
            item (str): The item to be added to the Bloom filter.
        """
        for seed in range(self.num_hashes):
            index = mmh3.hash(item, seed) % self.size
            self.bit_array[index] = 1

    def contains(self, item: str) -> bool:
        """
        Checks if an item is in the Bloom filter.

        Args:
            item (str): The item to check for presence in the Bloom
            filter.

        Returns:
            bool: True if the item is likely in the filter, False
            otherwise.
        """
        for seed in range(self.num_hashes):
            index = mmh3.hash(item, seed) % self.size
            if self.bit_array[index] == 0:
                return False
        return True


def check_password_uniqueness(
        bloom_filter: BloomFilter, new_passwords: list) -> dict:
    """
    Checks the uniqueness of new passwords using a Bloom filter.

    Args:
        bloom_filter (BloomFilter): An instance of BloomFilter.
        new_passwords (list): A list of new passwords to check for
        uniqueness.

    Returns:
        dict: A dictionary where keys are passwords and values are their
        uniqueness status.
    """
    results = {}
    for password in new_passwords:
        if not password:
            results[password] = "invalid"
        elif bloom_filter.contains(password):
            results[password] = "already used"
        else:
            results[password] = "unique"
            bloom_filter.add(password)
    return results


if __name__ == "__main__":
    # Initialize Bloom filter
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Add existing passwords
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Check new passwords
    new_passwords_to_check = [
        "password123", "newpassword", "admin123", "guest", ""
    ]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Print results with color
    for password, status in results.items():
        if status == "already used":
            print(
                Fore.RED + f"Password '{password}' - {status}." +
                Style.RESET_ALL
            )
        elif status == "unique":
            print(
                Fore.GREEN + f"Password '{password}' - {status}." +
                Style.RESET_ALL
            )
        else:
            print(
                Fore.YELLOW + f"Password '{password}' - {status}." +
                Style.RESET_ALL
                  )
