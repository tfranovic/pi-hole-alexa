Pi-hole Alexa Skill
=========================================

This project is aimed at creating a self-hosted Pi-hole Alexa skill which
allows you to control your Pi-hole setup using your Alexa-enabled devices.

Concepts
--------

This project is built on top of the [Alexa Skills Kit Python SDK](https://pypi.org/project/ask-sdk/)
and should work with any variant of Pi-hole as long as your self-hosted Alexa skill can access it.
It tells you the current status of the Pi-hole and allows to enable or temporarily disable it. It 
also works with screen-enabled devices, displaying a dashboard similar to the one on the Pi-hole
admin panel when not logged in.

Setting up and operating this skill should be almost completely free in terms of AWS costs, but
that also depends on the number of invocations. If your number of invocations does not exceed 1,000,000 a month,
you won't be paying any Lambda price. Same goes for CloudFront/S3.

Examples
------

### Example utterances

```Alexa, start Pi-hole``` - starts Pi-hole skill and shows status, keeps session open

```Alexa, ask Pi-hole the current status``` - shows current status, ends session

```Alexa, ask Pi-hole to disable blocking for 10 minutes``` - disables Pi-hole for 10 minutes, shows status

```Alexa, ask Pi-hole to enable blocking``` - enables Pi-hole, shows status

### Skill response as utterance

```Pi-hole is currently {status}. In the past 24 hours it had {total_queries} queries from {unique_clients} clients, and blocked {blocked} of them ({ads_percentage}%).```

### Skill response as card

<img src="https://d2u7kk3gg326io.cloudfront.net/skill_response_card.png" />

### Skill response as Echo Show UI

<img src="https://d2u7kk3gg326io.cloudfront.net/skill_response_ui.png" />

Setup
-----


### Prerequisites

* **Your Pi-hole needs to be accessible from the public Internet!** - this means you should be able to access the
setup from anywhere by providing a static IP or using a service like [duckdns.org](https://www.duckdns.org/) and
forwarding the necessary port (usually 80) on your router.

* [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) - Create one
here! This is used to deploy the Lambda needed for your Alexa skill.

* [Alexa Developer Account](https://developer.amazon.com/en-US/alexa/alexa-skills-kit) - Create one here! This is
used to host your Alexa skill and make it available on your Alexa devices. The Amazon account used for this account
needs to be the same as the one on your Alexa devices.

* [Setting up the Alexa Skill Kit (ASK) CLI](https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html) -
This is used to manage your skill from the command line and to deploy updates.


### Checking out the skill code

* ```git clone https://github.com/tfranovic/pi-hole-alexa.git```

### Deploying the skill

* Navigate to the repository root directory

* ```ask deploy``` - this will deploy the skill by creating the Lambda in your AWS account and all the necessary
settings on the Alexa Developer account.

### Configure the Lambda function's environment variables

* There are 3 environment variables that need to be configured:

```PIHOLE_SERVER``` - address or IP of the publicly available Pi-hole setup

```PIHOLE_IMAGES``` - pointer to the location of the images on S3/CloudFront, you can use ```https://d2u7kk3gg326io.cloudfront.net``` for now

```PIHOLE_PASSWORD``` - in order to be able to enable/disable Pi-hole

* You can configure them by navigating to the Lambda function in the AWS Console, and set the environment variables on 
the Configuration tab. Don't forget to save.

### Checking out the deployed skill

* The [ASK Developer Console](https://developer.amazon.com/alexa/console/ask) will contain all your skills in development

* Pick the Pi-hole skill and navigate around

### Testing the deployed skill in the Console

* There is a "Testing" tab which allows you to either speak or write the utterances to test the skill

### Testing from your Alexa-enabled devices

* Your custom skills are automatically enabled on all your Alexa devices so you should be able to use them without
any other set-up

Additional Resources
--------------------

### Pi-hole

-  [Pi-hole](https://pi-hole.net/) - Official website of the Pi-hole project
-  [Pi-hole Userspace](https://discourse.pi-hole.net/) - Join the discussion

### Tutorials & Guides

-  [Voice Design Guide](https://developer.amazon.com/designing-for-voice/) -
   A great resource for learning conversational and voice user interface design.

### Documentation

-  [Official Alexa Skills Kit Python SDK](https://pypi.org/project/ask-sdk/)
-  [Official Alexa Skills Kit Python SDK Docs](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/)
-  [Official Alexa Skills Kit Docs](https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html)

