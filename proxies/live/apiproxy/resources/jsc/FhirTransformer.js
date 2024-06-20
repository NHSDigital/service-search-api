var HealthcareServiceSchema = {
    "resourceType": "HealthcareService",
    "id": "example",
    "contained": [{
            "resourceType": "Location",
            "id": "Address",
            "description": "",
            "mode": "instance",
            "address": {},
            "position": {},
            "physicalType": {
                "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/location-physical-type",
                        "code": "bu",
                        "display": "Building"
                    }
                ]
            }
        }
    ],
    "identifier": [],
    "active": true,
    "providedBy": {},
    "category": [],
    "location": [{
            "reference": "#Address"
        }
    ],
    "name": "",
    "coverageArea": [{
            "reference": "#Address"
        }
    ],
}
 
var bundle = {
    "resourceType": "Bundle",
    "id": "9A05D8C6-587D-4CD7-B360-C5560961C01F",
    "type": "searchset",
    "total": 1,
    "link": [{
            "relation": "self",
            "url": "https://api.service.nhs.uk/service-search-api"
        }
    ],
    "entry": []
}
 
//functions
function contactMap(contactType) {
    var newtype = "";
 
    switch (contactType) {
    case "Telephone":
        newtype = "phone";
        break;
    case "Email":
        newtype = "email";
        break;
    case "Website":
        newtype = "url";
    }
    return newtype;
}
 
function dayMap(day) {
    var newtype = "";
 
    switch (day) {
    case "Monday":
        newtype = "mon";
        break;
    case "Tuesday":
        newtype = "tue";
        break;
    case "Wednesday":
        newtype = "wed";
        break;
    case "Thursday":
        newtype = "thu";
        break;
    case "Friday":
        newtype = "fri";
        break;
    case "Saturday":
        newtype = "sat";
        break;
    case "Sunday":
        newtype = "sun";
        break;
    }
    return newtype;
}
 
function timeFix(time) {
    return time + ":00";
}
 
function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}
 
function insertDualToHS(node, name1, val1, name2, val2) {
    node[name1] = val1;
    node[name2] = val2;
}
 
function createContact(system, value, use) {
    var json = {};
 
    if (system != null)
        json["system"] = system;
    if (value != null)
        json["value"] = value;
    if (use != null)
        json["use"] = "work";
 
    return json;
}
 
function createFacility(system, value, display) {
    var root = {};
    var coding = [];
    var json = {};
 
    if (system != null)
        json["system"] = system;
    if (display != null)
        json["display"] = display;
    if (value != null)
        json["value"] = value;
    coding[0] = json;
    root["coding"] = coding;
 
    return root;
}
 
function createCoding(system, code, display) {
    var root = {};
    var coding = [];
    var json = {};
    if (system != null)
        json["system"] = system;
    if (code != null)
        json["code"] = code;
    if (display != null)
        json["display"] = display;
    coding[0] = json;
    root["coding"] = coding;
 
    return root;
}
//end functions
 
 
function query(data) {
    var total = 0;
    //All Results
    for (var orgkey in data.value) {
        if (data.value.hasOwnProperty(orgkey)) {
            var Organisation = data.value[orgkey];
 
            var HealthcareService = JSON.parse(JSON.stringify(HealthcareServiceSchema));
 
            HealthcareService.id = Organisation.SearchKey;
 
            //Identifiers
            var identifier = {};
            identifier["system"] = "https://fhir.nhs.uk/Id/ods-organization-code";
            identifier["value"] = Organisation.ODSCode;
            HealthcareService.identifier[0] = identifier;
 
            //Provided By
            insertDualToHS(HealthcareService.providedBy, "reference", "https://fhir.nhs.uk/Id/ods-organization-code/" + Organisation.ODSCode, "display", Organisation.OrganisationName);
 
            //address
            var address = {};
            var topline = [];
            var lineNum = 0
                if (Organisation.Address1 != null && Organisation.Address1 != "") {
                    topline[lineNum] = Organisation.Address1;
                    lineNum++;
                }
                if (Organisation.Address2 != null && Organisation.Address2 != "") {
                    topline[lineNum] = Organisation.Address2;
                    lineNum++;
                }
                if (Organisation.Address3 != null && Organisation.Address3 != "") {
                    topline[lineNum] = Organisation.Address3;
                    lineNum++;
                }
                address["line"] = topline;
            if (Organisation.City != null && Organisation.City != "")
                address["city"] = Organisation.City;
            if (Organisation.County != null && Organisation.County != "")
                address["district"] = Organisation.County;
            if (Organisation.Postcode != null && Organisation.Postcode != "")
                address["postalCode"] = Organisation.Postcode;
            HealthcareService.contained[0].description = "Main Address";
            HealthcareService.contained[0].address = address;
            HealthcareService.contained[0].address.use = "work";
            HealthcareService.contained[0].address.type = "physical";
 
            //Position
            var position = {};
            position["longitude"] = Organisation.Longitude;
            position["latitude"] = Organisation.Latitude;
            position["altitude"] = 0;
            HealthcareService.contained[0].position = position;
 
            //contact
            if (!isEmpty(Organisation.Contacts)) {
                var telecom = [];
                HealthcareService["telecom"] = telecom;
                for (var key in Organisation.Contacts) {
                    if (Organisation.Contacts.hasOwnProperty(key)) {
                        var arr = Organisation.Contacts[key];
                        var json = createContact(contactMap(arr.ContactMethodType), arr.ContactValue, arr.ContactType)
 
                            HealthcareService.telecom[key] = json;
                    };
                };
            };
 
            //comment
            if (Organisation.SummaryText != null)
                HealthcareService["comment"] = Organisation.SummaryText;
 
            //category
            if (Organisation.OrganisationType != null && Organisation.OrganisationType != "") {
                var response = {};
 
                response = createCoding("https://api.service.nhs.uk/service-search-api", Organisation.OrganisationTypeId, Organisation.OrganisationType);
 
                HealthcareService.category[0] = response;
            }
 
            //Services
            if (!isEmpty(Organisation.Services)) {
                var types = [];
                HealthcareService["type"] = types;
                for (var key in Organisation.Services) {
                    if (Organisation.Services.hasOwnProperty(key)) {
                        var arr = Organisation.Services[key];
                        var response = {};
                        response = createCoding("https://api.service.nhs.uk/service-search-api", arr.ServiceCode, arr.ServiceName);
                        HealthcareService.type[key] = response;
                    };
                };
            };
 
            //Opening Hours
            if (!isEmpty(Organisation.OpeningTimes)) {
                var availableTime = [];
                HealthcareService["availableTime"] = availableTime;
                for (var key in Organisation.OpeningTimes) {
                    if (Organisation.OpeningTimes.hasOwnProperty(key)) {
                        var arr = Organisation.OpeningTimes[key];
                        var json = {};
                        var jsonDays = [];
                        jsonDays[0] = dayMap(arr.Weekday);
                        json["daysOfWeek"] = jsonDays;
                        json["availableStartTime"] = timeFix(arr.OpeningTime);
                        json["availableEndTime"] = timeFix(arr.ClosingTime);
                        HealthcareService.availableTime[key] = json;
                    };
                };
            };
 
            //Facilities
            if (!isEmpty(Organisation.Facilities)) {
                var characteristic = [];
                HealthcareService["characteristic"] = characteristic;
                var index = 0;
                for (var key in Organisation.Facilities) {
                    if (Organisation.Facilities.hasOwnProperty(key)) {
                        var arr = Organisation.Facilities[key];
                        var response = {};
                        if (arr.Value == "Yes") {
                            response = createFacility(null, null, arr.Name);
                            HealthcareService.characteristic[index] = response;
                            index++;
                        };
                    };
                };
            };
 
            HealthcareService.name = Organisation.OrganisationName;
 
            var resource = {};
            resource["fullUrl"] = "https://api.service.nhs.uk/service-search-api/" + Organisation.SearchKey;
            resource["resource"] = HealthcareService;
 
            bundle.entry[orgkey] = resource;
            total++
        }
    }
    bundle.total = total;
    return bundle;
}