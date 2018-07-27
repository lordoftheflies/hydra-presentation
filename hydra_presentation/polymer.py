import json
import logging

logger = logging.getLogger(__name__)

ELEMENT_ECMA_CLASS = 'window.Polymer.Element'


class Resource:

    def __init__(self, path: str = None, lazy: bool = False) -> None:
        self.path = path
        self.lazy = lazy

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Tag(Resource):
    """
    Simple presentation tag
    """
    FILENAME_TEMPLATE = '%s.html'

    def __init__(self, name: str, path: str = None, lazy: bool = False, **kwargs) -> None:
        super().__init__(path=path if path is not None else (self.FILENAME_TEMPLATE % name), lazy=lazy)
        self.name = name
        self.attributes = kwargs

    def __str__(self):
        return '<%s %s>%s</%s>' % (
            self.name,
            ' '.join(
                [(('%s="%s"' % (key, value)) if value is not None else key) for key, value in self.attributes.items()]),
            '',
            self.name
        )


class Component(Tag):

    def __init__(self, name: str, path: str = None, base=ELEMENT_ECMA_CLASS, lazy: bool = False, **kwargs) -> None:
        super(Component, self).__init__(name=name, path=path, lazy=lazy, **kwargs)
        self.base = base


class Style(Resource):

    def __init__(self, name: str, path: str = None, lazy: bool = False):
        super().__init__(path=path, lazy=lazy)
        self.name = name

    def __str__(self):
        return self.name


class Mixin(Resource):

    def __init__(self, namespace: str, name: str, path: str):
        super().__init__(path=path, lazy=False)
        self.namespace = namespace
        self.name = name

    @property
    def fqdn(self):
        return '%s.%s' % (
            self.namespace,
            self.name
        )

    def apply(self, base):
        return '%s.%s(%s)' % (
            self.namespace,
            self.name,
            base
        )


class Module(Component):

    def __init__(self, name: str, path: str, components: list = [], mixins: list = [], styles: list = [],
                 lazy: bool = False,
                 base=ELEMENT_ECMA_CLASS,
                 **kwargs) -> None:
        super().__init__(name=name, path=path, lazy=lazy, **kwargs)
        self.components = components
        self.mixins = mixins
        self.base = base
        self.styles = styles

    @property
    def included_styles(self):
        return ' '.join([str(style) for style in self.styles])


class Page(Module):
    TOKEN_SEPARATOR = '-'

    def __init__(self, name: str, path: str, title: str = None, components: list = [], **kwargs) -> None:
        super().__init__(name=name, path=path, components=components, lazy=True, **kwargs)
        self.title = title
        self.components = components

    @property
    def route(self):
        return self.TOKEN_SEPARATOR.join(self.name.split(self.TOKEN_SEPARATOR)[1:])


class Application(Module):

    def __init__(self, name: str, path: str, title: str = None, components: list = [], mixins: list = [],
                 styles: list = [],
                 lazy: bool = False, pages: dict = {},
                 **kwargs) -> None:
        super().__init__(name=name, path=path, components=components, styles=styles, lazy=lazy, mixins=mixins, **kwargs)
        self.title = title
        self.pages = pages
        self.lazy = lazy
        self.path = path

    def get_page(self, route: str):
        return self.pages[route]


class Builder:

    def __init__(self, owner=None):
        self.owner = owner

    def append(self):
        return self.owner if self.owner is not None else self

    def build(self):
        raise NotImplementedError()


class TagBuilder(Builder):
    """
    Builder for a tag.
    """

    def __init__(self, owner=None) -> None:
        super().__init__(owner=owner)
        self.name = None
        self.attributes = dict()

    def set_name(self, name: str) -> 'TagBuilder':
        self.name = name
        return self

    def set_flag(self, name: str) -> 'TagBuilder':
        self.attributes[name] = None
        return self

    def set_attribute(self, name: str, value: str) -> 'TagBuilder':
        self.attributes[name] = value
        return self

    def build(self) -> Tag:
        return Tag(
            name=self.name,
            **self.attributes
        )


class MixinBuilder(Builder):

    def __init__(self, owner=None):
        super().__init__(owner=owner)
        self.namespace = None
        self.name = None
        self.path = None

    def set_name(self, name: str) -> 'MixinBuilder':
        self.name = name
        return self

    def set_namespace(self, namespace: str) -> 'MixinBuilder':
        self.namespace = namespace
        return self

    def set_path(self, path: str) -> 'MixinBuilder':
        self.path = path
        return self

    def build(self) -> Mixin:
        return Mixin(
            name=self.name,
            namespace=self.namespace,
            path=self.path
        )

    def append(self):
        mixin = self.build()
        self.owner.mixins.append(mixin)
        logger.info('Apply mixin "%s" on "my-app"' % mixin.fqdn)
        return super().append()


class StyleBuilder(Builder):

    def __init__(self, owner=None):
        super().__init__(owner=owner)
        self.name = None
        self.path = None

    def set_name(self, name: str) -> 'StyleBuilder':
        self.name = name
        return self

    def set_path(self, path: str) -> 'StyleBuilder':
        self.path = path
        return self

    def build(self) -> Style:
        return Style(
            name=self.name,
            path=self.path
        )

    def append(self):
        style = self.build()
        self.owner.styles.append(style)
        logger.info('Apply style "%s" on "my-app"' % style.name)
        return super().append()


class ModuleBuilder(TagBuilder):

    def __init__(self, owner=None) -> None:
        super().__init__(owner=owner)
        self.path = None
        self.components = []
        self.mixins = []
        self.base = ELEMENT_ECMA_CLASS
        self.lazy = False
        self.styles = []

    def set_path(self, path: str) -> 'ModuleBuilder':
        self.path = path
        return self

    def set_base(self, base: str) -> 'ModuleBuilder':
        self.base = base
        return self

    def set_lazy(self, lazy: str) -> 'ModuleBuilder':
        self.lazy = lazy
        return self

    def mixin(self) -> MixinBuilder:
        return MixinBuilder(owner=self)

    def component(self) -> 'ComponentBuilder':
        return ComponentBuilder(owner=self)

    def style(self) -> StyleBuilder:
        return StyleBuilder(owner=self)

    def build(self):
        return Module(
            name=self.name,
            path=self.path,
            components=self.components,
            mixins=self.mixins,
            base=self.base,
            styles=self.styles,
            lazy=self.lazy,
            **self.attributes
        )


class ComponentBuilder(ModuleBuilder):

    def __init__(self, owner=None) -> None:
        super().__init__(owner=owner)
        self.lazy = False

    def build(self) -> Component:
        return Component(
            name=self.name,
            path=self.path,
            lazy=self.lazy,
            **self.attributes
        )

    def append(self) -> 'ModuleBuilder':
        component = self.build()
        self.owner.components.append(component)
        logger.info('Add component "%s" to "my-app"' % component.name)
        return super().append()


class PageBuilder(ModuleBuilder):

    def __init__(self, owner=None, route: str = None):
        super().__init__(owner=owner)
        self.route = route
        self.title = None

    def set_route(self, route: str) -> 'PageBuilder':
        self.route = route
        return self

    def set_title(self, title: str) -> 'PageBuilder':
        self.title = title
        return self

    def build(self) -> Page:
        return Page(
            name=self.name,
            title=self.title,
            path=self.path,
            components=self.components,
            mixins=self.mixins,
            styles=self.styles,
            **self.attributes
        )

    def append(self) -> 'ApplicationBuilder':
        page = self.build()
        self.owner.add(
            route=self.route,
            page=page
        )
        logger.info('Add page "%s" as "%s" to "my-app"' % (page.name, self.route))
        return super().append()


class ApplicationBuilder(ComponentBuilder):

    def __init__(self, application: Application = None, owner=None):
        super().__init__(owner=owner)

        self.application = application
        if application is None:
            self.title = None
            self.components = []
            self.pages = dict()
            self.mixins = []
            self.lazy = False
            self.base = ELEMENT_ECMA_CLASS
            self.path = None
            self.styles = []
            print('uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
        else:
            self.title = application.title
            self.name = application.name
            self.components = application.components
            self.pages = application.pages
            self.mixins = application.mixins
            self.lazy = application.lazy
            self.base = application.base
            self.path = application.path
            self.attributes = application.attributes
            self.styles = application.styles
            print('ooooooooooooooooooooooooooooooooooooooooooooooo')

        print('------------------eeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
        print(self.pages)

    def set_title(self, title: str) -> 'ApplicationBuilder':
        self.title = title
        return self

    def component(self, lazy: bool = True) -> ComponentBuilder:
        return ComponentBuilder(owner=self)

    def page(self) -> PageBuilder:
        return PageBuilder(owner=self)

    def add(self, route, page: Page):
        self.pages[route] = page

        return self

    def merge(self, updated_app: Application):
        current_app = self.application
        current_app.components = list(set(current_app.components + updated_app.components))
        current_app.pages = {**current_app.pages, **updated_app.pages}
        current_app.mixins = list(set(current_app.mixins + updated_app.mixins))
        current_app.lazy = updated_app.lazy
        current_app.base = updated_app.base
        current_app.path = updated_app.path
        current_app.title = updated_app.title
        current_app.name = updated_app.name
        current_app.attributes = {**current_app.attributes, **updated_app.attributes}
        current_app.styles = list(set(current_app.styles + updated_app.styles))
        return current_app

    def build(self) -> Application:
        if self.application is None:
            return Application(
                title=self.title,
                name=self.name,
                components=self.components,
                pages=self.pages,
                mixins=self.mixins,
                lazy=self.lazy,
                base=self.base,
                path=self.path,
                styles=self.styles,
                **self.attributes
            )
        else:
            return self.merge(Application(
                title=self.title,
                name=self.name,
                components=self.components,
                pages=self.pages,
                mixins=self.mixins,
                lazy=self.lazy,
                base=self.base,
                path=self.path,
                styles=self.styles,
                **self.attributes
            ))
