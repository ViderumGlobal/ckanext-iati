from ckan.lib.base import render, BaseController
from ckan.common import c
import ckan.logic as logic
import ckan.model as model
import ckan.plugins as p

from ckan.controllers.organization import OrganizationController

import logging
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

class PublisherController(OrganizationController):

    def _guess_group_type(self, expecting_name=False):
        return 'organization'

    def members_read(self, id):
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}

        try:
            c.members = logic.get_action('member_list')(
                context, {'id': id, 'object_type': 'user'}
            )
            c.group_dict = logic.get_action('organization_show')(context, {'id': id})
        except logic.NotAuthorized:
            p.toolkit.abort(401, p.toolkit._('Unauthorized to read group members %s') % '')
        except logic.NotFound:
            p.toolkit.abort(404, p.toolkit._('Group not found'))
        return render('organization/members_read.html')

    def dashboard_pending_organizations(self):
        return render('user/dashboard_pending_organizations.html')

    def index(self):
        log.error('in the publisher controller')
        log.error(self._guess_group_type())
        return OrganizationController.index(self)
