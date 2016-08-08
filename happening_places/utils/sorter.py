def get_newest(num, listings):
    """Return the 'num' latest items in given listing.
    """
    return sorted(listings, key=lambda x: len(x), reverse=True)[: num]
