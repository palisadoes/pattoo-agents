#!/usr/bin/env python3
"""Pattoo helper for the Linux _data.

Description:

    Uses Python2 to be compatible with most Linux systems


"""
# Standard libraries
import hashlib


def encode(value):
    """Encode string value to utf-8.

    Args:
        value: String to encode

    Returns:
        result: encoded value

    """
    # Initialize key variables
    result = value

    # Start decode
    if value is not None:
        if isinstance(value, str) is True:
            result = value.encode()

    # Return
    return result


def decode(value):
    """Decode utf-8 value to string.

    Args:
        value: String to decode

    Returns:
        result: decoded value

    """
    # Initialize key variables
    result = value

    # Start decode
    if value is not None:
        if isinstance(value, bytes) is True:
            result = value.decode('utf-8')

    # Return
    return result


def hashstring(string, sha=256, utf8=False):
    """Create a UTF encoded SHA hash string.

    Args:
        string: String to hash
        length: Length of SHA hash
        utf8: Return utf8 encoded string if true

    Returns:
        result: Result of hash

    """
    # Initialize key variables
    listing = [1, 224, 384, 256, 512]

    # Select SHA type
    if sha in listing:
        index = listing.index(sha)
        if listing[index] == 1:
            hasher = hashlib.sha1()
        elif listing[index] == 224:
            hasher = hashlib.sha224()
        elif listing[index] == 384:
            hasher = hashlib.sha512()
        elif listing[index] == 512:
            hasher = hashlib.sha512()
        else:
            hasher = hashlib.sha256()

    # Encode the string
    hasher.update(bytes(string.encode()))
    device_hash = hasher.hexdigest()
    if utf8 is True:
        result = device_hash.encode()
    else:
        result = device_hash

    # Return
    return result


def is_numeric(val):
    """Check if argument is a number.

    Args:
        val: String to check

    Returns:
        True if a number

    """
    # Try edge case
    if val is True:
        return False
    if val is False:
        return False

    # Try conversions
    try:
        float(val)
        return True
    except ValueError:
        return False
    except TypeError:
        return False
    except:
        return False
