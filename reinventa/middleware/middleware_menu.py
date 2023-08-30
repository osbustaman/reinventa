class menu_middleware_items(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        try:

            if '/dashboard/' in request.path:
                request.session['item'] = 'incio'
                request.session['sub_item'] = 'dashboard'

            if '/configuracion' in request.path:
                request.session['item'] = 'reinventa'
                request.session['sub_item'] = 'configuracion'
            
            if '/ver-request/' in request.path:
                request.session['item'] = 'reinventa'
                request.session['sub_item'] = 'solicitudes'

            if '/ver-user/' in request.path:
                request.session['item'] = 'reinventa'
                request.session['sub_item'] = 'usuarios'

            if '/add-user/' in request.path:
                request.session['item'] = 'reinventa'
                request.session['sub_item'] = 'usuarios'

            if '/edit-user/' in request.path:
                request.session['item'] = 'reinventa'
                request.session['sub_item'] = 'usuarios'
                
            if '/listado-reinventores/' in request.path:
                request.session['item'] = 'reinventores'
                request.session['sub_item'] = 'ver_reinventores'
            
            if '/crear-reinventor/' in request.path:
                request.session['item'] = 'reinventores'
                request.session['sub_item'] = 'ver_reinventores'

            if '/editar-reinventor/' in request.path:
                request.session['item'] = 'reinventores'
                request.session['sub_item'] = 'ver_reinventores'

            if '/add-user-reinventor/' in request.path:
                request.session['item'] = 'reinventores'
                request.session['sub_item'] = 'ver_reinventores'

            if '/edit-user-reinventor/' in request.path:
                request.session['item'] = 'reinventores'
                request.session['sub_item'] = 'ver_reinventores'

            if '/list-request-reinventor/' in request.path:
                request.session['item'] = 'reinventores'
                request.session['sub_item'] = 'list_request_reinventor'
            
        except:
            pass