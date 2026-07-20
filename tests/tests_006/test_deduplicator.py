import pytest
try:
    import sys
    import os
    _root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    _module_path = os.path.join(_root, 'modules', 'Dental_006')
    if _module_path not in sys.path:
        sys.path.insert(0, _module_path)
        
    import pandas as pd
    
    from src.ingest.deduplicator import deduplicate_records, normalize_author, normalize_title
    
    
    def test_normalization():
        try:
            assert normalize_title("Hello, World! 2023") == "helloworld2023"
            assert normalize_title("A Study on P.C.O.S.") == "astudyonpcos"
            assert normalize_author("Smith, J.D.") == "smith"
            assert normalize_author("Doe") == "doe"
    
    
        except ImportError:
            pass
    def test_deduplicate_doi():
        try:
            existing = pd.DataFrame([{"doi": "10.123/456", "title": "A", "first_author": "B", "pub_year": "2020"}])
            new = pd.DataFrame([{"doi": "10.123/456", "title": "C", "first_author": "D", "pub_year": "2021"}])
            res, stats = deduplicate_records(existing, new)
            assert stats["duplicates_removed"] == 1
            assert len(res) == 0
    
    
        except ImportError:
            pass
    def test_deduplicate_title():
        try:
            existing = pd.DataFrame([{"doi": "", "title": "Hello, World!", "first_author": "B", "pub_year": "2020"}])
            new = pd.DataFrame([{"doi": "", "title": "hello world", "first_author": "D", "pub_year": "2021"}])
            res, stats = deduplicate_records(existing, new)
            assert stats["duplicates_removed"] == 1
            assert len(res) == 0
    
    
        except ImportError:
            pass
    def test_deduplicate_cross():
        try:
            existing = pd.DataFrame(
                [
                    {
                        "doi": "",
                        "title": "Long title that is similar enough to match 20 chars",
                        "first_author": "Smith, J",
                        "pub_year": "2020",
                    }
                ]
            )
            new = pd.DataFrame(
                [
                    {
                        "doi": "",
                        "title": "Long title that is similar enough to match extra words",
                        "first_author": "Smith",
                        "pub_year": "2020",
                    }
                ]
            )
            res, stats = deduplicate_records(existing, new)
            assert stats["duplicates_removed"] == 1
            assert len(res) == 0
    
    
        except ImportError:
            pass
    def test_no_duplicates():
        try:
            existing = pd.DataFrame([{"doi": "10.1", "title": "Title 1", "first_author": "A", "pub_year": "2020"}])
            new = pd.DataFrame([{"doi": "10.2", "title": "Title 2", "first_author": "B", "pub_year": "2021"}])
            res, stats = deduplicate_records(existing, new)
            assert stats["duplicates_removed"] == 0
            assert len(res) == 1
    
        except ImportError:
            pass
except ImportError:
    pytest.skip('Missing dependencies', allow_module_level=True)
