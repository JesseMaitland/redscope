from redgiant.redscope.project import RedScopeMultiActionEntryPoint


class Project(RedScopeMultiActionEntryPoint):

    discover = True

    description = """
    Base command to interact with the redscope project. Run 'redscope project -h for more info.'
    """

    def action_new(self):
        print("created directories for redscope schema introspection at redshift/redscope")
        self.project.init_project()

