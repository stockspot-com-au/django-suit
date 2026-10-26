from django.test.runner import DiscoverRunner


class SuitTestRunner(DiscoverRunner):
    """
    Test modules in suit.tests are not named test*.py, so collect them all.
    """

    @classmethod
    def add_arguments(cls, parser):
        super().add_arguments(parser)
        parser.set_defaults(pattern='*.py')
