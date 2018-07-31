from configurations.management import call_command
from django.apps import apps
from django.conf import settings
from django.template import Context, engines
from django.template.backends.django import Template
from django.test import TestCase
from django.urls import reverse

from hydra_presentation import polymer as core
from hydra_presentation.templatetags import polymer as library
from django.test import Client


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

class PolymerBuilderTestCase(TestCase):

    def test_tag_builder(self):
        builder = core.TagBuilder()
        given = core.Tag(name='test-component', attribute_string='attribute_value', attribute_flag=None)
        tag = builder.set_attribute('attribute_string', 'attribute_value').set_name('test-component').set_flag(
            'attribute_flag').build()
        self.assertEqual(given.to_json(), tag.to_json())

    def test_component_builder(self):
        builder = core.ComponentBuilder()
        given = core.Component(
            name='test-component',
            base=core.ELEMENT_ECMA_CLASS,
            lazy=True, path='path',
            attribute_string='attribute_value',
            attribute_flag=None
        )
        component = builder.set_attribute('attribute_string', 'attribute_value').set_name('test-component').set_flag(
            'attribute_flag').set_path('path').set_lazy(True).set_base(core.ELEMENT_ECMA_CLASS).build()
        self.assertEqual(given.to_json(), component.to_json())

    def test_mixin_builder(self):
        builder = core.MixinBuilder()
        given = core.Mixin(
            name='name',
            path='path',
            namespace='ns'
        )
        mixin = builder.set_path('path').set_name('name').set_namespace('ns').build()
        self.assertEqual(given.to_json(), mixin.to_json())

    def test_style_builder(self):
        builder = core.StyleBuilder()
        given = core.Style(name='name', path='path')
        style = builder.set_name('name').set_path('path').build()
        self.assertEqual(given.to_json(), style.to_json())

    def test_module_builder(self):
        builder = core.ModuleBuilder()

        given_style = core.Style(name='name', path='path')
        given_component = core.Component(
            name='test-component',
            base=core.ELEMENT_ECMA_CLASS,
            lazy=True,
            path='path',
            attribute_string='attribute_value',
            attribute_flag=None
        )
        given_mixin = core.Mixin(
            name='name',
            path='path',
            namespace='ns'
        )
        given = core.Module(
            name='name',
            path='path',
            components=[given_component],
            mixins=[given_mixin],
            styles=[given_style],
            lazy=True,
            attribute_string='value',
            attribute_flag=None
        )

        module = builder \
            .set_name('name') \
            .set_path('path') \
            .set_lazy(True) \
            .set_flag('attribute_flag') \
            .set_attribute(name='attribute_string', value='value') \
            .mixin() \
            .set_path('path') \
            .set_name('name') \
            .set_namespace('ns') \
            .append() \
            .style() \
            .set_name('name') \
            .set_path('path') \
            .append() \
            .component() \
            .set_attribute(name='attribute_string', value='attribute_value') \
            .set_name('test-component') \
            .set_flag('attribute_flag') \
            .set_path('path') \
            .set_lazy(True) \
            .set_base(core.ELEMENT_ECMA_CLASS) \
            .append() \
            .build()

        self.assertEqual(given.to_json(), module.to_json())

    def test_page_builder(self):
        builder = core.PageBuilder()
        given_component = core.Component(
            name='test-component',
            base=core.ELEMENT_ECMA_CLASS,
            lazy=True,
            path='path',
            attribute_string='attribute_value',
            attribute_flag=None
        )
        given = core.Page(
            name='name',
            path='path',
            title='title',
            components=[given_component],
            attribute_string='attribute_value',
            mixins=[],
            styles=[]
        )
        page = builder \
            .set_name('name') \
            .set_path('path') \
            .set_attribute(name='attribute_string', value='attribute_value') \
            .set_title('title') \
            .set_base(core.ELEMENT_ECMA_CLASS) \
            .component() \
            .set_attribute(name='attribute_string', value='attribute_value') \
            .set_name('test-component') \
            .set_flag('attribute_flag') \
            .set_path('path') \
            .set_lazy(True) \
            .set_base(core.ELEMENT_ECMA_CLASS) \
            .append() \
            .build()
        self.assertEqual(given.to_json(), page.to_json())

    def test_application_builder(self):
        builder = core.ApplicationBuilder()

        given = core.Application(name='name', path='path', title='title')

        app = builder \
            .set_name('name') \
            .set_path('path') \
            .set_title('title') \
            .build()

        self.assertEqual(given.to_json(), app.to_json())


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
                    name='TestMixin0',
                    path='src/test-mixin0.html'
                ),
                core.Mixin(
                    namespace='TestNameSpace',
                    name='TestMixin1',
                    path='src/test-mixin1.html'
                ),
                core.Mixin(
                    namespace='TestNameSpace',
                    name='TestMixin2',
                    path='src/test-mixin2.html'
                ),
                core.Mixin(
                    namespace='TestNameSpace',
                    name='TestMixin3',
                    path='src/test-mixin3.html'
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
                    name='TestMixin',
                    path='src/test-mixin.html'
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


class PresentationViewsTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_service_worker(self):
        response = self.client.get(reverse('service_worker'))
        self.assertEqual(response.status_code, 200)

    def test_application(self):
        response = self.client.get(reverse('application'))
        self.assertEqual(response.status_code, 200)

    def test_page_404(self):
        current_app = apps.get_app_config(app_label=settings.PRESENTATION['ROOT_APP'])
        current_app.application.pages['view404'] = core.Page(name='view404', path='src/my-view404.html')

        response = self.client.get(reverse('page', args=['view404']))
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_src(self):
        # response = self.client.get(reverse('page'))
        # self.assertEqual(response.status_code, 200)
        pass

    def test_user_info(self):
        response = self.client.get(reverse('user_info'))
        self.assertEqual(response.status_code, 200)

    def test_application_index(self):
        response = self.client.get(reverse('application_index'))
        self.assertEqual(response.status_code, 200)
