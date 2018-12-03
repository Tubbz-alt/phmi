import csv
from phmi import models
from django.db import transaction
from django.core.management.base import BaseCommand, CommandError


ORG_TYPES = [
    "CCG",
    "NHS Trust",
    "Local Authority",
    "NHS England",
]


class Command(BaseCommand):
    help = "Load in some activities"

    def get_justification(self, justification_activity, org_type_name):
        """
        There are some differences in terms of the prefix
        (e.g. commsissioner duties vs duties) so we
        search by the suffix. Then do a match.
        """
        org_type = models.OrgType.objects.get(name=org_type_name)
        prefix, justification_suffix = justification_activity.split(":", 1)
        legal_justification = models.LegalJustification.objects.filter(
            org_type=org_type
        )
        legal_justification = legal_justification.filter(
            name__endswith=justification_suffix
        )

        for i in legal_justification:
            if i.name.split(":")[0] in prefix:
                return i

        self.stdout.write(
            f"Unable to find {justification_activity} for {org_type_name}"
        )

    def create_statutes(self, org_type_name):
        """
        Looks up for similar names in the statutes csvs.

        Notably the names of duties/powers in the statute have more details

        for example they have things such as Comissioner duties rather than
        just Duties as it would be called in the statutes.

        As a result we have to do some fiddling to make them
        match up.

        We can't just use the suffix as for some suffixes there is both
        a Duty and a Power
        """
        file_name = "data/csvs/statutes/{}.csv".format(
            org_type_name.lower().replace(" ", "-")
        )
        count = 0

        with open(file_name) as f:
            reader = csv.reader(f)
            for i in reader:
                justification = self.get_justification(i[1], org_type_name)
                if justification:
                    justification.statute = i[2]
                    justification.save()
                    count += 1

        return count

    @transaction.atomic
    def handle(self, *args, **options):
        total = 0
        self.stdout.write("Legal justifications removed")
        models.LegalJustification.objects.all().update(statute="")
        for org_type in ORG_TYPES:
            total += self.create_statutes(org_type)
        self.stdout.write(f"Saving {total} legal justifications")



