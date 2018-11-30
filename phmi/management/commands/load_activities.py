import csv
from phmi import models
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError


IMPLIED = "Implied consent/reasonable expectations"
SET_ASIDE = "Set aside as data will be de-identified for this purpose"


ACT_1 = ("Allocating risk scores and stratifying populations \
for specified future adverse events causing poor health outcomes \
to individuals", SET_ASIDE,)

ACT_2 = ("Identifying and managing research cohorts", SET_ASIDE,)

ACT_3 = (
    "Managing quality of health and care services (inc. clinical audit)",
    SET_ASIDE,
)

ACT_4 = ("Reviewing, evaluating and transforming current health and care \
service provision across and within populations", SET_ASIDE,)


ACT_5 = (
    "Systematically selecting impactible individuals within \
risk-stratified population cohorts for early intervention or prevention",
    IMPLIED
)

ACT_6 = (
    "General provision of population health management", IMPLIED
)



data = {
    ACT_1: {
        "Local Authority": [
            "COMMISSIONER POWER: To provide preventative services",
        ],
        "NHS England": [
            "DUTY: To exercise relevant public health functions",
            "POWER: To assist SoS in providing health services and \
exercising public health functions",
        ]
    },
    ACT_2: {
        "CCG": [
            "DUTY: To promote the involvement of each patient",
            "DUTY: Research",
            "DUTY: Public and patient involvement",
            "POWER: To conduct research",
        ],
        "NHS England": [
            "DUTY: Public and patient involvement",
            "POWER: To conduct research",
        ],
        "Local Authority": [
            "COMMISSIONER POWER: To conduct research",
            "COMMISSIONER DUTY:  To ensure the involvement of local people in decision-making",
        ],

    },
    ACT_3: {
        "CCG": [
            "DUTY: Arrangement of personal health budgets",
        ],
        "NHS England": [
            "POWER: To make payments to CCGs in respect of quality of services",
            "DUTY: Co-operation with social services regarding the provision \
of NHS continuing healthcare",
            "DUTY: Arrangement of personal health budgets",
        ],
        "Local Authority": [
            "COMMISSIONER DUTY: To make direct payments to meet care needs",
            "COMMISSIONER DUTIES: Social care (various)",
            "COMMISSIONER POWER: To make direct payments to patients",
        ],
    },
    ACT_4: {
        "CCG": [
            "POWER: To make direct payments to patients",
            "DUTY: To promote the involvement of each patient",
            "DUTY: Public and patient involvement",
            "DUTY: To work with local authorities regarding adoption services",
            "DUTY: To consider the economic, social and environmental benefits \
to be achieved through commissioning"
        ],
        "NHS England": [
            "DUTY: Public and patient involvement",
            "DUTY: To collect and analyse information relating to safety of \
services",
            "DUTY: To consider the economic, social and environmental benefits to be achieved through commissioning",
        ],
        "Local Authority": [
            "COMMISSIONER DUTY: To prepare a joint strategic needs assessment",
            "COMMISSIONER DUTY:  To ensure the involvement of local people in \
decision-making",
            "COMMISSIONER DUTY: To consider the economic, social and \
environmental benefits to be achieved through commissioning"
        ]
    },
    ACT_5: {
        "Local Authority": [
            "PROVIDER POWER: To provide preventative services",
            "PROVIDER DUTIES: Social care (various)",
        ],
        "NHS Trust": [
            "DUTY: Provision of NHS goods and services",
        ],
    },
    ACT_6: {
        "NHS England": [
            "DUTY: To promote a comprehensive health service",
            "POWER:  To do anything that will facilitate the discharge of \
functions under the 2006 Act",
            "DUTY: To exercise functions efficiently",
            "DUTY: To secure continuous improvement in the quality of services",
            "DUTY:  To reduce health inequalities",
            "DUTY: To promote integrated health services",
            "DUTY: To promote integration between health services and \
health-related services",
            "DUTY: To promote innovation",
            "POWER: To obtain and analyse data",
            "DUTY: Eliminate discrimination, harassment and victimisation \
and advance equality of opportunity",
            "DUTY:  To share information",
        ],
        "CCG": [
            "POWER:  To do anything that will facilitate the discharge of \
functions under the 2006 Act",
            "POWER: To assist Secretary of State in providing health services \
and exercising public health functions",
            "DUTY:  To exercise any functions delegated to the CCG by the \
Secretary of State",
            "DUTY: Exercise its functions efficiently",
            "DUTY: Securing continuous improvement in quality of services \
provided to individuals",
            "DUTY: Reduce health inequalities",
            "DUTY: To promote innovation",
            "DUTY: to promote integrated health services",
            "DUTY: to promote integration between health services and \
health-related services",
            "POWER: For a CCG to deliver services jointly with another CCG",
            "POWER: For a CCG to deliver services jointly with a combined \
authority",
            "POWER: For NHS England to deliver CCG services instead of or \
jointly with a CCG",
            "DUTY: To make CCG facilities available to local authorities ",
            "POWER: To obtain and analyse data",
            "DUTY: To co-operate with local authorities",
            "DUTY:  To co-operate with NHS bodies when delivering care \
functions",
            "DUTY: Eliminate discrimination, harassment and victimisation and \
advance equality of opportunity",
            "DUTY:  To share information",
            "POWER: Be partnership organisations",
            "POWER:  To partner with local authorities",
        ],
        "Local Authority": [
            "DUTY:  To promote individual wellbeing",
            "DUTY: To carry out functions with the aim of integrating services",
            "DUTY:  To co-operate with NHS bodies when delivering care functions",
            "DUTY:  To meet the care and support needs of eligible adults",
            "POWER:  To meet the care and support needs of eligible adults",
            "DUTY:  To meet the support needs of eligible carers",
            "POWER:  To meet the support needs of eligible carers",
            "DUTY: To improve the well-being of and reduce inequalities for children",
            "DUTY: Eliminate discrimination, harassment and victimisation and advance equality of opportunity",
            "DUTY:  To share information",
            "POWER:  General power",
            "DUTY:  To exercise any functions delegated to the local authority by the Secretary of State",
            "DUTY:  To make services available to NHS bodies",
            "DUTY: To co-operate with CCGs and NHS England",
            "POWER: To obtain and analyse data",
        ],
        "NHS Trust": [
            "DUTY (NHS Trust Only): Provision of NHS goods and services",
            "DUTY (NHS Trust Only): Efficient delivery of functions",
            "DUTY: NHS bodies to co-operate ",
            "POWER (NHS Trust Only): General power",
            "POWER (NHS Trust Only): Joint exercise of functions",
            "DUTY: Eliminate discrimination, harassment and victimisation and advance equality of opportunity",
            "DUTY: To share information",
            "POWER: Be partnership organisations",
        ]
    }
}


class Command(BaseCommand):
    help = "Load in some activities"

    def parse_name(self, some_name):
        allowed_prefixes = ["DUTY", "POWER", "DUTIES"]
        prefix, suffix = some_name.split(":", 1)
        for allowed_prefix in allowed_prefixes:
            if allowed_prefix in prefix.upper():
                return f"{allowed_prefix.strip()}: {suffix.strip()}"
        raise ValueError(f"Unable fo parse {some_name}")

    def create_activities(self, activitiy, org_type, names):
        """
        Looks up for similar names in the statutes csvs.

        Notably the names above are more details for example they
        have things such as COMISSIONER DUTIES rather than just
        DUTIES as it would be called in the statutes.

        As a result we have to do some fiddling to make them
        match up.

        We can't just use the suffix as for some suffixes there is both
        a DUTY and a POWER
        """
        file_name = "data/csvs/statutes/{}.csv".format(
            org_type.name.lower().replace(" ", "-")
        )
        count = 0

        names_to_original_names = {self.parse_name(i): i for i in names}
        name_to_statute = {}
        with open(file_name) as f:
            reader = csv.reader(f)
            for i in reader:
                justification = self.clean_justification(i[1])
                if not justification:
                    continue
                dict_name = self.parse_name(justification)
                if dict_name in name_to_statute:
                    raise ValueError(f"Duplicate of {dict_name} in {file_name}")
                name_to_statute[dict_name] = i[2]

        for name, original_name in names_to_original_names.items():
            if name not in name_to_statute:
                raise ValueError(f"Unable to find {name} in {file_name}")

            justification, created = models.LegalJustification.objects.get_or_create(
                name=original_name,
                statute=name_to_statute[name],
                org_type=org_type
            )
            justification.activities.add(activitiy)

            if created:
                count += 1
        return count

    def clean_justification(self, justification):
        if "(NHS FT Only)" in justification:
            return
        return justification.replace("(NHS Trust Only)", "")

    @transaction.atomic
    def handle(self, *args, **options):
        total = 0
        for activity_details, org_type_dict in data.items():
            activity, _ = models.Activity.objects.get_or_create(
                name=activity_details[0],
                duty_of_confidence=activity_details[1]
            )
            for org_type_name, justifications in org_type_dict.items():
                justifications = [
                    self.clean_justification(i) for i in justifications
                ]
                justifications = [i for i in justifications if i]

                org_type = models.OrgType.objects.get(
                    name__startswith=org_type_name
                )
                total += self.create_activities(
                    activity, org_type, justifications
                )

        self.stdout.write(f"Saving {total} legal justifications")


