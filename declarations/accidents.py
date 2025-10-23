from google.genai import types

get_accident_count_tool = types.FunctionDeclaration(
            name="get_accidents_count",
            description="Get the total count of distinct accidents that occurred within a given date range.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    'start_date': types.Schema(
                        type=types.Type.STRING, 
                        description="The start date of the period, in YYYY-MM-DD format."
                    ),
                    'end_date': types.Schema(
                        type=types.Type.STRING, 
                        description="The end date of the period, in YYYY-MM-DD format."
                    ),
                },
                required=["start_date", "end_date"]
            )
        )

