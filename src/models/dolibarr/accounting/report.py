import logging
from typing import Any, List, Optional

import pandas as pd
import psycopg2.extras
from pandas import DataFrame

from src.helpers.crud.postgres import Postgres
from src.models.exceptions import AccountingError, MissingDataError

logger = logging.getLogger(__name__)


# class DolibarrAccountingStatement(MyBaseModel):
#     date: datetime


class Report(Postgres):
    """Model that fetch and calculate
    the numbers needed for financial
    reporting to Skatteverket based
    on the accounting model in Dolibarr.
    aka DolibarrYearlyAccountingReport"""

    year: int
    eu_goods: bool  # eu_goods_bought_this_year
    data: Optional[List[Any]] = None
    column_names: Optional[List[str]] = None
    dataframe: Optional[DataFrame] = None
    credit_account_totals: Any = None
    debit_account_totals: Any = None
    total_outgoing_vat: int = 0
    total_eu_goods_vat: int = 0
    total_eu_service_vat: int = 0
    total_swedish_income: int = 0
    total_swedish_income_minus_reimbursements: int = 0
    total_swedish_income_minus_reimbursements_minus_withdrawals: int = 0
    c3000: int = 0
    c3002: int = 0
    c3300: int = 0
    d3001: int = 0
    d4000: int = 0
    d4531: int = 0
    d4535: int = 0
    d4536: int = 0
    d5000: int = 0
    d5400: int = 0
    d5410: int = 0
    d5420: int = 0
    d5480: int = 0
    d5600: int = 0
    d5700: int = 0
    d6000: int = 0
    d6200: int = 0
    d6310: int = 0
    d6500: int = 0
    d6900: int = 0
    d6901: int = 0
    eu_goods_expenses: int = 0
    eu_service_expenses: int = 0
    eu_income: int = 0
    incoming_vat_to_report: int = 0
    outgoing_vat_25: int = 0
    outgoing_vat_12: int = 0
    outgoing_vat_6: int = 0
    own_withdrawal: int = 0
    profit: int = 0
    r5: int = 0
    r6: int = 0
    sum_2610: int = 0
    sum_2620: int = 0
    sum_2630: int = 0
    sum_3001: int = 0
    change_in_stock_value: int = 0
    total_income: int = 0
    total_eu_expenses: int = 0
    total_expenses: int = 0
    total_outgoing_vat_eu_25: int = 0
    upwork_fees: int = 0
    vat_debt: int = 0

    class Config:  # dead: disable
        arbitrary_types_allowed = True

    def start(self):
        self.get_data_and_calculate()
        self.print_report()

    def get_data_and_calculate(self):
        self.get_all_accounting_statements()
        self.convert_to_dataframe()
        self.do_calculations_and_checks()

    def get_all_accounting_statements(self):
        """Fetch all accounting statements"""
        # Check if ref_ext is already inserted from before
        self.connect()
        # Create a cursor object
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = (
            "SELECT *"
            "FROM llx_accounting_bookkeeping "
            "WHERE doc_date <= '12/31/%s' and doc_date >= '01/01/%s'"
        )
        r = cursor.mogrify(query, (self.year, self.year))
        # logger.debug(r)
        cursor.execute(r)
        # logger.info(cursor.rowcount)
        if cursor.rowcount > 0:
            self.data = cursor.fetchall()
            # logger.debug(result)
            # Execute a SELECT query to retrieve data from the table
            # cursor.execute("SELECT * FROM llx_accounting_bookkeeping LIMIT 0")

            # Fetch the column names from the cursor description
            self.column_names = [desc[0] for desc in cursor.description]

            # Print the list of column names
            logger.debug(f"Column names: {self.column_names}")
            # exit()
            # logger.info(result)
        else:
            raise ValueError(
                "Got no rows from dolibarr database. "
                "Please commit the acocunting to the main ledger in Dolibarr"
            )
        # save as statements?

    def convert_to_dataframe(self) -> None:
        """column_names =
        ['rowid', 'entity', 'doc_date', 'doc_type', 'doc_ref',
        'fk_doc', 'fk_docdet', 'thirdparty_code', 'subledger_account',
        'subledger_label', 'numero_compte', 'label_compte', 'label_operation',
        'debit', 'credit', 'montant', 'sens', 'multicurrency_amount',
        'multicurrency_code', 'lettering_code', 'date_lettering',
        'date_lim_reglement', 'fk_user_author', 'fk_user_modif',
        'date_creation', 'tms', 'fk_user', 'code_journal',
        'journal_label', 'piece_num', 'date_validated',
        'import_key', 'extraparams', 'date_export']"""
        # Convert the list of lists to a DataFrame
        df = pd.DataFrame(self.data, columns=self.column_names)
        df = df.rename(
            columns={"numero_compte": "account", "label_compte": "account_label"}
        )
        # Remove columns with only null values
        df = df.dropna(axis=1, how="all")
        # Convert the 'credit' column to numeric type
        df["credit"] = pd.to_numeric(df["credit"], errors="coerce")
        df["debit"] = pd.to_numeric(df["debit"], errors="coerce")
        self.dataframe = df

    def calculate_account_totals(self):
        """Each new year run this and adapt it to the accounts that are used"""
        # extract for each account aka numero_compte:
        # debit total
        # credit total
        # Group the DataFrame by 'account' and calculate the sum of 'credit' for each group
        self.credit_account_totals = self.dataframe.groupby("account")["credit"].sum()
        self.debit_account_totals = self.dataframe.groupby("account")["debit"].sum()

    def print_reimbursements(self):
        # AV er reimbursements
        # Filter the DataFrame based on the condition
        reimbursement_df = self.dataframe[
            self.dataframe["doc_ref"].str.startswith("AV", na=False)
        ]
        # Print the filtered DataFrame
        logger.info(f"Reimbursements during {self.year}")
        # logger.info(reimbursement_df)
        for _index, row in reimbursement_df.iterrows():
            account = row["account"]
            debit = row["debit"]
            credit = row["credit"]

            # Print the values for each row
            logger.info(f"row: account: {account}, Debit: {debit}, Credit: {credit}")

    def check_stock_value_change(self):
        # Assets
        c1460 = int(
            self.credit_account_totals.get(key="1460")
            if self.credit_account_totals.get(key="1460") is not None
            else 0
        )  # föränding lager av handelsvaror
        d1460 = int(
            self.debit_account_totals.get(key="1460")
            if self.debit_account_totals.get(key="1460") is not None
            else 0
        )  # föränding lager av handelsvaror
        # We use and here because we only want a value in either credit or debit. Never both.
        if c1460 == 0 and d1460 == 0:
            raise AccountingError(
                "The change of value in "
                "the stock has not been added to the ledger, please fix"
            )

    def calculate_income(self):
        """This depends on calculation of withdrawals"""
        self.calculate_own_withdrawals()
        # Income
        self.c3000 = int(
            self.credit_account_totals.get(key="3000")
        )  # Försäljning och utfört arbete samt övriga momspliktiga intäkter
        # d3000 = int(self.credit_account_totals.get(key="3000"))
        # sum_3000 = abs(c3000 - d3000)
        c3001 = int(
            self.credit_account_totals.get(key="3001")
            if self.credit_account_totals.get(key="3001") is not None
            else 0
        )  # cykel
        d3001 = int(
            self.debit_account_totals.get(key="3001")
            if self.debit_account_totals.get(key="3001") is not None
            else 0
        )  # cykel
        self.sum_3001 = c3001 - d3001  # income after reimbursements
        self.c3002 = int(
            self.credit_account_totals.get(key="3002")
            if self.credit_account_totals.get(key="3002") is not None
            else 0
        )  # symaskin
        self.c3300 = int(
            self.credit_account_totals.get(key="3300")
            if self.credit_account_totals.get(key="3300") is not None
            else 0
        )  # Inkomst från försäljning inom EU (Upwork)
        c3510 = int(
            self.credit_account_totals.get(key="3510")
            if self.credit_account_totals.get(key="3510") is not None
            else 0
        )  # Fakturerade fraktkostnader
        # # momsfri intäkt
        # c3404 = int(
        #     self.credit_account_totals.get(key="3404")
        #     if self.credit_account_totals.get(key="3404") is not None
        #     else 0
        # )
        # untaxed_income =
        swedish_income = [self.c3000, c3001, self.c3002, c3510]
        # for number in credits:
        #     logger.info(number)
        self.total_swedish_income = sum(swedish_income)
        self.total_swedish_income_minus_reimbursements = (
            self.total_swedish_income - d3001
        )
        self.total_swedish_income_minus_reimbursements_minus_withdrawals = (
            self.total_swedish_income - d3001 - self.own_withdrawal
        )
        logger.info(f"total_swedish_income = {self.total_swedish_income}")
        logger.info(
            f"total_swedish_income_minus_reimbursements = {self.total_swedish_income_minus_reimbursements}"
        )
        self.eu_income = self.c3300
        self.total_income = self.total_swedish_income + self.eu_income

    def calculate_expenses(self):
        # Expenses
        # Goods
        self.d4000 = int(self.debit_account_totals.get(key="4000"))
        # d4010 = int(self.debit_account_totals.get(key='4010'))
        # d4220 = int(self.debit_account_totals.get(key='4220'))
        self.d4531 = int(
            self.debit_account_totals.get(key="4531")
            if self.debit_account_totals.get(key="4531") is not None
            else 0
        )  # upwork service fee
        self.d4535 = int(
            self.debit_account_totals.get(key="4535")
            if self.debit_account_totals.get(key="4535") is not None
            else 0
        )  # Varuinköp inom EU
        if not self.d4535 and self.eu_goods is True:
            raise MissingDataError(
                "No lines concerning goods purchases from EU found. "
                "This is probably an accounting error"
            )
        # EU services expenses
        self.d4536 = int(
            self.debit_account_totals.get(key="4536")
            if self.debit_account_totals.get(key="4536") is not None
            else 0
        )
        # d4545 = int(self.debit_account_totals.get(key='4545'))
        expenses_4xxx = sum([self.d4000, self.d4531, self.d4535])
        # Non-goods like rent
        d5000 = int(self.debit_account_totals.get(key="5000"))
        self.d5400 = int(
            self.debit_account_totals.get(key="5400")
            if self.debit_account_totals.get(key="5400") is not None
            else 0
        )
        self.d5410 = int(self.debit_account_totals.get(key="5410"))
        self.d5420 = int(self.debit_account_totals.get(key="5420"))
        self.d5480 = int(
            self.debit_account_totals.get(key="5480")
            if self.debit_account_totals.get(key="5480") is not None
            else 0
        )
        self.d5600 = int(
            self.debit_account_totals.get(key="5600")
            if self.debit_account_totals.get(key="5600") is not None
            else 0
        )
        self.d5700 = int(
            self.debit_account_totals.get(key="5700")
            if self.debit_account_totals.get(key="5700") is not None
            else 0
        )
        expenses_5xxx = sum(
            [
                d5000,
                self.d5400,
                self.d5410,
                self.d5420,
                self.d5480,
                self.d5600,
                self.d5700,
            ]
        )
        # Non-goods like bank expenses
        self.d6000 = int(
            self.debit_account_totals.get(key="6000")
            if self.debit_account_totals.get(key="6000") is not None
            else 0
        )
        # d6100 = int(self.debit_account_totals.get(key='6400'))
        self.d6200 = int(
            self.debit_account_totals.get(key="6200")
            if self.debit_account_totals.get(key="6200") is not None
            else 0
        )
        self.d6310 = int(
            self.debit_account_totals.get(key="6310")
            if self.debit_account_totals.get(key="6310") is not None
            else 0
        )
        self.d6500 = int(
            self.debit_account_totals.get(key="6500")
            if self.debit_account_totals.get(key="6500") is not None
            else 0
        )
        self.d6900 = int(
            self.debit_account_totals.get(key="6900")
            if self.debit_account_totals.get(key="6900") is not None
            else 0
        )
        self.d6901 = int(
            self.debit_account_totals.get(key="6901")
            if self.debit_account_totals.get(key="6901") is not None
            else 0
        )  # upwork bank transactions
        # d6970 = int(self.debit_account_totals.get(key='6700'))
        expenses_6xxx = sum([self.d6000, self.d6200,
                             self.d6310, self.d6500,
                             self.d6900, self.d6901])
        # self.upwork_fees = d4531
        # total_upwork_expenses = sum([d4531, d6901])
        self.total_expenses = sum([expenses_4xxx, expenses_5xxx, expenses_6xxx])
        logger.info(
            f"total_expenses = {self.total_expenses}, "
            # f"inclusive upwork expenses amounting to {total_upwork_expenses}"
        )
        # EU goods expenses 25% VAT
        self.eu_goods_expenses = self.d4535
        # EU service expenses 25% VAT
        self.eu_service_expenses = self.d4536
        self.total_eu_expenses = sum({self.d4535, self.d4531, self.d4536})

    def calculate_change_in_stock_value(self):
        # Change in stock value
        c4960 = int(
            self.credit_account_totals.get(key="4960")
            if self.credit_account_totals.get(key="4960") is not None
            else 0
        )
        logger.info(f"c4960: {c4960}")
        d4960 = (
            int(self.debit_account_totals.get(key="4960"))
            if self.debit_account_totals.get(key="4960")
            else 0
        )
        logger.info(f"d4960: {d4960}")
        self.change_in_stock_value = c4960 - d4960  # plus indicates increase

    def calculate_profit(self):
        # Profit
        self.profit = self.total_income - self.total_expenses
        # Vad är de här?
        r5 = sum(
            [
                self.d4000,
                self.d4531,
                self.d4535,
                self.d5400,
                self.d5410,
                self.d5420,
                self.d5480,
                self.d5600,
                self.d5700,
            ]
        )
        logger.info(f"r5 = {r5}")
        r6 = sum(
            [
                self.d5000,
                self.d6000,
                self.d6200,
                self.d6310,
                self.d6500,
                self.d6900,
                self.d6901,
            ]
        )
        logger.info(f"r6 = {r6}")

    def calculate_outgoing_vat(self):
        # Utgående moms 25%
        d2610 = int(
            self.debit_account_totals.get(key="2610")
            if self.debit_account_totals.get(key="2610") is not None
            else 0
        )
        logger.info(f"d2610: {d2610}")
        c2610 = int(
            self.credit_account_totals.get(key="2610")
            if self.credit_account_totals.get(key="2610") is not None
            else 0
        )
        logger.info(f"c2610: {c2610}")
        self.outgoing_vat_25 = abs(c2610 - d2610)

        # Utgående moms 12%
        d2620 = int(self.debit_account_totals.get(key="2620"))
        logger.info(f"d2620: {d2620}")
        c2620 = int(self.credit_account_totals.get(key="2620"))
        logger.info(f"c2620: {c2620}")
        self.outgoing_vat_12 = abs(c2620 - d2620)

        # Utgående moms 6%
        d2630 = int(
            self.debit_account_totals.get(key="2630")
            if self.debit_account_totals.get(key="2630") is not None
            else 0
        )
        logger.info(f"d2630: {d2630}")
        c2630 = int(
            self.credit_account_totals.get(key="2630")
            if self.credit_account_totals.get(key="2630") is not None
            else 0
        )
        logger.info(f"c2630: {c2630}")
        self.outgoing_vat_6 = abs(c2630 - d2630)
        total_outgoing_vat_se = sum(
            {self.outgoing_vat_25, self.outgoing_vat_12, self.outgoing_vat_6}
        )

        ## Utgående moms försäljning av tjänster EU enligt huvudregeln 25%
        # d2614 = int(self.debit_account_totals.get(key="2614"))
        # logger.info(f"d2614: {d2614}")
        # c2614 = int(self.credit_account_totals.get(key="2614"))
        # logger.info(f"c2614: {c2614}")
        # sum_2614 = abs(c2614 - d2614)

        ## Utgående moms varuimport EU 25%
        if self.eu_goods is False:
            d2615 = 0
        else:
            try:
                d2615 = int(self.debit_account_totals.get(key="2615"))
            except TypeError as err:
                raise MissingDataError(
                    "No VAT lines concerning goods purchases from EU found. "
                    "This is probably an accounting error"
                ) from err
        logger.info(f"d2615: {d2615}")
        c2615 = int(
            self.credit_account_totals.get(key="2615")
            if self.credit_account_totals.get(key="2615") is not None
            else 0
        )
        logger.info(f"c2615: {c2615}")
        self.total_eu_goods_vat = abs(c2615 - d2615)

        ## Utgående moms på inköp av tjänster från annat EU-land enligt huvudregeln 25%
        d2617 = int(
            self.debit_account_totals.get(key="2617")
            if self.debit_account_totals.get(key="2617") is not None
            else 0
        )
        logger.info(f"d2617: {d2617}")
        c2617 = int(
            self.credit_account_totals.get(key="2617")
            if self.credit_account_totals.get(key="2617") is not None
            else 0
        )
        logger.info(f"c2617: {c2617}")
        self.total_eu_service_vat = abs(c2617 - d2617)

        # EU moms 25%
        self.total_outgoing_vat_eu_25 = sum(
            [self.total_eu_service_vat, self.total_eu_goods_vat]
        )

        # total
        self.total_outgoing_vat = total_outgoing_vat_se + self.total_outgoing_vat_eu_25

    def calculate_incoming_vat(self):
        ## Ingående moms
        d2640 = int(self.debit_account_totals.get(key="2640"))
        logger.info(f"d2640: {d2640}")
        c2640 = int(self.credit_account_totals.get(key="2640"))
        logger.info(f"c2640: {c2640}")
        incoming_vat = d2640 - c2640
        # we add total eu vat here to make the report to skatteverket correct
        self.incoming_vat_to_report = incoming_vat + self.total_outgoing_vat_eu_25

    def calculate_vat(self):
        # We calculate outgoing first because it is needed for calculating incoming vat correctly
        self.calculate_outgoing_vat()
        self.calculate_incoming_vat()
        # Momsskuld
        self.vat_debt = (
            sum([self.outgoing_vat_25, self.outgoing_vat_12, self.outgoing_vat_6])
            - self.incoming_vat_to_report
        )

    def check_vat(self):
        if self.vat_debt == 0:
            raise MissingDataError("vat_debt was zero which " "is always wrong")
        if self.incoming_vat_to_report == 0:
            raise MissingDataError("incoming_vat was zero which " "is always wrong")
        if self.total_eu_service_vat == 0:
            raise MissingDataError(
                "total_eu_goods_vat was zero which "
                "is wrong if any facebook ads have been bought this year"
            )
        if self.total_eu_goods_vat == 0 and self.eu_goods:
            raise MissingDataError(
                "total_eu_goods_vat was zero which "
                "is wrong because eu_goods is True "
                "which means eu goods have been imported"
            )

    def calculate_own_withdrawals(self):
        # Egna uttag
        # we calculate this based on 2011 minus 3404.
        d2011 = int(self.debit_account_totals.get(key="2011"))
        c3404 = int(self.credit_account_totals.get(key="3404"))
        self.own_withdrawal = d2011 - c3404

    def check_own_withdrawal(self):
        if self.own_withdrawal == 0:
            raise MissingDataError(
                "own_withdrawal was zero which "
                "is always wrong, please manually "
                "account for the withdrawals in the "
                "ledger like in 2024"
            )

    def do_calculations_and_checks(self):
        self.calculate_account_totals()
        # Print the account totals
        # logger.info(#self.credit_account_totals,
        #     self.debit_account_totals)
        # exit()
        self.print_reimbursements()
        if self.year != 2024:
            raise Exception("check that reimbursements are supported in the code")
        self.calculate_change_in_stock_value()
        self.calculate_expenses()
        self.calculate_income()
        self.calculate_profit()
        self.calculate_vat()
        self.check_stock_value_change()
        self.check_own_withdrawal()
        self.check_vat()

    def print_report(self):
        print("Momsredovisning")
        # Inga VMB 2022, vi har slutat med det pga. krångel. Inga återköp har gjorts heller.
        print(
            f"05: Total försäljning i Sverige (minus återköp, refunderingar "
            f"och VMB vinstmarginal och "
            f"momspliktiga egna uttag) : {self.total_swedish_income_minus_reimbursements_minus_withdrawals}"
        )
        print(
            "OBS! följande avdrag har gjorts för återköp och refunderingar har gjorts:"
        )
        print(f"3001: {self.d3001}")
        print(f"06: {self.own_withdrawal}")
        print("07-08: 0")
        print(f"10: Utgående moms 25%: {self.sum_2610}")
        print(f"11: Utgående moms 12%: {self.sum_2620}")
        print(f"12: Utgående moms 6%: {self.sum_2630} <- this should be zero!")
        print("Varor importerad inom EU:")
        print(f"20: Total inköp av varor inom EU: {self.eu_goods_expenses}")
        print(
            f"21: inköp av tjänster från annat EU-land enligt huvudregeln 25%: {self.upwork_fees}"
        )
        print(f"30: total moms EU inköp 25%: {self.total_outgoing_vat_eu_25}")
        print(
            f"39: försäljning av tjänster EU enligt huvudregeln 25%: {self.eu_service_expenses}"
        )
        # Vi har slutat med att importera från utanför EU
        # print("Varor importerad utanför EU:")
        # print(f"4545 Import av varor utanför EU (ruta 50): {self.d4545}")
        # Vi har slutat med VMB
        # print("3223 VMB vinstmarginal (ruta 07): 0")
        print(f"Ingående moms: 2645: {self.incoming_vat_to_report}")
        print(f"Egenberäknad momsskuld: = {self.vat_debt}")
        print("-------")
        print(f"Bokslut år {self.year}")
        print(
            "Beräkna milersättning enligt uppgifter i Telegram. "
            "Gör beräkningen i Libreoffice calc och lägg in i bokslutsmappen som bilaga"
        )
        print("Balansräkning")
        print("B1-B5 = 0")
        print(
            f"B6 Varulager: kolla lagerinventeringen/uppgörelsen ultimo {self.year} i bokslutsmappen"
        )
        print("B7-B8 = 0")
        print(f"B9 kolla kontoutdrag för december {self.year}")
        print("B10-B16 = 0")
        print("--")
        print("Resultaträkning")
        print("Försäljning:")
        print(f"Diverse: {self.c3000}")
        print(f"Cykel: {self.sum_3001}")
        print(f"Symaskin: {self.c3002}")
        print(f"Upwork: {self.c3300}")
        print(
            f"R1 Total försäljning "
            f"(minus återköp och refunderingar): "
            f"{self.total_swedish_income_minus_reimbursements}"
        )
        print(
            f"R2: Momsfri försäljning "
            f"(tex vid omvänd skatteskyldighet till utlandet): {self.eu_income}"
        )
        print("R3-R4 = 0")
        print("Inköp:")
        print("R5 inköp av varor, material och tjänster: ")
        print(f"4000 varor som lagerhålls i Dolibarr: {self.d4000}")
        print(f"4331 Försäljningskostnad Upwork EU: {self.d4531}")
        print(f"4535 EU varor: {self.d4535}")
        print(f"4536 EU tjänster: {self.d4536}")
        print(f"Total inköp EU: {self.total_eu_expenses}")
        print(f"5400 förbrukning: {self.d5400}")
        print(f"5410 förbrukningsverktyg: {self.d5410}")
        print(f"5420 förbrukningsinventarier (ej verktyg): {self.d5420}")
        print(f"5480 kläder m.m.: {self.d5480}")
        print(f"5700 frakt och transporter: {self.d5700}")
        print(f"R5 totalt: {self.r5}")
        print("R6 övriga externa kostnader: ")
        print(f"5000 lokal: {self.d5000}")
        print(f"5600 kostnader för transportmedel: {self.d5600}")
        print(f"6000 övriga försäljningskostnader: {self.d6000}")
        print(f"6200 telefon och porto: {self.d6200}")
        print(f"6310 företagsförsäkring: {self.d6310}")
        print(
            f"6500 övriga externa tjänster (tågresor, inhyrning av personal, m.m.): {self.d6500}"
        )
        print(f"6900 övriga externa kostnader: {self.d6900}")
        # print(f"6970 facklitteratur: {self.d6970}")
        print(f"R6 totalt: {self.r6}")
        print(f"Summa kostnader: {self.total_expenses}")
        print(
            f"4960 Förändring i varulagervärde: {self.change_in_stock_value} (plus betyder ökning av varulagret)"
        )
        print(
            f"Vinst/Förlust efter återköp och refunderingar: {self.profit} (plus betyder vinst)"
        )
        print("R13-R17 = 0")
        print("R18-R21 = 0")
        print("R22-R29 = 0")
        print("R30-R33 = 0")
        print("R36-R39 = 0")
        print(
            "Kryssa i och låt skatteverket beräkna avsättning till periodiseringsfond, m.m."
        )
        print("Kryssa i och låt skatteverket beräkna avdrag, m.m.")
