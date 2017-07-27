from django.db.models import OuterRef, Count, Subquery, Value, F, When, DecimalField, Case
from django.db.models.functions import Coalesce
from django.shortcuts import render

from .models import Book, Rental


def myview(request):
    rentals = Rental.objects.filter(book=OuterRef('pk'))
    cat_rentals = Rental.objects.filter(book__category=OuterRef('category'))
    count_rentals = rentals.annotate(numrent=Count('*')).values('numrent')
    count_cat_rentals = cat_rentals.annotate(numcatrent=Count('*', distinct=True)).values('numcatrent')

    candidates = Book.objects.annotate(
        rentals=Coalesce(Subquery(count_rentals), Value(0)),
        catrentals=Coalesce(Subquery(count_cat_rentals), Value(0)),
    ).annotate(
        success_rate=Case(
            When(rentals__lt=1, then=Value('0')),
            default=(F('rentals') / F('catrentals')),
            output_field=DecimalField()
        ))
    return render(request, 'myview.html', {'candidates': candidates})
