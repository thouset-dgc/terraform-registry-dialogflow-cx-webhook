from google.cloud import bigquery


def get_bigquery_sql_result(sql_query, project_id=None, location=None, credentials=None):
    """
    Executes a BigQuery SQL query and returns the results.

    Args:
        sql_query: The SQL query to execute as a string.
        project_id: (Optional) The Google Cloud project ID. If not provided,
            the default project will be used based on the environment or
            provided credentials.  See the Client library documentation on how
            projects are determined.
        location: (Optional) The geographic location of the BigQuery dataset.
            If not provided, defaults to the client's default location.
        credentials: (Optional) Explicitly provided Google Cloud credentials.
            If not provided, credentials are automatically discovered based on
            the environment.

    Returns:
        A `google.cloud.bigquery.query_job.QueryJob` object representing
        the results of the query.  The results themselves can be accessed via the
        `result()` method of this object, yielding rows as dictionaries.

    Raises:
        google.api_core.exceptions.BadRequest: If the query is invalid.
        google.api_core.exceptions.*: For other API request errors.
    """
    stringified_results = []

    client = bigquery.Client(
        project=project_id, credentials=credentials, location=location
    )

    query_job = client.query(sql_query)

    print(f"User query : {sql_query}" )
    
    results = query_job.result()

    for row in results:
        stringified_results.append({k: str(v) for k, v in row.items()})

    return stringified_results


# Example usage:
sql = """
    SELECT
    SUM(summary_tickets.Total_CA) AS Total_CA,

FROM `development-259117.development.summary_tickets_Mat` AS summary_tickets
LEFT JOIN `development-259117.development.reporting_site_from_dtt` AS reporting_site_from_dtt
    ON reporting_site_from_dtt.id = summary_tickets.id_site_from_dtt
WHERE 
  summary_tickets.Jour BETWEEN '2025-01-01' AND '2025-01-31'
  AND reporting_site_from_dtt.idmRealSite = 289
"""

if __name__ == "__main__":
    results_list = []
    try:
        bq_result = get_bigquery_sql_result(sql_query=sql)

        print(bq_result)
    except Exception as e:
        print(f"An error occurred: {e}")
