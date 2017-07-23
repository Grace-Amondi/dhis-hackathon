from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from .utils import get_org_units, get_data_el, get_geojson, get_analytics, get_geojson_4


def org_view(request):
    if 'q' in request.GET:
        q = request.GET['q']
        org_units = get_org_units(query=q)
    else:
        org_units = get_org_units()

    data = []
    for org in org_units['organisationUnits']:
        data.append(org)

    context = {
        'org_units': data
    }
    return render(request, 'org_units.html', context)


def data_elements_view(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data_elements = get_data_el(query=q)
    else:
        data_elements = get_data_el()
    data = []
    for el in data_elements['dataElements']:
        data.append(el)

    context = {
        'data_els': data
    }
    return render(request, 'data_elements.html', context)


def org_map_data(request):
    geo_data = get_geojson()
    return HttpResponse(geo_data)


def map_view(request):
    return render(request, 'maps.html')


dx_names = {
    "YtbsuPPo010": "Measles doses given",
    "s46m5MS0hxu": "BCG doses given",
    "l6byfWFUGaP": "Yellow Fever doses given"
}


def get_dx_name(id_key):
    for k, v in dx_names.items():
        if k == id_key:
            return v


def analytics_data(request):
    an_data = get_analytics()

    columns = {
        "records": []
    }
    #
    dx = []

    for i in range(len(an_data["rows"])):
        dat = {}
        d = an_data['rows'][i][0]
        dx.append(d)
        pe = an_data['rows'][i][1]
        val = an_data['rows'][i][2]
        dat['Indicator'] = d
        dat['pe'] = pe
        dat['val'] = float(val)
        columns['records'].append(dat)

    unique_dx = set(dx)

    #
    def get_geojson_pk():
        x = get_geojson().json()

    collection = {}

    for dx in unique_dx:
        collection[dx] = [{"period": [], "value": [], "name": ''}]

    geojson = get_geojson().json()

    for x in unique_dx:
        for n in columns["records"]:
            dx = n["Indicator"]
            if x == dx:
                dx_name = get_dx_name(x)
                collection[x][0]["period"].append(n['pe'])
                collection[x][0]["value"].append(n['val'])
                collection[x][0]["name"] = dx_name

                for i in range(len(geojson["features"])):
                    feat = geojson["features"][i]
                    id = feat["id"]
                    if "ImspTQPwCqd" == id:
                        print "id found "
                        total = sum(collection[x][0]["value"])
                        av = total / len(collection[x][0]["period"])

                        feat["properties"]['average'] = av
    collection["geojson"] = geojson
    return JsonResponse(collection)


def analytics(request):
    return render(request, 'analytics.html')

def graphs(request):
    return render(request,'charts.html')

def get_g_4(request):
    data = get_geojson_4().json()
    return JsonResponse(data)
