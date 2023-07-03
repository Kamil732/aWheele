from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .models import (
    Car,
    ImageCar,
    Part,
    ImagePart,
    Motorcycle,
    ImageMotorcycle,
    CURRENCY,
    YEAR_PRODUCTION,
    MARK,
    FUEL_TYPE,
    GEARBOX,
    CAR_TYPE,
    MOTORCYCLE_TYPE,
    COLOR,
    COLOR_OPTION,
    CONDITION,
    PART_TYPE,
    DRIVE,
)
from cities_light.models import City
from cities_light.loading import CITIES

class EmptyChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), empty_label=None, required=True, widget=None, label=None, initial=None, help_text=None, *args, **kwargs):

        # prepend an empty label if it exists (and field is not required!)
        if empty_label is not None:
            choices = tuple([(u'', empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(choices=choices, required=required, widget=widget, label=label, initial=initial, help_text=help_text, *args, **kwargs)

class SelectWOA(forms.Select):
    """
    Select With Option Attributes:
        subclass of Django's Select widget that allows attributes in options,
        like disabled="disabled", title="help text", class="some classes",
              style="background: color;"...

    Pass a dict instead of a string for its label:
        choices = [ ('value_1', 'label_1'),
                    ...
                    ('value_k', {'label': 'label_k', 'foo': 'bar', ...}),
                    ... ]
    The option k will be rendered as:
        <option value="value_k" foo="bar" ...>label_k</option>
    """

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        if isinstance(label, dict):
            opt_attrs = label.copy()
            label = opt_attrs.pop('label')
        else:
            opt_attrs = {}
        option_dict = super(SelectWOA, self).create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        for key, val in opt_attrs.items():
            option_dict['attrs'][key] = val
        return option_dict

class SendEmailForm(forms.Form):
    email = forms.EmailField(
        label = 'Email',
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    phonenumber = PhoneNumberField(
        required = False,
        help_text = 'OPTIONAL',
        label = 'Phonenumber',
        widget = PhoneNumberInternationalFallbackWidget(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    message = forms.CharField(
        label = 'Message',
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
            }
        )
    )

class CreateProductForm(forms.ModelForm):
    condition = forms.ChoiceField(
        choices = CONDITION,
        widget = forms.RadioSelect(
            attrs = {
                'class': 'custom-control-input',
            }
        )
    )

    mark = EmptyChoiceField(
        choices = MARK,
        empty_label = {'label': 'Choose...', 'hidden': 'true'},
        widget = SelectWOA(
            attrs = {
                'class': 'form-control close-with-x average-price-required',
            }
        ),
    )

    price = forms.IntegerField(
        min_value = 400,
        max_value = 9999999999999,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control shadow-sm',
            }
        ),
    )

    price_netto = forms.BooleanField(
        label_suffix = '(+23% VAT)',
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class': 'custom-control-input',
            }
        )
    )

    currency = forms.ChoiceField(
        choices = CURRENCY,
        widget = forms.Select(
            attrs = {
                'class': 'form-control rounded-0 shadow-sm',
            }
        )
    )

    to_negotiate = forms.BooleanField(
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class': 'custom-control-input',
            }
        )
    )

    title = forms.CharField(
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control shadow-sm',
            }
        )
    )

    first_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    phonenumber = PhoneNumberField(
        widget = PhoneNumberInternationalFallbackWidget(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    city = EmptyChoiceField(
        choices = CITIES,
        empty_label = {'label': '', 'hidden': 'true'},
        widget = SelectWOA(
            attrs = {
                'class': 'form-control close-with-x',
            }
        ),
    )

    youtube_link = forms.URLField(
        required = False,
        widget = forms.URLInput(
            attrs = {
                'class': 'form-control shadow-sm',
            }
        )
    )

    description = forms.CharField(
        required = False,
        widget = forms.Textarea(
            attrs = {
                'rows': 6,
                'class': 'form-control',
            }
        )
    )

    warranty = forms.DateField(
        required = False,
        widget = forms.DateInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

    class Meta:
        exclude = (
            'delete_at',
            'raise_list_times',
            'colorful_list_days',
            'promo_days',
            'slug',
            'views',
            'phonenumber_views',
            'pub_date',
            'seller',
        )

    def clean_city(self):
        city = self.cleaned_data.get('city')
        city = City.objects.get(slug=city)

        return city

class CreateVehicalForm(CreateProductForm):
    first_owner = forms.BooleanField(
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class': 'custom-control-input',
            }
        )
    )

    year_production = EmptyChoiceField(
        choices = YEAR_PRODUCTION,
        empty_label = {'label': 'Choose...', 'hidden': 'true'},
        widget = SelectWOA(
            attrs = {
                'class': 'form-control close-with-x average-price-required',
            }
        ),
    )

    power = forms.IntegerField(
        min_value = 0,
        max_value = 500,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control valid-number-field-from average-price-required',
            }
        ),
    )

    gearbox = EmptyChoiceField(
        choices = GEARBOX,
        empty_label = {'label': 'Choose...', 'hidden': 'true'},
        widget = SelectWOA(
            attrs = {
                'class': 'form-control close-with-x average-price-required',
            }
        ),
    )

    mileage = forms.IntegerField(
        min_value = 0,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control valid-number-field-from average-price-required',
            }
        ),
    )

    color = EmptyChoiceField(
        choices = COLOR,
        empty_label = {'label': 'Choose...', 'class': 'text-muted', 'hidden': 'true'},
        widget = SelectWOA(
            attrs = {
                'class': 'form-control close-with-x shadow-sm',
            }
        ),
    )

    color_option = EmptyChoiceField(
        choices = COLOR_OPTION,
        empty_label = {'label': 'Choose...', 'class': 'text-muted', 'hidden': 'true'},
        widget = SelectWOA(
            attrs = {
                'class': 'form-control close-with-x shadow-sm',
            }
        ),
    )

    co2_emission = forms.IntegerField(
        required = False,
        min_value = 0,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control valid-number-field-from'
            }
        )
    )

    particulate_filter = forms.BooleanField(
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class': 'custom-control-input',
            }
        )
    )

    first_registeration = forms.DateField(
        required = False,
        widget = forms.DateInput(
            attrs = {
                'class': 'form-control',
            }
        )
    )

class CreateCarForm(CreateVehicalForm):
    right_hand_drive = forms.BooleanField(
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class': 'custom-control-input',
            }
        )
    )

    fuel_type = EmptyChoiceField(
        choices = FUEL_TYPE,
        empty_label = {'label': 'Choose...', 'hidden': 'true'},
        widget = SelectWOA(
            attrs = {
                'class': 'form-control close-with-x average-price-required',
            }
        ),
    )

    num_of_doors = forms.IntegerField(
        min_value = 2,
        max_value = 8,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control average-price-required',
            }
        ),
    )

    num_of_seats = forms.IntegerField(
        min_value = 0,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control valid-number-field-from',
            }
        ),
    )

    car_type = EmptyChoiceField(
        choices = CAR_TYPE,
        empty_label = {'label': 'Choose...', 'hidden': 'true'},
        widget = SelectWOA(
            attrs = {
                'class': 'form-control close-with-x',
            }
        ),
    )

    drive = EmptyChoiceField(
        choices = DRIVE,
        empty_label = {'label': 'Choose...', 'hidden': 'true'},
        widget = SelectWOA(
            attrs = {
                'class': 'form-control close-with-x',
            }
        ),
    )

    class Meta(CreateProductForm.Meta):
        model = Car

class CreatePartForm(CreateProductForm):
    price = forms.IntegerField(
        min_value = 1,
        max_value = 999999,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control shadow-sm',
            }
        ),
    )

    part_type = EmptyChoiceField(
        choices = PART_TYPE,
        empty_label = {'label': 'Choose...', 'hidden': 'true'},
        widget = SelectWOA(
            attrs = {
                'class': 'form-control close-with-x',
            }
        )
    )

    delivery = forms.BooleanField(
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class': 'custom-control-input',
            }
        )
    )

    class Meta(CreateProductForm.Meta):
        model = Part

class CreateMotorcycleForm(CreateVehicalForm):
    motorcycle_type = EmptyChoiceField(
        choices = MOTORCYCLE_TYPE,
        empty_label = {'label': 'Choose...', 'hidden': 'true'},
        widget = SelectWOA(
            attrs = {
                'class': 'form-control close-with-x shadow-sm',
            }
        ),
    )

    class Meta(CreateProductForm.Meta):
        model = Motorcycle

# ImageCarFormset = forms.inlineformset_factory(
#     Car,
#     ImageCar,
#     fields = ('image',),
#     extra = 10,
#     can_delete = False,
#     widgets = {
#         'image': forms.FileInput(
#             attrs = {
#                 'class': 'xd',
#             }
#         )
#     }
# )
