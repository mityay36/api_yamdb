from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
)
from rest_framework.viewsets import GenericViewSet


class ModelMixinSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    pass


class SignUpMixinSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    pass
