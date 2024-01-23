from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import FlowerCategoriesForm, FlowerForm
from django.contrib import messages
from profiles.models import UserProfile
from django.views.generic import UpdateView, ListView, DeleteView, TemplateView
from .models import Flower, OrderHistory, FlowerCategories
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# for sanding email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class CreateFlowerCategoryView(LoginRequiredMixin, View):
    template_name = 'create_flower_category.html'
    form_class = FlowerCategoriesForm
    login_url = 'user_login'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Add Category successfully !!')
            return redirect('homepage')
        return render(request, self.template_name, {'form': form})


class CreateFlowerView(LoginRequiredMixin, View):
    template_name = 'create_flower.html'
    form_class = FlowerForm
    login_url = 'user_login'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            flower = form.save(commit=False)

            user_profile, created = UserProfile.objects.get_or_create(
                user=request.user)

            flower.seller = user_profile
            flower.save()
            messages.success(self.request, 'Add Flower successfully !!')
            return redirect('homepage')
        return render(request, self.template_name, {'form': form})


class OrderDeshbordView(LoginRequiredMixin, ListView):
    template_name = 'order_deshbord.html'
    context_object_name = 'orders'
    model = OrderHistory
    login_url = 'user_login'


def OrderConfirmView(request, order_id):
    if request.method == 'POST':
        order = OrderHistory.objects.get(pk=order_id)
        order.status = 'Completed'

        order.save()

        email_subject = 'Order Confirmation Email'
        email_body = render_to_string(
            'order_confirm_email.html', {'user': order.user})

        email = EmailMultiAlternatives(

            email_subject, '', to=[order.user.user.user_profile.user.email])
        email.attach_alternative(email_body, 'text/html')
        email.send()

        return redirect('order_deshbord')


class CategoryPageView(ListView):
    template_name = 'category_page_view.html'
    model = Flower
    context_object_name = 'flowers'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Flower.objects.filter(category=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        category = FlowerCategories.objects.get(id=category_id)
        context['selected_category'] = category
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


class AboutPageView(TemplateView):
    template_name = 'about_us.html'

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


@login_required(login_url='user_login')
def AddOrder(request, flower_id):

    order_flower = get_object_or_404(Flower, id=flower_id)
    order_user = request.user.user_profile

    if order_flower.available_quantity > 0:
        order = OrderHistory(
            user=order_user,
            flower=order_flower,
            quantity=1,
            total_price=order_flower.price
        )

        order.save()

        order_flower.available_quantity -= 1
        order_flower.save()
        email_subject = 'Customer Placing Order'
        email_body = render_to_string(
            'order_send_email.html', {'user': request.user})
        email = EmailMultiAlternatives(
            email_subject, '', to=[request.user.email])
        email.attach_alternative(email_body, 'text/html')
        email.send()
        messages.success(request, 'Order placed successfully!')

    else:
        messages.error(
            request, 'Not enough available quantity for this flower.')

    return redirect('homepage')


class CartView(LoginRequiredMixin, ListView):
    template_name = 'cart.html'
    model = OrderHistory
    context_object_name = 'orders'
    login_url = 'user_login'

    def get_queryset(self):
        user_profile = self.request.user.user_profile

        if user_profile.is_admin:
            return OrderHistory.objects.none()
        else:

            return OrderHistory.objects.filter(user=user_profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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


class UpdateFlowerView(LoginRequiredMixin, UpdateView):
    template_name = 'update_flower.html'
    model = Flower
    form_class = FlowerForm
    login_url = 'user_login'

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Flower Update Successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('homepage')


class FlowerDeshbordView(LoginRequiredMixin, ListView):
    template_name = 'flower_deshbord.html'
    model = Flower
    context_object_name = 'flowers'
    login_url = 'user_login'


class DeleteFlowerView(LoginRequiredMixin, DeleteView):
    model = Flower
    template_name = 'delete_confirmation.html'
    login_url = 'user_login'

    def get_success_url(self):
        messages.success(self.request, 'Flower Delete Successfully !!')
        return reverse_lazy('flower_deshbord_view')


@login_required(login_url='user_login')
def RemoveOrderToCart(request, order_id):
    order = get_object_or_404(OrderHistory, pk=order_id)

    if request.method == 'POST':
        flower = order.flower
        flower.available_quantity += 1
        flower.save()

        order.delete()

        messages.success(request, 'Order removed successfully.')
        return redirect('cart_view')
