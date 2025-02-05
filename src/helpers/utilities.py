# Copyright (C) 2021, 2024 Dennis Priskorn
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import argparse
import logging

from requests import Response
from rich import print

from src.models.vat_rate import VatRate

logger = logging.getLogger(__name__)


#
# CLI related
#


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--interactive", help="Interactive mode", action="store_true"
    )
    parser.add_argument(
        "--loglevel",
        help="Loglevel",
    )
    parser.add_argument(
        "-r",
        "--external_ref",
        help="Product ID",
    )
    parser.add_argument(
        "-u",
        "--url",
        help="Product URL",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        help="SQL pattern to search for",
    )
    parser.add_argument(
        "-a",
        "--amount",
        help="Amount for payment",
    )
    parser.add_argument(
        "--total_sek",
        help=(
            "Total amount in sek, see "
            "http://dolibarr.localhost/compta/bank/bankentries_list.php "
            "and search for upwork within the relevant dates"
        ),
    )
    parser.add_argument(
        "-n",
        "--new-multiprice1",
        help="New price",
    )
    # https://stackoverflow.com/questions/
    # 15753701/how-can-i-pass-a-list-as-a-command-line-argument-
    # with-argparse
    parser.add_argument(
        # "-l",
        "--list",
        nargs="+",
        help="List of supplier product IDs",
    )
    parser.add_argument(
        # "-l",
        "--file",
        help="File to process",
    )
    parser.add_argument(
        # "-l",
        "--seb",
        help="SEB csv file to process. Download from online bank.",
    )
    parser.add_argument(
        # "-l",
        "--upwork",
        help="Upwork csv file to process. Download from upwork.com -> transactions",
    )
    return parser.parse_args()


def print_result(response: Response, success_text: str, fail_text: str):
    """Response is a Response-object"""
    if response.status_code == 200:
        print(f"{success_text}.")
        # json = response.json()
        # if config.debug: print(json)
    else:
        if response.text == "":
            text = "(no body content)"
        else:
            text = response.text
        raise ValueError(
            f"Error {fail_text}. "
            + "Dolibarr returned: "
            + f"{response.status_code}\n{text}"
        )


def vat_rate_to_float_multiplier(vat_rate) -> float:
    if not vat_rate:
        raise ValueError("Vat rate was None")
    if not isinstance(vat_rate, VatRate):
        raise ValueError("not a VatRate")
    return float((100 + float(vat_rate.value)) / 100)


# def fallback_weight(dolibarr_response):
#     # Fallback to dolibarr
#     weight = dolibarr_response["weight"]
#     if not empty_or_false(weight):
#         if dolibarr_response["weight_units"] == "0":
#             logger.info("Converting weight: " + f"{weight} from doli to grams")
#             return weight * 1000
#     else:
#         weight = ask_mandatory(
#             input_type=InputType.INTEGER,
#             text="No weight data found in " + "Dolibarr for this supplier",
#             unit="grams",
#         )
#         return weight


# def find_codename(product):
#     """ Guess from other fields
#     First check if ms_ref, shimano_ref or jofrab_ref is set
#     Then guess from external_ref
#     param product is a dolibarr products get-API response json item
#     """
#     product_id = product["id"]
#     codename = False
#     for item in config.supported_codename_refs:
#         if not empty_or_false_extrafield(
#                 product, item.lower()+"_ref",
#         ):
#             codename = item
#     else:
#         # guess from external_ref
#         print(f"Guessing from external_ref {product['external_ref']}")
#         # match JO or CSN (min 2 max 3 upper case letters followed by a "-")
#         pattern = re.compile("^([A-Z]{2,3})-")
#         result = pattern.findall(product["external_ref"])
#         if len(result) > 0:
#             codename = result[0]
#             # print(codename)
#     if codename:
#         print(f"Found codename {codename}")
#         create.insert_extrafield(
#             "product", product_id, "main_supplier_codename", codename
#         )
#         return codename
#     else:
#         print("Could not find codename from external_ref-ids")
