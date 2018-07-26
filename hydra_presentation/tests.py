from configurations.management import call_command
from django.conf import settings
from django.template import Context, engines
from django.template.backends.django import Template
from django.test import TestCase
from hydra_presentation import polymer as core
from hydra_presentation.templatetags import polymer as library


# Create your tests here.
# class CommandsTestCase(TestCase):
#
#     def test_synchronize_source(self):
#         "Test deploy Polymer project as static resources"
#
#         args = [
#             "build"
#         ]
#         opts = {
#             'src': "../hydra-frontend",
#             'distro': "es6-unbundled",
#             'app': "hydra_presentation",
#             'compile': False
#         }
#         call_command('polymer', *args, **opts)
#
#     def test_build_source(self):
#         "Test deploy Polymer project as static resources"
#
#         args = [
#             "build"
#         ]
#         opts = {
#             'src': "../hydra-frontend",
#             'distro': "es6-unbundled",
#             'app': "hydra_presentation",
#             'compile': True
#         }
#         call_command('polymer', *args, **opts)


class PolymerTemplateTagsTestCase(TestCase):
    TOKEN_IN_POLYMER_CASE = 'my-polymer-element'
    TOKEN_IN_CAMEL_CASE = 'MyPolymerElement'
    TOKEN_IN_PYTHON_CASE = 'my_polymer_element'

    TOKEN_LOWER = 'aaaaaa1'
    TOKEN_VARIOUS = 'AaAaAa1'
    TOKEN_UPPER = 'AAAAAA1'

    # def setUp(self):
    #     self.user = get_user_model().objects.create(username='zoidberg')

    def tag_test(self, template, context, output):
        django_engine = engines['django']
        t = django_engine.from_string("{% load polymer %}" + template)
        c = context
        self.assertEqual(t.render(c), output)

    def test_load(self):
        django_engine = engines['django']
        t = django_engine.from_string("{% load polymer %}")
        c = dict()
        self.assertEqual(t.render(c), '')

    def test_camel_case_on_camel_case(self):
        print('camel_case: %s -> %s' % (self.TOKEN_IN_CAMEL_CASE, self.TOKEN_IN_CAMEL_CASE))
        self.assertEqual(self.TOKEN_IN_CAMEL_CASE, library.camel_case(self.TOKEN_IN_CAMEL_CASE))

    def test_camel_case_on_polymer_case(self):
        print('camel_case: %s -> %s' % (self.TOKEN_IN_POLYMER_CASE, self.TOKEN_IN_CAMEL_CASE))
        self.assertEqual(self.TOKEN_IN_CAMEL_CASE, library.camel_case(self.TOKEN_IN_POLYMER_CASE))

    def test_camel_case_on_python_case(self):
        print('camel_case: %s -> %s' % (self.TOKEN_IN_PYTHON_CASE, self.TOKEN_IN_CAMEL_CASE))
        self.assertEqual(self.TOKEN_IN_CAMEL_CASE, library.camel_case(self.TOKEN_IN_PYTHON_CASE))

    def test_polymer_case_on_camel_case(self):
        print('polymer_case: %s -> %s' % (self.TOKEN_IN_CAMEL_CASE, self.TOKEN_IN_POLYMER_CASE))
        self.assertEqual(self.TOKEN_IN_POLYMER_CASE, library.polymer_case(self.TOKEN_IN_CAMEL_CASE))

    def test_polymer_case_on_polymer_case(self):
        print('polymer_case: %s -> %s' % (self.TOKEN_IN_POLYMER_CASE, self.TOKEN_IN_POLYMER_CASE))
        self.assertEqual(self.TOKEN_IN_POLYMER_CASE, library.polymer_case(self.TOKEN_IN_POLYMER_CASE))

    def test_polymer_case_on_python_case(self):
        print('polymer_case: %s -> %s' % (self.TOKEN_IN_PYTHON_CASE, self.TOKEN_IN_POLYMER_CASE))
        self.assertEqual(self.TOKEN_IN_POLYMER_CASE, library.polymer_case(self.TOKEN_IN_PYTHON_CASE))

    def test_upper(self):
        self.assertEqual(self.TOKEN_UPPER, library.upper(self.TOKEN_LOWER))
        self.assertEqual(self.TOKEN_UPPER, library.upper(self.TOKEN_VARIOUS))
        self.assertEqual(self.TOKEN_UPPER, library.upper(self.TOKEN_UPPER))

    def test_lower(self):
        self.assertEqual(self.TOKEN_LOWER, library.lower(self.TOKEN_LOWER))
        self.assertEqual(self.TOKEN_LOWER, library.lower(self.TOKEN_VARIOUS))
        self.assertEqual(self.TOKEN_LOWER, library.lower(self.TOKEN_UPPER))

    def test_base(self):
        module = core.Module(
            name='test-module',
            path='src/test-module.html',
            mixins=[
                core.Mixin(
                    namespace='TestNameSpace',
                    name='TestMixin0'
                ),
                core.Mixin(
                    namespace='TestNameSpace',
                    name='TestMixin1'
                ),
                core.Mixin(
                    namespace='TestNameSpace',
                    name='TestMixin2'
                ),
                core.Mixin(
                    namespace='TestNameSpace',
                    name='TestMixin3'
                ),
            ],
            base='TestNameSpace.BaseElement'
        )
        base_string = 'TestNameSpace.TestMixin3(TestNameSpace.TestMixin2(TestNameSpace.TestMixin1(TestNameSpace.TestMixin0(TestNameSpace.BaseElement))))'

        self.assertEquals(base_string, library.base(module))

    def test_tag(self):
        tag = core.Tag(
            name='test-tag',
            attribute_string='testdata0',
            attribute_number=1,
            attribute_object=dict(a='adata', b='bdata'),
            flag=None,
            flag_true=True,
            flag_false=False,
        )

        django_engine = engines['django']
        template = '{% tag testtag %}'
        t = django_engine.from_string("{% load polymer %} " + template)
        c = dict(testtag=tag)
        result = str(t.render(c))
        print(result)
        self.assertTrue('<test-tag' in result)
        self.assertTrue('</test-tag>' in result)
        self.assertTrue('attribute-number="1"' in result)
        self.assertTrue('attribute-string="testdata0"' in result)
        self.assertTrue('flag' in result)
        self.assertTrue('flag-true="true"' in result)
        self.assertTrue('flag-false="false"' in result)

    def test_link_eager(self):
        component = core.Component(
            name='test-component',
            path='src/test-component.html',
            attribute_string='testdata0',
            attribute_number=1,
            attribute_object=dict(a='adata', b='bdata'),
            flag=None,
            flag_true=True,
            flag_false=False,
        )

        django_engine = engines['django']
        template = '{% link testcomponent %}'
        t = django_engine.from_string("{% load polymer %}" + template)
        c = dict(testcomponent=component)

        result = str(t.render(c))
        print(result)
        self.assertEquals(result, '<link rel="import" href="src/test-component.html">')

    def test_link_lazy(self):
        component = core.Component(
            name='test-component',
            path='src/test-component.html',
            lazy=True
        )

        django_engine = engines['django']
        template = '{% link testcomponent %}'
        t = django_engine.from_string("{% load polymer %}" + template)
        c = dict(testcomponent=component)

        result = str(t.render(c))
        print(result)
        self.assertEquals(result, '<link rel="lazy-import" href="src/test-component.html">')

    def test_dom_module(self):
        module = core.Module(
            name='test-component',
            path='src/test-component.html',
            lazy=True,
            mixins=[
                core.Mixin(
                    namespace='TestNamespace',
                    name='TestMixin'
                )
            ],
            base='Polymer.Element'
        )

        django_engine = engines['django']
        template = '{% dom_module testmodule %}'
        t = django_engine.from_string("{% load polymer %}" + template)
        c = dict(testmodule=module)

        result = str(t.render(c))
        print(result)
        # print(result.replace('\n', ''))

        self.assertTrue('<dom-module id="test-component">' in result)
        self.assertTrue('class TestComponent extends TestNamespace.TestMixin(Polymer.Element)' in result)
        self.assertTrue('window.customElements.define(TestComponent.is, TestComponent);' in result)
        self.assertTrue("static get is() { return 'test-component'; }" in result)
