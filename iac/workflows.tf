
# resource "google_workflows_workflow" "trigger_export_agent" {
#   project     = var.project_id
#   region      = var.region
#   name        = "${var.project_id}-export-agent-trigger-${var.environment}"
#   description = "Workflow for ${upper(var.environment)} environment. This workflow can be triggered manually."

#   service_account = var.cf_service_account_email

#   source_contents = <<YAML
#     main:
#     steps:
#     - pubsubMessage:
#         call: googleapis.pubsub.v1.projects.topics.publish
#         args:
#             topic: ${google_pubsub_topic.topics["export-agent"].id}
#             body:
#             messages:
#             - data: ${base64encode("Trigger from 'trigger_export_agent' workflow")}
#                 attributes:
#                 source_environment: ${var.environment}
#     YAML
# }
