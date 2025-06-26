import logging

from jinja2 import Template


logger = logging.getLogger(__file__)


class StringUtils:
    """Utility class for string operations.

    Provides static methods for manipulating and formatting strings,
    such as populating template variables.
    """

    @staticmethod
    def populate_variables(
        template_text: str, variables: dict[str, any]
    ) -> str:
        try:
            logger.info({'TEMPLATE_TEXT': template_text})
            logger.info({'TEMPLATE_VARIABLES': {**variables}})
            template = Template(template_text)
            populated_template = template.render(**variables)
            logger.info({'POPULATED_TEMPLATE': populated_template})
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
