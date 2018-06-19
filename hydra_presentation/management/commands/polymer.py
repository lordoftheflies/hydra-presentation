import json
import os
import pathlib
import shutil
import subprocess

from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Polymer-CLI wrapper command.'

    MODULE_STATIC_DIRECTORYNAME = 'static'
    MODULE_TEMPLATE_DIRECTORYNAME = 'templates'
    POLYMER_BULD_DIRECTORYNAME = 'build'
    POLYMER_SRC_DIRECTORYNAME = 'src'

    POLYMER_CONFIGURATION_FILENAME = 'polymer.json'
    BOWER_CONFIGURATION_FILENAME = 'bower.json'
    BOWER_COMPONENTS_DIRECTORYNAME = 'bower_components'

    POLYMER_CLI = 'polymer'
    POLYMER_CLI_COMMAND_ANALYZE = 'analyze'
    POLYMER_CLI_COMMAND_BUILD = 'build'
    POLYMER_CLI_COMMAND_INIT = 'init'
    POLYMER_CLI_COMMAND_INSTALL = 'install'
    POLYMER_CLI_COMMAND_LINT = 'lint'
    POLYMER_CLI_COMMAND_SERVE = 'serve'
    POLYMER_CLI_COMMAND_TEST = 'test'

    POLYMER_BUILD_ES6_UNBUNDLED = 'es6-unbundled'
    POLYMER_BUILD_ES6_BUNDLED = 'es6-bundled'
    POLYMER_BUILD_ES5_BUNDLED = 'es5-bundled'

    POLYMER_DISTIRBUTIONS = [
        POLYMER_BUILD_ES5_BUNDLED,
        POLYMER_BUILD_ES6_BUNDLED,
        POLYMER_BUILD_ES6_UNBUNDLED
    ]

    POLYMER_CLI_COMMANDS = [
        POLYMER_CLI_COMMAND_ANALYZE,
        POLYMER_CLI_COMMAND_INIT,
        POLYMER_CLI_COMMAND_INSTALL,
        POLYMER_CLI_COMMAND_BUILD,
        POLYMER_CLI_COMMAND_LINT,
        POLYMER_CLI_COMMAND_SERVE,
        POLYMER_CLI_COMMAND_TEST,
    ]

    def __init__(self, stdout=None, stderr=None, no_color=False):
        super().__init__(stdout, stderr, no_color)
        self._bower_configuration = None

    def add_arguments(self, parser):
        parser.add_argument(
            'command',
            choices=self.POLYMER_CLI_COMMANDS,
            type=str,
            help='Polymer CLI commands'
        )

        parser.add_argument(
            '--src',
            type=str,
            help='Home directory of the Polymer application'
        )
        parser.add_argument(
            '--app',
            type=str,
            help='Parent Django application'
        )
        parser.add_argument(
            '--distro',
            type=str,
            choices=self.POLYMER_DISTIRBUTIONS,
            help='Polymer build distribution'
        )
        parser.add_argument(
            '--compile',
            action='store_true',
            dest='compile',
            default=False,
            help='Switch to compile'
        )

    def label_dict(self, options: dict, **kwargs):
        return {kwargs[k]: options[k] for k in kwargs}

    def handle(self, *args, **options):
        print(args)
        print(options)

        self.stdout.write(self.style.WARNING('Django Polymer build'))
        self.stdout.write(self.style.WARNING(json.dumps(
            self.label_dict(
                options=options,

                command='Polymer CLI command',
                src='Polymer project home',
                distro='Build type',
                app='Django module',
                compile='Compile source',

            ),
            sort_keys=True,
            indent=4
        )))

        self.source_directory = options['src']
        self.python_module = options['app']
        self.polymer_distro = options['distro']
        self.compile = options['compile']

        # self.stdout.write(self.style.WARNING('Django Polymer'))
        # self.stdout.write('Polymer source directory: %s' % self.source_directory)
        # self.stdout.write('Polymer distribution: %s' % self.polymer_distro)
        # self.stdout.write('Django module name: %s' % self.python_module)
        # if self.check_configurations() is False:
        #     raise ValueError('Bower - incompatible components')

        # if command not in self.POLYMER_CLI_COMMANDS:
        #     raise ValueError('Polymer - invalid command')

        # # Delete builf directory
        # self.stdout.write(self.style.WARNING(
        #     'Erase static directory in module[%s]: %s' % (self.python_module, self.module_static_directory)))
        # shutil.rmtree(path=self.module_static_directory)
        # self.build_cleanup()

        if self.compile:
            self.build()
            self.copy_static_resources_from_build()


        else:
            if os.path.exists(self.polymer_build_path):
                self.build_cleanup()

            self.copy_static_resources_from_source()

        self.remove_module_static_bower()
        # # Create module specific static directory
        # pathlib.Path(self.module_static_path).mkdir(parents=True, exist_ok=True)
        # # Create module specific template directory
        # pathlib.Path(self.module_template_path).mkdir(parents=True, exist_ok=True)

        self.django_bower_monkey_patch()

        self.stdout.write(
            self.style.SUCCESS('Successfully installed  "%(name)s#%(version)s"' % self.bower_configuration))

    def load_bower_json(self, *args):
        with open(os.path.join(*args)) as f:
            bower_configuration = json.load(f)
        return bower_configuration

    @property
    def polymer_path(self):
        return os.path.join(self.source_directory)

    @property
    def bower_configuration(self):
        if self._bower_configuration is None:
            self._bower_configuration = self.load_bower_json(self.source_directory, self.BOWER_CONFIGURATION_FILENAME)
        return self._bower_configuration

    @property
    def polymer_configuration(self):
        if self._polymer_configuration is None:
            self._polymer_configuration = self.load_bower_json(self.source_directory,
                                                               self.POLYMER_CONFIGURATION_FILENAME)
        return self._polymer_configuration

    @property
    def module_static_directory(self):
        return os.path.join(settings.BASE_DIR, self.python_module, self.MODULE_STATIC_DIRECTORYNAME)

    @property
    def module_static_bower_components_path(self):
        return os.path.join(self.module_static_directory, self.BOWER_COMPONENTS_DIRECTORYNAME)

    @property
    def module_static_path(self):
        return os.path.join(self.module_static_directory, self.python_module)

    @property
    def module_template_directory(self):
        return os.path.join(settings.BASE_DIR, self.python_module, self.MODULE_TEMPLATE_DIRECTORYNAME)

    @property
    def module_template_path(self):
        return os.path.join(self.module_template_directory, self.python_module)

    @property
    def polymer_build_path(self):
        return os.path.join(self.source_directory, self.POLYMER_BULD_DIRECTORYNAME, self.polymer_distro)

    @property
    def module_static_src_path(self):
        return os.path.join(self.module_static_directory, self.POLYMER_SRC_DIRECTORYNAME)

    def build_cleanup(self):
        # Delete build directory
        self.stdout.write(self.style.WARNING(
            'Erase build[%s] directory from polymer source: %s' % (self.polymer_distro, self.polymer_build_path)))
        shutil.rmtree(path=self.polymer_build_path)

    def build(self):
        # Build Polymer application
        self.stdout.write('Polymer %s %s#%s ...' % (
            self.POLYMER_CLI_COMMAND_BUILD, self.bower_configuration['name'], self.bower_configuration['version']))
        self.call_bash_script(command=self.POLYMER_CLI_COMMAND_BUILD)

    def copy_static_resources_from_build(self):
        # Delete build directory
        shutil.rmtree(path=self.module_static_directory)

        # Move distribution
        self.stdout.write('Copy built distribution: %s -> %s' % (self.polymer_build_path, self.module_static_directory))
        shutil.copytree(
            src=self.polymer_build_path,
            dst=self.module_static_directory,
        )

    def copy_static_resources_from_source(self):
        # Delete build directory
        shutil.rmtree(path=self.module_static_directory)

        # Move distribution
        self.stdout.write('Copy sources: %s -> %s' % (self.polymer_build_path, self.module_static_directory))
        shutil.copytree(
            src=self.polymer_path,
            dst=self.module_static_directory,
            ignore = shutil.ignore_patterns('build', 'test', 'index.html')
        )

    def remove_module_static_bower(self):
        # Delete build directory
        shutil.rmtree(path=self.module_static_bower_components_path)

    def django_bower_monkey_patch(self):
        # Static components of <polymer-app>
        self.stdout.write('Change link of Bower components under %s' % (self.module_static_path))
        self.process_directories_reqursively(
            path=self.module_static_directory,
            path_from='bower_components/',
            path_to=''
        )

        # Static components of <polymer-app>/src
        self.process_directories_reqursively(
            path=self.module_static_src_path,
            path_from='bower_components/',
            path_to=''
        )

    def check_configurations(self):
        bower_dependencies = self.bower_configuration['dependencies']

        already_installed_apps = settings.BOWER_INSTALLED_APPS
        currently_deployed_apps = [bower_dependencies[k] for k in bower_dependencies.keys()]

        return set(already_installed_apps) == set(currently_deployed_apps)

    def process_directories_reqursively(self, path, path_from, path_to):

        if os.path.isfile(path):
            self.replace_link_of_bower_components(
                filepath=path,
                path_from=path_from,
                path_to=path_to
            )
        else:
            files = os.listdir(path)
            for file in files:
                self.process_directories_reqursively(
                    path=os.path.join(path, file),
                    path_from=path_from,
                    path_to=path_to,
                )

    def call_bash_script(self, command=POLYMER_CLI_COMMAND_BUILD):
        subprocess.call(
            ["polymer", command],
            # shell=True,
            cwd=self.polymer_path)
        # self.stdout.writelines(res.splitlines())

    def replace_link_of_bower_components(self, filepath, path_from, path_to):
        if pathlib.Path(filepath).suffix == '.html':
            self.stdout.write('* %s -> %s in %s' % (
                path_from,
                path_to,
                pathlib.Path(filepath).relative_to(self.module_static_directory)
            ))

            fileInput = open(filepath, 'r')
            filedata = fileInput.read()
            fileInput.close()

            # Replace the target string
            filedata = filedata.replace(path_from, path_to)

            # Write the file out again
            fileOutput = open(filepath, 'w')
            fileOutput.write(filedata)
            fileOutput.close()
