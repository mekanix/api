from flask_restplus import abort
from mongoengine.errors import ValidationError

from ..models import Service
from .fields.cluster_service import post_fields
from .fields.service import get_fields
from .mixins import ClusterMixin
from .namespaces import ns_cluster
from .resources import ProtectedResource


parser = ns_cluster.parser()
parser.add_argument('service_id', type=str, required=True, location='json')


@ns_cluster.route(
    '/<cluster_id>/services',
    endpoint='clusters_cluster_services',
)
class ClusterServiceListAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(get_fields)
    def get(self, cluster_id):
        """List cluster services"""
        cluster = self._find_cluster(cluster_id)
        return cluster.services

    @ns_cluster.doc(body=post_fields)
    @ns_cluster.marshal_with(get_fields)
    @ns_cluster.response(409, 'Service already exist')
    def post(self, cluster_id):
        """Create cluster service"""
        args = parser.parse_args()
        cluster = self._find_cluster(cluster_id)
        service_id = args.get('service_id')
        for service in cluster.services:
            if str(service.id) == service_id:
                abort(
                    409,
                    'Service %s is already part of cluster %s' % (
                        service_id,
                        cluster.name,
                    )
                )

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            abort(404, 'No such service')
        except ValidationError as e:
            abort(409, e.message)

        cluster.services.append(service)
        cluster.save()
        return service


@ns_cluster.route(
    '/<cluster_id>/services/<service_id>',
    endpoint='clusters_cluster_service',
)
class ClusterServiceAPI(ProtectedResource, ClusterMixin):
    @ns_cluster.marshal_with(get_fields)
    @ns_cluster.response(404, 'Service not found')
    @ns_cluster.expect(get_fields)
    def delete(self, cluster_id, service_id):
        """Delete service"""
        cluster = self._find_cluster(cluster_id)
        for service in cluster.services:
            if str(service.id) == service_id:
                cluster.services.remove(service)
                cluster.save()
                return service
        abort(404, 'Service %s not found' % service_id)
        return service
