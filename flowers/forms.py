from django import forms
from .models import FlowerCategories, Flower


class FlowerCategoriesForm(forms.ModelForm):
    class Meta:
        model = FlowerCategories
        fields = ['category_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control bg-light text-dark border rounded py-3 px-4 focus:outline-none focus:bg-white focus:border-secondary w-full',
            })


class FlowerForm(forms.ModelForm):
    class Meta:
        model = Flower
        fields = ['title', 'category', 'description',
                  'price', 'available_quantity', 'image_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control bg-light text-dark border rounded py-3 px-4 focus:outline-none focus:bg-white focus:border-secondary w-full',
            })
