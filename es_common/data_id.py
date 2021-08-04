"""
Example / testbed for Data Identifier usage
"""
import uuid


def create_data_id(datatype, data=None):
    """
    Top-level interface for creating a data id
    """
    # By default, we just have a UUID
    return "http://earthscope.org/id/%s/%s" % (datatype, str(uuid.uuid1()))


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
