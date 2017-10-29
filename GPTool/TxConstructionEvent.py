import arcpy
import pythonaddins
import os
import functools
import threading
import webbrowser

import requests
 
# A decorator that will run its wrapped function in a new thread
def run_in_other_thread(function):
    # functool.wraps will copy over the docstring and some other metadata
    # from the original function
    @functools.wraps(function)
    def fn_(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs)
        thread.start()
        thread.join()
    return fn_
 
# Our new wrapped versions of os.startfile and webbrowser.open
startfile = run_in_other_thread(os.startfile)
openbrowser = run_in_other_thread(webbrowser.open)

class CreateRoutingEvent(object):
    """Implementation for StreetView_addin.GSV_TL (Tool)"""
    def __init__(self):
        self.enabled = True
        self.shape = "NONE"
        self.cursor = 3

        self.start_x = None
        self.start_y = None

        self.end_x = None
        self.end_y = None

        self.request_url = None

        self.token = self.getWebGISToken()
    
    def onMouseDownMap(self, x, y, button, shift):
        # Create an in-memory Point object
        point = arcpy.Point()
        # Populate the point's longitude property with the returned longitude from the onMouseDownMap function
        point.X = x
        # Populate the point's latitude property with the returned latitude from the onMouseDownMap function
        point.Y = y
        # Create an in-memory PointGeometry object from the point and associating the point's latitude and longitude values with the Web Mercator Auxillary Sphere projection
        # and then project those coordinate property values to WGS-1984 and assign those results as the PointGeometry's respective coordinate property values
        displayPoint = arcpy.PointGeometry(point, arcpy.SpatialReference(3857)).projectAs(arcpy.SpatialReference(4326))
        xWGS = displayPoint.centroid.X
        yWGS = displayPoint.centroid.Y
        
        self.start_x = xWGS
        self.start_y = yWGS

    def onMouseUpMap(self, x, y, button, shift):
        # Create an in-memory Point object
        point = arcpy.Point()
        # Populate the point's longitude property with the returned longitude from the onMouseDownMap function
        point.X = x
        # Populate the point's latitude property with the returned latitude from the onMouseDownMap function
        point.Y = y
        # Create an in-memory PointGeometry object from the point and associating the point's latitude and longitude values with the Web Mercator Auxillary Sphere projection
        # and then project those coordinate property values to WGS-1984 and assign those results as the PointGeometry's respective coordinate property values
        displayPoint = arcpy.PointGeometry(point, arcpy.SpatialReference(3857)).projectAs(arcpy.SpatialReference(4326))
        xWGS = displayPoint.centroid.X
        yWGS = displayPoint.centroid.Y

        self.end_x = xWGS
        self.end_y = yWGS

        self.request_url = self.buildRouteRequest(self.start_x, self.start_y, self.end_x, self.end_y, self.token)

        self.getRouteEvent(self.request_url)

    def getWebGISToken(self):

        token = "gx7FcRrANS0U-HXutDLWRAhvrHmfqJUCurUHZf85ui1724uvLHis1bzNCkKSelQv8l4zQTu7D2X2gcltEnux-Wv0C__fVu4j00VNYJEQYsZ0zaVnYe76SSSkkE9qeA0RFsXEfKPr8ZjHYzBN36b8wg.."

        return token

    def getRouteEvent(self, request_url):

        # Sample request 
        # http://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve?
        # token=Zfrq3Cgh-_YE_QOJEY8BoeQRpzrSquqKyP_r9GOijDmw7UsKNs4_GL6BgAuVZsmwrEAJHkaNGNRCLh2xCDaYTvzZdWOwquvVsPROQ9UXQlWQwANnXhvLXbb9nlRHNp_EmrMIaaUcVEs7lpp6OkV_mg..
        # &stops=-122.4079,37.78356;-122.404,37.782&f=json
        
        startfile(request_url)
        
        r = requests.get(request_url)
        r_json = r.json()

        

        # message = "Your mouse clicked:" + str(x) + ", " + str(y)

        # pythonaddins.MessageBox(request_url, "Request: ")
        # pythonaddins.MessageBox(str(r_json), "My JSON") 


    def buildRouteRequest(self, start_x, start_y, end_x, end_y, token, f="json"):

        routing_service_base_url = r"http://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve?"

        # Stops Syntax Example: stops=-117.1957,34.0564; -117.184,34.0546
        routing_stops = "{0},{1}; {2},{3}".format(start_x, start_y, end_x, end_y)

        request_url = r"{0}token={1}&stops={2}&f={3}".format(routing_service_base_url, self.token, routing_stops, f)

        return request_url