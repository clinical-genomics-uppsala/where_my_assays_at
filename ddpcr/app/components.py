from django_components import component

@component.register('assay_info_modal')
class AssayInfoModal(component.Component):
    def context(self, assay):
        return {
            'assay': assay,
        }

    def template(self, context):
        return "components/assay_info_modal/assay_info_modal.html"

@component.register('basic_assay_list')
class BasicAssayList(component.Component):
    def context(self, button, icon, objects, title, url):
        return {
            'button': button,
            'icon': icon,
            'objects': objects,
            'title': title,
            'url': url,
        }

    def template(self, context):
        return "components/basic_assay_list/basic_assay_list.html"

@component.register('basic_lot_form')
class BasicLotForm(component.Component):
    def context(self, form, icon, object, title):
        return {
            'form': form,
            'icon': icon,
            'object': object,
            'title': title,
        }

    def template(self, context):
        return "components/basic_lot_form/basic_lot_form.html"

@component.register('basic_lot_list')
class BasicLotList(component.Component):
    def context(self, button, complete, icon, objects, title, url):
        return {
            'button': button,
            'complete': complete,
            'icon': icon,
            'objects': objects,
            'title': title,
            'url': url,
        }

    def template(self, context):
        return "components/basic_lot_list/basic_lot_list.html"

@component.register('lot_info_modal')
class LotInfoModal(component.Component):
    def context(self, lot):
        return {
            'lot': lot,
        }

    def template(self, context):
        return "components/lot_info_modal/lot_info_modal.html"

@component.register('lot_status')
class LotStatus(component.Component):
    def context(self, status):
        return {
            'status': status,
        }

    def template(self, context):
        return "components/lot_status/lot_status.html"

@component.register('message_alert')
class MessageAlert(component.Component):
    def context(self, message):
        return {
            'message': message,
        }

    def template(self, context):
        return "components/message_alert/message_alert.html"

@component.register('nav_dropdown')
class NavDropdown(component.Component):
    def context(self, icon, title):
        return {
            'icon': icon,
            'title': title,
        }

    def template(self, context):
        return "components/nav_dropdown/nav_dropdown.html"

    class Media:
        css = 'components/nav_dropdown/nav_dropdown.css'
        js = None
