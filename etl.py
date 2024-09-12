import luigi
import pandas as pd
from pangres import upsert

from helper.db_connection import connect_db_source, connect_db_warehouse
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
        return [TransformSalesData(), ExtractNLP()]

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

    def output(self):
        return [
            luigi.LocalTarget("data/load/sales_load.csv"),
            luigi.LocalTarget("data/load/nlp_load.csv"),
        ]


if __name__ == "__main__":
    luigi.build([LoadData()])
