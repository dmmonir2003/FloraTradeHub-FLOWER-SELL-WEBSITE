from django.shortcuts import render
from django.views.generic import ListView
from flowers.models import Flower, OrderHistory, FlowerCategories
from django.db.models import Sum
# Create your views here.


class HomePage(ListView):
    template_name = 'index.html'
    model = Flower
    context_object_name = 'flowers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FlowerCategories.objects.all()
        context['all_flowers'] = Flower.objects.all()
        if self.request.user.is_authenticated:
            order_user = self.request.user.user_profile

            total_quantity = OrderHistory.objects.filter(user=order_user).aggregate(
                Sum('quantity'))['quantity__sum'] or 0

            previous_orders_total_price = OrderHistory.objects.filter(
                user=order_user).aggregate(Sum('total_price'))['total_price__sum'] or 0

            context["total_quantity"] = total_quantity
            context["previous_orders_total_price"] = previous_orders_total_price
        else:

            context["total_quantity"] = 0
            context["previous_orders_total_price"] = 0
        return context


# class CategorySearch(ListView):
#     model = Flower
#     template_name = 'index.html'
#     context_object_name = 'flowers'

#     def get_queryset(self):
#         category_id = self.kwargs['category_id']
#         return Flower.objects.filter(category=category_id)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = FlowerCategories.objects.all()
#         context['all_flowers'] = Flower.objects.all()

#         if self.request.user.is_authenticated:
#             order_user = self.request.user.user_profile

#             total_quantity = OrderHistory.objects.filter(user=order_user).aggregate(
#                 Sum('quantity'))['quantity__sum'] or 0

#             previous_orders_total_price = OrderHistory.objects.filter(
#                 user=order_user).aggregate(Sum('total_price'))['total_price__sum'] or 0

#             context["total_quantity"] = total_quantity
#             context["previous_orders_total_price"] = previous_orders_total_price
#         else:

#             context["total_quantity"] = 0
#             context["previous_orders_total_price"] = 0
#         return context


def sand_categories_navber(request):
    categories = FlowerCategories.objects.all()

    return render(request, 'navber.html', {'categories': categories})
