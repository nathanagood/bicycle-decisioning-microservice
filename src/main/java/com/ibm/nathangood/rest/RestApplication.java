package com.ibm.nathangood.rest;

import java.util.logging.Logger;

import jakarta.ws.rs.ApplicationPath;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.Application;
import jakarta.ws.rs.core.MediaType;

/**
 * There is certainly a way that you can call this with the built-in ADS endpoint
 * and avoid writing your own microservice. But, because of some abstraction this
 * could give you as well as deployment choices, this may be a good option.
 * 
 * See https://www.ibm.com/docs/en/cloud-paks/cp-biz-automation/23.0.1?topic=runtime-calling-decision-services
 * for more information about calling the ADS endpoints directly.
 */
@ApplicationPath("/api")
public class RestApplication extends Application {
}
