import sqlite3
import pytest
from learning.sql.day_067_sql_window_functions_row_number_rank import SalesRankingAnalyzer


@pytest.fixture
def analyzer():
    analyzer_instance = SalesRankingAnalyzer(":memory:")
    analyzer_instance.seed_data()
    yield analyzer_instance
    analyzer_instance.close()


def test_row_number_uniqueness(analyzer):
    rankings = analyzer.get_rankings()
    tech_rankings = [r for r in rankings if r["department"] == "Tech"]

    row_nums = [r["row_num"] for r in tech_rankings]
    assert row_nums == [1, 2, 3, 4]


def test_rank_with_ties(analyzer):
    rankings = analyzer.get_rankings()
    tech_rankings = [r for r in rankings if r["department"] == "Tech"]

    # Bob (120000) and Charlie (120000) tie for rank 2
    # Diana (90000) gets rank 4 (rank skips rank 3)
    ranks = [r["rank_val"] for r in tech_rankings]
    assert ranks == [1, 2, 2, 4]


def test_dense_rank_without_gaps(analyzer):
    rankings = analyzer.get_rankings()
    tech_rankings = [r for r in rankings if r["department"] == "Tech"]

    # Bob (120000) and Charlie (120000) tie for dense_rank 2
    # Diana (90000) gets dense_rank 3 (no rank skip)
    dense_ranks = [r["dense_rank_val"] for r in tech_rankings]
    assert dense_ranks == [1, 2, 2, 3]


def test_sales_dept_rankings(analyzer):
    rankings = analyzer.get_rankings()
    sales_rankings = [r for r in rankings if r["department"] == "Sales"]

    # Eve and Frank tie at 200k (rank 1), Grace at 180k (rank 3), Heidi at 150k (rank 4)
    sales_ranks = [r["rank_val"] for r in sales_rankings]
    assert sales_ranks == [1, 1, 3, 4]

    sales_dense_ranks = [r["dense_rank_val"] for r in sales_rankings]
    assert sales_dense_ranks == [1, 1, 2, 3]


def test_get_top_n_per_department(analyzer):
    top_1 = analyzer.get_top_n_per_department(top_n=1)

    tech_top_1 = [r["employee_name"] for r in top_1 if r["department"] == "Tech"]
    sales_top_1 = [r["employee_name"] for r in top_1 if r["department"] == "Sales"]

    assert tech_top_1 == ["Alice"]
    assert sorted(sales_top_1) == ["Eve", "Frank"]


def test_custom_data_seeding():
    custom_analyzer = SalesRankingAnalyzer(":memory:")
    custom_data = [
        ("Xavier", "HR", 500.0),
        ("Yolanda", "HR", 500.0),
        ("Zack", "HR", 400.0),
    ]
    custom_analyzer.seed_data(custom_data)
    rankings = custom_analyzer.get_rankings()

    assert len(rankings) == 3
    assert rankings[0]["rank_val"] == 1
    assert rankings[1]["rank_val"] == 1
    assert rankings[2]["rank_val"] == 3
    custom_analyzer.close()
