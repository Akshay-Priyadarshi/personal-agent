from typing import Any

from jinja2 import Template

from common_utils.logger import LoggerUtils


logger = LoggerUtils.get_logger(__name__)


class StringUtils:
    """Utility class for string operations.

    Provides static methods for manipulating and formatting strings,
    such as populating template variables.
    """

    @staticmethod
    def populate_variables(
        template_text: str, variables: dict[str, Any] = None
    ) -> str:
        if variables is None:
            variables = {}
        try:
            # logger.debug({'TEMPLATE_TEXT': template_text})
            # logger.debug({'TEMPLATE_VARIABLES': {**variables}})
            template = Template(template_text)
            populated_template = template.render(**variables)
            logger.debug(
                'populated template successfully',
                extra={'populated_template': populated_template},
            )
            return populated_template
        except Exception as e:
            raise Exception(
                f"""
                unable to populate template
                {template_text}
                with variables
                {variables}
                """
            ) from e
