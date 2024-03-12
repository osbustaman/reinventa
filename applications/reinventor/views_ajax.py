import datetime
import io
import json
import base64
from numpy import isnan
from openpyxl import Workbook
import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation
import pandas as pd
from io import BytesIO

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from applications.account.models import Comuna, Pais, Region, Reinventor, RequestTracking, WithdrawalRequestReinventor
from applications.reinventor.forms import RequestTrackingForm
from reinventa.utils import getLatitudeLongitude

@csrf_exempt  
def new_observation(request):
    if request.method == 'POST':
        try:
            RequestTracking.objects.create( 
                user = User.objects.get(id = request.session['id']),
                withdrawalRequestReinventor = WithdrawalRequestReinventor.objects.get(wrr_id=int(request.POST["wrr_id"])),
                rt_observation = request.POST["respuesta"]
            )

            response = {
                'message': 'success',
                'error': False
            }
            response_data = {'response': response}
            return JsonResponse(response_data)
        
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Error al decodificar JSON: {}'.format(str(e))}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def download_excel_for_upload_reinventor(request):
    if request.method == 'POST':
        try:

            reinventores = ['REINVENTOR', 'NOMBRE', 'EMAIL', 'DIRECCION', 'REGION', 'COMUNA']
            locations = ['NOMBRE COMUNA', 'REGION COMUNA']

            df_reinventores = pd.DataFrame(columns=reinventores)
            df_comunnes = pd.DataFrame(columns=locations)

            #Fecha actual
            filename_excel ='plantilla_carga_masiva.xlsx'
            writer = pd.ExcelWriter(f'{filename_excel}', engine='xlsxwriter')

            df_reinventores.to_excel(writer, sheet_name='reinventores', index=False)
            df_comunnes.to_excel(writer, sheet_name='comunas', index=False)

            df_reinventores.columns = reinventores
            df_comunnes.columns = locations

            writer.save()

            # Abre el archivo Excel existente
            workbook = openpyxl.load_workbook(filename=filename_excel)

            sheet_cc = workbook['comunas']
            sheet = workbook['reinventores']

            object_comunas = Comuna.objects.all()
            cont = 2
            for comunas in object_comunas:
                sheet_cc[f'A{cont}'] = comunas.com_nombre
                sheet_cc[f'B{cont}'] = comunas.region.re_nombre
                cont += 1

            # Oculta la hoja
            # sheet_cc.sheet_state = 'hidden'
            excel_base64 = ""

                    # Crear una lista de opciones para la lista desplegable de regiones
            object_region = Region.objects.all()
            array_regiones = []
            for region in object_region:
                array_regiones.append(region.re_nombre)

            validation_regiones = DataValidation(type="list", formula1=f'"{",".join(array_regiones)}"')
            validation_regiones.add(f'E2:E50')
            sheet.add_data_validation(validation_regiones)

            # Guardamos el archivo con los cambios
            workbook.save(filename_excel)

            # Codifica el archivo en base64
            with open(filename_excel, 'rb') as file:
                excel_base64 = base64.b64encode(file.read()).decode('utf-8').replace('\n', '')

            response = {
                'message': excel_base64,
                'error': False
            }
            response_data = {'response': response}
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({'error': 'Error al descargar el archivo Excel: {}'.format(str(e))}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt  
def upload_file(request):
    if request.method == 'POST':
        try:

            not_save = []

            # Obtén la cadena base64 del cuerpo del request
            file_data = request.POST.get("file_data", "")

            # Decodifica la cadena base64
            decoded_data = base64.b64decode(file_data)

            # Leer el archivo Excel
            excel_file = io.BytesIO(decoded_data)
            df_excel = pd.read_excel(excel_file, sheet_name=None)
            hojas_excel = df_excel.keys()


            datos_por_hoja = {}
            for hoja in hojas_excel:
                # Lee los datos de la hoja actual
                # skiprows omite la primera fila
                df_hoja = pd.read_excel(excel_file, sheet_name=hoja, skiprows=0)

                # Guarda los datos de la hoja actual en un array
                datos_hoja = []
                for index, row in df_hoja.iterrows():
                    datos_hoja.append(row.to_dict())

                # Agrega los datos de la hoja actual al diccionario
                datos_por_hoja[hoja] = datos_hoja
            
            the_country = Pais.objects.filter(pa_id=1)
            if not the_country.exists():
                raise Exception('El país no existe, debe crearlo primero')
            
            

            for value in datos_por_hoja["reinventores"]:

                if any(pd.isna(value[col]) for col in ['REINVENTOR', 'NOMBRE', 'DIRECCION', 'REGION', 'COMUNA', 'EMAIL']):
                    not_save.append({
                        "cliente": str(value["REINVENTOR"]),
                        "nombre_a_cargo": str(value["NOMBRE"]),
                        "direccion": str(value["DIRECCION"]),
                        "region": str(value["REGION"]),
                        "comuna": str(value["COMUNA"]),
                        "email": str(value["EMAIL"]),
                        "error": "faltan campos",
                    })
                else:

                    object_reinventor = Reinventor.objects.filter(re_email=value['EMAIL']).exists()
                    
                    if not object_reinventor:

                        address = f"{ value['DIRECCION'] }, { value['COMUNA'] }, { value['REGION'] }, { the_country[0].pa_nombre }"
                        lat_lng = getLatitudeLongitude(address)

                        if not lat_lng:
                            re_latitude = 0
                            re_longitude = 0
                        else:
                            re_latitude = lat_lng['latitude'] 
                            re_longitude = lat_lng['longitude']

                        Reinventor.objects.create(
                            re_nameentity = value['REINVENTOR'],
                            re_email = value['EMAIL'],
                            re_namereinventor = value['NOMBRE'],
                            re_address = value['DIRECCION'],
                            pais = the_country[0],
                            region = Region.objects.get(re_nombre=value['REGION']),
                            comuna = Comuna.objects.get(com_nombre=value['COMUNA']),
                            re_latitude = re_latitude,
                            re_longitude = re_longitude
                        )

                    else:
                        not_save.append({
                            "cliente": str(value["REINVENTOR"]),
                            "error": "cliente ya existe",
                        })

            if len(not_save) > 0:

                # Convertir la lista en un DataFrame de Pandas
                df = pd.DataFrame(not_save)

                # Guardar el DataFrame en un archivo Excel
                excel_file = 'datos.xlsx'
                df.to_excel(excel_file, index=False)

                # Leer el archivo Excel recién creado
                with open(excel_file, 'rb') as file:
                    excel_content = file.read()

                # Codificar el contenido del archivo Excel en base64
                excel_base64 = base64.b64encode(excel_content).decode('utf-8')

            else:
                excel_base64 = False

            response = {
                'message': 'success',
                'error': False,
                'details': excel_base64
            }
            response_data = {'response': response}
            return JsonResponse(response_data)
        
        except Exception as e:
            return JsonResponse({'error': 'Error al procesar el archivo Excel: {}'.format(str(e))}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)