
locals {
  topic_config = {
    "export-agent" = "604800s"
  }
}

resource "google_pubsub_topic" "topics" {
  for_each                   = local.topic_config
  project                    = var.project_id
  name                       = "${var.project_id}-${each.key}-topic"
  message_retention_duration = each.value
}
