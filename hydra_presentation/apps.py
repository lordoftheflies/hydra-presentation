import json
import logging
import traceback

from django.apps import AppConfig
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse

from hydra_presentation import polymer

logger = logging.getLogger(__name__)


class PresentationAppConfig(AppConfig):
    APP_NAME = 'my-app'
    APP_TITLE = 'My application'
    APP_PATH = 'src/my-app.html'
    APP_BASE = polymer.ELEMENT_ECMA_CLASS

    application_instance = None

    @property
    def application(self):
        return PresentationAppConfig.application_instance

    def render(self, builder: polymer.ApplicationBuilder) -> polymer.ApplicationBuilder:
        return builder \
            .set_name(self.APP_NAME) \
            .set_title(self.APP_TITLE) \
            .set_path(self.APP_PATH) \
            .set_base(self.APP_BASE) \
            .set_attribute(name='application-index-endpoint-url', value=reverse('application_index')) \
            .style() \
            .set_path(static('src/shared-styles.html')) \
            .set_name('shared-styles') \
            .append() \
            .mixin() \
            .set_namespace('Plutonium') \
            .set_name('NavigationHostMixin') \
            .set_path(static('src/plutonium-navigation-mixin.html')) \
            .append() \
            .mixin() \
            .set_namespace('Plutonium') \
            .set_name('SecurityMixin') \
            .set_path(static('src/plutonium-security-mixin.html')) \
            .append() \
            .mixin() \
            .set_namespace('Plutonium') \
            .set_name('NotificationConsumerMixin') \
            .set_path(static('src/plutonium-notification-mixin.html')) \
            .append() \
            .page() \
            .set_name('my-profile') \
            .set_route('profile') \
            .set_title('Profil') \
            .set_path(static('src/my-profile-view.html')) \
            .append() \
            .component() \
            .set_name('plutonium-application-selector') \
            .set_path(static('src/plutonium-application-selector.html')) \
            .append() \
            .page() \
            .set_route('view404') \
            .set_name('my-view404') \
            .set_path(static('src/my-view404.html')) \
            .append() \
            .page() \
            .set_route('view1') \
            .set_name('my-view1') \
            .set_path(static('src/my-view1.html')) \
            .append() \
            .page() \
            .set_route('view2') \
            .set_name('my-view2') \
            .set_path(static('src/my-view2.html')) \
            .append() \
            .page() \
            .set_route('view3') \
            .set_name('my-view3') \
            .set_path(static('src/my-view3.html')) \
            .append() \
            .page() \
            .set_route('components-demo') \
            .set_name('my-components-demo') \
            .set_path(static('src/my-components-demo.html')) \
            .append()

    def ready(self):
        super().ready()

        # self.application = polymer.ApplicationBuilder().set_name(self.APP_NAME).set_title(self.APP_TITLE).set_path(
        #     self.APP_PATH).set_base(self.APP_BASE).build()

        try:
            logger.info('Initialize presentation layer ...')
            if PresentationAppConfig.application_instance is None:
                PresentationAppConfig.application_instance = self.render(builder=polymer.ApplicationBuilder()).build()
            else:
                PresentationAppConfig.application_instance = self.render(builder=polymer.ApplicationBuilder(application=PresentationAppConfig.application_instance)).build()

            logger.debug('------------------------------------------------------------------------------------------')
            logger.debug('Polymer configuration')
            logger.debug('------------------------------------------------------------------------------------------')
            logger.debug(PresentationAppConfig.application_instance.to_json())
            logger.debug('\n------------------------------------------------------------------------------------------')

        except BaseException as e:
            logger.warning(str(e))
            traceback.print_exc()


class HydraPresentationConfig(PresentationAppConfig):
    name = 'hydra_presentation'

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
