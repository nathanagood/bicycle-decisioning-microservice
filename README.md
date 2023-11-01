# Example Open Liberty Microservice for Calling ADS Rules

This is an example Java project, deployed as a [microservice](https://en.wikipedia.org/wiki/Microservices)
using [OpenLiberty.io](https://openliberty.io/) that can be packaged and deployed
as a war or as a container that you can run with [Podman](https://podman.io/) or install in 
[OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) 
as a [Deployment](https://docs.openshift.com/container-platform/4.14/applications/deployments/what-deployments-are.html).

The single service endpoint, found at `${WS ROOT}/decisionws/api/bicycleTypeCalculator`,
exposes a HTTP POST operation that accepts a JSON object and returns a 
result in _text/plain_ format. Using the information provided to it in the POST
body, the web service uses an operation designed and developed in IBM [Automation Decision Service](https://www.ibm.com/products/automation-decision-services) (ADS) 
to evaluate rules and return the result of the evaluation.

The goal of this example is to demonstrate how rules could be developed in ADS
and used even in an external system, such as a microservice. The rules are 
updated in this particular project just like any other Maven dependency.

> **It should be noted that you can deploy and execute your rules in ADS
> using the platform. See details [here](https://www.ibm.com/docs/en/cloud-paks/cp-biz-automation/23.0.1?topic=services-deploying-decision-runtime-rest-api).**

See the companion project, which contains the actual rules, at 
https://github.com/nathanagood/bicycle-decisioning-service-test. The project
was developed basically by just following the ADS [Getting Started tutorial](https://www.ibm.com/docs/en/cloud-paks/cp-biz-automation/23.0.1?topic=started-task-1-making-decision-service). More information can be found
in the README in that project.

## Developing this project

When I created this project, I followed these steps:

1. With ADS installed, I developed a sample [decision automation](https://www.ibm.com/docs/en/cloud-paks/cp-biz-automation/23.0.1?topic=started-task-1-making-decision-service#s1__title__1) by following the
the ["Getting Started" ](https://www.ibm.com/docs/en/cloud-paks/cp-biz-automation/23.0.1?topic=resources-getting-started) tutorial.
1. I connected a GitHub repository using the instructions [here](https://www.ibm.com/docs/en/cloud-paks/cp-biz-automation/23.0.1?topic=gs-task-2-connecting-git-repository-sharing-decision-service) and used
ADS to deploy my code to the repository. 
That repository can be found [here](https://github.com/nathanagood/bicycle-decisioning-service-test).
1. I pulled the code from the repository, built it, and installed it into my
Maven repository.
1. With the ADS decision project installed in Maven, I went to "[Get started with Open Liberty](https://openliberty.io/start/)" and created this project.
1. I added the rule project to this project's `pom.xml` file. 
1. I used a combination of the documentation at https://www.ibm.com/docs/en/cloud-paks/cp-biz-automation/23.0.1?topic=api-executing-decision-operation and [this example](https://github.com/icp4a/automation-decision-services-samples/blob/master/samples/ExecutionApiSample/src/main/java/com/ibm/ads/samples/LoanApproval.java)
to create the service in `BicycleResource`.
1. I added the references to the `execution-api` and the `engine-de-api`. The
`pom.xml` file has comments with more information.
1. I had to add a couple Jackson dependencies. They are also commented in `pom.xml`.

## Building

To build this project, clone this repo then run the command:

```bash
./mvnw compile
```

Remember, you will need to have the repository that has the IBM ADS artifacts 
in it configured in Maven. One of the easiest ways to do that is the `settings.xml`
file, which is documented in greater detail [here](https://maven.apache.org/settings.html).

## Running in Open Liberty

To run this project in Open Liberty locally, use the commands `./mvnw liberty:dev`
to start Open Liberty in dev mode or use `./mvnw liberty:start` to start it in
the background. See "[Starting and stopping Open Liberty in the background](https://openliberty.io/guides/getting-started.html#starting-and-stopping-open-liberty-in-the-background)" for more details.

## Running in a container

The `Dockerfile` was generated with the project, but it allows you to build
and deploy this service as a container. As a container, you can either run this
on any container platform, or you can deploy this to [Red Hat Openshift]().

To build the container with `podman`, use this command, where _decisionws_ is the
tag given to the container.

```bash
podman build -t decisionws .
```

Then, to run the container on the same machine, use the following command to run
it in interactive mode so you can see all the logs:

```bash
podman run -it -p 9080:9080 decisionws
```
