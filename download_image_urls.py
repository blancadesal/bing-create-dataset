import os
from typing import List, Dict

from azure.cognitiveservices.search.imagesearch import ImageSearchClient as api
from msrest.authentication import CognitiveServicesCredentials as auth

# I don't have the nsfw_queries.txt file anymore, but I believe it looked something like this:

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
endpoint = "https://imageserach.cognitiveservices.azure.com/"


def search_bing_images(
    key: str, term: str, min_sz: int = 460, count: int = 50
) -> List[str]:
    client = api(endpoint, auth(key))
    image_results = client.images.search(
        query=term, count=count, min_height=min_sz, min_width=min_sz, safe_search="off"
    )
    # return image_results
    if image_results.value:
        print(
            f"Total number of image urls returned for query {term}: {len(image_results.value)}"
        )
        image_urls = [img.content_url for img in image_results.value]
        return image_urls
    else:
        print("No image results returned!")
        return []


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
                query_urls = search_bing_images(key, query)
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
