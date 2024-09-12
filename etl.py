import luigi
import pandas as pd
from pangres import upsert

from helper.db_connection import connect_db_source, connect_db_warehouse
from helper.electronics_helper import (
    categorize_shipping,
    handle_condition,
    handle_is_available,
    handle_manufacturer,
)
from helper.scrape_website import scrape_news_site


class ExtractSalesData(luigi.Task):
    def requires(self):
        pass

    def run(self):
        engine = connect_db_source()
        select_query = "SELECT * FROM amazon_sales_data;"
        df = pd.read_sql(select_query, engine)
        df.to_csv(self.output().path, index=False)

    def output(self):
        return luigi.LocalTarget("data/raw/sales_raw.csv")


class TransformSalesData(luigi.Task):
    def requires(self):
        return ExtractSalesData()

    def run(self):
        main_df = pd.read_csv(self.input().path)
        main_df["ratings"] = pd.to_numeric(main_df["ratings"], errors="coerce")
        main_df["no_of_ratings"] = (
            pd.to_numeric(main_df["no_of_ratings"], errors="coerce")
            .fillna(0)
            .astype(int)
        )

        ratings_median = main_df["ratings"].median()
        df_filled = main_df.fillna({"ratings": ratings_median})
        df_filled = df_filled.drop_duplicates(keep="last")

        def convert_price(price):
            if pd.isnull(price):
                return None
            cleaned_price = str(price.replace("₹", "").strip())
            return pd.to_numeric(cleaned_price, errors="coerce")

        df_filled["actual_price"] = df_filled["actual_price"].apply(convert_price)
        df_filled["discount_price"] = df_filled["discount_price"].apply(convert_price)

        actual_price_median = df_filled["actual_price"].median()
        discount_price_median = df_filled["discount_price"].median()

        df_filled.fillna(
            {
                "discount_price": discount_price_median,
                "actual_price": actual_price_median,
            },
            inplace=True,
        )
        df_filled = df_filled.drop(columns=["Unnamed: 0"])
        df_filled.to_csv(self.output().path, index=False)

    def output(self):
        return luigi.LocalTarget("data/transform/sales_transform.csv")


class ExtractElectronicsData(luigi.Task):
    def requires(self):
        pass

    def run(self):
        file_path = "./data/raw/ElectronicsProductsPricingData.csv"
        electronics_df = pd.read_csv(file_path)
        electronics_df.to_csv(self.output().path, index=False)

    def output(self):
        return luigi.LocalTarget("data/raw/electronics_raw.csv")


class TransformElectronics(luigi.Task):
    def requires(self):
        return ExtractElectronicsData()

    def run(self):
        df = pd.read_csv(self.input().path)
        df = df.drop(
            columns=[
                "Unnamed: 26",
                "Unnamed: 27",
                "Unnamed: 28",
                "Unnamed: 29",
                "Unnamed: 30",
            ]
        )
        df = df.rename(
            columns={
                "id": "product_id",
                "prices.amountMax": "price_max",
                "prices.amountMin": "price_min",
                "prices.availability": "is_available",
                "prices.condition": "condition",
                "prices.currency": "currency",
                "prices.dateSeen": "dates_seen",
                "prices.isSale": "is_on_sale",
                "prices.merchant": "merchant_name",
                "prices.shipping": "shipping_method",
                "dateAdded": "date_added",
                "dateUpdated": "date_updated",
                "ean": "ean_code",
                "imageURLs": "image_urls",
                "keys": "product_keys",
                "manufacturer": "manufacturer",
                "manufacturerNumber": "manufacturer_number",
                "name": "product_name",
                "primaryCategories": "primary_category",
                "sourceURLs": "source_urls",
                "upc": "upc_code",
                "weight": "weight_lbs",
            }
        )
        df = df.fillna({"ean_code": "No Code"})
        df = df.drop(columns=["prices.sourceURLs"])
        df["shipping_method"] = df["shipping_method"].apply(categorize_shipping)
        df["manufacturer"] = df["manufacturer"].str.strip().str.title()
        df["manufacturer"].unique()

        manufacturer_mapping = {
            "Bose": ["Bose", "Bose Corporation", "BOSE"],
            "Samsung": ["Samsung", "Samsung Electronics", "Samsung It"],
            "Yamaha": ["Yamaha", "Yamaha Electronics"],
            "Razer": ["Razer", "Razer Usa", "Razer Inc"],
            "Kenwood": ["Kenwood", "Kenwood Corporation", "Kenwood Usa"],
            "Apple": [
                "Apple",
                "Apple Computer",
                "Apple Computer (Direct)",
                "Apple Inc",
            ],
            "Onkyo": ["Onkyo", "Onkyo Corporation"],
        }
        reverse_mapping = {
            v: k for k, values in manufacturer_mapping.items() for v in values
        }
        df["manufacturer"] = df["manufacturer"].replace(reverse_mapping)
        df["manufacturer"].unique()

        df["manufacturer"] = df["manufacturer"].apply(handle_manufacturer)
        df["is_available"] = df["is_available"].apply(handle_is_available)

        df["condition"] = df["condition"].apply(handle_condition)
        df = df.drop_duplicates(keep="first")
        df["weight_lbs"] = df["weight_lbs"].str.extract(r"(\d+\.?\d*)").astype(float)
        df = df.drop(columns=["product_id"])
        df.to_csv(self.output().path, index=False)

    def output(self):
        return luigi.LocalTarget("data/transform/electronics_transform.csv")


class ExtractNLP(luigi.Task):
    def requires(self):
        pass

    def run(self):
        nlp_df = scrape_news_site()
        nlp_df.to_csv(self.output().path, index=False)

    def output(self):
        return luigi.LocalTarget("data/raw/nlp_raw.csv")


class LoadData(luigi.Task):

    def requires(self):
        return [TransformSalesData(), ExtractNLP(), TransformElectronics()]

    def run(self):
        engine = connect_db_warehouse()
        load_sales = pd.read_csv(self.input()[0].path)
        load_sales.insert(0, "product_id", range(0, 0 + len(load_sales)))
        load_sales = load_sales.set_index("product_id")
        table_name_sales = "amazon_sales_data"

        upsert(
            con=engine,
            df=load_sales,
            table_name=table_name_sales,
            if_row_exists="update",
        )
        load_sales.to_csv(self.output()[1].path, index=False)

        load_nlp = pd.read_csv(self.input()[1].path)
        load_nlp.insert(0, "article_id", range(0, 0 + len(load_nlp)))
        load_nlp = load_nlp.set_index("article_id")
        table_name_nlp = "nlp_data"

        upsert(
            con=engine, df=load_nlp, table_name=table_name_nlp, if_row_exists="update"
        )
        load_nlp.to_csv(self.output()[1].path, index=False)

        load_electronics = pd.read_csv(self.input()[2].path)
        load_electronics.insert(0, "product_id", range(0, 0 + len(load_electronics)))
        load_electronics = load_electronics.set_index("product_id")
        table_name_electronics = "electronics_data"

        upsert(
            con=engine,
            df=load_electronics,
            table_name=table_name_electronics,
            if_row_exists="update",
        )

    def output(self):
        return [
            luigi.LocalTarget("data/load/sales_load.csv"),
            luigi.LocalTarget("data/load/nlp_load.csv"),
            luigi.LocalTarget("data/laod/electronics_load.csv"),
        ]


if __name__ == "__main__":
    luigi.build([LoadData()])
