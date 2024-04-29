"use strict";

const log = require("loglevel");
const searchPlaceResponse = require("./responses/search-place_v2.json");
const searchPostcodeResponse = require("./responses/search-postcode_v2.json");
const organisationsResponse = require("./responses/organisations_v2.json");
const organisationsNotFoundResponse = require("./responses/organisations-not-found_v3.json");
const organisationsSingleResponse = require("./responses/organisations-single_v3.json");
const searchPostcodeOrPlaceInvalidResponse = require("./responses/search-postcode-invalid_template_v2.json");
const organisationTypesResponse = require("./responses/organisation-types_v1.json");
const organisationTypesNotFoundResponse = require("./responses/organisation-types-not-found_v1.json");
const organisationTypesSingleItemResponse = require("./responses/organisation-types-single-item_v1.json");
const resourceNotFound = require("./responses/bad-api-version-resource-not-found.json");
const organisationByOdsCodeFilteredResponse = require("./responses/search-organisations-service-code-filtered-response.json");
const organisationByNameFilteredResponse = require("./responses/search-organisations-by-name-filtered-response.json");
const organisationByLocationResponse = require("./responses/search-organisations-location-response.json")
const organisationByGeocodeFilteredResponse = require("./responses/search-organisations-geocode-filtered-response.json");
const organisationsByNearestFilteredResponse = require("./responses/search-organisations-by-nearest-filter-postcode-response.json");

const filterByServiceCode = "Services / any (x: x/ServiceCode eq 'EPS0001')";
const filterByServiceCodeAndOrganisationTypeDistance =  "Services / any (x: x/ServiceCode eq 'EPS0001') and OrganisationTypeId eq 'PHA' and OrganisationSubType eq 'DistanceSelling'";
const filterByServiceCodeAndOrganisationTypeCommunity = "Services / any (x: x/ServiceCode eq 'EPS0001') and OrganisationTypeId eq 'PHA' and OrganisationSubType eq 'Community'";
const orderByGeocode = "geo.distance(Geocode, geography'POINT(-0.76444095373153675 52.000820159912109)')";
const filterByPostcodeServiceCodeOrganisationType = "search.ismatch('B11', 'Postcode') and Services / any (x: x/ServiceCode eq 'EPS0001') and OrganisationTypeId eq 'PHA' and OrganisationSubType eq 'Community'"

function populateSearchPostcodeOrPlaceInvalidResponse(search) {
  const response = Object.assign({}, searchPostcodeOrPlaceInvalidResponse);
  Object.keys(response).forEach((key) => {
    response[key] = response[key].replace(/REPLACE_ME/g, search);
  });
  return response;
}

async function status(req, res, next) {
  res.json({
    status: "pass",
    ping: "pong",
    service: req.app.locals.app_name,
    version: req.app.locals.version_info,
  });
  res.end();
  next();
}

async function organisationTypes(req, res, next) {
  const queryStringParameters = req?.query;
  const _search = queryStringParameters?.["search"];
  const search = typeof _search === "string" ? _search.toLowerCase() : null;
  if (queryStringParameters?.["api-version"] !== "1") {
    res.status(404).json(resourceNotFound);
  } else if (search === "pharmacy") {
    res.status(200).json(organisationTypesSingleItemResponse);
  } else if (search !== null) {
    res.status(200).json(organisationTypesNotFoundResponse);
  } else {
    res.status(200).json(organisationTypesResponse);
  }

  res.end();
  next();
}

async function searchPostcodeOrPlace(req, res, next) {
  const queryStringParameters = req?.query;
  const search = (queryStringParameters?.["search"] || "").toLowerCase();
  if (queryStringParameters?.["api-version"] !== "2") {
    res.status(404).json(resourceNotFound);
  } else if (search === "manchester") {
    res.status(200).json(searchPlaceResponse);
  } else if (search === "wc1n 3jh") {
    res.status(200).json(searchPostcodeResponse);
  } else {
    res.status(500).json(populateSearchPostcodeOrPlaceInvalidResponse(search));
  }

  res.end();
  next();
}

async function organisations(req, res, next) {
  req.body
  const queryStringParameters = req?.query;
  const search = queryStringParameters?.["search"];
  const searchFields = queryStringParameters?.["searchFields"];
  const filter = queryStringParameters?.["$filter"];
  const orderBy = queryStringParameters?.["$orderby"];
  const searchParamWasProvided = typeof search === "string";
  
  if (queryStringParameters?.["api-version"] !== "3") {
    res.status(404).json(resourceNotFound);
  } else if (search === "Y02494") {
    res.status(200).json(organisationsSingleResponse);
  } else if(searchFields === "ODSCode" && filter === filterByServiceCode) {
    res.status(200).json(organisationByOdsCodeFilteredResponse);
  } else if(search === "pharmacy2u" && searchFields === "OrganisationName" && filter === filterByServiceCodeAndOrganisationTypeDistance) {
    res.status(200).json(organisationByNameFilteredResponse);
  } else if(search === "Bletchley" && searchFields === "Address3,City,County") {
    res.status(200).json(organisationByLocationResponse);
  } else if(filter === filterByServiceCodeAndOrganisationTypeCommunity && orderBy === orderByGeocode) {
    res.status(200).json(organisationByGeocodeFilteredResponse);
  } else if(filter === filterByPostcodeServiceCodeOrganisationType) {
    res.status(200).json(organisationsByNearestFilteredResponse);
  } else if (searchParamWasProvided) {
    res.status(200).json(organisationsNotFoundResponse);
  } else {
    res.status(200).json(organisationsResponse);
  }

  res.end();
  next();
}

async function organisationsPost(req, res, next) {
  const queryStringParameters = req?.query;
  const postBody = req?.body;
  const search = postBody?.["search"];
  const searchFields = postBody?.["searchFields"]
  const filter = postBody?.["filter"];
  const orderBy = postBody?.["orderby"];
  const bodyWasProvided = typeof postBody === "object";

  if (queryStringParameters?.["api-version"] !== "3") {
    res.status(404).json(resourceNotFound);
  } else if (search === "Y02494") {
    res.status(200).json(organisationsSingleResponse);
  } else if(searchFields === "ODSCode" && filter === filterByServiceCode) {
    res.status(200).json(organisationByOdsCodeFilteredResponse)
  } else if(search === "pharmacy2u" && searchFields === "OrganisationName" && filter === filterByServiceCodeAndOrganisationTypeDistance) {
    res.status(200).json(organisationByNameFilteredResponse)
  } else if(search === "Bletchley"  && searchFields === "Address3,City,County") {
    res.status(200).json(organisationByLocationResponse)
  } else if(filter === filterByServiceCodeAndOrganisationTypeCommunity && orderBy === orderByGeocode) {
    res.status(200).json(organisationByGeocodeFilteredResponse);
  } else if(filter === filterByPostcodeServiceCodeOrganisationType) {
    res.status(200).json(organisationsByNearestFilteredResponse);
  } else if (!bodyWasProvided || search === "no-organisation") {
    res.status(200).json(organisationsNotFoundResponse);
  } else {
    res.status(200).json(organisationsResponse);
  }

  res.end();
  next();
}

module.exports = {
  status: status,
  organisationTypes,
  searchPostcodeOrPlace,
  organisations,
  organisationsPost
};
