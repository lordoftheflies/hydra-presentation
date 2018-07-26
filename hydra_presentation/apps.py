import json
import logging
import traceback

from django.apps import AppConfig

from hydra_presentation import polymer

logger = logging.getLogger(__name__)


class PresentationAppConfig(AppConfig):
    APP_NAME = 'my-app'
    APP_TITLE = 'My application'
    APP_PATH = 'src/my-application.html'
    APP_BASE = 'Polymer.Element'
    application = polymer.ApplicationBuilder().set_name(APP_NAME).set_title(APP_TITLE).set_path(APP_PATH).set_base(
        'Polymer.Element').build()

    def render(self, builder: polymer.ApplicationBuilder) -> polymer.ApplicationBuilder:
        return builder.set_name('my-app').set_title('My application').set_path('src/my-app.html') \
            .set_base('Polymer.Element') \
            .style().set_path('src/shared-styles.html').set_name('shared-styles').append() \
            .mixin().set_namespace('Plutonium').set_name('NavigationHostMixin').append() \
            .mixin().set_namespace('Plutonium').set_name('SecurityMixin').append() \
            .mixin().set_namespace('Plutonium').set_name('NotificationConsumerMixin').append() \
            .page().set_name('my-profile').set_route('profile').set_title('Profil').set_path(
            'src/my-profile-view.html').append() \
            .component().set_name('my-application-selector').set_path('my-application-selector.html').append()

    def ready(self):
        try:
            super().ready()
            logger.info('Initialize presentation layer ...')
            self.application = self.render(
                builder=polymer.ApplicationBuilder(application=self.application)
            ).build()

            logger.debug('---------------------')
            logger.debug('Polymer configuration')
            logger.debug('---------------------')
            logger.debug(self.application.to_json())
            logger.debug('---------------------')
        except BaseException as e:
            logger.warning(str(e))
            traceback.print_exc()


class HydraPresentationConfig(PresentationAppConfig):
    name = 'hydra_presentation'

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
