
import pandas as pd

class SalesAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self._load_data()

    def _load_data(self):
        df = pd.read_csv(self.file_path)
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.month
        df["year"] = df["date"].dt.year
        df["week"] = df["date"].dt.isocalendar().week.astype(int)
        return df

    def _apply_filters(self, df, branch_id=None, year=None, month=None):
        filtered_df = df.copy()
        if branch_id:
            filtered_df = filtered_df[filtered_df["branch_id"] == branch_id]
        if year:
            filtered_df = filtered_df[filtered_df["year"] == year]
        if month:
            filtered_df = filtered_df[filtered_df["month"] == month]
        return filtered_df

    def monthly_sales_analysis(self, branch_id=None, year=None, month=None):
        filtered_df = self._apply_filters(self.df, branch_id, year, month)
        monthly_sales = filtered_df.groupby([filtered_df["date"].dt.to_period("M"), "branch_id"])["total_amount"].sum().reset_index()
        monthly_sales["date"] = monthly_sales["date"].astype(str)
        return monthly_sales

    def price_analysis_by_product(self, branch_id=None, year=None, month=None):
        filtered_df = self._apply_filters(self.df, branch_id, year, month)
        product_price_analysis = filtered_df.groupby(["product_name"])["price"].agg(["mean", "min", "max"]).reset_index()
        return product_price_analysis

    def weekly_sales_analysis(self, branch_id=None, year=None):
        filtered_df = self._apply_filters(self.df, branch_id, year, None) # Month filter not applicable for weekly
        weekly_sales = filtered_df.groupby(["year", "week", "branch_id"])["total_amount"].sum().reset_index()
        return weekly_sales

    def product_preference_analysis(self, branch_id=None, year=None, month=None):
        filtered_df = self._apply_filters(self.df, branch_id, year, month)
        product_preference = filtered_df.groupby(["product_name"])["quantity"].sum().reset_index()
        product_preference = product_preference.sort_values(by="quantity", ascending=False)
        return product_preference

    def total_sales_distribution_analysis(self, branch_id=None, year=None, month=None):
        filtered_df = self._apply_filters(self.df, branch_id, year, month)
        total_sales_distribution = filtered_df.groupby(["category"])["total_amount"].sum().reset_index()
        total_sales_distribution = total_sales_distribution.sort_values(by="total_amount", ascending=False)
        return total_sales_distribution



