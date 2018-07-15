from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
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
    </label><br>"""
form_phone = """
    <br>
    <label>Phone number:
        <input name='phone_number' size='15' value={}>
    </label>
    <label>Phone type:
        <select name="phone_type" value={}>
            <option value=1>Home</option>
            <option value=2>Business</option>
            <option value=3>Mobile</option>
        </select>
    </label>"""
form_email = """
    <br>
    <label>E-mail address:
        <input name='email' size='20' value={}>
    </label>
    <label>E-mail type:
        <select name="email_type" value={}>
            <option value=1>Home</option>
            <option value=2>Business</option>
        </select>
    </label>"""
form_address = """
    <br>
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
    </label>
"""
form_group = """
    <label>Group:
        <input name='group' size='15' value={}>
    </label>
"""
form_end = "<input type='submit' value='Add'></form>"


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
                    <td align="center"><a href='/Delete/person/{0}/{0}' style="color:red">delete</a>
                        <a href='/modify/{0}' style="color:green">modify</a></td>
                </tr>
                """.format(person.id, person.surname, person.name)
        table += "</table><br>"
        table += """<form><button formaction="/new/">Add new person</button>"""
        table += """<button formaction="/groups/">Show all groups</button>"""
        table += """<button formaction="/GroupSearch/">Search in groups</button></form>"""
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
                each_email += "<li>{}: {}</li>".format(email.types[(int(email.email_type) - 1)][1], email.email_address)
            table += """
                <tr>
                    <td>E-mails</td>
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
                each_phone += "<li>{}: {}</li>".format(phone.types[(int(phone.phone_type) - 1)][1], phone.phone_number)
            table += """
                <tr>
                    <td>Phones</td>
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
                each_address += "<li>{} {} / {} {}</li>".format(address.street,
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
            form += "<br>Phones:"
            form += "<table>"
            i = 0
            for phone in phones:
                form += """
                    <tr>
                        <td>
                            <input name=phone_type_{0} value={1} size=5>: 
                        </td>
                        <td>
                            <input name=phone_number_{0} value={2} size=15>
                        </td>
                        """.format(i, phone.phone_type, phone.phone_number)
                form += """
                        <td>
                            <button formaction="/Delete/phone/{}/{}">Erase number</button>
                        </td>
                    </tr>""".format(phone.id, id)
                i += 1
            form += "</table>"
        if emails.exists():
            form += "<br>E-mails:"
            form += "<table>"
            i = 0
            for email in emails:
                form += """
                    <tr>
                        <td>
                            <input name=email_type_{0} value={1} size=5>: 
                        </td>
                        <td>
                            <input name=email_address_{0} value={2} size=15>
                        </td>
                        """.format(i, email.email_type, email.email_address)
                form += """
                        <td>
                            <button formaction="/Delete/email/{}/{}">Erase e-mail</button>
                        </td>
                    </tr>""".format(email.id, id)
                i += 1
            form += "</table>"
        if addresses.exists():
            form += "<br>Addresses:"
            form += "<table>"
            i = 0
            for address in addresses:
                form += """
                    <tr>
                        <td>
                            <input name=street_{0} value={1} size=10>
                        </td>
                        <td>
                            <input name=house_number_{0} value={2} size=5> /
                        </td>
                        <td>
                            <input name=apartment_number_{0} value={3} size=5>
                        </td>
                        <td>
                            <input name=city_{0} value={4} size=10>
                        </td>
                        """.format(i, address.street, address.house_number, address.apartment_number, address.city)
                form += """
                        <td>
                            <button formaction="/Delete/address/{}/{}">Erase address</button>
                        </td>
                    </tr>""".format(address.id, id)
                i += 1
            form += "</table>"
        if groups.exists():
            form += "<br>Groups:"
            form += "<table>"
            for group in groups:
                form += "<br><tr><td>" + group.group_name + "</td>"
                form += """<td><button formaction="/{}/{}/EraseFromGroup/">Erase from group</button></td></tr>""".format(
                    person.id,
                    group.id)
            form += "</table>"
        form += "<br><br><input type='submit' value='Modify'></form>"
        return form

    def post(self, request, id):
        person = Person.objects.get(id=id)
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        description = request.POST.get("description")
        person.name = name
        person.surname = surname
        person.description = description
        person.save()
        phones_list = []
        emails_list = []
        addresses_list = []
        phones = Phone.objects.filter(person=person)
        emails = Email.objects.filter(person=person)
        addresses = Address.objects.filter(person=person)
        for i in range(phones.count()):
            phone_type = int(request.POST.get("phone_type_{}".format(i)))
            phone_number = request.POST.get("phone_number_{}".format(i))
            phone_tuple = (phone_type, phone_number)
            phones_list.append(phone_tuple)
        for i in range(emails.count()):
            email_type = int(request.POST.get("email_type_{}".format(i)))
            email_address = request.POST.get("email_address_{}".format(i))
            email_tuple = (email_type, email_address)
            emails_list.append(email_tuple)
        for i in range(addresses.count()):
            street = request.POST.get("street_{}".format(i))
            house_number = request.POST.get("house_number_{}".format(i))
            apartment_number = request.POST.get("apartment_number_{}".format(i))
            city = request.POST.get("city_{}".format(i))
            address_tuple = (street, house_number, apartment_number, city)
            addresses_list.append(address_tuple)
        i = 0
        for phone in phones:
            new_phone = Phone.objects.get(id=phone.id)
            new_phone.phone_type = phones_list[i][0]
            new_phone.phone_number = phones_list[i][1]
            new_phone.save()
            i += 1
        i = 0
        for email in emails:
            new_email = Email.objects.get(id=email.id)
            new_email.email_type = emails_list[i][0]
            new_email.email_address = emails_list[i][1]
            new_email.save()
            i += 1
        i = 0
        for address in addresses:
            new_address = Address.objects.get(id=address.id)
            new_address.street = addresses_list[i][0]
            new_address.house_number = addresses_list[i][1]
            new_address.apartment_number = addresses_list[i][2]
            new_address.city = addresses_list[i][3]
            new_address.save()
            i += 1
        return HttpResponseRedirect(reverse("person", kwargs={'id': id}))


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
            response = HttpResponse('Not enough data')
        return response


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
        for member in members.person.all():
            table += """
                        <tr>
                            <td>{}</td>
                            <td>{} {}</td>
                        </tr>
                    """.format(i, member.name, member.surname)
            i += 1
        table += "</table>"
        return table


@method_decorator(csrf_exempt, name='dispatch')
class AddToGroup(View):
    @decor_warp_html
    def get(self, request, id):
        groups = Groups.objects.all()
        person = Person.objects.get(id=id)
        form = """
            <label>
                Add {} {} to: 
                <select name="group">""".format(person.name, person.surname)
        for group in groups:
            form += "<option value={}>{}</option>".format(group.id, group.group_name)
        form += "</select></label><br>"
        return form_start + form + form_end

    def post(self, request, id):
        group_number = int(request.POST.get("group"))
        my_person = Person.objects.get(id=id)
        group = Groups.objects.get(id=group_number)
        group.person.add(my_person)
        return HttpResponseRedirect(reverse("person", kwargs={'id': id}))


@method_decorator(csrf_exempt, name='dispatch')
class EraseFromGroup(View):
    def post(self, request, id_person, id_group):
        my_person = Person.objects.get(id=id_person)
        group = Groups.objects.get(id=id_group)
        group.person.remove(my_person)
        return HttpResponseRedirect(reverse("modify", kwargs={'id': id_person}))


@method_decorator(csrf_exempt, name='dispatch')
class DeleteData(View):
    def post(self, request, data, id, id_person):
        if data == "person":
            model = Person
            object_to_delete = model.objects.get(id=id)
            object_to_delete.delete()
            answer = HttpResponseRedirect(reverse('all'))
        else:
            if data == "email":
                model = Email
                answer = HttpResponseRedirect(reverse("modify", kwargs={'id': id_person}))
            elif data == "phone":
                model = Phone
                answer = HttpResponseRedirect(reverse("modify", kwargs={'id': id_person}))
            elif data == "address":
                model = Address
                answer = HttpResponseRedirect(reverse("modify", kwargs={'id': id_person}))
            else:
                return HttpResponse("Wrong data to delete")
            object_to_delete = model.objects.get(id=id)
            object_to_delete.delete()
        return answer


@method_decorator(csrf_exempt, name='dispatch')
class GroupSearch(View):
    @decor_warp_html
    def get(self, request):
        form = """
            <input name="searching_field" placeholder="who are you looking for?"></input>
            <input type='submit' value='Search'></form>
        """
        return form_start + form

    @decor_warp_html
    def post(self, request):
        searching_field = request.POST.get("searching_field")
        persons = Person.objects.all()
        table = """
            <table>
                <tr>
                    <td>
                        Results:
                    </td>
                </tr>"""
        i = 1
        for person in persons:
            if person.name == searching_field or person.surname == searching_field:
                table += """
                    <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                    </tr>""".format(i, person.name, person.surname)
                i += 1
        table += "</table>"
        if i < 2:
            return "No results"
        else:
            return table

