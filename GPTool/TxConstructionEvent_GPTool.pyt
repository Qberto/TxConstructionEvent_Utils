import arcpy
import requests
import json
import urllib

### PSEUDOCODE ###

# 1. Process inputs
# 2. Create request to world routing NA service
# 3. Send request and ingest response JSON
# 4. Use the geometry from the response JSON to send an applyEdits request to the target feature service of construction events.

### ACTUALCODE ###

# Updated 10/31/2017

class Toolbox(object):
    def __init__(self):
        self.label =  "Port Construction Events"
        self.alias  = "Events"

        # List of tool classes associated with this toolbox
        self.tools = [CreateConstructionEvent] 

class CreateConstructionEvent(object):
    def __init__(self):
        self.label       = "Create Construction Event"
        self.description = "Uses defined user start and end points to create an event."

    def getParameterInfo(self):
        #Define parameter definitions

        # Input Features parameter
        in_start_point = arcpy.Parameter(
            displayName="Start Point",
            name="in_start_point",
            datatype="GPFeatureRecordSetLayer",
            parameterType="Required",
            direction="Input")

        # Input Features parameter
        in_end_point = arcpy.Parameter(
            displayName="End Point",
            name="in_end_point",
            datatype="GPFeatureRecordSetLayer",
            parameterType="Required",
            direction="Input")

        # # Input Features parameter
        # in_events_lyr = arcpy.Parameter(
        #     displayName="Events Dataset",
        #     name="in_events_lyr",
        #     datatype="GPFeatureLayer",
        #     parameterType="Required",
        #     direction="Input")
        

        
        # Input Features parameter
        in_events_lyr = arcpy.Parameter(
            displayName="Construction Events Service REST URL",
            name="in_events_lyr",
            datatype="GPString",
            parameterType="Required",
            direction="Input")     

        # Input Features parameter
        in_token = arcpy.Parameter(
            displayName="App Token",
            name="in_token",
            datatype="GPString",
            parameterType="Required",
            direction="Input")


        parameters = [in_start_point, in_end_point, in_events_lyr, in_token]
        
        return parameters

    def isLicensed(self): #optional
        return True

    def updateParameters(self, parameters): #optional
        return

    def updateMessages(self, parameters): #optional
        return

    # def routeConfig(self, parameters):
    #     self.outRouteSR = "102100"
    #     self.
    #     self.routeOutputGeometryPrecision = 10
    

    def getRoutes(self, in_start_point, in_end_point, in_token):

        routing_service_base_url = r"http://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve?"

        f='JSON'
        
        for row in arcpy.da.SearchCursor(in_start_point, ["SHAPE@XY"], spatial_reference=arcpy.SpatialReference(4326)):
            start_x, start_y = row[0]
            print("{}, {}".format(start_x, start_y))

        for row in arcpy.da.SearchCursor(in_end_point, ["SHAPE@XY"], spatial_reference=arcpy.SpatialReference(4326)):
            end_x, end_y = row[0]
            print("{}, {}".format(end_x, end_y))

        routing_stops = "{0},{1}; {2},{3}".format(start_x, start_y, end_x, end_y)

        outSR = "102100"

        # request_url = r"{0}token={1}&stops={2}&f={3}&outSR={4}".format(routing_service_base_url, in_token, routing_stops, f, outSR)

        route_payload = {'f': 'json', 'token': in_token, 'stops': routing_stops, 'outSR': outSR}

        # 3. Send request and ingest response JSON
        
        # r = requests.get(request_url)
        r = requests.get(routing_service_base_url, params=route_payload)
        arcpy.AddMessage(str(r))
        r_json = r.json()
        arcpy.AddMessage(r_json)

        # Build request JSON
        
        # Get the features from the route response
        features = r_json['routes']['features']
        paths = features[0]['geometry']['paths']
        length = float(features[0]['attributes']['Total_Miles'])
        arcpy.AddMessage("Route length: {0}".format(str(length)))

        return paths, length

    def getShortestRoute(self, in_start_point, in_end_point, in_token):

        a_b_route_path, a_b_route_length = self.getRoutes(in_start_point, in_end_point, in_token)

        b_a_route_path, b_a_route_length = self.getRoutes(in_end_point, in_start_point, in_token)

        if a_b_route_length < b_a_route_length:
            arcpy.AddMessage("Selected A_B Route")
            return a_b_route_path
        else:
            arcpy.AddMessage("Selected B_A Route")
            return b_a_route_path

    def execute(self, parameters, messages):

        # 1. Process inputs
        
        in_start_point  = parameters[0].value
        in_end_point   = parameters[1].value
        in_events_lyr = parameters[2].value
        in_token = parameters[3].value

        # work_gdb = r"C:\Users\albe9057\Documents\ANieto_SolutionEngineering\Projects\DOT\PANYNJ\Work\EventCreator_Proto"

        # 2. Create request to world routing NA service
        
        # paths, length = self.getRoutes(in_start_point, in_end_point, in_token)
        paths = self.getShortestRoute(in_start_point, in_end_point, in_token)
        
        # routing_service_base_url = r"http://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve?"

        # f='JSON'
        
        # for row in arcpy.da.SearchCursor(in_start_point, ["SHAPE@XY"], spatial_reference=arcpy.SpatialReference(4326)):
        #     start_x, start_y = row[0]
        #     print("{}, {}".format(start_x, start_y))

        # for row in arcpy.da.SearchCursor(in_end_point, ["SHAPE@XY"], spatial_reference=arcpy.SpatialReference(4326)):
        #     end_x, end_y = row[0]
        #     print("{}, {}".format(end_x, end_y))

        # routing_stops = "{0},{1}; {2},{3}".format(start_x, start_y, end_x, end_y)

        # outSR = "102100"

        # # request_url = r"{0}token={1}&stops={2}&f={3}&outSR={4}".format(routing_service_base_url, in_token, routing_stops, f, outSR)

        # route_payload = {'f': 'json', 'token': in_token, 'stops': routing_stops, 'outSR': outSR}

        # # 3. Send request and ingest response JSON
        
        # # r = requests.get(request_url)
        # r = requests.get(routing_service_base_url, params=route_payload)
        # arcpy.AddMessage(str(r))
        # r_json = r.json()
        # arcpy.AddMessage(r_json)

        # # Build request JSON
        
        # # Get the features from the route response
        # features = r_json['routes']['features']
        # paths = features[0]['geometry']['paths']

        # json_payload = [{
        #     "geometry": {
        #         "paths": paths
        #     },
        #     "attributes": {
        #         "AnalysisSettings":None,
        #         "Version":None,
        #         "RouteName":None,
        #         "TotalMinutes":None,
        #         "TotalMeters":None,
        #         "TotalLateMinutes":None,
        #         "TotalWaitMinutes":None,
        #         "TotalCosts":None,
        #         "StartTime":None,
        #         "StartUTCOffset":None,
        #         "EndTime":None,
        #         "EndUTCOffset":None,
        #         "Messages":None
        #     }
        # }]
        # arcpy.AddMessage(json_payload)
        

        # 4. Use the geometry from the response JSON to send an applyEdits request to the target feature service of construction events.
        
        update_base_url = "{0}/{1}".format(in_events_lyr, "applyEdits")

        # manual_adds = r'[{"geometry":{"paths":[[[-8620184.529356662,4716784.926280767],[-8620005.380071633,4716991.545122833]]],"spatialReference":{"wkid":102100,"latestWkid":3857}},"attributes":{"AnalysisSettings":null,"Version":null,"RouteName":null,"TotalMinutes":null,"TotalMeters":null,"TotalLateMinutes":null,"TotalWaitMinutes":null,"TotalCosts":null,"StartTime":null,"StartUTCOffset":null,"EndTime":null,"EndUTCOffset":null,"Messages":null}}]'
        # manual_adds = r'[{"geometry":{"paths":[[[-8620184.529356662,4716784.926280767],[-8620005.380071633,4716991.545122833]]]},"attributes":{"AnalysisSettings":null,"Version":null,"RouteName":null,"TotalMinutes":null,"TotalMeters":null,"TotalLateMinutes":null,"TotalWaitMinutes":null,"TotalCosts":null,"StartTime":null,"StartUTCOffset":null,"EndTime":null,"EndUTCOffset":null,"Messages":null}}]'
        # manual_adds = r'[{"geometry": {"paths": [[[-8620384.6147, 4716581.070799999], [-8620336.4642, 4716630.728100002], [-8620234.0502, 4716723.7892], [-8620053.4761, 4716934.951800004]]]},"attributes":{"AnalysisSettings":null,"Version":null,"RouteName":null,"TotalMinutes":null,"TotalMeters":null,"TotalLateMinutes":null,"TotalWaitMinutes":null,"TotalCosts":null,"StartTime":null,"StartUTCOffset":null,"EndTime":null,"EndUTCOffset":null,"Messages":null}}]'
        manual_adds = '[{{"geometry": {{"paths": {0}}},"attributes":{{"AnalysisSettings":null,"Version":null,"RouteName":null,"TotalMinutes":null,"TotalMeters":null,"TotalLateMinutes":null,"TotalWaitMinutes":null,"TotalCosts":null,"StartTime":null,"StartUTCOffset":null,"EndTime":null,"EndUTCOffset":null,"Messages":null}}}}]'.format(paths)
        # manual_adds = '[{"geometry": {"paths": [[[-8620384.6147, 4716581.070799999], [-8620336.4642, 4716630.728100002], [-8620234.0502, 4716723.7892], [-8620053.4761, 4716934.951800004]]]},"attributes":{"AnalysisSettings":null,"Version":null,"RouteName":null,"TotalMinutes":null,"TotalMeters":null,"TotalLateMinutes":null,"TotalWaitMinutes":null,"TotalCosts":null,"StartTime":null,"StartUTCOffset":null,"EndTime":null,"EndUTCOffset":null,"Messages":null}}]'

        # manual_adds = '[{{"geometry": {{"paths": {0}}},"attributes":{{"AnalysisSettings":null,"Version":null,"RouteName":null,"TotalMinutes":null,"TotalMeters":null,"TotalLateMinutes":null,"TotalWaitMinutes":null,"TotalCosts":null,"StartTime":null,"StartUTCOffset":null,"EndTime":null,"EndUTCOffset":null,"Messages":null}}}}]'.format(paths)

        # payload = {'f': 'json', 'adds': features}
        payload = {'f': 'json', 'adds': manual_adds}
        # payload = {'f': 'json', 'adds': adds}

        arcpy.AddMessage("Base URL:")
        arcpy.AddMessage(update_base_url)

        arcpy.AddMessage("Payload:")
        arcpy.AddMessage(payload)

        update_result = requests.post(update_base_url, data=payload)
        update_result_json = update_result.json()
        arcpy.AddMessage(str(update_result_json))

        # https://services.arcgis.com/hRUr1F8lE8Jq2uJo/arcgis/rest/services/PANYNJ_Construction_Events/FeatureServer/0/applyEdits
        # 
        # f:json
        # adds:[{"geometry":{"paths":[[[-8620184.529356662,4716784.926280767],[-8620005.380071633,4716991.545122833]]],"spatialReference":{"wkid":102100,"latestWkid":3857}},"attributes":{"AnalysisSettings":null,"Version":null,"RouteName":null,"TotalMinutes":null,"TotalMeters":null,"TotalLateMinutes":null,"TotalWaitMinutes":null,"TotalCosts":null,"StartTime":null,"StartUTCOffset":null,"EndTime":null,"EndUTCOffset":null,"Messages":null}}]