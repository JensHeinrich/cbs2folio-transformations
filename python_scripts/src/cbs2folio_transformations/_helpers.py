"""Module for reusable codesnippets."""
from typing import NoReturn
from typing import TypeVar

from lxml import etree  # nosec blacklist

_ExceptionType = TypeVar("_ExceptionType", bound=Exception)


# Source: https://stackoverflow.com/questions/9157210/how-do-i-raise-the-same-exception-with-a-custom-message-in-python  # noqa: E501
def reraise(
    e: _ExceptionType, info: str
) -> NoReturn:  # pyright: reportInvalidTypeVarUse=false
    """Reraise an exception after adding information.

    Args:
        e (_ExceptionType): Exception to reraise
        info (str): Additional information

    Raises:
        e.with_traceback (_ExceptionType): The appended Exception

    Returns:
        NoReturn: Does not return
    """
    e.args = info, *e.args
    raise e.with_traceback(e.__traceback__)


# Based on: https://www.mail-archive.com/lxml@python.org/msg00011.html
def get_variable_from_xsl(variable_name: str, xsl: etree._ElementTree) -> str:
    """Get the value of an XSL variable.

    Args:
        variable_name (str): Name of the variable to find
        xsl (etree._ElementTree): XSL Tree to search in

    Raises:
        ValueError: Unkmown variable

    Returns:
        str: Value of the variable
    """
    xpath_results = xsl.xpath(
        "//xsl:variable[@name=$name]",
        name=variable_name,
        namespaces={"xsl": "http://www.w3.org/1999/XSL/Transform"},
    )

    for xpath_result in xpath_results:
        if xpath_result.get("name") == variable_name:
            for xpath_child in xpath_result.xpath(
                "xsl:value-of",
                namespaces={"xsl": "http://www.w3.org/1999/XSL/Transform"},
            ):
                if "select" in xpath_child.keys():
                    return xpath_child.get("select").strip("'")
                if "text" in xpath_child.keys():
                    return xpath_child.text.strip("'")

            if hasattr(xpath_result, "text"):
                _value: str = xpath_result.text
                return _value.strip("'")

    raise ValueError(f"{variable_name} not defined in XSL")
