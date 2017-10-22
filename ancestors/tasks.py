from celery import shared_task

from ancestors.models import Ancestor


@shared_task
def update_ancestors(actor_id, acted_id, action):
    actor = Ancestor.objects.get(id=actor_id)
    acted = Ancestor.objects.get(id=acted_id)
    ancestors_ids = list(actor.ancestors.all().values_list('id', flat=True))
    ancestors_ids.append(actor.id)
    ancestors = Ancestor.objects.filter(id__in=ancestors_ids)\
        .prefetch_related('ancestors')
    for ancestor in ancestors:
        if action == 'create':
            ancestor.ancestors.add(acted)
        elif action == 'delete':
            ancestor.ancestors.remove(acted)

