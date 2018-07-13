from django.apps import AppConfig

from hydra_presentation import polymer


class HydraPresentationConfig(AppConfig):
    name = 'hydra_presentation'

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.application = None

    def render(self, builder: polymer.ApplicationBuilder) -> polymer.ApplicationBuilder:
        return builder.set_name('my-app').set_title('My application').set_path('src/my-application.html')\
            .set_base('Polymer.Element') \
            .mixin().set_namespace('Plutonium').set_name('NavigationHostMixin').append() \
            .mixin().set_namespace('Plutonium').set_name('SecurityMixin').append() \
            .mixin().set_namespace('Plutonium').set_name('NotificationConsumerMixin').append() \
            .mixin().set_namespace('Polymer').set_name('Element').append() \
            .page().set_name('my-profile').set_route('profile').set_title('Profil').set_path('src/my-profile-view.html').append() \
            .component().set_name('my-application-selector').set_path('my-application-selector.html').append() \
            .page().append()

    def ready(self):
        super().ready()
        self.application = self.render(
            builder=polymer.ApplicationBuilder()
        ).build()
