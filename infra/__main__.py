import pulumi
import pulumi_aws as aws

gcf_data_mapper = aws.ecr.Repository(
    "gcf-data-mapper",
    encryption_configurations=[
        {
            "encryption_type": "AES256",
        }
    ],
    image_scanning_configuration={
        "scan_on_push": False,
    },
    image_tag_mutability="MUTABLE",
    name="gcf-data-mapper",
    region="eu-west-1",
    opts=pulumi.ResourceOptions(protect=True),
)

pulumi.export("repository_url", gcf_data_mapper.repository_url)
