# Compatibility Guide

### Introduction

Cardinal uses [scout](https://github.com/cardinal-dev/scout) to communicate with autonomous Cisco access points (APs) over SSH.
scout can perform actions like gathering AP information and modifying AP configurations. Currently, the CI/CD 
pipeline is limited when it comes to test coverage of various Cisco AP models. The following table will act as a compatibility guide 
for all Cardinal users. AP models will be categorized into two classifications: Supported and Community-Based.

### Support Classifications

APs with the "Supported" designation indicate compatibility with Cardinal environments. The CI/CD pipeline
tests against models with a "Supported" designation. Users can submit issues for bugs and feature requests upstream. Fixes
will be addressed by the Cardinal project.

APs with the "Community-Based" designation indicate limited supportability when it comes to Cardinal usage. AP models are reported, 
in good faith, from the community. When reporting an AP model as Community-Based, Cardinal community members will be politely asked 
to provide a GitHub handle for contact purposes. Providing a GitHub handle will enable other Cardinal users who may be using a Community-Based model 
to ask for assistance or to test functionality that may not be tested in the upstream. Cardinal community members can also submit issues
and PRs for upstream fixes. However, core functionality will be prioritized to "Supported" AP models. Additional verifications may be required
before upstream merges occur.

### Community-Based Approval Process

In order to add a new AP model for Cardinal compatibility, please follow these instructions:

1. Open an issue report under the cardinal-dev/Cardinal [repository](https://github.com/cardinal-dev/Cardinal/issues)
2. Name the issue report in a way that identifies the ask (e.g. [Proposal] Add Cisco 2702i to Cardinal compatibility guide)
3. Submit supplemental information that describes proof of functionality. You can prove functionality by running tests from [scout/ci/tests](https://github.com/cardinal-dev/scout/tree/main/ci/tests) and paste the redacted output of the tests to the report
4. Please note the GitHub handle used to submit the proposal will be the handle added to the `Verified By` column
5. Once approved, a PR will be opened against cardinal-dev/Cardinal to add the entry into the `Official Compatibility Guide`

If anyone has any questions or feedback on the preceding processes, please submit an issue report to cardinal-dev/Cardinal.

### Official Compatibility Table

| Access Point Model | Support Designation | Verified By         |
| ------------------ | ------------------- | ------------------- |
| Cisco 1142N        | Supported           | Cardinal Project    |
| Cisco 3602i        | Supported           | Cardinal Project    |
