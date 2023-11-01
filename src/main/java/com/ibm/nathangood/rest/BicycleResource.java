package com.ibm.nathangood.rest;

import java.util.UUID;
import java.util.logging.Logger;

import com.ibm.decision.run.DecisionRunner;
import com.ibm.decision.run.RunContext;
import com.ibm.decision.run.provider.ClassLoaderDecisionRunnerProvider;
import com.ibm.decision.run.provider.DecisionRunnerProvider;
import com.ibm.decision.run.trace.Trace;
import com.ibm.decision.run.trace.TraceConfiguration;
import com.ibm.nathangood.bicyclemodel.bicycle_Model.Input;

import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

/**
 * Call this with something like:
 * 
 * ```
 * cat ./src/test/resources/gravelBike.json| http POST
 * :9080/decisionws/api/bicycleTypeCalculator
 * ```
 * Assuming you have [HTTPie](https://httpie.io/) installed.
 * 
 * See https://openliberty.io/guides/microprofile-openapi.html for information
 * about how to fully document these APIs.
 * 
 */
@Path("bicycleTypeCalculator")
public class BicycleResource {
    private static final Logger LOG = Logger.getLogger(RestApplication.class.getName());

    @POST
    @Produces(MediaType.TEXT_PLAIN)
    @Consumes(MediaType.APPLICATION_JSON)
    public String getBicycleType(BicycleInput input) {
        LOG.info("Evalutating rules now...");

        // Here, we load the rules using the decision service and submit the
        // input as the JSON document. Here, the model expected by the rules
        // and the model expected by the web service are the same, but they
        // don't necessarily have to be. Using more of a MVVM approach here, where
        // the model expected and returned by the services can be thought of as
        // the "View Model", then there is a level of abstraction between the two.

        // This code borrowed heavily from the sample here:
        // https://github.com/icp4a/automation-decision-services-samples/blob/master/samples/ExecutionApiSample/src/main/java/com/ibm/ads/samples/LoanApproval.java

        // Here, instead of loading the file from the file system, we will use
        // the class loader because the JAR was added to the classpath by Maven
        DecisionRunnerProvider provider = new ClassLoaderDecisionRunnerProvider.Builder()
                .build();


        // If you're looking at code, get this from the <name> element in the
        // model's `operation.dop` file.
        //
        DecisionRunner runner = provider.getDecisionRunner("Bicycle-Model");

        // Set up tracing so we can log this out...
        // trace config
        TraceConfiguration trace = new TraceConfiguration() {
            {
                printedMessages = true;
                rules.allRules = true;
                rules.executedRules = true;
                rules.nonExecutedRules = true;
            }
        };

        RunContext context = runner.createRunContext("UniqueID_" + UUID.randomUUID());
        context.setTraceConfiguration(trace);

        // Need to use the same type of object the rule expects.
        // See https://www.ibm.com/docs/en/cloud-paks/cp-biz-automation/23.0.1?topic=api-executing-decision-operation
        Input in = new Input();
        in.gearing = (double)input.getGearing();
        in.geometry = input.getGeometry();
        in.tireSize = (long)input.getTireSize();

        Object out = runner.execute(in, context);
        Trace t = context.getTrace();
        if (t != null) {
            t.printedMessages.forEach(m -> LOG.info(m.toString()));
            t.exceptionsRaised.forEach(e -> LOG.severe(e.toString()));
        }

        String result = out.toString();
        return result;
    }
}
