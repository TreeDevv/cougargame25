import random
import pygame

photoList = [
    "axes1.jpg","axes2.jpg",
    "ball1.jpg","ball2.jpg",
    "bar1.jpg","bar2.jpg",
    "bass1.jpg","bass2.jpg",
    "bat1.jpg","bat2.jpg",
    "bow1.jpg","bow2.jpg",
    "broke1.jpg","broke2.jpg",
    "chile1.jpg","chile2.jpg",
    "china1.jpg","china2.jpg",
    "converse1.jpg","converse2.jpg",
    "cow1.jpg","cow2.jpg",
    "crane1.jpg","crane2.jpg",
    "flush1.jpg","flush2.jpg",
    "fly1.jpg","fly2.jpg",
    "gas1.jpg","gas2.jpg",
    "grave1.jpg","grave2.jpg",
    "jam1.jpg","jam2.jpg",
    "land1.jpg","land2.jpg",
    "lead1.jpg","lead2.jpg",
    "leaves1.jpg","leaves2.jpg",
    "light1.jpg","light2.jpg",
    "mark1.jpg","mark2.jpg",
    "minute1.jpg","minute2.jpg",
    "palm1.jpg","palm2.jpg",
    "park1.jpg","park2.jpg",
    "patient1.jpg","patient2.jpg",
     "peak1.jpg","peak2.jpg",
     "pen1.jpg","pen2.jpg",
    "record1.jpg","record2.jpg",
]

# Create tuple pairs
pairs = [(photoList[i], photoList[i + 1]) for i in range(0, len(photoList), 2)]

# Create index pool
_available_indices = list(range(len(pairs)))


def get_image_by_index(index, is_first):
    img1, img2 = pairs[index]
    return img1 if is_first else img2


def get_Random_Index():
    global _available_indices

    if not _available_indices:
        return None  # all used up

    index = random.choice(_available_indices)
    _available_indices.remove(index)
    return index


def get_record_name(index) -> str:
    return pairs[index][0].split(".")[0].rstrip("0123456789")


def get_total_num():
    return len(pairs)
