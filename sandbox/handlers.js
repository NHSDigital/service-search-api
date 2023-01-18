"use strict";

const log = require("loglevel");
const searchPostcodeOrPlaceResponse = require("./responses/search-postcode_v2.json");
const organisationsResponse = require("./responses/organisations_v2.json");
const organisationsNotFoundResponse = require("./responses/organisations-not-found_v2.json");
const organisationsSingleResponse = require("./responses/organisations-single_v2.json");
const searchPostcodeOrPlaceInvalidResponse = require("./responses/search-postcode-invalid_template_v2.json");
const organisationTypesResponse = require("./responses/organisation-types_v1.json");
const organisationTypesNotFoundResponse = require("./responses/organisation-types-not-found_v1.json");
const organisationTypesSingleItemResponse = require("./responses/organisation-types-single-item_v1.json");
const resourceNotFound = require("./responses/bad-api-version-resource-not-found.json");

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
    res.status(200).json(searchPostcodeOrPlaceResponse);
  } else {
    res.status(500).json(populateSearchPostcodeOrPlaceInvalidResponse(search));
  }

  res.end();
  next();
}

async function organisations(req, res, next) {
  const queryStringParameters = req?.query;
  const search = queryStringParameters?.["search"];
  const searchParamWasProvided = typeof search === "string";

  if (queryStringParameters?.["api-version"] !== "2") {
    res.status(404).json(resourceNotFound);
  } else if (search === "DN601") {
    res.status(200).json(organisationsSingleResponse);
  } else if (searchParamWasProvided) {
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
};
