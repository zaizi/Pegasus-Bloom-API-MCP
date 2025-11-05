tool_specifications = [
    {
        "toolSpec": {
            "name": "get_accidents_count",
            "description": "Get the total count of distinct accidents that occurred within a given date range.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "start_date": {
                            "type": "string",
                            "description": "The start date of the period, in YYYY-MM-DD format."
                        },
                        "end_date": {
                            "type": "string",
                            "description": "The end date of the period, in YYYY-MM-DD format."
                        }
                    },
                    "required": ["start_date", "end_date"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "generate_service_user_report",
            "description": "Generate a detailed report of a single service user's activity within a date range, using their ID.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "start_date": {
                            "type": "string",
                            "description": "The start date for the report, in YYYY-MM-DD format."
                        },
                        "end_date": {
                            "type": "string",
                            "description": "The end date for the report, in YYYY-MM-DD format."
                        },
                        "user_id": {
                            "type": "integer",
                            "description": "The unique ID of the service user."
                        }
                    },
                    "required": ["start_date", "end_date", "user_id"]
                }
            }
        }
    }
]