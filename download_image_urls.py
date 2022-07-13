import os
from typing import List, Dict
from search_bing_api import search_images_bing

# I don't have the below .txt file anymore, but I believe it looked something like this:

"""
sfw
cat
dog
woman on the beach
etc.
nsfw
a dirty query
an even dirtier query
etc.
"""

search_query_file = "../nsfw_queries.txt"
key = os.environ.get("AZURE_SEARCH_KEY")


def download_urls(file_path: str, cat_prefix: str) -> Dict[str, List[str]]:
    # Get search terms from file, save results as a Dict
    with open(file_path) as infile:
        result_dict = {}
        for query in infile:
            query = query.rstrip()
            if cat_prefix in query:
                # Set current subcategory
                subcategory = query.split("/")[-1]
                subcategory_urls = []
            else:
                # Fetch image urls pertaining to subcategory
                query_urls = search_images_bing(key, query)
                subcategory_urls.extend(query_urls)
                # Save dict containing {dir_path : [img_urls]}
                result_dict[subcategory] = subcategory_urls
    return result_dict


def write_urls_to_file(url_dict: Dict[str, List[str]], base_path: str):
    # Create base dir if needed
    try:
        os.mkdir(base_path)
    except FileExistsError:
        print("Directory exists already")
    # Write one file per subcategory, save to base dir
    for subcat, url_list in url_dict.items():
        file_name = f"{subcat}.txt"
        file_path = os.path.join(base_path, file_name)
        with open(file_path, "w") as outfile:
            for url in url_list:
                url = url + "\n"
                outfile.writelines(url)
