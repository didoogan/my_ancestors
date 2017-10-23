from celery import shared_task

from ancestors.models import Ancestor


@shared_task
def update_ancestors(actor_id, acted_id, action):
    """
    When some one create/delete an ancestor, ancestor field of all related
    ancestors should be updated
    :param actor_id: id of some ancestor, who create new ancestor
    :param acted_id: id of created ancestor
    :param action: create or delete
    """
    actor = Ancestor.objects.get(id=actor_id).prefetch_related('ancestors')
    acted = Ancestor.objects.get(id=acted_id).prefetch_related('ancestors')
    actor_ancestors_ids = list(actor.ancestors.all()
                                  .values_list('id', flat=True))
    acted_ancestors_ids = list(acted.ancestors.all()
                               .values_list('id', flat=True))
    all_ids = actor_ancestors_ids + acted_ancestors_ids
    all_ids.append(actor.id)
    all_ids.append(acted.id)
    ancestors = Ancestor.objects.filter(id__in=all_ids)\
        .prefetch_related('ancestors')
    for ancestor in ancestors:
        if action == 'create':
            if ancestor.id != acted.id and \
                            ancestor not in acted.ancestors.all():
                ancestor.ancestors.add(acted)
            if ancestor.id != actor.id and \
                            ancestor not in actor.ancestors.all():
                ancestor.ancestors.add(actor.id)
        elif action == 'delete':
            if ancestor.id != acted.id:
                ancestor.ancestors.remove(acted)
            if ancestor.id != actor.id:
                ancestor.ancestors.remove(actor)

