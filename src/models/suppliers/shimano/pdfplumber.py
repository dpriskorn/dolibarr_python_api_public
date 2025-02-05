import logging
from datetime import datetime
from typing import TYPE_CHECKING, List, Tuple

import numpy as np
import pandas as pd  # type: ignore
import pdfplumber  # type: ignore
from pandas import DataFrame
from pdfplumber.page import Page  # type: ignore
from pdfplumber.pdf import PDF  # type: ignore
from requests import Session

import config
from src.models.basemodels.shimano import ShimanoBaseModel
from src.models.suppliers.shimano.order_row import ShimanoOrderRow
from src.models.suppliers.shimano.product import ShimanoProduct

if TYPE_CHECKING:
    from src.models.suppliers.shimano.order import ShimanoOrder

logger = logging.getLogger(__name__)


class Pdfplumber(ShimanoBaseModel):
    session: Session
    file_path: str
    invoice_id: str
    text: str = ""
    columns: List[str] = [
        "row",
        "external_ref",
        "label",
        "quantity",
        "unused",
        "discount",
        "cost_price",
        "line_total",
    ]

    @staticmethod
    def __my_float__(input_text: str):
        return float(input_text.replace(",", "."))

    def __extract_date__(self, date_text: str, date_format="%y/%m/%d") -> datetime:
        """Extract the date using format
        Shimano has different date formats on the same page which is terrible design"""
        logger.debug("__extract_date__: Running")
        logger.debug(f"raw date: {date_text}")
        try:
            return datetime.strptime(date_text, date_format).astimezone(
                tz=self.stockholm_timezone
            )
        except ValueError:
            try:
                return datetime.strptime(date_text, "%Y-%m-%d").astimezone(
                    tz=self.stockholm_timezone
                )
            except ValueError as err:
                raise ValueError(f"Could not parse the date: {date_text}") from err

    def __extract_invoice_date__(self, page: Page) -> datetime:
        return self.__extract_date__(
            date_text=str(
                page.within_bbox(
                    (250, 75, page.width - 300, page.height - 740)
                ).extract_text()
            )
        )

    def __extract_due_date__(self, page: Page) -> datetime:
        return self.__extract_date__(
            date_text=str(
                page.within_bbox(
                    (370, 700, page.width - 150, page.height - 100)
                ).extract_text()
            ),
            date_format="%d/%m/%y",
        )

    @staticmethod
    def __remove_shipping_line__(df: DataFrame):
        return df[df.label != "Shipping Costs"]

    def parse_into_shimano_order(self) -> Tuple[datetime, "ShimanoOrder"]:
        pdf = pdfplumber.open(self.file_path)  # type: ignore
        page_count = len(pdf.pages)
        if page_count == 1:
            p1 = pdf.pages[0]
            table = p1.crop((13, 358, p1.width - 30, p1.height - 160))
            # These settings were found by loading the pdf page as image in gimp and looking at the coordinates
            table_settings = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "text",
                "explicit_vertical_lines": [
                    25,  # left edge of row
                    58,  # left edge of product number
                    129,  # right edge of product number
                    298,
                    351,
                    408,
                    451,
                    504,
                    553,
                ],
                "intersection_x_tolerance": 15,
            }
            extracted_table = table.extract_table(table_settings=table_settings)
            df = pd.DataFrame(extracted_table, columns=self.columns)
            df.replace("", np.nan, inplace=True)
            df.drop(["row", "unused", "discount"], axis=1, inplace=True)
            # df = df.columns
            df = df.dropna(subset=["line_total"])
            df = self.__remove_shipping_line__(df)
            invoice_date = self.__extract_invoice_date__(page=p1)
            due_date = self.__extract_due_date__(page=p1)
            print(df, invoice_date, due_date)
            # raise DebugExit()
        elif page_count == 2:
            # page 1
            # here we find invoice_date and a table
            p1 = pdf.pages[0]
            table = p1.crop((13, 360, p1.width - 30, p1.height - 100))
            # These settings were found by loading the pdf page as image in gimp and looking at the coordinates
            table_settings = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "text",
                "explicit_vertical_lines": [
                    20,  # left edge of row
                    58,  # left edge of product number
                    135,  # right edge of product number
                    298,
                    351,
                    408,
                    451,
                    504,
                    553,
                ],
                "snap_y_tolerance": 5,
                "intersection_x_tolerance": 15,
            }
            extracted_table = table.extract_table(table_settings=table_settings)
            df1 = pd.DataFrame(extracted_table, columns=self.columns)
            df1.replace("", np.nan, inplace=True)
            df1.drop(["row", "unused", "discount"], axis=1, inplace=True)
            df1 = df1.dropna(subset=["line_total"])
            invoice_date = self.__extract_invoice_date__(page=p1)
            # page 2
            # here we find due_date and a smaller table
            p2 = pdf.pages[1]
            table2 = p2.crop((13, 256, p2.width - 30, p2.height - 160))
            # TODO test this!
            table_settings = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "text",
                "explicit_vertical_lines": [
                    25,  # left edge of row
                    57,  # left edge of product number
                    129,  # right edge of product number
                    298,
                    351,
                    408,
                    451,
                    504,
                    553,
                ],
                "snap_y_tolerance": 5,
                "intersection_x_tolerance": 15,
            }
            extracted_table = table2.extract_table(table_settings=table_settings)
            if len(extracted_table[0]) == 2:
                # This happens when there is no lines on page 2
                df2 = pd.DataFrame()
            else:
                df2 = pd.DataFrame(extracted_table, columns=self.columns)
                df2.replace("", np.nan, inplace=True)
                df2.drop(["row", "unused", "discount"], axis=1, inplace=True)
                df2 = df2.dropna(subset=["line_total"])
            due_date = self.__extract_due_date__(page=p2)
            df = pd.concat([df1, df2], ignore_index=True)
            df = self.__remove_shipping_line__(df)
            if config.loglevel in [logging.INFO, logging.DEBUG]:
                print(df, invoice_date, due_date)
            # raise DebugExit()
        else:
            raise ValueError(f"page_count {page_count} not supported")
        from src.models.suppliers.shimano import ShimanoOrder

        order = ShimanoOrder(
            reference=self.invoice_id, order_date=invoice_date, session=self.session
        )
        order.rows = []
        for row in df.itertuples(index=False):
            # Avoid adding shipping lines which have no external refs
            if str(row.external_ref).lower() != "nan":
                product = ShimanoProduct(sku=row.external_ref, session=self.session)
                product.scrape_product()
                # Update the cost price so it always mimics the invoice
                # (they could have changed the price in the mean time)
                product.cost_price = self.__my_float__(row.cost_price)
                order.rows.append(
                    ShimanoOrderRow(entity=product, quantity=int(row.quantity))
                )
        return due_date, order

    def __parse_all_text__(self):
        pdf = pdfplumber.open(self.file_path)
        for page in pdf.pages:
            self.text += page.extract_text()
        # print(self.text)

    def find_order_numbers_in_invoice_text(self) -> List[str]:
        if len(self.text) == 0:
            self.__parse_all_text__()
        order_numbers = []
        for line in self.text.splitlines():
            if "Orderdatum" in line:
                logger.debug(f"found order number in line {line}")
                order_number = line.split(" ")[0]
                order_numbers.append(order_number)
        if config.loglevel == logging.DEBUG:
            logger.debug("Order numbers found:")
            print(order_numbers)
        return order_numbers

    def find_freight_in_invoice_text(self):
        if len(self.text) == 0:
            self.__parse_all_text__()
        for line in self.text.splitlines():
            if "Shipping Costs" in line:
                logger.info(f"Found freight in {line} :)")
                # Return early
                return True
        # Default to False if not found
        return False
