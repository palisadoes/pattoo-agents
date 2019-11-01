#!/usr/bin/env python3
"""Do interesting things."""

import itertools
import argparse


def main():
    """Process data."""
    # Create Gunicorn object to daemonize
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--values', '-v', help='List of integers to process.', type=str)
    args = parser.parse_args()
    listing_str = args.values.split(',')
    listing = list(map(int, listing_str))
    print(listing)
    ranges = ranger_modbus(listing)
    print(list(ranges))


def ranger_modbus(listing):
    """Convert a list of integers into ranges.

    Args:
        listing: List of integers to group

    Returns:
        result: List of tuples [(start, length of range), ...]

    """
    # Process data
    result = []
    ranges = list(ranger(listing))
    for (start, stop) in ranges:
        result.append((start, stop - start + 1))
    result.sort()
    return result


def ranger(listing):
    """Convert a list of integers into ranges.

    Args:
        listing: List of integers to group

    Yields:
        List of tuples [(start, stop of range), ...]

    """
    # Remove duplicates
    listing = list(set(listing))
    
    # Sort data beforehand to ensure grouping works.
    listing.sort()

    # Group data.
    for _, second in itertools.groupby(
            enumerate(listing), lambda pair: pair[1] - pair[0]):
        second = list(second)
        yield second[0][1], second[-1][1]


if __name__ == '__main__':
    main()
