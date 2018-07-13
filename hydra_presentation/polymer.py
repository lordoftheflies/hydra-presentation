class Tag:
    """
    Simple presentation tag
    """

    def __init__(self, name: str, **kwargs) -> None:
        self.name = name
        self.attributes = kwargs


class Component(Tag):
    FILENAME_TEMPLATE = '%s.html'

    def __init__(self, name: str, path: str = None, lazy: bool = False, **kwargs) -> None:
        super().__init__(name=name, path=path, **kwargs)
        self.path = path if path is not None else (self.FILENAME_TEMPLATE % self.name)
        self.lazy = lazy

    def __str__(self):
        return '<%s %s>%s</%s>' % (
            self.name,
            ' '.join([(('%s=%s' % (key, value)) if value is not None else key) for key, value in self.attributes]),
            '',
            self.name
        )


class Mixin:

    def __init__(self, namespace: str, name):
        self.namespace = namespace
        self.name = name

    def apply(self, base):
        return '%s.%s(%s)' % (
            self.namespace,
            self.name,
            base
        )


class Module(Component):

    def __init__(self, name: str, path: str, components: list = [], mixins=[], base='Polymer.Element',
                 **kwargs) -> None:
        super().__init__(name=name, path=path, **kwargs)
        self.components = components
        self.mixins = mixins
        self.base = base


class Page(Module):
    TOKEN_SEPARATOR = '-'

    def __init__(self, name: str, path: str, title: str = None, components: list = [], **kwargs) -> None:
        super().__init__(name=name, path=path, components=components, **kwargs)
        self.title = title
        self.components = components

    @property
    def route(self):
        return self.TOKEN_SEPARATOR.join(self.name.split(self.TOKEN_SEPARATOR)[1:])


class Application(Module):

    def __init__(self, name: str, path: str, title: str = None, components: list = [], pages: list = [],
                 **kwargs) -> None:
        super().__init__(name=name, path=path, components=components, **kwargs)
        self.title = title
        self.pages = pages


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

    def set_name(self, name: str) -> 'MixinBuilder':
        self.name = name
        return self

    def set_namespace(self, namespace: str) -> 'MixinBuilder':
        self.namespace = namespace
        return self

    def build(self):
        return Mixin(
            name=self.name,
            namespace=self.namespace
        )

    def append(self):
        self.owner.mixins.append(self.build())
        return super().append()


class ModuleBuilder(TagBuilder):

    def __init__(self, owner=None) -> None:
        super().__init__(owner=owner)
        self.path = None
        self.components = []
        self.mixins = []
        self.base = 'Polymer.Element'

    def set_path(self, path: str) -> 'ModuleBuilder':
        self.path = path
        return self

    def set_base(self, base: str) -> 'ModuleBuilder':
        self.base = base
        return self

    def mixin(self) -> MixinBuilder:
        return MixinBuilder(owner=self)

    def build(self):
        return Module(
            name=self.name,
            path=self.path,
            components=self.components,
            mixins=self.mixins,
            base=self.base,
            **self.attributes
        )


class ComponentBuilder(ModuleBuilder):

    def __init__(self, owner: 'ApplicationBuilder') -> None:
        super().__init__(owner=owner)
        self.lazy = False

    def build(self) -> Component:
        return Component(
            name=self.name,
            path=self.path,
            lazy=self.lazy,
            **self.attributes
        )

    def append(self) -> 'ApplicationBuilder':
        self.owner.components.append(self.build())
        return super().append()


class PageBuilder(ModuleBuilder):

    def __init__(self, owner: 'ApplicationBuilder', route: str = None):
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
            mixins=self.mixins
        )

    def append(self) -> 'ApplicationBuilder':
        self.owner.add(
            route=self.route,
            page=self.build()
        )
        return super().append()


class ApplicationBuilder(ComponentBuilder):

    def __init__(self, owner=None):
        super().__init__(owner=owner)

        self.title = None
        self.name = None
        self.components = []
        self.pages = dict()

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

    def build(self) -> Application:
        return Application(
            name=self.name,
            title=self.title,
            path=self.path
        )
