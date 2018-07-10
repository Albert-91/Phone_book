from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from phone_book.models import Person, Email, Phone, Address, Groups
form_start = """<html><body><form action='#' method='POST'>"""
form_name = """
    <label> Name:
        <input name='name' size='10' value={}>
    </label><br><br>
    <label> Surname:
        <input name='surname' size='10' value={}>
    </label><br><br>
    <label> Description:
        <input name='description' size = '50' placeholder='Describe here' value="{}"></input>
    </label><br><br>"""

form_phone = """
    <label>Phone number:
        <input name='phone_number' size='15' value={}>
    </label>
    <label>Phone type:
        <select name="phone_type" value={}>
            <option value=1>Home</option>
            <option value=2>Business</option>
            <option value=3>Mobile</option>
        </select>
    </label><br><br>"""
form_email = """
    <label>E-mail address:
        <input name='email' size='20' value={}>
    </label>
    <label>Phone type:
        <select name="email_type">
            <option value=1>Home</option>
            <option value=2>Business</option>
        </select>
    </label><br><br>"""
form_address = """
    <label>Street:
        <input name='street' size='15' value={}>
    </label>
    <label>House number:
        <input name='house_number' size='5' value={}>
    </label>
    <label>Apartment number:
        <input name='apartment_number' size='5' value={}>
    </label>
    <label>City:
        <input name='city' size='15' value={}>
    </label><br><br>
"""
form_group = """
    <label>Group:
        <input name='group' size='15' value={}>
    </label>
"""
form_end = "<input type='submit' value='Dodaj'></form>"


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


@method_decorator(csrf_exempt, name='dispatch')
class ShowAll(View):
    @decor_warp_html
    def get(self, request):
        table = """
            <table border=1>
                <tr>
                    <td align="center">Surname and name</td>
                    <td align="center">Options</td>
                </tr>
            """
        persons = Person.objects.order_by('surname')
        for person in persons:
            table += """
                <tr>
                    <td align="center"><a href='/person/{0}' style="color:black">{1} {2}</a></td>
                    <td align="center"><a href='/delete/{0}' style="color:red">delete</a>
                        <a href='/modify/{0}' style="color:green"> modify</a></td>
                </tr>
                """.format(person.id, person.surname, person.name)
        table += "</table><br>"
        table += """<form><button formaction="/new/">Add new person</button>"""
        table += """<button formaction="/groups/">Show all groups</button></form>"""
        return table


@method_decorator(csrf_exempt, name='dispatch')
class ShowDetail(View):
    @decor_warp_html
    def get(self, request, id):
        person = Person.objects.get(id=id)
        table = """
            <table border=1>
                <tr>
                    <td></td>
                    <td align="center">Data</td>
                </tr>
                <tr>
                    <td>Name</td>
                    <td>{}</td>
                </tr>
                <tr>
                    <td>Surname</td>
                    <td>{}</td>
                </tr>
                <tr>
                    <td>Description</td>
                    <td>{}</td>
                </tr>
                
        """.format(person.name, person.surname, person.description)
        emails = Email.objects.filter(person=person)
        phones = Phone.objects.filter(person=person)
        addresses = Address.objects.filter(person=person)
        groups = Groups.objects.filter(person=person)
        if len(emails) > 0:
            each_email = ""
            for email in emails:
                each_email += "<li>{}:{}</li>".format(email.email_type, email.email_address)
            table += """
                <tr>
                    <td>Email</td>
                    <td>
                        <ul>
                            {}
                        </ul>
                    </td>
                </tr>
            """.format(each_email)
        if len(phones) > 0:
            each_phone = ""
            for phone in phones:
                each_phone += "<li>{}:{}</li>".format(phone.phone_type, phone.phone_number)
            table += """
                <tr>
                    <td>Phone</td>
                    <td>
                        <ul>
                            {}
                        </ul>
                    </td>
                </tr>
            """.format(each_phone)
        if len(addresses) > 0:
            each_address = ""
            for address in addresses:
                each_address += "<li>{} {} {} {}</li>".format(address.street,
                                                              address.house_number,
                                                              address.apartment_number,
                                                              address.city)
            table += """
                <tr>
                    <td>Addresses</td>
                    <td>{}</td>
                </tr>
            """.format(each_address)
        if len(groups) > 0:
            each_group = ""
            for group in groups:
                each_group += "<li>{}</li>".format(group.group_name)
            table += """
                <tr>
                    <td>Groups</td>
                    <td>
                        <ul>
                            {}
                        </ul>
                    </td>
                </tr>
            """.format(each_group)

        table += "</table><br>"
        table += """
            <form><button formaction="/{0}/AddAddress">Add address</button>
            <button formaction="/{0}/AddPhone">Add phone number</button>
            <button formaction="/{0}/AddEmail">Add e-mail</button>
            <button formaction="/{0}/AddToGroup">Add to group</button>
            <br><br>
            <button formaction="/modify/{0}">Modify person</button></form>
            """.format(id)
        return table


@method_decorator(csrf_exempt, name='dispatch')
class ModifyPerson(View):
    @decor_warp_html
    def get(self, request, id):
        person = Person.objects.get(id=id)
        form = form_start + "<h1>Modify data:</h1>"
        form += form_name.format(person.name, person.surname, person.description)
        phones = Phone.objects.filter(person=person)
        emails = Email.objects.filter(person=person)
        addresses = Address.objects.filter(person=person)
        groups = Groups.objects.filter(person=person)
        if phones.exists():
            # phones = Phone.objects.get(person=person)
            form += "Phones: <br>"
            for phone in phones:
                form += form_phone.format(phone.phone_number, phone.phone_type)
        if emails.exists():
            # emails = Email.objects.get(person=person)
            form += "E-mails: <br>"
            for email in emails:
                form += form_email.format(email.email_address, email.email_type)
        if addresses.exists():
            # addresses = Address.objects.get(person=person)
            form += "Addresses: <br>"
            for address in addresses:
                form += form_address.format(address.street, address.house_number, address.apartment_number, address.city)
        if groups.exists():
            form += "Groups: <br>"
            for group in groups:
                form += form_group.format(group.group_name)
        form += "<br><input type='submit' value='Modify'></form>"
        return form

    @decor_warp_html
    def post(self, request):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class AddPerson(View):
    @decor_warp_html
    def get(self, request):
        empty = ''
        result = form_start + form_name + form_end
        return result.format(empty, empty, empty)

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        description = request.POST.get('description')
        if name and surname:
            Person.objects.create(name=name, surname=surname, description=description)
            last_id = Person.objects.order_by('-id')[0]
            response = HttpResponseRedirect('/person/{}'.format(last_id.id))
        else:
            response = 'Not enough data'
        return response


@method_decorator(csrf_exempt, name='dispatch')
class DeletePerson(View):
    @decor_warp_html
    def get(self, request, id):
        person = Person.objects.get(id=id)
        person.delete()
        answer = "{} {} was deleted from database".format(person.name, person.surname)
        return answer


@method_decorator(csrf_exempt, name='dispatch')
class AddAddress(View):
    @decor_warp_html
    def get(self, request, id):
        empty = ''
        form = form_start + form_address + form_end
        return form.format(empty, empty, empty, empty)

    def post(self, request, id):
        person = Person.objects.get(id=id)
        city = request.POST.get('city')
        house_number = request.POST.get('house_number')
        apartment_number = request.POST.get('apartment_number')
        street = request.POST.get('street')
        if city and 0 < len(house_number) < 5 and street and 0 < len(apartment_number) < 5:
            Address.objects.create(city=city,
                                   house_number=house_number,
                                   street=street,
                                   apartment_number=apartment_number,
                                   person=person)
            result = HttpResponseRedirect('/person/{}'.format(id))
        else:
            result = HttpResponse('Wrong data')
        return result


@method_decorator(csrf_exempt, name='dispatch')
class AddPhone(View):
    @decor_warp_html
    def get(self, request, id):
        empty = ''
        form = form_start + form_phone + form_end
        return form.format(empty, 1)

    def post(self, request, id):
        person = Person.objects.get(id=id)
        phone_number = request.POST.get('phone_number')
        phone_type = request.POST.get('phone_type')
        if 9 < len(phone_number) < 15:
            Phone.objects.create(phone_number=phone_number,
                                 phone_type=phone_type,
                                 person=person)
            result = HttpResponseRedirect('/person/{}'.format(id))
        else:
            result = HttpResponse('Wrong data')
        return result


@method_decorator(csrf_exempt, name='dispatch')
class AddEmail(View):
    @decor_warp_html
    def get(self, request, id):
        empty = ''
        form = form_start + form_email + form_end
        return form.format(empty, 1)

    def post(self, request, id):
        person = Person.objects.get(id=id)
        email = request.POST.get('email')
        email_type = request.POST.get('email_type')
        if email:
            Email.objects.create(email_address=email,
                                 email_type=email_type,
                                 person=person)
            result = HttpResponseRedirect('/person/{}'.format(id))
        else:
            result = HttpResponse('Wrong data')
        return result


@method_decorator(csrf_exempt, name='dispatch')
class GroupsView(View):
    @decor_warp_html
    def get(self, request):
        groups = Groups.objects.order_by('group_name')
        table = """
            <table border=1>
                <tr>
                    <td colspan="2">Groups</td>
                </tr>"""
        i = 1
        for group in groups:
            table += """
                <tr>
                    <td>{}</td>
                    <td><a href="/Members/{}" style="color:black">{}</td>
                </tr>
            """.format(i, group.id, group.group_name)
            i += 1
        table += "</table><br>"
        table += """<form><button formaction="/AddGroup/">Add new group</button></form>"""
        return table


@method_decorator(csrf_exempt, name='dispatch')
class AddGroup(View):
    @decor_warp_html
    def get(self, request):
        form = """
            <label>
                Group name:
                <input name="group_name">
            </label>"""
        return form_start + form + form_end

    def post(self, request):
        group_name = request.POST.get("group_name")
        new_group = Groups.objects.create(group_name=group_name)
        new_group.save()
        return HttpResponseRedirect(reverse('groups'))


@method_decorator(csrf_exempt, name='dispatch')
class Members(View):
    @decor_warp_html
    def get(self, request, id):
        members = Groups.objects.get(id=id)
        table = """
                    <table border=1>
                        <tr>
                            <td colspan="2">Members of {}</td>
                        </tr>""".format(members.group_name)
        i = 1
        for member in members:
            table += """
                        <tr>
                            <td>{}</td>
                            <td>>{} {}</td>
                        </tr>
                    """.format(i, member.person.name, member.person.surname)
            i += 1
        table += "</table>"
        return table


