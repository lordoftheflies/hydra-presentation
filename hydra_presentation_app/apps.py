from django.apps import AppConfig

from hydra_presentation import polymer
from hydra_presentation.apps import PresentationAppConfig


class HydraPresentationAppConfig(PresentationAppConfig):
    name = 'hydra_presentation_app'

    def render(self, builder: polymer.ApplicationBuilder) -> polymer.ApplicationBuilder:
        return builder.set_name('my-app').set_title('My custom application').set_path('src/my-app.html') \
            .set_base('Polymer.Element') \
            .style().set_path('src/shared-styles.html').set_name('shared-styles').append() \
            .mixin().set_namespace('Hydra').set_name('StaticMixin').append() \
            .page().set_name('my-page-static').set_route('page-static').set_title('Statikus oldal').set_path(
            'src/my-page-static.html').append() \
            .page().set_name('my-page-dynamic').set_route('page-dynamic').set_title('Dinamikus oldal').set_path(
            'src/my-page-dynamic.html').append() \
            .component().set_name('my-component-static').set_path('src/my-component-static.html').append() \
            .component().set_name('my-component-dynamic').set_path('src/my-component-dynamic.html').append() \
