"""Regression tests for safe CLI result pagination.

These tests exercise a pure filtering helper without requiring live models or APIs.
"""
import pytest

from moonshot.integrations.cli.utils.process_data import filter_data


def test_paginating_empty_list_returns_empty_list():
    assert filter_data([], pagination=(1, 10)) == []
    assert filter_data([], pagination=(5, 10)) == []


def test_pagination_keeps_original_rows_unchanged():
    rows = [{"name": "alpha"}, {"name": "beta"}, {"name": "gamma"}]

    result = filter_data(rows, pagination=(1, 2))

    assert result == [
        {"name": "alpha", "idx": 1},
        {"name": "beta", "idx": 2},
    ]
    assert rows == [{"name": "alpha"}, {"name": "beta"}, {"name": "gamma"}]
    assert result[0] is not rows[0]


def test_pagination_out_of_range_returns_last_page():
    result = filter_data([{"name": "a"}, {"name": "b"}, {"name": "c"}], pagination=(99, 2))
    assert result == [{"name": "c", "idx": 3}]


@pytest.mark.parametrize("page,size", [(0, 1), (1, 0), (-1, 3)])
def test_invalid_pagination_is_rejected(page, size):
    with pytest.raises(RuntimeError, match="Invalid page number"):
        filter_data([{"name": "a"}], pagination=(page, size))
