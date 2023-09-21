from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class LoginUserForm(AuthenticationForm):
	captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
