import numpy as np

# do not change the code in the block below
# __________start of block__________
class DummyMatch:
    def __init__(self, queryIdx, trainIdx, distance):
        self.queryIdx = queryIdx  # index in des1
        self.trainIdx = trainIdx  # index in des2
        self.distance = distance
# __________end of block__________

def match_key_points_numpy(des1: np.ndarray, des2: np.ndarray) -> list:
    """
    Match descriptors using brute-force matching with cross-check.

    Args:
        des1 (np.ndarray): Descriptors from image 1, shape (N1, D)
        des2 (np.ndarray): Descriptors from image 2, shape (N2, D)

    Returns:
        List[DummyMatch]: Sorted list of mutual best matches.
    """
    # YOUR CODE HERE
    matches = []

    d1_pair = []
    for i, d1 in enumerate(des1):
        min_dist = None
        d2_idx = None
        for j, d2 in enumerate(des2):
            dist = np.linalg.norm(d1 - d2)
            if min_dist is None or dist < min_dist:
                min_dist = dist
                d2_idx = j

        d1_pair.append(d2_idx)

    d2_pair = []
    for i, d2 in enumerate(des2):
        min_dist = None
        d1_idx = None
        for j, d1 in enumerate(des1):
            dist = np.linalg.norm(d2 - d1)
            if min_dist is None or dist < min_dist:
                min_dist = dist
                d1_idx = j

        d2_pair.append(d1_idx)

    for d1_idx, d2_idx in enumerate(d1_pair):
        if d1_idx == d2_pair[d2_idx]:
            matches.append(DummyMatch(d1_idx, d2_idx, np.linalg.norm(des1[d1_idx] - des2[d2_idx])))

    matches.sort(key=lambda x: x.distance)

    return matches