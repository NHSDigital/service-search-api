"use strict";

const log = require("loglevel");
const searchPostcodeOrPlaceResponse = require("./responses/search-postcode_v2.json");
const organisationsResponse = require("./responses/organisations_v2.json");
const organisationsNotFoundResponse = require("./responses/organisations-not-found_v2.json");
const organisationsSingleResponse = require("./responses/organisations-single_v2.json");
const searchPostcodeOrPlaceInvalidResponse = require("./responses/search-postcode-invalid_v2.json");
const searchPostcodeOrPlaceNotFoundResponse = require("./responses/search-postcode-not-found_v2.json");
const organisationTypesResponse = require("./responses/organisation-types_v1.json");
const organisationTypesNotFoundResponse = require("./responses/organisation-types-not-found_v1.json");
const organisationTypesSingleItemResponse = require("./responses/organisation-types-single-item_v1.json");

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
  if (queryStringParameters?.["api-version"] !== "1") {
    res.status(404).json({ statusCode: 404, message: "Resource not found" });
  } else if (queryStringParameters?.["search"].toLowerCase() === "pharmacy") {
    res.status(200).json(organisationTypesSingleItemResponse);
  } else if (queryStringParameters?.["search"].toLowerCase() === "nothing") {
    res.status(200).json(organisationTypesNotFoundResponse);
  } else {
    res.json(organisationTypesResponse);
  }

  res.end();
  next();
}

async function searchPostcodeOrPlace(req, res, next) {
  const queryStringParameters = req?.query;
  if (queryStringParameters?.["api-version"] !== "2") {
    res.status(404).json({ statusCode: 404, message: "Resource not found" });
  } else if (!queryStringParameters?.["search"]) {
    // No search parameter is a 404 without a body (this is returned from the backend service)
    res.status(404);
  } else if (queryStringParameters?.["search"].toLowerCase() === "manchester") {
    res.status(200).json(searchPostcodeOrPlaceResponse);
  } else if (queryStringParameters?.["search"].toLowerCase() === "ls42pb") {
    res.status(500).json(searchPostcodeOrPlaceNotFoundResponse);
  } else {
    res.status(500).json(searchPostcodeOrPlaceInvalidResponse);
  }

  res.end();
  next();
}

async function organisations(req, res, next) {
  const queryStringParameters = req?.query;
  if (queryStringParameters?.["api-version"] !== "2") {
    res.status(404).json({ statusCode: 404, message: "Resource not found" });
  } else if (queryStringParameters?.["search"] === "no-organisation") {
    res.status(200).json(organisationsNotFoundResponse);
  } else if (queryStringParameters?.["search"] === "DN601") {
    res.status(200).json(organisationsSingleResponse);
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
