import pagination

from flask_jwt import current_identity
from flask_restplus import abort
from mongoengine.queryset import NotUniqueError

from .fields.service import fields, get_fields
from .mixins import ServiceMixin
from .namespaces import ns_service
from .resources import ProtectedResource

from ..models import Service
from ..utils import check_fields, all_fields_optional


parser = ns_service.parser()
parser.add_argument('name', type=str, required=True, location='json')


@ns_service.route('', endpoint='services')
class ServiceListAPI(ProtectedResource):
    @ns_service.marshal_with(get_fields)
    @ns_service.doc(parser=pagination.parser)
    def get(self):
        """List services"""
        page, per_page = pagination.pages()

        services = Service.objects().paginate(page, per_page)
        paging = pagination.Pagination(services)
        return services.items, 200, paging.headers

    @ns_service.doc(body=fields)
    @ns_service.marshal_with(get_fields)
    @ns_service.response(409, 'Service with that name already exists')
    def post(self):
        """Create service"""
        args = parser.parse_args()
        check_fields(args)
        name = args.get('name')
        service = Service(name=name, user=current_identity.pk)
        try:
            service.save()
        except NotUniqueError:
            abort(409, error='Service with that name already exists')
        return service, 201


@ns_service.route('/<id>', endpoint='services_service')
@ns_service.response(404, 'Service not found')
class ServiceAPI(ProtectedResource, ServiceMixin):
    @ns_service.marshal_with(get_fields)
    def get(self, id):
        """Show service details"""
        service = self._find_service(id)
        return service

    @ns_service.expect(fields)
    @ns_service.marshal_with(get_fields)
    def patch(self, id):
        """Update service"""
        service = self._find_service(id)
        patch_parser = all_fields_optional(parser)
        args = patch_parser.parse_args()
        service.name = args.get('name') or service.name
        service.save()
        return service

    @ns_service.marshal_with(get_fields)
    def delete(self, id):
        """Delete the service."""
        service = self._find_service(id)
        service.delete()
        return service
