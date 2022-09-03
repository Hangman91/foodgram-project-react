from rest_framework import mixins, viewsets


class ReadListObjectViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin
):
    pass


class ReadListViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class ReadOrCreateViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class CreateOrDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass
