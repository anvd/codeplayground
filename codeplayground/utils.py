# -*- coding: utf-8 -*-
#

# Imports ###########################################################

import logging
import pkg_resources


import time
from django.template import Context, Template

# Globals ###########################################################

log = logging.getLogger(__name__)


# Functions #########################################################


current_milli_time = lambda: int(round(time.time() * 1000))


def load_resource(resource_path):
    """
    Gets the content of a resource
    """
    resource_content = pkg_resources.resource_string(__name__, resource_path)
    return unicode(resource_content.decode("utf8"))


def render_template(template_path, context={}):
    """
    Evaluate a template by resource path, applying the provided context
    """
    template_str = load_resource(template_path)
    template = Template(template_str)
    return template.render(Context(context))

def resource_string(self, path):
    """
    Handy helper for getting resources from our kit.
    """
    data = pkg_resources.resource_string(__name__, path)
    return data.decode("utf8")