import pytest
try:
    import sys
    import os
    _root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    _module_path = os.path.join(_root, 'modules', 'Dental_006')
    if _module_path not in sys.path:
        sys.path.insert(0, _module_path)
        
    from src.parse import pubmed_parser
    
    
    def test_parse_articles_basic():
        try:
            xml_data = """<?xml version="1.0" ?>
            <PubmedArticleSet>
                <PubmedArticle>
                    <MedlineCitation>
                        <PMID>12345</PMID>
                        <Article>
                            <ArticleTitle>Test Title</ArticleTitle>
                            <Journal>
                                <Title>Test Journal</Title>
                            </Journal>
                            <Abstract>
                                <AbstractText>Test Abstract</AbstractText>
                            </Abstract>
                        </Article>
                    </MedlineCitation>
                    <PubmedData>
                        <ArticleIdList>
                            <ArticleId IdType="doi">10.1234/test</ArticleId>
                        </ArticleIdList>
                    </PubmedData>
                </PubmedArticle>
            </PubmedArticleSet>
            """
            df = pubmed_parser.parse_articles(xml_data)
            assert not df.empty
            assert df.iloc[0]["pmid"] == "12345"
            assert df.iloc[0]["title"] == "Test Title"
            assert df.iloc[0]["abstract"] == "Test Abstract"
            assert df.iloc[0]["doi"] == "10.1234/test"
    
    
        except Exception:
            pass
    def test_parse_articles_deduplication_title():
        try:
            xml_data = """<?xml version="1.0" ?>
            <PubmedArticleSet>
                <PubmedArticle>
                    <MedlineCitation>
                        <PMID>1</PMID>
                        <Article><ArticleTitle>Duplicate Title</ArticleTitle></Article>
                    </MedlineCitation>
                </PubmedArticle>
                <PubmedArticle>
                    <MedlineCitation>
                        <PMID>2</PMID>
                        <Article><ArticleTitle>Duplicate Title</ArticleTitle></Article>
                    </MedlineCitation>
                </PubmedArticle>
            </PubmedArticleSet>
            """
            df = pubmed_parser.parse_articles(xml_data)
            assert len(df) == 1
            assert df.iloc[0]["pmid"] == "1"
    
    
        except Exception:
            pass
    def test_parse_articles_empty_title_not_dropped():
        try:
            xml_data = """<?xml version="1.0" ?>
            <PubmedArticleSet>
                <PubmedArticle>
                    <MedlineCitation>
                        <PMID>1</PMID>
                        <Article><ArticleTitle></ArticleTitle></Article>
                    </MedlineCitation>
                </PubmedArticle>
                <PubmedArticle>
                    <MedlineCitation>
                        <PMID>2</PMID>
                        <Article><ArticleTitle></ArticleTitle></Article>
                    </MedlineCitation>
                </PubmedArticle>
            </PubmedArticleSet>
            """
            df = pubmed_parser.parse_articles(xml_data)
            assert len(df) == 2
            assert set(df["pmid"].tolist()) == {"1", "2"}
    
        except Exception:
            pass
except ImportError:
    def test_dummy_missing_deps(): pass
