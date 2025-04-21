import os
import pytest

from src.services.fallback_pdf_service import FallbackPDFService


@pytest.fixture
def service():
    return FallbackPDFService()


@pytest.fixture
def test_params():
    return {
        "test_file": "dummy.pdf",
        "output_dir": os.getcwd(),
        "base_filename": "base",
    }


def test_get_pdf_info_structure(service, test_params):
    test_file = test_params["test_file"]

    info = service.get_pdf_info(test_file)

    assert isinstance(info, dict)
    assert "page_count" in info
    assert "file_path" in info
    assert "file_name" in info
    assert info["file_path"] == test_file
    assert info["file_name"] == os.path.basename(test_file)
    assert isinstance(info["page_count"], int)
    assert info["page_count"] >= 0


def test_split_by_fixed_range_returns_list(service, test_params):
    result = service.split_by_fixed_range(
        test_params["test_file"],
        2,
        test_params["output_dir"],
        base_filename=test_params["base_filename"],
    )

    assert isinstance(result, list)
    for path in result:
        assert isinstance(path, str)


def test_split_by_custom_ranges_returns_list(service, test_params):
    ranges = [(1, 1), (2, 2)]

    result = service.split_by_custom_ranges(
        test_params["test_file"],
        ranges,
        test_params["output_dir"],
        base_filename=test_params["base_filename"],
    )

    assert isinstance(result, list)
    for path in result:
        assert isinstance(path, str)
