"""
Example / testbed for Data Identifier usage
"""
import uuid


def create_data_id(datatype, paths=None, add_uuid=True):
    """
    Top-level interface for creating a data id
    """
    # Need data or added uuid
    fullpath = [
        datatype,
    ]
    if paths:
        fullpath.extend(list(paths))
    if add_uuid:
        fullpath.append(str(uuid.uuid1()))
    if not fullpath:
        raise Exception("No path created")
    return "http://earthscope.org/%s/" % "/".join(fullpath)


def join_provenances(provenance1, provenance2):
    """
    Given two provenances (lists of id strings) join them together
    """
    # Use a dict to join them
    joined = dict(
        (p, True) for p in provenance1
    )
    joined.update(
        (p, True) for p in provenance2
    )
    return list(joined.keys())
