import decimal
import datetime

from django import forms
from django.contrib.auth.models import User

class ExpenseAddForm(forms.Form):
    name = forms.CharField(max_length=64)
    amount = forms.DecimalField(max_digits=14, decimal_places=2)
    date = forms.DateField(('%m/%d/%Y',),
	widget=forms.DateTimeInput(format='%m/%d/%Y', attrs={
	    'class': 'input',
	    'size': '15',
	})
    )

    def clean(self):
	super(ExpenseAddForm, self).clean()
	data = self.cleaned_data
	date = data['date']
	today = datetime.date.today()
	if date > today:
	    raise forms.ValidationError("This date is in the future.")
	return data

    def process(self, uid, account_id):
	data = self.cleaned_data
	user = User.objects.get(id=uid)
	profile = user.get_profile()

	date = data['date']
	name = data['name']
	amount = data['amount']
	account = profile.accounts.get(id=account_id)

	account.add_debit(date=date, name=name, amount=amount)
