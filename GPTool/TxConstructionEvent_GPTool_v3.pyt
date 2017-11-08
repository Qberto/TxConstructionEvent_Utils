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
        
        ### In Construction Event Attributes ###
        in_PID = arcpy.Parameter(
            displayName="Project ID",
            name="in_PID",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")   

        in_CAP = arcpy.Parameter(
            displayName="CAP ID",
            name="in_CAP",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")

        in_C_Cntr = arcpy.Parameter(
            displayName="Contract Number",
            name="in_C_Cntr",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")   

        in_Title = arcpy.Parameter(
            displayName="Project Title",
            name="in_Title",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")  

        in_LineDept = arcpy.Parameter(
            displayName="Line Department",
            name="in_LineDept",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")   

        in_FACY = arcpy.Parameter(
            displayName="Facility Code",
            name="in_FACY",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")

        in_Facility = arcpy.Parameter(
            displayName="Facility",
            name="in_Facility",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")   

        in_CPOP = arcpy.Parameter(
            displayName="Capital/Operating",
            name="in_CPOP",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")  

        in_LeadDis = arcpy.Parameter(
            displayName="Lead Discipline",
            name="in_LeadDis",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")   

        in_DEA_Name = arcpy.Parameter(
            displayName="LE/A Name",
            name="in_DEA_Name",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")

        in_PROC = arcpy.Parameter(
            displayName="Procurement Type",
            name="in_PROC",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")   

        in_CTRS = arcpy.Parameter(
            displayName="Contract Strategy",
            name="in_CTRS",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")  

        in_PM_Name = arcpy.Parameter(
            displayName="Project Engineer Name",
            name="in_PM_Name",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")   

        in_RE_Name = arcpy.Parameter(
            displayName="Resident Engineer Name",
            name="in_RE_Name",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")

        in_STAG = arcpy.Parameter(
            displayName="Stage",
            name="in_STAG",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")           

        in_SORT = arcpy.Parameter(
            displayName="Stage Status",
            name="in_SORT",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")  

        in_ES = arcpy.Parameter(
            displayName="Start Date",
            name="in_ES",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input")  

        in_EF = arcpy.Parameter(
            displayName="End Date",
            name="in_EF",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input")  
       
        in_BIDS = arcpy.Parameter(
            displayName="Bid Date",
            name="in_BIDS",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input")  

        in_AWRD = arcpy.Parameter(
            displayName="Award Date",
            name="in_AWRD",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input")  
       
        in_PARV = arcpy.Parameter(
            displayName="PAWide Review Date",
            name="in_PARV",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input")  

        in_FD = arcpy.Parameter(
            displayName="Signed Mylar Date",
            name="in_FD",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input")  
        
        in_SC = arcpy.Parameter(
            displayName="Substantial Completion Date",
            name="in_SC",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input") 

        in_EEST = arcpy.Parameter(
            displayName="Engineering Estimate",
            name="in_EEST",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")  
        
        in_BID = arcpy.Parameter(
            displayName="Bid Amount",
            name="in_BID",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input") 

        in_AWD = arcpy.Parameter(
            displayName="Award Amount",
            name="in_AWD",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")     

        in_chargecode = arcpy.Parameter(
            displayName="Charge Code",
            name="in_chargecode",
            datatype="GPLong",
            parameterType="Optional",
            direction="Input")                                                                                     

        in_CM923ST = arcpy.Parameter(
            displayName="PA-923 Sent",
            name="in_CM923ST",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input")  
        
        in_CM923SG = arcpy.Parameter(
            displayName="PA-923 Signed",
            name="in_CM923SG",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input") 

        in_X0SUB = arcpy.Parameter(
            displayName="50% Submittal",
            name="in_X0SUB",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input")  
        
        in_X90SUB = arcpy.Parameter(
            displayName="90% Submittal",
            name="in_X90SUB",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input") 

        in_X00SUB = arcpy.Parameter(
            displayName="100% Submittal",
            name="in_X00SUB",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input")   

        in_Sandy = arcpy.Parameter(
            displayName="Sandy Project Flag",
            name="in_Sandy",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input")

        in_messages = arcpy.Parameter(
            displayName="Notes or Messages",
            name="in_messages",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")

        # Input Features parameter
        in_events_lyr = arcpy.Parameter(
            displayName="Construction Events Service REST URL",
            name="in_events_lyr",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        in_events_lyr.value = "http://neenterprise.esri.com/server/rest/services/Hosted/PANYNJ_Construction_Events_B01/FeatureServer/0"  

        # Token parameter - to be replaced by automated token retrieval
        in_token = arcpy.Parameter(
            displayName="App Token",
            name="in_token",
            datatype="GPString",
            parameterType="Required",
            direction="Input")


        parameters = [
        in_start_point, 
        in_end_point, 
        in_PID,
        in_CAP,
        in_C_Cntr,
        in_Title,
        in_LineDept,
        in_FACY,
        in_Facility,
        in_CPOP,
        in_LeadDis,
        in_DEA_Name,
        in_PROC,
        in_CTRS,
        in_PM_Name,
        in_RE_Name,
        in_STAG,
        in_SORT,
        in_ES,
        in_EF,
        in_BIDS,
        in_AWRD,
        in_PARV,
        in_FD,
        in_SC,
        in_EEST,
        in_BID,
        in_AWD,
        in_chargecode,
        in_CM923ST,
        in_CM923SG,
        in_X0SUB,
        in_X90SUB,
        in_X00SUB,
        in_Sandy,
        in_messages,
        in_events_lyr, 
        in_token]
        
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
        
        in_start_point = parameters[0].value
        in_end_point = parameters[1].value
        in_PID = parameters[2].value
        in_CAP = parameters[3].value
        in_C_Cntr = parameters[4].value
        in_Title = parameters[5].value
        in_LineDept = parameters[6].value
        in_FACY = parameters[7].value
        in_Facility = parameters[8].value
        in_CPOP = parameters[9].value
        in_LeadDis = parameters[10].value
        in_DEA_Name = parameters[11].value
        in_PROC = parameters[12].value
        in_CTRS = parameters[13].value
        in_PM_Name = parameters[14].value
        in_RE_Name = parameters[15].value
        in_STAG = parameters[16].value
        in_SORT = parameters[17].value
        in_ES = parameters[18].value
        in_EF = parameters[19].value
        in_BIDS = parameters[20].value
        in_AWRD = parameters[21].value
        in_PARV = parameters[22].value
        in_FD = parameters[23].value
        in_SC = parameters[24].value
        in_EEST = parameters[25].value
        in_BID = parameters[26].value
        in_AWD = parameters[27].value
        in_chargecode = parameters[28].value
        in_CM923ST = parameters[29].value
        in_CM923SG = parameters[30].value
        in_X0SUB = parameters[31].value
        in_X90SUB = parameters[32].value
        in_X00SUB = parameters[33].value
        in_Sandy = parameters[34].value
        in_messages = parameters[35].value
        in_events_lyr = parameters[36].value
        in_token = parameters[37].value

        # 2. Create request to world routing NA service
        
        # paths, length = self.getRoutes(in_start_point, in_end_point, in_token)
        paths = self.getShortestRoute(in_start_point, in_end_point, in_token)
        
        # 4. Use the geometry from the response JSON to send an applyEdits request to the target feature service of construction events.
        
        update_base_url = "{0}/{1}".format(in_events_lyr, "applyEdits")
        
        route_attr_payload = '"AnalysisSettings":null,"Version":null,"RouteName":null,"TotalMinutes":null,"TotalMeters":null,"TotalLateMinutes":null,"TotalWaitMinutes":null,"TotalCosts":null,"StartTime":null,"StartUTCOffset":null,"EndTime":null,"EndUTCOffset":null,"Messages":null'

        fc_attr_payload = '"pid":{0},"cap":{1},"c_cntr":{2},"title":{3},"linedept":{4},"facy":{5},"facility":{6},"cpop":{7},"leaddis":{8},"dea_name":{9},"proc":{10},"ctrs":{11},"pm_name":{12},"re_name":{13},"stag":{14},"sort":{15},"es":{16},"ef":{17},"bids":{18},"awrd":{19},"parv":{20},"fd":{21},"sc":{22},"eest":{23},"bid":{24},"awd":{25},"chargecode":{26},"cm923st":{27},"cm923sg":{28},"x0sub":{29},"x90sub":{30},"x00sub":{31},"sandy_project_flag":{32},"messages":{33}'.format(in_PID, in_CAP, in_C_Cntr, in_Title, in_LineDept, in_FACY, in_Facility, in_CPOP, in_LeadDis, in_DEA_Name, in_PROC, in_CTRS, in_PM_Name, in_RE_Name, in_STAG, in_SORT, in_ES, in_EF, in_BIDS, in_AWRD, in_PARV, in_FD, in_SC, in_EEST, in_BID, in_AWD, in_chargecode, in_CM923ST, in_CM923SG, in_X0SUB, in_X90SUB, in_X00SUB, in_Sandy, in_messages)

        full_attr_payload = route_attr_payload + "," + fc_attr_payload

        manual_adds = '[{{"geometry": {{"paths": {0}}},"attributes":{{{1}}}}}]'.format(paths, full_attr_payload)
        payload = {'f': 'json', 'adds': manual_adds}

        arcpy.AddMessage("Base URL:")
        arcpy.AddMessage(update_base_url)

        arcpy.AddMessage("Payload:")
        arcpy.AddMessage(payload)

        update_result = requests.post(update_base_url, data=payload)
        update_result_json = update_result.json()
        arcpy.AddMessage(str(update_result_json))