from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


def dict_form_html():
    form = '''
    <form action="#" method="POST">
        <label>
            Klucz:
            <input type="text" name="key">
        </label>
        <label>
            Wartość:
            <input type="text" name="value">
        </label>
        <input type="submit" name="convertionType">
    </form>
    '''
    return form


def decor_warp_html(form):
    def wrap_html(*args, **kwargs):
        html = """
            <html>
                <body>
                    {}
                </body>
            </html>""".format(form(*args, **kwargs))
        return HttpResponse(html)
    return wrap_html


@decor_warp_html
@method_decorator(csrf_exempt, name='dispatch')
class ShowAll(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


@decor_warp_html
@method_decorator(csrf_exempt, name='dispatch')
class ShowDetail(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


@decor_warp_html
@method_decorator(csrf_exempt, name='dispatch')
class ModifyPerson(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


@decor_warp_html
@method_decorator(csrf_exempt, name='dispatch')
class AddPerson(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


@decor_warp_html
@method_decorator(csrf_exempt, name='dispatch')
class DeletePerson(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
