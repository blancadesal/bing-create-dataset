from azure.cognitiveservices.search.imagesearch import ImageSearchClient as api
from msrest.authentication import CognitiveServicesCredentials as auth
from typing import List
import os

key = os.environ.get("AZURE_SEARCH_KEY")
endpoint = "https://imageserach.cognitiveservices.azure.com/"


def search_images_bing(
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
