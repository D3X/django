import django

from django.test import TestCase

from .models import MyModel


class Mytest(TestCase):
    def setUp(self):
        MyModel.objects.create(id=1, x=5)

    def test_queryset(self):
        '''
        This one does not work on Django 2.

        The query qenerated on 1.11.8:

        SELECT "mytest_mymodel"."id", "mytest_mymodel"."x", "mytest_mymodel"."parent_id"
        FROM "mytest_mymodel"
        WHERE "mytest_mymodel"."x" = (SELECT U0."x" AS Col1 FROM "mytest_mymodel" U0 LIMIT 1)

        On 2.0:

        SELECT "mytest_mymodel"."id", "mytest_mymodel"."x", "mytest_mymodel"."parent_id"
        FROM "mytest_mymodel"
        WHERE "mytest_mymodel"."x" = (SELECT U0."id" FROM "mytest_mymodel" U0  LIMIT 1)
        '''
        qs = MyModel.objects.filter(
            x=MyModel.objects.values('x')[:1]
        )

        assert qs.exists()
        assert qs.first().x == 5

    def test_queryset_with_in(self):
        '''
        This one works fine on both 1.11 and 2.0.
        '''
        qs = MyModel.objects.filter(
            x__in=MyModel.objects.values('x')
        )

        assert qs.exists()
        assert qs.first().x == 5
