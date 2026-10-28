"""Test attribute selectors."""
from .. import util


class TestAttribute(util.TestCase):
    """Test attribute selectors."""

    MARKUP = """
    <div id="div">
    <p id="0">Some text <span id="1"> in a paragraph</span>.</p>
    <a id="2" href="http://google.com">Link</a>
    <span id="3">Direct child</span>
    <pre id="pre">
    <span id="4">Child 1</span>
    <span id="5">Child 2</span>
    <span id="6">Child 3</span>
    </pre>
    </div>
    """

    def test_attribute_not_equal_no_quotes(self):
        """Test attribute with value that does not equal specified value (no quotes)."""

        # No quotes
        self.assert_selector(
            self.MARKUP,
            'body [id!=\\35]',
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

    def test_attribute_not_equal_quotes(self):
        """Test attribute with value that does not equal specified value (quotes)."""

        # Quotes
        self.assert_selector(
            self.MARKUP,
            "body [id!='5']",
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

    def test_attribute_not_equal_double_quotes(self):
        """Test attribute with value that does not equal specified value (double quotes)."""

        # Double quotes
        self.assert_selector(
            self.MARKUP,
            'body [id!="5"]',
            ["div", "0", "1", "2", "3", "pre", "4", "6"],
            flags=util.HTML5
        )

    def test_attribute_quoted_escaped_newlines(self):
        """Test attribute with escaped new lines (`\\f`, `\\r`, `\\r\\n`) in quoted strings."""

        self.assert_selector(
            self.MARKUP,
            '[id="pr\\\fe"]',
            ["pre"],
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            "[id='pr\\\re']",
            ["pre"],
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            '[id="pr\\\r\ne"]',
            ["pre"],
            flags=util.HTML
        )

    def test_bad_attribute_unclused(self):
        """Test bad attribute fails for syntax error, not timeout error."""

        self.assert_syntax_error_no_timeout('[a="' + ('x' * 300))

    def test_bad_attribute_unclosed_single_quote(self):
        """Test bad attribute with unclosed single quote fails for syntax error, not timeout error."""

        self.assert_syntax_error_no_timeout("[a='" + ('x' * 300))

    def test_bad_attribute_unclosed_escaped_newlines(self):
        """Test bad attribute with unclosed quote and escaped new lines fails for syntax error, not timeout error."""

        self.assert_syntax_error_no_timeout('[a="' + ('\\\f' * 100))
        self.assert_syntax_error_no_timeout("[a='" + ('\\\r' * 100))

    def test_bad_pseudo_class_value_unclosed(self):
        """Test pseudo-classes with unclosed quoted values fail for syntax error, not timeout error."""

        self.assert_syntax_error_no_timeout(':-soup-contains("' + ('x' * 300))
        self.assert_syntax_error_no_timeout(":lang('" + ('x' * 300))
