from configurations.management import call_command
from django.test import TestCase


# Create your tests here.
class CommandsTestCase(TestCase):

    def test_synchronize_source(self):
        "Test deploy Polymer project as static resources"

        args = [
            "build"
        ]
        opts = {
            'src': "../hydra-frontend",
            'distro': "es6-unbundled",
            'app': "hydra_presentation",
            'compile': False
        }
        call_command('polymer', *args, **opts)

    def test_build_source(self):
        "Test deploy Polymer project as static resources"

        args = [
            "build"
        ]
        opts = {
            'src': "../hydra-frontend",
            'distro': "es6-unbundled",
            'app': "hydra_presentation",
            'compile': True
        }
        call_command('polymer', *args, **opts)
