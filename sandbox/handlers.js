"use strict";

const log = require("loglevel");
const organisationTypesResponse = require("./responses/organisation-types_v1.json");
const searchPostcodeOrPlaceResponse = require("./responses/search-postcode_v2.json");
const organisationsResponse = require("./responses/organisation_v2.json");

const write_log = (res, log_level, options = {}) => {
  if (log.getLevel() > log.levels[log_level.toUpperCase()]) {
    return;
  }
  if (typeof options === "function") {
    options = options();
  }
  let log_line = {
    timestamp: Date.now(),
    level: log_level,
    correlation_id: res.locals.correlation_id,
  };
  if (typeof options === "object") {
    options = Object.keys(options).reduce(function (obj, x) {
      let val = options[x];
      if (typeof val === "function") {
        val = val();
      }
      obj[x] = val;
      return obj;
    }, {});
    log_line = Object.assign(log_line, options);
  }
  if (Array.isArray(options)) {
    log_line["log"] = {
      log: options.map((x) => {
        return typeof x === "function" ? x() : x;
      }),
    };
  }

  log[log_level](JSON.stringify(log_line));
};

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
  if (req?.query?.["api-version"] !== "1") {
    res.status(404).json({ statusCode: 404, message: "Resource not found" });
  } else {
    res.json(organisationTypesResponse);
  }

  res.end();
  next();
}

async function searchPostcodeOrPlace(req, res, next) {
  if (req?.query?.["api-version"] !== "2") {
    res.status(404).json({ statusCode: 404, message: "Resource not found" });
  } else if (!req?.query?.["search"]) {
    // No search parameter is a 404 without a body (this is returned from the backend service)
    res.status(404);
  } else {
    res.status(200).json(searchPostcodeOrPlaceResponse);
  }

  res.end();
  next();
}

async function organisations(req, res, next) {
  if (req?.query?.["api-version"] !== "2") {
    res.status(404).json({ statusCode: 404, message: "Resource not found" });
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
