"""Get a list of vacant lots in a neighborhood."""
import json

import pandas as pd


def get_block_list(neighborhood=None):
    """Get a list of blocks in a neighborhood."""
    if not neighborhood:
        return []
    file_data = []
    with open("tax_map.json") as json_file:
        file_data = json.load(json_file)
    neighborhood_info = file_data.get(neighborhood)
    boro_num = neighborhood_info.get("boro_num")
    range_list = neighborhood_info.get("block_range")
    nested_list = [list_from_range(i) for i in range_list]
    flat_list = [item for sublist in nested_list for item in sublist]
    return [boro_num, flat_list]


def list_from_range(k=None):
    """Return a list based of ints where k can be a range string or an int."""
    if not k:
        return []
    if isinstance(k, int):
        return [k]
    bounds = [int(i) for i in k.split("-")]
    return list(range(bounds[0], bounds[1]))


def parse_dataset(boro_num=None, block_list=[]):
    """Parse dataset to get list of vacant lots in the neighborhood."""
    if not boro_num or not block_list:
        return []
    full_df = pd.read_csv("vendor/Vacant_Publicly_Owned_Land.csv")
    vacant_df = full_df[
        (full_df["BOROUGH"] == boro_num) & (full_df["BLOCK"].isin(block_list))
    ]
    return vacant_df


def main():
    """Main."""
    [boro_num, block_list] = get_block_list("astoria")
    df = parse_dataset(boro_num, block_list)
    print(
        df[
            ["BOROUGH", "BLOCK", "LOT", "PARCEL_NAME", "PARCEL_ADDRESS"]
        ].sort_values(["BOROUGH", "BLOCK", "LOT"])
    )


if __name__ == "__main__":
    main()
