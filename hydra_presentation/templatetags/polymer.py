import logging
import re
import traceback

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from hydra_presentation import polymer

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter
@stringfilter
def camel_case(value: str):
    """Converts a string into CamelCase"""
    try:
        if value[0].islower() and '-' in value:
            result = re.sub('-([A-Za-z])', lambda match: match.group(1).upper(), value[0].upper() + value[1:])
        else:
            # else:
            #     # return re.sub('_([A-Za-z])', lambda match: match.group(1).upper(), value[0].upper() + value[1:])
            #     return re.sub('_([A-Za-z])', lambda match: match.group(1).upper(), value[0].upper() + value[1:])

            result = re.sub('_([A-Za-z])', lambda match: match.group(1).upper(), value[0].upper() + value[1:])

        logger.debug('%s -> %s' % (value, result))
    except BaseException as e:
        logger.warning(str(e))
        traceback.print_exc()
    finally:
        return result


@register.filter
@stringfilter
def polymer_case(value: str):
    """Converts a string into polymer-case"""
    result = value
    try:
        if '-' in value and value[0].islower():  # polymer-case
            result = value.lower()
        elif '_' in value and value[0].islower():  # python_case
            result = re.sub('_([A-Za-z])', lambda match: '-' + match.group(1).lower(),
                            value[0].lower() + value[1:]).lower()
        else:  # CamelCase
            result = re.sub('([A-Z])', lambda match: '-' + match.group(1).lower(), value[0].lower() + value)[2:]

        logger.debug('%s -> %s' % (value, result))
    except BaseException as e:
        logger.warning(str(e))
        traceback.print_exc()
    finally:
        return result


@register.filter
@stringfilter
def lower(value: str):  # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()


@register.filter
@stringfilter
def upper(value: str):  # Only one argument.
    """Converts a string into all uppercase"""
    return value.upper()


@register.filter
def base(module: polymer.Module):
    base_string = module.base
    for mixin in module.mixins:
        base_string = mixin.apply(base=base_string)
    return base_string


@register.simple_tag
def tag(tag: polymer.Tag):
    return mark_safe('<%s %s>%s</%s>' % (
        tag.name,
        ' '.join([(('%s="%s"' % (polymer_case(value=key).lower(), str(value).lower() if isinstance(value, bool) else value)) if value is not None else key) for key, value in tag.attributes.items()]),
        '',
        tag.name
    ))


@register.simple_tag
def link(component: polymer.Component):
    import_attribute = 'lazy-import' if component.lazy else 'import'
    return mark_safe('<link rel="%s" href="%s">' % (
        import_attribute,
        component.path
    ))


@register.inclusion_tag('hydra_presentation/dom_module.html')
def dom_module(module: polymer.Module):
    return dict(
        module=module
    )
