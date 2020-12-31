import sqlparse
from typing import Tuple, List
from redgiant.redscope.introspection.schema.view import View
from redgiant.redscope.introspection.formatters.base_formatter import DDLFormatter


class ViewFormatter(DDLFormatter):

    def __init__(self):
        super().__init__()

    def format(self, raw_ddl: Tuple[str]) -> List[View]:

        template = self.template_env.get_template('view.sql')

        views = []
        for ddl in raw_ddl:
            schema, name, content = ddl
            content = sqlparse.format(sql=content, reindent=True)
            content = template.render(schema=schema, name=name, content=content)
            view = View(schema=schema, name=name, ddl=content)
            views.append(view)

        return views
