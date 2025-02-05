from typing import List

from flatten_json import flatten

import config
from src.models.basemodels.shimano import ShimanoBaseModel
from src.models.exceptions import (
    MissingInformationError,
    ProductNotFoundError,
    ScrapeError,
)
from src.models.suppliers.shimano.product.search_product import ShimanoSearchProduct


class ShimanoProductSearchEndpoint(ShimanoBaseModel):
    """This endpoint has price and other product information that we want

    This endpoint has a little less details than the product
    endpoints but it has the bit advantage that it works consistently

    2024: updated endpoint url"""

    product_code: str
    products: List[ShimanoSearchProduct] = []

    def get(self) -> ShimanoSearchProduct:
        if not self.session or not self.product_code:
            raise MissingInformationError()
        url = (
            "https://api.c5vp9gk-shimanoin2-p1-public."
            "model-t.cc.commerce.ondemand.com"
            f"/occ/v2/shimanoBike-se/products/{self.product_code}?"
            f"fields=name,purchasable,baseOptions(DEFAULT),baseProduct,"
            f"variantMatrix,variantOptions(DEFAULT),variantType,averageRating,"
            f"images(FULL),classifications,manufacturer,numberOfReviews,"
            f"categories(FULL),FULL&lang=sv&curr=SEK"
        )
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Authorization': 'bearer cHNINqaeSDBtDDa-gIqLxgEgaas',
            "Origin": "https://b2b.shimano.com",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://b2b.shimano.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
        }
        response = self.session.get(
            url,
            headers=headers,
        )
        if response.status_code == 200:
            data = response.json()
            flat_data = flatten(data)
            if not flat_data:
                raise ValueError("no data")
            # with open("flattened.json", "w") as file:
            #     json.dump(flat_data, file, indent=4)
            # exit()
            if config.debug_responses:
                print(flat_data)
            return ShimanoSearchProduct(**flat_data)
        elif response.status_code == 400:
            data = response.json()
            if data["errors"][0]["message"] == "product.not.found":
                raise ProductNotFoundError(f"see {url}")
            else:
                raise ScrapeError(f'unknown error: {data["errors"][0]["message"]}')
        else:
            # find cause of errors
            # print(response.text)
            raise ScrapeError(
                f"got {response.status_code} and {response.text} from Shimano, see {url}"
            )
