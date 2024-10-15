
const request = require("supertest");
const assert = require("chai").assert;
// const expect = require("chai").expect;

const organisationsSingleResponse = require("./responses/organisations-single_v3.json");
const organisationsAllResponse = require("./responses/organisations_v3.json");
const organisationsNotFoundResponse = require("./responses/organisations-not-found_v3.json");
const organisationByOdsCodeFilteredResponse = require("./responses/search-organisations-service-code-filtered-response.json");
const organisationByNameFilteredResponse = require("./responses/search-organisations-by-name-filtered-response.json");
const organisationByLocationResponse = require("./responses/search-organisations-location-response.json")
const organisationByGeocodeFilteredResponse = require("./responses/search-organisations-geocode-filtered-response.json");
const organisationsByNearestFilteredResponse = require("./responses/search-organisations-by-nearest-filter-postcode-response.json");
const organisationsByClosingTime = require("./responses/search-organisation-closing-time-city-filtered.json")


describe("app handler tests", function () {
    let server;
    let env;
    const version_info = {
        build_label:"1233-shaacdef1",
        releaseId:"1234",
        commitId:"acdef12341ccc"
    };

    before(function () {
        env = process.env;
        let app = require("./app");
        app.setup({
            VERSION_INFO: JSON.stringify(version_info),
            LOG_LEVEL: (process.env.NODE_ENV === "test" ? "warn": "debug")
        });
        server = app.start();
    });

    after(function () {
        process.env = env;
        server.close();
    });

    it("responds to /_ping", (done) => {
        request(server)
            .get("/_ping")
            .expect(200, {
                status: "pass",
                ping: "pong",
                service: "service-search-api",
                version: version_info
            })
            .expect("Content-Type", /json/, done);
    });

    it("responds to /_status", (done) => {
        request(server)
            .get("/_status")
            .expect(200, {
                status: "pass",
                ping: "pong",
                service: "service-search-api",
                version: version_info
            })
            .expect("Content-Type", /json/, done);
    });

    it("GET A single organisation", (done) => {
        request(server)
            .get("/?search=Y02494&api-version=3")
            .expect(200, organisationsSingleResponse)
            .expect("Content-Type", /json/, done);
    });

    it("POST A single organisation", (done) => {
        request(server)
            .post("/?&api-version=3")
            .send({
                "search": "Y02494",
                "searchFields": "ODSCode",
                "top": 1,
                "select": "*"
            })
            .expect(200, organisationsSingleResponse)
            .expect("Content-Type", /json/, done);
    });

    it("GET All organisations", (done) => {
        request(server)
            .get("/?api-version=3")
            .expect(200, organisationsAllResponse)
            .expect("Content-Type", /json/, done);
    });

    it("POST All organisations", (done) => {
        request(server)
            .post("/?api-version=3")
            .send({
                "search": "*"
            })
            .expect(200, organisationsAllResponse)
            .expect("Content-Type", /json/, done);
    });

    it("GET Organisation filtered by EPS enabled", (done) => {
        request(server)
            .get("?searchFields=ODSCode&$filter=IsEpsEnabled eq 'true'&api-version=3")
            .expect(200, organisationByOdsCodeFilteredResponse)
            .expect("Content-Type", /json/, done);
    });

    it("POST Organisation filtered by EPS enabled", (done) => {
        request(server)
            .post("/?api-version=3")
            .send({
                "search": "FKH23",
                "searchMode": "all",
                "searchFields": "ODSCode",
                "top": 10,
                "count": true,
                "select": "ODSCode,OrganisationName,Contacts,Address1,Address2,Address3,City,Postcode,OrganisationType,OrganisationSubType",
                "filter": "IsEpsEnabled eq 'true'"
            })
            .expect(200, organisationByOdsCodeFilteredResponse)
            .expect("Content-Type", /json/, done);
    });

    it("GET Organisation by name, filtered by EPS enabled and organisation type", (done) => {
        request(server)
            .get("?search=pharmacy2u&searchFields=OrganisationName&$filter=IsEpsEnabled eq 'true' and OrganisationTypeId eq 'PHA' and OrganisationSubType eq 'DistanceSelling'&api-version=3")
            .expect(200, organisationByNameFilteredResponse)
            .expect("Content-Type", /json/, done);
    });

    it("POST Organisation by name, filtered by EPS enabled and organisation type", (done) => {
        request(server)
            .post("/?api-version=3")
            .send({
                "search": "pharmacy2u", 
                "searchMode": "all",
                "searchFields": "OrganisationName",
                "top": 10,
                "count": true,
                "select": "ODSCode,OrganisationName,Contacts,Address1,Address2,Address3,City,Postcode,OrganisationType,OrganisationSubType",
                "filter": "IsEpsEnabled eq 'true' and OrganisationTypeId eq 'PHA' and OrganisationSubType eq 'DistanceSelling'"
            })
            .expect(200, organisationByNameFilteredResponse)
            .expect("Content-Type", /json/, done);
    });

    it("GET Organisation by location", (done) => {
        request(server)
            .get("?search=Bletchley&searchFields=Address3,City,County&api-version=3")
            .expect(200, organisationByLocationResponse)
            .expect("Content-Type", /json/, done);
    });

    it("POST Organisation by location", (done) => {
        request(server)
            .post("/?api-version=3")
            .send({
                "search": "Bletchley",
                "searchMode": "all",
                "searchFields": "Address3,City,County",
                "top": 10,
                "count": true,
                "select": "Latitude,Longitude,Address3,City,County,Postcode" 
            })
            .expect(200, organisationByLocationResponse)
            .expect("Content-Type", /json/, done);
    });

    it("GET Organisation filtered by location and type ordered by geocode", (done) => {
        request(server)
            .get("?$filter=IsEpsEnabled eq 'true' and OrganisationTypeId eq 'PHA' and OrganisationSubType eq 'Community'&$orderby=geo.distance(Geocode, geography'POINT(-0.76444095373153675 52.000820159912109)')&api-version=3")
            .expect(200, organisationByGeocodeFilteredResponse)
            .expect("Content-Type", /json/, done);
    });

    it("POST Organisation filtered by location and type ordered by geocode", (done) => {
        request(server)
            .post("/?api-version=3")
            .send({
                "search": "*", 
                "searchMode": "all", 
                "searchFields": "*", 
                "top": 10, 
                "count": true, 
                "select": "ODSCode,OrganisationName,Contacts,Address1,Address2,Address3,City,Postcode,OrganisationSubType",
                "filter": "IsEpsEnabled eq 'true' and OrganisationTypeId eq 'PHA' and OrganisationSubType eq 'Community'", 
                "orderby": "geo.distance(Geocode, geography'POINT(-0.76444095373153675 52.000820159912109)')"
            })
            .expect(200, organisationByGeocodeFilteredResponse)
            .expect("Content-Type", /json/, done);
    });

    it("GET Organisation filtered by postcode, EPS enabled and organisation type", (done) => {
        request(server)
            .get("?$filter=search.ismatch('B11', 'Postcode') and IsEpsEnabled eq 'true' and OrganisationTypeId eq 'PHA' and OrganisationSubType eq 'Community'&api-version=3")
            .expect(200, organisationsByNearestFilteredResponse)
            .expect("Content-Type", /json/, done);
    });

    it("POST Organisation filtered by postcode, EPS enabled and organisation type", (done) => {
        request(server)
            .post("/?api-version=3")
            .send({	
                "search": "*",
                "searchMode": "all",
                "searchFields": "*",
                "top": 10,
                "count": true,
                "select": "ODSCode, OrganisationType, OrganisationSubType, OrganisationName, Contacts, Address1, Address2, Address3, City, Postcode, Latitude, Longitude",
                "filter": "search.ismatch('B11', 'Postcode') and IsEpsEnabled eq 'true' and OrganisationTypeId eq 'PHA' and OrganisationSubType eq 'Community'"
            })
            .expect(200, organisationsByNearestFilteredResponse)
            .expect("Content-Type", /json/, done);
    });

    it("GET Organisation not found", (done) => {
        request(server)
            .get("?search=no-organisation&api-version=3")
            .expect(200, organisationsNotFoundResponse)
            .expect("Content-Type", /json/, done);
    });

    it("POST Organisation not found", (done) => {
        request(server)
            .post("/?api-version=3")
            .send({
                "search": "no-organisation",
                "searchFields": "ODSCode",
                "top": 1,
                "select": "*"
            })
            .expect(200, organisationsNotFoundResponse)
            .expect("Content-Type", /json/, done);
    });

    it("GET single organisation by closing time", (done) => {
        request(server)
            .get("?search=Bletchley&searchFields=Address3&api-version=3&$filter=OpeningTimes / any (x: x/ClosingTime eq '14:00')")
            .expect(200, organisationsByClosingTime)
            .expect("Content-Type", /json/, done);
    });
});